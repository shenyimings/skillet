#!/usr/bin/env python3
"""Compare ETBC menu tree with IAM menu tree using legacy resource mapping."""

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


def normalize_parent(value: str) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    if not value or value == "0" or value.lower() == "null":
        return None
    return value


def normalize_sort(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def write_csv(path: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_index(rows: list[dict[str, str]], id_col: str) -> dict[str, dict[str, str]]:
    index = {}
    for row in rows:
        key = row.get(id_col, "").strip()
        if key:
            index[key] = row
    return index


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


def filter_mapping_by_tenant(
    rows: list[dict[str, str]],
    tenant_id: str,
    legacy_tenant_col: str,
    iam_tenant_col: str,
) -> tuple[list[dict[str, str]], bool]:
    if not tenant_id or not rows:
        return rows, False
    has_legacy = bool(legacy_tenant_col) and column_exists(rows, legacy_tenant_col)
    has_iam = bool(iam_tenant_col) and column_exists(rows, iam_tenant_col)
    if not (has_legacy or has_iam):
        return rows, False
    filtered = []
    for row in rows:
        legacy_val = row.get(legacy_tenant_col, "").strip() if has_legacy else ""
        iam_val = row.get(iam_tenant_col, "").strip() if has_iam else ""
        if legacy_val == tenant_id or iam_val == tenant_id:
            filtered.append(row)
    return filtered, True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare ETBC menu tree with IAM menu tree using legacy mappings."
    )
    parser.add_argument("--etbc-resources", required=True)
    parser.add_argument("--iam-resources", required=True)
    parser.add_argument("--legacy-resource", required=True)
    parser.add_argument("--out-dir", required=True)

    parser.add_argument("--etbc-id-col", default="id")
    parser.add_argument("--etbc-parent-col", default="parentId")
    parser.add_argument("--etbc-sort-col", default="sort")
    parser.add_argument("--etbc-name-col", default="name")
    parser.add_argument("--etbc-uri-col", default="url")

    parser.add_argument("--iam-id-col", default="id")
    parser.add_argument("--iam-parent-col", default="parentId")
    parser.add_argument("--iam-sort-col", default="sort")
    parser.add_argument("--iam-name-col", default="name")
    parser.add_argument("--iam-uri-col", default="uri")

    parser.add_argument("--legacy-id-col", default="legacy_resource_id")
    parser.add_argument("--legacy-iam-col", default="iam_resource_id")
    parser.add_argument("--legacy-parent-col", default="legacy_parent_resource_id")
    parser.add_argument("--legacy-iam-parent-col", default="iam_parent_resource_id")
    parser.add_argument("--tenant-id", default="", help="Tenant ID for scoped checks")
    parser.add_argument("--etbc-tenant-col", default="tenantId")
    parser.add_argument("--iam-tenant-col", default="tenant_id")
    parser.add_argument("--legacy-tenant-col", default="legacy_tenant_id")
    parser.add_argument("--legacy-iam-tenant-col", default="iam_tenant_id")

    parser.add_argument("--ignore-name", action="store_true")
    parser.add_argument("--ignore-uri", action="store_true")
    parser.add_argument("--max-diff", type=int, default=20000)

    args = parser.parse_args()

    etbc_rows, etbc_tenant_applied = filter_by_tenant(
        read_rows(args.etbc_resources), args.tenant_id, args.etbc_tenant_col
    )
    iam_rows, iam_tenant_applied = filter_by_tenant(
        read_rows(args.iam_resources), args.tenant_id, args.iam_tenant_col
    )
    mapping_rows, mapping_tenant_applied = filter_mapping_by_tenant(
        read_rows(args.legacy_resource),
        args.tenant_id,
        args.legacy_tenant_col,
        args.legacy_iam_tenant_col,
    )

    etbc_index = build_index(etbc_rows, args.etbc_id_col)
    iam_index = build_index(iam_rows, args.iam_id_col)

    legacy_to_iam = {}
    legacy_parent_to_iam_parent = {}
    for row in mapping_rows:
        legacy_id = row.get(args.legacy_id_col, "").strip()
        iam_id = row.get(args.legacy_iam_col, "").strip()
        if legacy_id and iam_id:
            legacy_to_iam[legacy_id] = iam_id
        legacy_parent = row.get(args.legacy_parent_col, "").strip()
        iam_parent = row.get(args.legacy_iam_parent_col, "").strip()
        if legacy_id and (legacy_parent or iam_parent):
            legacy_parent_to_iam_parent[legacy_id] = (legacy_parent, iam_parent)

    diffs: list[dict[str, str]] = []

    def add_diff(diff_type: str, legacy_id: str, iam_id: str, details: str) -> None:
        if len(diffs) >= args.max_diff:
            return
        diffs.append(
            {
                "type": diff_type,
                "legacy_resource_id": legacy_id,
                "iam_resource_id": iam_id,
                "details": details,
            }
        )

    legacy_ids_to_check = list(etbc_index.keys())
    if args.tenant_id and mapping_tenant_applied:
        legacy_ids_to_check = [
            legacy_id for legacy_id in legacy_to_iam.keys() if legacy_id in etbc_index
        ]

    for legacy_id in legacy_ids_to_check:
        etbc_row = etbc_index.get(legacy_id)
        if not etbc_row:
            continue
        iam_id = legacy_to_iam.get(legacy_id)
        if not iam_id:
            add_diff("missing_mapping", legacy_id, "", "no legacy_resource_mapping")
            continue

        iam_row = iam_index.get(iam_id)
        if not iam_row:
            add_diff("missing_iam_resource", legacy_id, iam_id, "iam resource not found")
            continue

        etbc_parent = normalize_parent(etbc_row.get(args.etbc_parent_col, ""))
        iam_parent_actual = normalize_parent(iam_row.get(args.iam_parent_col, ""))
        expected_parent = None
        if etbc_parent:
            expected_parent = legacy_to_iam.get(etbc_parent)

        if expected_parent and iam_parent_actual and expected_parent != iam_parent_actual:
            add_diff(
                "parent_mismatch",
                legacy_id,
                iam_id,
                f"expected_parent={expected_parent} actual_parent={iam_parent_actual}",
            )

        mapping_parent = legacy_parent_to_iam_parent.get(legacy_id)
        if mapping_parent:
            _, mapping_iam_parent = mapping_parent
            if mapping_iam_parent and iam_parent_actual and mapping_iam_parent != iam_parent_actual:
                add_diff(
                    "mapping_parent_mismatch",
                    legacy_id,
                    iam_id,
                    f"mapping_parent={mapping_iam_parent} actual_parent={iam_parent_actual}",
                )

        etbc_sort = normalize_sort(etbc_row.get(args.etbc_sort_col, ""))
        iam_sort = normalize_sort(iam_row.get(args.iam_sort_col, ""))
        if etbc_sort is not None and iam_sort is not None and etbc_sort != iam_sort:
            add_diff(
                "sort_mismatch",
                legacy_id,
                iam_id,
                f"etbc_sort={etbc_sort} iam_sort={iam_sort}",
            )

        if not args.ignore_name:
            etbc_name = etbc_row.get(args.etbc_name_col, "").strip()
            iam_name = iam_row.get(args.iam_name_col, "").strip()
            if etbc_name and iam_name and etbc_name != iam_name:
                add_diff(
                    "name_mismatch",
                    legacy_id,
                    iam_id,
                    f"etbc_name={etbc_name} iam_name={iam_name}",
                )

        if not args.ignore_uri:
            etbc_uri = etbc_row.get(args.etbc_uri_col, "").strip()
            iam_uri = iam_row.get(args.iam_uri_col, "").strip()
            if etbc_uri and iam_uri and etbc_uri != iam_uri:
                add_diff(
                    "uri_mismatch",
                    legacy_id,
                    iam_id,
                    f"etbc_uri={etbc_uri} iam_uri={iam_uri}",
                )

    mapped_iam_ids = set(legacy_to_iam.values())
    iam_ids_for_extra = set(iam_index.keys())
    if args.tenant_id and (not iam_tenant_applied or not mapping_tenant_applied):
        iam_ids_for_extra = mapped_iam_ids
    extra_iam = sorted(iam_ids_for_extra - mapped_iam_ids)
    for iam_id in extra_iam:
        add_diff("extra_iam_resource", "", iam_id, "iam resource not in mapping")

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    write_csv(
        os.path.join(out_dir, "menu_tree_diff.csv"),
        ["type", "legacy_resource_id", "iam_resource_id", "details"],
        diffs,
    )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "etbc_resource_count": len(etbc_index),
        "iam_resource_count": len(iam_index),
        "mapping_count": len(legacy_to_iam),
        "diff_count": len(diffs),
        "tenant_id": args.tenant_id,
        "tenant_filter_etbc": etbc_tenant_applied,
        "tenant_filter_iam": iam_tenant_applied,
        "tenant_filter_mapping": mapping_tenant_applied,
    }

    with open(os.path.join(out_dir, "menu_tree_summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=True)

    return 1 if diffs else 0


if __name__ == "__main__":
    raise SystemExit(main())
