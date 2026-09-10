#!/usr/bin/env python3
"""Login smoke checks for IAM auth center and portal endpoints using RSA encryption."""

from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http import cookiejar


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_url(base_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return base_url.rstrip("/") + "/" + path.lstrip("/")


def make_opener(insecure: bool) -> tuple[urllib.request.OpenerDirector, cookiejar.CookieJar]:
    jar = cookiejar.CookieJar()
    handlers = [urllib.request.HTTPCookieProcessor(jar), NoRedirectHandler()]
    if insecure:
        context = ssl._create_unverified_context()
        handlers.append(urllib.request.HTTPSHandler(context=context))
    return urllib.request.build_opener(*handlers), jar


def read_json_response(resp) -> dict:
    data = resp.read()
    if not data:
        return {}
    return json.loads(data.decode("utf-8"))


def get_json(opener, url: str, headers: dict[str, str], timeout: int) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with opener.open(req, timeout=timeout) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as err:
        payload = err.read()
        if payload:
            return json.loads(payload.decode("utf-8"))
        raise


def post_json(
    opener,
    url: str,
    payload: dict,
    headers: dict[str, str],
    timeout: int,
) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req_headers = {"Content-Type": "application/json", **headers}
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    try:
        with opener.open(req, timeout=timeout) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as err:
        payload = err.read()
        if payload:
            return json.loads(payload.decode("utf-8"))
        raise


def get_oauth_state(
    opener,
    authorize_url: str,
    params: dict[str, str],
    headers: dict[str, str],
    timeout: int,
) -> str:
    url = authorize_url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with opener.open(req, timeout=timeout) as resp:
            location = resp.headers.get("Location")
    except urllib.error.HTTPError as err:
        location = err.headers.get("Location")
    if not location:
        raise RuntimeError("Missing redirect Location header for oauth_state")
    parsed = urllib.parse.urlparse(location)
    query = urllib.parse.parse_qs(parsed.query)
    oauth_state = query.get("oauth_state", [""])[0]
    if not oauth_state:
        raise RuntimeError("oauth_state not found in redirect URL")
    return oauth_state


def rsa_encrypt_base64(plain: str, public_key_b64: str, openssl_cmd: str) -> str:
    key_der = base64.b64decode(public_key_b64)
    with tempfile.NamedTemporaryFile(delete=False) as key_file:
        key_file.write(key_der)
        key_file.flush()
        key_path = key_file.name
    try:
        encrypted = run_openssl_encrypt(openssl_cmd, key_path, plain.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")
    finally:
        os.unlink(key_path)


def run_openssl_encrypt(openssl_cmd: str, key_path: str, payload: bytes) -> bytes:
    pkeyutl_cmd = [
        openssl_cmd,
        "pkeyutl",
        "-encrypt",
        "-pubin",
        "-inkey",
        key_path,
        "-keyform",
        "DER",
        "-pkeyopt",
        "rsa_padding_mode:pkcs1",
    ]
    try:
        return subprocess.run(
            pkeyutl_cmd,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except subprocess.CalledProcessError:
        rsautl_cmd = [
            openssl_cmd,
            "rsautl",
            "-encrypt",
            "-pubin",
            "-inkey",
            key_path,
            "-keyform",
            "DER",
        ]
        return subprocess.run(
            rsautl_cmd,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout


def parse_server_response(payload: dict) -> tuple[bool, dict, str]:
    if not payload:
        return False, {}, "empty response"
    code = payload.get("code")
    if code in (0, "0", "200", 200):
        return True, payload.get("data") or {}, ""
    return False, payload.get("data") or {}, payload.get("message") or str(code)


def self_test(openssl_cmd: str) -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        priv_path = os.path.join(temp_dir, "priv.pem")
        pub_der_path = os.path.join(temp_dir, "pub.der")
        subprocess.run(
            [
                openssl_cmd,
                "genpkey",
                "-algorithm",
                "RSA",
                "-pkeyopt",
                "rsa_keygen_bits:2048",
                "-out",
                priv_path,
            ],
            check=True,
        )
        subprocess.run(
            [
                openssl_cmd,
                "pkey",
                "-in",
                priv_path,
                "-pubout",
                "-outform",
                "DER",
                "-out",
                pub_der_path,
            ],
            check=True,
        )
        with open(pub_der_path, "rb") as handle:
            public_key_b64 = base64.b64encode(handle.read()).decode("utf-8")

        plain = "self-test-password"
        encrypted_b64 = rsa_encrypt_base64(plain, public_key_b64, openssl_cmd)
        encrypted = base64.b64decode(encrypted_b64)

        decrypted = subprocess.run(
            [
                openssl_cmd,
                "pkeyutl",
                "-decrypt",
                "-inkey",
                priv_path,
                "-pkeyopt",
                "rsa_padding_mode:pkcs1",
            ],
            input=encrypted,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.decode("utf-8")

        if decrypted != plain:
            raise RuntimeError("RSA self-test failed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Login smoke checks for IAM auth center and portal endpoints."
    )
    parser.add_argument("--config", required=True, help="Path to JSON config")
    parser.add_argument("--out-dir", default="login_reports")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--openssl", default="openssl")

    args = parser.parse_args()

    if args.self_test:
        return self_test(args.openssl)

    with open(args.config, "r", encoding="utf-8") as handle:
        config = json.load(handle)

    base_url = config.get("base_url", "").strip()
    if not base_url:
        raise RuntimeError("base_url is required")

    cert_endpoint = config.get("cert_endpoint", "/api/iam/ac/public/cert/get")
    authorize_endpoint = config.get("authorize_endpoint", "/api/iam/oauth/authorize")
    login_endpoint = config.get("login_endpoint", "/api/iam/ac/public/v2/auth/tenant/login")
    portal_endpoints = config.get("portal_endpoints", {})
    portal_headers = config.get("portal_headers", {})

    headers = config.get("headers", {})
    timeout = int(config.get("timeout_seconds", 15))
    insecure = bool(config.get("insecure", False))

    oauth_config = config.get("oauth", {})
    oauth_params = {
        "client_id": oauth_config.get("client_id", ""),
        "redirect_uri": oauth_config.get("redirect_uri", ""),
        "response_type": oauth_config.get("response_type", "none"),
    }
    if not oauth_params["client_id"] or not oauth_params["redirect_uri"]:
        raise RuntimeError("oauth.client_id and oauth.redirect_uri are required")
    if oauth_config.get("scope"):
        oauth_params["scope"] = oauth_config["scope"]
    if oauth_config.get("state"):
        oauth_params["state"] = oauth_config["state"]
    if oauth_config.get("nonce"):
        oauth_params["nonce"] = oauth_config["nonce"]
    if oauth_config.get("user_type"):
        oauth_params["user_type"] = oauth_config["user_type"]

    users = config.get("users", [])
    if not users:
        raise RuntimeError("users list is required")

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_count": len(users),
        "success_count": 0,
        "failures": [],
    }

    for user in users:
        login_name = user.get("loginName", "")
        password = user.get("password", "")
        if not login_name or not password:
            summary["failures"].append({"loginName": login_name, "error": "missing credentials"})
            continue

        if args.dry_run:
            summary["success_count"] += 1
            continue

        opener, _ = make_opener(insecure)

        cert_url = build_url(base_url, cert_endpoint)
        authorize_url = build_url(base_url, authorize_endpoint)
        login_url = build_url(base_url, login_endpoint)

        cert_payload = get_json(opener, cert_url, headers, timeout)
        ok, cert_data, err_msg = parse_server_response(cert_payload)
        if not ok:
            summary["failures"].append({"loginName": login_name, "error": f"cert: {err_msg}"})
            continue
        public_key = cert_data.get("publicKey", "")
        if not public_key:
            summary["failures"].append({"loginName": login_name, "error": "missing publicKey"})
            continue

        try:
            oauth_state = get_oauth_state(opener, authorize_url, oauth_params, headers, timeout)
        except Exception as exc:
            summary["failures"].append({"loginName": login_name, "error": f"oauth_state: {exc}"})
            continue

        try:
            encrypted_password = rsa_encrypt_base64(password, public_key, args.openssl)
        except Exception as exc:
            summary["failures"].append({"loginName": login_name, "error": f"encrypt: {exc}"})
            continue

        login_payload = {
            "loginName": login_name,
            "password": encrypted_password,
            "oauthState": oauth_state,
        }

        login_resp = post_json(opener, login_url, login_payload, headers, timeout)
        ok, login_data, err_msg = parse_server_response(login_resp)
        if not ok:
            summary["failures"].append({"loginName": login_name, "error": f"login: {err_msg}"})
            continue

        session_id = login_data.get("sessionId")
        user_report = {
            "loginName": login_name,
            "sessionId": session_id,
            "expiresAt": login_data.get("expiresAt"),
            "activated_solutions": None,
            "menus": {},
        }

        portal_call_headers = dict(headers)
        portal_call_headers.update(portal_headers)
        if session_id:
            portal_call_headers.setdefault("x-session-id", session_id)

        activated_endpoint = portal_endpoints.get("activated_solutions")
        if activated_endpoint:
            activated_url = build_url(base_url, activated_endpoint)
            activated_resp = get_json(opener, activated_url, portal_call_headers, timeout)
            ok, activated_data, err_msg = parse_server_response(activated_resp)
            if ok:
                user_report["activated_solutions"] = activated_data
            else:
                user_report["activated_solutions"] = {"error": err_msg}

        menu_endpoint = portal_endpoints.get("menus")
        solution_ids = user.get("solutionIds", [])
        if menu_endpoint and solution_ids:
            for solution_id in solution_ids:
                menu_url = (
                    build_url(base_url, menu_endpoint)
                    + "?"
                    + urllib.parse.urlencode({"id": solution_id})
                )
                menu_resp = get_json(opener, menu_url, portal_call_headers, timeout)
                ok, menu_data, err_msg = parse_server_response(menu_resp)
                user_report["menus"][solution_id] = menu_data if ok else {"error": err_msg}

        with open(
            os.path.join(out_dir, f"{login_name}_portal.json"),
            "w",
            encoding="utf-8",
        ) as handle:
            json.dump(user_report, handle, indent=2, ensure_ascii=True)

        summary["success_count"] += 1

    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=True)

    return 0 if summary["success_count"] == summary["user_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
