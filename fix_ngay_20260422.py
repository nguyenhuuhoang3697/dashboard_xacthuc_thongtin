"""Cap nhat file xac_thuc bang du lieu moi nhat tu VBI_TT08 theo ngay."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append VBI_TT08 vao file xac_thuc theo ngay")
    parser.add_argument(
        "--xac-thuc",
        default="xac_thuc_theo_dinh_nghia_v_xac_thuc_luy_ke_20260421.txt",
        help="Duong dan file xac_thuc",
    )
    parser.add_argument(
        "--vbi-file",
        default=None,
        help="Duong dan file VBI_TT08. Neu bo trong se tu tim file moi nhat VBI_TT08* trong thu muc hien tai",
    )
    parser.add_argument(
        "--target-date",
        type=int,
        required=True,
        help="Ngay du lieu can cap nhat, dinh dang YYYYMMDD. Vi du: 20260424",
    )
    return parser.parse_args()


def detect_sep(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        header = f.readline()
    return "|" if header.count("|") >= header.count(",") else ","


def pick_latest_vbi_file() -> Path:
    candidates = sorted(Path(".").glob("VBI_TT08*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError("Khong tim thay file nao khop mau VBI_TT08*")
    return candidates[0]


def main() -> None:
    args = parse_args()
    xac_thuc_path = Path(args.xac_thuc)
    vbi_path = Path(args.vbi_file) if args.vbi_file else pick_latest_vbi_file()

    # Column mapping: VBI_TT08 -> xac_thuc
    col_map = {
        "sltb_xac_thuc": "sltb_xac_thuc_final",
        "sltb_xac_thuc_gboc": "sltb_xac_thuc_final_giao_gboc",
        "sltb_xac_thuc_gboc_offline": "sltb_xac_thuc_final_giao_gboc_offline",
        "sltb_xacthuc_gboc_offline": "sltb_xac_thuc_final_giao_gboc_offline",
        "sltb_gboc_vungsau_vungxa": "sltb_gboc_vung_sau_vung_xa",
    }
    excluded_cols = {
        "sltb_01",
        "sltb_02",
        "sltb_01_trung_cccd_yeu_the",
        "sltb_01_trung_cccd_con_lai",
        "sltb_01_full",
        "sltb_02_full",
        "sltb_01_trung_cccd_yeu_the_full",
        "sltb_01_trung_cccd_con_lai_full",
    }

    print(f"=== Buoc 1: Doc file xac_thuc ({xac_thuc_path}) va drop ngay {args.target_date} ===")
    df_xt = pd.read_csv(xac_thuc_path, sep="|", low_memory=False, dtype={"ngay": int})
    before = len(df_xt)
    df_xt = df_xt[df_xt["ngay"] != args.target_date]
    after = len(df_xt)
    print(f"  Da xoa {before - after:,} dong ngay {args.target_date}. Con lai: {after:,} dong")

    print(f"\n=== Buoc 2: Doc VBI_TT08 ({vbi_path}) va map cot ===")
    sep = detect_sep(vbi_path)
    df_vbi = pd.read_csv(vbi_path, sep=sep, low_memory=False)
    df_vbi.columns = [str(col).strip().lower() for col in df_vbi.columns]

    if "prd_id" in df_vbi.columns and "ngay" not in df_vbi.columns:
        df_vbi = df_vbi.rename(columns={"prd_id": "ngay"})
    if "ngay" not in df_vbi.columns:
        raise KeyError("File VBI khong co cot ngay/prd_id de loc theo ngay")

    df_vbi["ngay"] = pd.to_numeric(df_vbi["ngay"], errors="coerce").fillna(0).astype(int)
    df_vbi = df_vbi[df_vbi["ngay"] == args.target_date]
    print(f"  So dong VBI ngay {args.target_date}: {len(df_vbi):,}")
    cols_to_drop = [col for col in excluded_cols if col in df_vbi.columns]
    if cols_to_drop:
        df_vbi = df_vbi.drop(columns=cols_to_drop)
        print(f"  Da loai {len(cols_to_drop)} cot khong su dung: {', '.join(sorted(cols_to_drop))}")

    df_vbi = df_vbi.rename(columns=col_map)

    # Bao dam du cot de align voi file xac_thuc
    missing_cols = [c for c in df_xt.columns if c not in df_vbi.columns]
    for c in missing_cols:
        df_vbi[c] = 0
    df_vbi = df_vbi[df_xt.columns]

    print("\n=== Buoc 3: Append va ghi lai file xac_thuc ===")
    df_final = pd.concat([df_xt, df_vbi], ignore_index=True)
    df_final = df_final.sort_values(["ngay", "province_code_home"], na_position="last").reset_index(drop=True)
    print(f"  Tong so dong sau gop: {len(df_final):,}")
    print(f"  So dong cua ngay {args.target_date}: {(df_final['ngay'] == args.target_date).sum():,}")

    df_final.to_csv(xac_thuc_path, sep="|", index=False)
    size_mb = os.path.getsize(xac_thuc_path) / 1024 / 1024
    print(f"  Ghi xong: {xac_thuc_path} ({size_mb:.1f} MB)")
    print("\nDone!")


if __name__ == "__main__":
    main()
