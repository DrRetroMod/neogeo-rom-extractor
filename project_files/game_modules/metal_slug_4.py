#!/usr/bin/env python3

# NeoGeo ROM Extractor
# Copyright (C) 2026 Dr. RetroMod
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

r"""
Metal Slug 4 Code Mystics / Amazon Prime Gaming standalone converter.

Builds an mslug4h-style Neo Geo ZIP from the Code Mystics source files used by
Metal Slug 4 from Amazon Prime Gaming, following the public shell conversion
flow credited to alhumbra, scrap-a, Tomasz Bednarz, and Lionel Cordesses.

This script replaces dd, split, cat, srec_cat, ss_unswizzle, zip, and the
old external neo-cmc command-line step with Python-side conversion helpers.

Expected source files in --source:
  p1.bin
  m1.bin
  v1.bin
  c1.bin
  s2.bin

Example, Windows PowerShell:
  py .\mslug4_code_mystics_converter.py `
    --source "PATH\TO\Metal Slug 4\Data\rom" `
    --output .\mslug4h.zip

Example, macOS/Linux:
  python3 ./mslug4_code_mystics_converter.py \
    --source "/path/to/Metal Slug 4/Data/rom" \
    --output ./mslug4h.zip
"""

# Extraction notes:
# This module was developed through source-file analysis, local testing,
# hash comparison, and comparison with public Neo Geo extraction, emulation,
# and preservation research.
#
# Metal Slug 4 extraction behaviour was informed by goNCommand
# by Lionel Cordesses:
# https://github.com/lioneltrs/goNCommand
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

from __future__ import annotations

import argparse
import binascii
import sys
import zipfile
from pathlib import Path

from neogeo.cmc import cmc50_gfx_encrypt, cmc50_m1_encrypt
from neogeo.pcm2 import pcm2_encrypt

ROM_ID = "263"
ZIP_NAME = "mslug4h"

SIZE_S = 0x020000
SIZE_V_TOTAL = 0x1000000
SIZE_V_PART = 0x800000
SIZE_M_PREFIX = 0x010000
SIZE_M_PAD = 0x010000
SIZE_P1 = 0x100000
SIZE_P2 = 0x400000
SIZE_C_PART = 0x800000
SIZE_C_HALF = 0x1800000
SIZE_C_TOTAL = 0x3000000


GAME = {
    "id": "mslug4h_code_mystics",
    "title": "Metal Slug 4",
    "mame_set": "mslug4h",
    "source_family": "code_mystics",
    "module_type": "custom_converter",
    "search_folder_names": [
        "Metal Slug 4",
        "METAL SLUG 4",
        "mslug4",
    ],
    "source_subfolders": ["Data/rom", "data/rom", "rom", "."],
    "required_source_files": ["p1.bin", "m1.bin", "v1.bin", "c1.bin", "s2.bin"],

    "notes": {
        "summary": "Code Mystics/Amazon source layout for Metal Slug 4. This module uses its own custom converter with built-in Neo Geo helpers.",
        "details": [
            "The conversion logic remains game-specific inside this module.",
            "The core should only call run_custom_converter when a module provides it.",
            "Uses the shared neogeo helper package for PCM2 and CMC50 conversion.",
        ],
    },
    "outputs": [
        {
            "zip_name": "mslug4h.zip",
            "set_name": "mslug4h",
            "type": "main",
            "description": "MAME-compatible mslug4h set reconstructed from Code Mystics source files using built-in Neo Geo helpers.",
            "files": [
                "263-c1.c1",
                "263-c2.c2",
                "263-c3.c3",
                "263-c4.c4",
                "263-c5.c5",
                "263-c6.c6",
                "263-m1.m1",
                "263-ph1.p1",
                "263-ph2.sp2",
                "263-s1d.s1",
                "263-v1.v1",
                "263-v2.v2",
            ],
        }
    ],
    # Required by the current module loader. Actual file building is handled by run_custom_converter.
    "files": [],
}


def read_exact_prefix(path: Path, size: int) -> bytes:
    data = path.read_bytes()
    if len(data) < size:
        raise ValueError(
            f"{path.name} is too small: expected at least 0x{size:X} bytes, got 0x{len(data):X}"
        )
    return data[:size]


