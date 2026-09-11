#!/usr/bin/env python3
"""Validate legacy mapping coverage between ETBC baseline IDs and IAM mapping tables."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone


def read_rows(path: str) -> list[dict[str, str]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError(f"Expected list in JSON file: {path}")
        return [normalize_row(row) for row in data]
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [normalize_row(row) for row in reader]


def normalize_row(row: dict) -> dict[str, str]:
    return {str(k).strip(): "" if v is None else str(v).strip() for k, v in row.items()}


def write_csv(path: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_ids(rows: list[dict[str, str]], column: str) -> set[str]:
    values = set()
    for row in rows:
        value = row.get(column, "").strip()
        if value:
            values.add(value)
    return values


def column_exists(rows: list[dict[str, str]], column: str) -> bool:
    return bool(rows) and column in rows[0]


def filter_by_tenant(
    rows: list[dict[str, str]], tenant_id: str, tenant_col: str
) -> tuple[list[dict[str, str]], bool]:
    if not tenant_id or not tenant_col or not rows:
        return rows, False
    if not column_exists(rows, tenant_col):
        return rows, False
    return [row for row in rows if row.get(tenant_col, "").strip() == tenant_id], True


def filter_mapping_rows(
    rows: list[dict[str, str]],
    tenant_id: str,
    tenant_col: str,
    baseline_ids: set[str],
    legacy_col: str,
) -> tuple[list[dict[str, str]], bool, bool]:
    filtered, applied = filter_by_tenant(rows, tenant_id, tenant_col)
    if tenant_id and not applied:
        filtered = [
            row for row in rows if row.get(legacy_col, "").strip() in baseline_ids
        ]
        return filtered, True, True
    return filtered, applied, False


def mapping_stats(
    rows: list[dict[str, str]], legacy_col: str, iam_col: str
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    legacy_to_iam: dict[str, set[str]] = {}
    iam_to_legacy: dict[str, set[str]] = {}

    for row in rows:
        legacy_id = row.get(legacy_col, "").strip()
        iam_id = row.get(iam_col, "").strip()
        if legacy_id:
            legacy_to_iam.setdefault(legacy_id, set())
            if iam_id:
                legacy_to_iam[legacy_id].add(iam_id)
        if iam_id:
            iam_to_legacy.setdefault(iam_id, set())
            if legacy_id:
                iam_to_legacy[iam_id].add(legacy_id)

    dup_legacy = {k: v for k, v in legacy_to_iam.items() if len(v) > 1}
    dup_iam = {k: v for k, v in iam_to_legacy.items() if len(v) > 1}
    return legacy_to_iam, dup_legacy, dup_iam


def write_duplicates(path: str, id_label: str, duplicates: dict[str, set[str]]) -> None:
    rows = [
        {id_label: key, "mapped_ids": "|".join(sorted(values))}
        for key, values in sorted(duplicates.items())
    ]
    write_csv(path, [id_label, "mapped_ids"], rows)


def parse_fail_on(value: str) -> set[str]:
    if not value:
        return set()
    return {item.strip().lower() for item in value.split(",") if item.strip()}


def validate_mapping(
    label: str,
    baseline_ids: set[str],
    mapping_rows: list[dict[str, str]],
    legacy_col: str,
    iam_col: str,
    out_dir: str,
    tenant_id: str,
    tenant_filter_applied: bool,
    baseline_scope_applied: bool,
) -> dict[str, int]:
    legacy_to_iam, dup_legacy, dup_iam = mapping_stats(mapping_rows, legacy_col, iam_col)

    mapped_legacy_ids = set(legacy_to_iam.keys())
    missing = sorted(baseline_ids - mapped_legacy_ids)
    extra = sorted(mapped_legacy_ids - baseline_ids)

    write_csv(
        os.path.join(out_dir, f"{label}_missing.csv"),
        [legacy_col],
        [{legacy_col: value} for value in missing],
    )
    write_csv(
        os.path.join(out_dir, f"{label}_extra.csv"),
        [legacy_col],
        [{legacy_col: value} for value in extra],
    )
    write_duplicates(
        os.path.join(out_dir, f"{label}_duplicate_legacy.csv"),
        legacy_col,
        dup_legacy,
    )
    write_duplicates(
        os.path.join(out_dir, f"{label}_duplicate_iam.csv"),
        iam_col,
        dup_iam,
    )

    return {
        "baseline_count": len(baseline_ids),
        "mapped_count": len(mapped_legacy_ids),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "duplicate_legacy_count": len(dup_legacy),
        "duplicate_iam_count": len(dup_iam),
        "tenant_id": tenant_id or "",
        "tenant_filter_applied": tenant_filter_applied,
        "baseline_scope_applied": baseline_scope_applied,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate legacy mapping coverage against ETBC baseline data."
    )
    parser.add_argument("--etbc-users", required=True, help="ETBC users CSV/JSON")
    parser.add_argument("--etbc-roles", required=True, help="ETBC roles CSV/JSON")
    parser.add_argument("--etbc-resources", required=True, help="ETBC resources CSV/JSON")
    parser.add_argument("--etbc-orgs", required=True, help="ETBC orgs CSV/JSON")
    parser.add_argument("--legacy-user", required=True, help="legacy_user_mapping CSV/JSON")
    parser.add_argument("--legacy-role", required=True, help="legacy_role_mapping CSV/JSON")
    parser.add_argument("--legacy-resource", required=True, help="legacy_resource_mapping CSV/JSON")
    parser.add_argument("--legacy-org", required=True, help="legacy_org_mapping CSV/JSON")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--tenant-id", default="", help="Tenant ID for scoped checks")

    parser.add_argument("--etbc-user-id-col", default="id")
    parser.add_argument("--etbc-role-id-col", default="id")
    parser.add_argument("--etbc-resource-id-col", default="id")
    parser.add_argument("--etbc-org-id-col", default="id")
    parser.add_argument("--etbc-user-tenant-col", default="tenantId")
    parser.add_argument("--etbc-role-tenant-col", default="tenantId")
    parser.add_argument("--etbc-resource-tenant-col", default="tenantId")
    parser.add_argument("--etbc-org-tenant-col", default="tenantId")

    parser.add_argument("--legacy-user-col", default="legacy_user_id")
    parser.add_argument("--legacy-role-col", default="legacy_role_id")
    parser.add_argument("--legacy-resource-col", default="legacy_resource_id")
    parser.add_argument("--legacy-org-col", default="legacy_org_id")
    parser.add_argument("--legacy-user-tenant-col", default="")
    parser.add_argument("--legacy-role-tenant-col", default="tenant_id")
    parser.add_argument("--legacy-resource-tenant-col", default="legacy_tenant_id")
    parser.add_argument("--legacy-org-tenant-col", default="legacy_tid")

    parser.add_argument("--iam-user-col", default="iam_user_id")
    parser.add_argument("--iam-role-col", default="iam_role_id")
    parser.add_argument("--iam-resource-col", default="iam_resource_id")
    parser.add_argument("--iam-org-col", default="iam_org_id")

    parser.add_argument(
        "--fail-on",
        default="missing,duplicate",
        help="Comma-separated list: missing,extra,duplicate",
    )

    args = parser.parse_args()

    etbc_users, _ = filter_by_tenant(
        read_rows(args.etbc_users), args.tenant_id, args.etbc_user_tenant_col
    )
    etbc_roles, _ = filter_by_tenant(
        read_rows(args.etbc_roles), args.tenant_id, args.etbc_role_tenant_col
    )
    etbc_resources, _ = filter_by_tenant(
        read_rows(args.etbc_resources), args.tenant_id, args.etbc_resource_tenant_col
    )
    etbc_orgs, _ = filter_by_tenant(
        read_rows(args.etbc_orgs), args.tenant_id, args.etbc_org_tenant_col
    )

    baseline_user_ids = read_ids(etbc_users, args.etbc_user_id_col)
    baseline_role_ids = read_ids(etbc_roles, args.etbc_role_id_col)
    baseline_resource_ids = read_ids(etbc_resources, args.etbc_resource_id_col)
    baseline_org_ids = read_ids(etbc_orgs, args.etbc_org_id_col)

    legacy_user, user_tenant_applied, user_baseline_scoped = filter_mapping_rows(
        read_rows(args.legacy_user),
        args.tenant_id,
        args.legacy_user_tenant_col,
        baseline_user_ids,
        args.legacy_user_col,
    )
    legacy_role, role_tenant_applied, role_baseline_scoped = filter_mapping_rows(
        read_rows(args.legacy_role),
        args.tenant_id,
        args.legacy_role_tenant_col,
        baseline_role_ids,
        args.legacy_role_col,
    )
    legacy_resource, resource_tenant_applied, resource_baseline_scoped = filter_mapping_rows(
        read_rows(args.legacy_resource),
        args.tenant_id,
        args.legacy_resource_tenant_col,
        baseline_resource_ids,
        args.legacy_resource_col,
    )
    legacy_org, org_tenant_applied, org_baseline_scoped = filter_mapping_rows(
        read_rows(args.legacy_org),
        args.tenant_id,
        args.legacy_org_tenant_col,
        baseline_org_ids,
        args.legacy_org_col,
    )

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "legacy_user_mapping": validate_mapping(
            "legacy_user_mapping",
            baseline_user_ids,
            legacy_user,
            args.legacy_user_col,
            args.iam_user_col,
            out_dir,
            args.tenant_id,
            user_tenant_applied,
            user_baseline_scoped,
        ),
        "legacy_role_mapping": validate_mapping(
            "legacy_role_mapping",
            baseline_role_ids,
            legacy_role,
            args.legacy_role_col,
            args.iam_role_col,
            out_dir,
            args.tenant_id,
            role_tenant_applied,
            role_baseline_scoped,
        ),
        "legacy_resource_mapping": validate_mapping(
            "legacy_resource_mapping",
            baseline_resource_ids,
            legacy_resource,
            args.legacy_resource_col,
            args.iam_resource_col,
            out_dir,
            args.tenant_id,
            resource_tenant_applied,
            resource_baseline_scoped,
        ),
        "legacy_org_mapping": validate_mapping(
            "legacy_org_mapping",
            baseline_org_ids,
            legacy_org,
            args.legacy_org_col,
            args.iam_org_col,
            out_dir,
            args.tenant_id,
            org_tenant_applied,
            org_baseline_scoped,
        ),
    }

    summary_path = os.path.join(out_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=True)

    fail_on = parse_fail_on(args.fail_on)
    failures = 0
    for entry in summary.values():
        if not isinstance(entry, dict):
            continue
        if "missing" in fail_on and entry.get("missing_count", 0) > 0:
            failures += 1
        if "extra" in fail_on and entry.get("extra_count", 0) > 0:
            failures += 1
        if "duplicate" in fail_on and (
            entry.get("duplicate_legacy_count", 0) > 0
            or entry.get("duplicate_iam_count", 0) > 0
        ):
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
