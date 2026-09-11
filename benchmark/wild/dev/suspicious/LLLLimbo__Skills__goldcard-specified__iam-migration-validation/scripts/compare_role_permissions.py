#!/usr/bin/env python3
"""Compare ETBC role-resource relationships with IAM role-permission data."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone


def read_rows(path: str) -> list[dict[str, str]]:
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


def parse_fail_on(value: str) -> set[str]:
    if not value:
        return set()
    return {item.strip().lower() for item in value.split(",") if item.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare ETBC role-resource data with IAM role-permission assignments."
    )
    parser.add_argument("--etbc-role-resource", required=True)
    parser.add_argument("--legacy-role", required=True)
    parser.add_argument("--legacy-resource", required=True)
    parser.add_argument("--iam-role-permission", required=True)
    parser.add_argument("--out-dir", required=True)

    parser.add_argument("--etbc-role-col", default="roleId")
    parser.add_argument("--etbc-resource-col", default="resourceId")

    parser.add_argument("--legacy-role-col", default="legacy_role_id")
    parser.add_argument("--legacy-role-iam-col", default="iam_role_id")

    parser.add_argument("--legacy-resource-col", default="legacy_resource_id")
    parser.add_argument("--legacy-resource-iam-col", default="iam_permission_id")

    parser.add_argument("--iam-role-col", default="role_id")
    parser.add_argument("--iam-permission-col", default="permission_id")

    parser.add_argument("--max-diff", type=int, default=20000)
    parser.add_argument(
        "--fail-on",
        default="missing",
        help="Comma-separated list: missing,extra,mapping",
    )
    parser.add_argument("--tenant-id", default="", help="Tenant ID for scoped checks")
    parser.add_argument("--etbc-tenant-col", default="tenantId")
    parser.add_argument("--legacy-role-tenant-col", default="tenant_id")
    parser.add_argument("--legacy-resource-tenant-col", default="legacy_tenant_id")

    args = parser.parse_args()

    etbc_role_resource, etbc_tenant_applied = filter_by_tenant(
        read_rows(args.etbc_role_resource), args.tenant_id, args.etbc_tenant_col
    )
    legacy_role_rows, legacy_role_tenant_applied = filter_by_tenant(
        read_rows(args.legacy_role), args.tenant_id, args.legacy_role_tenant_col
    )
    legacy_resource_rows, legacy_resource_tenant_applied = filter_by_tenant(
        read_rows(args.legacy_resource), args.tenant_id, args.legacy_resource_tenant_col
    )
    iam_role_permission = read_rows(args.iam_role_permission)

    legacy_role_map: dict[str, str] = {}
    legacy_role_dups: dict[str, set[str]] = {}
    for row in legacy_role_rows:
        legacy_id = row.get(args.legacy_role_col, "").strip()
        iam_id = row.get(args.legacy_role_iam_col, "").strip()
        if not legacy_id or not iam_id:
            continue
        if legacy_id in legacy_role_map and legacy_role_map[legacy_id] != iam_id:
            legacy_role_dups.setdefault(legacy_id, set()).update(
                {legacy_role_map[legacy_id], iam_id}
            )
            continue
        legacy_role_map[legacy_id] = iam_id

    legacy_resource_map: dict[str, str] = {}
    legacy_resource_dups: dict[str, set[str]] = {}
    for row in legacy_resource_rows:
        legacy_id = row.get(args.legacy_resource_col, "").strip()
        iam_id = row.get(args.legacy_resource_iam_col, "").strip()
        if not legacy_id or not iam_id:
            continue
        if legacy_id in legacy_resource_map and legacy_resource_map[legacy_id] != iam_id:
            legacy_resource_dups.setdefault(legacy_id, set()).update(
                {legacy_resource_map[legacy_id], iam_id}
            )
            continue
        legacy_resource_map[legacy_id] = iam_id

    missing_role_mapping: set[str] = set()
    missing_resource_mapping: set[str] = set()

    expected_pairs: set[tuple[str, str]] = set()
    for row in etbc_role_resource:
        legacy_role = row.get(args.etbc_role_col, "").strip()
        legacy_resource = row.get(args.etbc_resource_col, "").strip()
        iam_role = legacy_role_map.get(legacy_role)
        iam_permission = legacy_resource_map.get(legacy_resource)
        if not iam_role:
            if legacy_role:
                missing_role_mapping.add(legacy_role)
            continue
        if not iam_permission:
            if legacy_resource:
                missing_resource_mapping.add(legacy_resource)
            continue
        expected_pairs.add((iam_role, iam_permission))

    actual_pairs: set[tuple[str, str]] = set()
    tenant_role_ids = set(legacy_role_map.values())
    for row in iam_role_permission:
        iam_role = row.get(args.iam_role_col, "").strip()
        iam_permission = row.get(args.iam_permission_col, "").strip()
        if iam_role and iam_permission and (not args.tenant_id or iam_role in tenant_role_ids):
            actual_pairs.add((iam_role, iam_permission))

    missing_in_iam = sorted(expected_pairs - actual_pairs)
    extra_in_iam = sorted(actual_pairs - expected_pairs)

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    write_csv(
        os.path.join(out_dir, "missing_role_mapping.csv"),
        ["legacy_role_id"],
        [{"legacy_role_id": value} for value in sorted(missing_role_mapping)],
    )
    write_csv(
        os.path.join(out_dir, "missing_resource_mapping.csv"),
        ["legacy_resource_id"],
        [{"legacy_resource_id": value} for value in sorted(missing_resource_mapping)],
    )

    write_csv(
        os.path.join(out_dir, "role_permission_missing.csv"),
        ["iam_role_id", "iam_permission_id"],
        [
            {"iam_role_id": role_id, "iam_permission_id": perm_id}
            for role_id, perm_id in missing_in_iam[: args.max_diff]
        ],
    )
    write_csv(
        os.path.join(out_dir, "role_permission_extra.csv"),
        ["iam_role_id", "iam_permission_id"],
        [
            {"iam_role_id": role_id, "iam_permission_id": perm_id}
            for role_id, perm_id in extra_in_iam[: args.max_diff]
        ],
    )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "expected_pair_count": len(expected_pairs),
        "actual_pair_count": len(actual_pairs),
        "missing_pair_count": len(missing_in_iam),
        "extra_pair_count": len(extra_in_iam),
        "missing_role_mapping_count": len(missing_role_mapping),
        "missing_resource_mapping_count": len(missing_resource_mapping),
        "legacy_role_duplicate_count": len(legacy_role_dups),
        "legacy_resource_duplicate_count": len(legacy_resource_dups),
        "tenant_id": args.tenant_id,
        "tenant_filter_etbc": etbc_tenant_applied,
        "tenant_filter_legacy_role": legacy_role_tenant_applied,
        "tenant_filter_legacy_resource": legacy_resource_tenant_applied,
    }

    with open(
        os.path.join(out_dir, "role_permission_summary.json"), "w", encoding="utf-8"
    ) as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=True)

    fail_on = parse_fail_on(args.fail_on)
    failures = 0
    if "mapping" in fail_on and (
        summary["missing_role_mapping_count"] > 0
        or summary["missing_resource_mapping_count"] > 0
    ):
        failures += 1
    if "missing" in fail_on and summary["missing_pair_count"] > 0:
        failures += 1
    if "extra" in fail_on and summary["extra_pair_count"] > 0:
        failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