def crc32_hex(data: bytes) -> str:
    return f"{binascii.crc32(data) & 0xFFFFFFFF:08x}"


def ss_unswizzle(data: bytes) -> tuple[bytes, bytes]:
    """
    Python port of Ack's ss_unswizzle.c.

    Input is Code Mystics-style swizzled sprite data.
    Output is odd/even plane streams, equivalent to:
      ss_unswizzle c1.bin odd even
    """
    if len(data) % 128 != 0:
        raise ValueError(f"c1.bin size must be a multiple of 128 bytes; got {len(data)}")

    odd = bytearray()
    even = bytearray()
    block_offsets = ((4, 0), (4, 8), (0, 0), (0, 8))

    for tile_start in range(0, len(data), 128):
        tile = data[tile_start:tile_start + 128]

        for x_offset, y_offset in block_offsets:
            for row in range(8):
                planes = [0, 0, 0, 0]
                offset = x_offset + (y_offset * 8) + (row * 8)

                for i in range(3, -1, -1):
                    value = tile[offset + i]

                    planes[0] = (planes[0] << 1) | ((value >> 4) & 0x01)
                    planes[0] = (planes[0] << 1) | ((value >> 0) & 0x01)

                    planes[1] = (planes[1] << 1) | ((value >> 5) & 0x01)
                    planes[1] = (planes[1] << 1) | ((value >> 1) & 0x01)

                    planes[2] = (planes[2] << 1) | ((value >> 6) & 0x01)
                    planes[2] = (planes[2] << 1) | ((value >> 2) & 0x01)

                    planes[3] = (planes[3] << 1) | ((value >> 7) & 0x01)
                    planes[3] = (planes[3] << 1) | ((value >> 3) & 0x01)

                odd.append(planes[0])
                odd.append(planes[1])
                even.append(planes[2])
                even.append(planes[3])

    return bytes(odd), bytes(even)


def interleave_odd_even(odd: bytes, even: bytes) -> bytes:
    """Equivalent to the srec_cat -unsplit odd/even step used by the shell script."""
    if len(odd) != len(even):
        raise ValueError(f"odd/even sizes differ: odd=0x{len(odd):X}, even=0x{len(even):X}")
    out = bytearray(len(odd) + len(even))
    out[0::2] = odd
    out[1::2] = even
    return bytes(out)


def split_odd_even(data: bytes) -> tuple[bytes, bytes]:
    """Equivalent to srec_cat -split 2 0 and -split 2 1."""
    return data[0::2], data[1::2]


def add_zip_entry(zf: zipfile.ZipFile, arcname: str, data: bytes, report: list[tuple[str, int, str]]) -> None:
    zf.writestr(arcname, data)
    report.append((arcname, len(data), crc32_hex(data)))


def convert(source_dir: Path, output_zip: Path) -> list[tuple[str, int, str]]:
    source_dir = source_dir.resolve()
    output_zip = output_zip.resolve()

    required = ["p1.bin", "m1.bin", "v1.bin", "c1.bin", "s2.bin"]
    missing = [name for name in required if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing required source file(s): " + ", ".join(missing))

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    report: list[tuple[str, int, str]] = []

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # S: fixed/text data. The shell script takes this from s2.bin, not s1.bin.
        add_zip_entry(zf, f"{ROM_ID}-s1d.s1", read_exact_prefix(source_dir / "s2.bin", SIZE_S), report)

        # V: sound sample data.
        v_data = pcm2_encrypt((source_dir / "v1.bin").read_bytes(), value=8)
        if len(v_data) < SIZE_V_TOTAL:
            raise ValueError(
                f"PCM2 V output too small: expected 0x{SIZE_V_TOTAL:X}, got 0x{len(v_data):X}"
            )
        add_zip_entry(zf, f"{ROM_ID}-v1.v1", v_data[0:SIZE_V_PART], report)
        add_zip_entry(zf, f"{ROM_ID}-v2.v2", v_data[SIZE_V_PART:SIZE_V_TOTAL], report)

        # M: Z80 code. Shell script uses first 64 KiB from m1.bin, then 64 KiB of 0xFF padding.
        m_dec = read_exact_prefix(source_dir / "m1.bin", SIZE_M_PREFIX) + (b"\xFF" * SIZE_M_PAD)
        m_out = cmc50_m1_encrypt(m_dec)
        add_zip_entry(zf, f"{ROM_ID}-m1.m1", m_out, report)

        # P: 68K program code. No CMC step in the Metal Slug 4 shell script.
        p_source = source_dir / "p1.bin"
        add_zip_entry(zf, f"{ROM_ID}-ph1.p1", read_exact_prefix(p_source, SIZE_P1), report)
        p_all = read_exact_prefix(p_source, SIZE_P1 + SIZE_P2)
        add_zip_entry(zf, f"{ROM_ID}-ph2.sp2", p_all[SIZE_P1:SIZE_P1 + SIZE_P2], report)

        # C: sprites.
        c_source = (source_dir / "c1.bin").read_bytes()
        odd, even = ss_unswizzle(c_source)
        if len(odd) < SIZE_C_HALF or len(even) < SIZE_C_HALF:
            raise ValueError(
                "ss_unswizzle output too small: "
                f"expected at least 0x{SIZE_C_HALF:X} each, "
                f"got odd=0x{len(odd):X}, even=0x{len(even):X}"
            )

        # The shell script uses the first three 8 MiB chunks from odd and even.
        odd1 = odd[:SIZE_C_HALF]
        even1 = even[:SIZE_C_HALF]
        c_dec = interleave_odd_even(odd1, even1)
        if len(c_dec) != SIZE_C_TOTAL:
            raise ValueError(f"C intermediate size mismatch: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(c_dec):X}")

        c_enc = cmc50_gfx_encrypt(c_dec, extra_xor=0x31)
        if len(c_enc) < SIZE_C_TOTAL:
            raise ValueError(
                f"CMC50 C output too small: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(c_enc):X}"
            )

        odd_enc, even_enc = split_odd_even(c_enc[:SIZE_C_TOTAL])
        if len(odd_enc) < SIZE_C_HALF or len(even_enc) < SIZE_C_HALF:
            raise ValueError("Encrypted C odd/even split produced unexpected sizes")

        for index, offset in [(1, 0x0000000), (3, 0x0800000), (5, 0x1000000)]:
            add_zip_entry(zf, f"{ROM_ID}-c{index}.c{index}", odd_enc[offset:offset + SIZE_C_PART], report)
        for index, offset in [(2, 0x0000000), (4, 0x0800000), (6, 0x1000000)]:
            add_zip_entry(zf, f"{ROM_ID}-c{index}.c{index}", even_enc[offset:offset + SIZE_C_PART], report)

    return sorted(report, key=lambda item: item[0])


def run_custom_converter(
    *,
    source_folder: Path,
    output_folder: Path,
    module_folder: Path,
    log: list[str],
) -> bool:
    """
    Custom converter hook for neogeo_extractor.py.

    This keeps Metal Slug 4-specific processing inside the game module while allowing
    the core to treat it as a detected game module.
    """
    output_zip = output_folder / "mslug4h.zip"

    log.append("Custom converter: Metal Slug 4 Code Mystics")
    log.append("  Helpers: built-in Neo Geo PCM2 + CMC50")
    log.append(f"  Output ZIP: {output_zip}")

    report = convert(
        source_dir=source_folder,
        output_zip=output_zip,
    )

    log.append("  Created ZIP contents:")
    for name, size, crc in report:
        log.append(f"    - {name}: size={size}, crc32={crc}")

    return True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build mslug4h.zip from Code Mystics/Amazon Prime Gaming Metal Slug 4 source files."
    )
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="Path to the Metal Slug 4 Data/rom folder containing p1.bin, m1.bin, v1.bin, c1.bin, s2.bin.",
    )

    parser.add_argument("--output", default=f"{ZIP_NAME}.zip", type=Path, help="Output ZIP path. Default: mslug4h.zip")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        report = convert(args.source, args.output)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Created: {args.output}")
    print()
    print("Contents:")
    for name, size, crc in report:
        print(f"  {name:<12} size=0x{size:08X} ({size:>8} bytes) crc32={crc}")

    print()
    print("Next suggested check:")
    print("  mame -verifyroms mslug4h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
