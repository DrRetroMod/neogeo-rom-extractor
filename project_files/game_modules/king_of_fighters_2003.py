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
KOF2003 Code Mystics / Amazon Prime Gaming standalone converter.

Builds a kof2003h-style Neo Geo ZIP from the Code Mystics source files used by
The King of Fighters 2003 from Amazon Prime Gaming, following the public shell
conversion flow credited to Shigeshigeru, alhumbra, scrap-a, Tomasz Bednarz,
and Lionel Cordesses.

This script replaces dd, srec_cat, ss_unswizzle, zip, and the old external
neo-cmc command-line step with Python-side conversion helpers.

Expected source files in --source:
  p1.bin
  m1.bin
  v1.bin
  c1.bin

Example:
  python3 kof2003_code_mystics_converter.py \
    --source "/path/to/source_rom_folder" \
    --output ./kof2003h.zip

On Windows PowerShell:
  py .\kof2003_code_mystics_converter.py `
    --source "PATH\TO\SOURCE_ROM_FOLDER" `
    --output .\kof2003h.zip
"""

# Extraction notes:
# This module was developed through source-file analysis, local testing,
# hash comparison, and comparison with public Neo Geo extraction, emulation,
# and preservation research.
#
# The King of Fighters 2003 extraction behaviour was informed by
# goNCommand by Lionel Cordesses and related public KOF 2003 research:
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
from neogeo.pcm2 import pcm2_unswap
from neogeo.pvc import kof2003_p_encrypt

ROM_ID = "271"
ZIP_NAME = "kof2003h"

MIB = 1024 * 1024
SIZE_P_SOURCE = 0x900000
SIZE_P12 = 0x800000
SIZE_P3 = 0x100000
SIZE_M = 0x080000
SIZE_V_TOTAL = 0x1000000
SIZE_V_PART = 0x800000
SIZE_C_TOTAL = 0x4000000
SIZE_C_PART = 0x800000
SIZE_C_HALF = 0x2000000


GAME = {
    "id": "kof2003h_code_mystics",
    "title": "The King of Fighters 2003",
    "mame_set": "kof2003h",
    "source_family": "code_mystics",
    "module_type": "custom_converter",
    "search_folder_names": [
        "The King of Fighters 2003",
        "King of Fighters 2003",
        "KOF 2003",
        "KOF2003",
        "kof2003",
    ],
    "source_subfolders": ["Data/rom", "data/rom", "rom", "."],
    "required_source_files": ["p1.bin", "m1.bin", "v1.bin", "c1.bin"],
    "notes": {
        "summary": "Code Mystics/Amazon source layout for The King of Fighters 2003. This module uses its own custom converter with built-in Neo Geo helpers.",
        "details": [
            "The conversion logic remains game-specific inside this module.",
            "The core should only call run_custom_converter when a module provides it.",
            "Uses the shared neogeo helper package for PCM2, CMC50, and PVC conversion.",
        ],
    },
    "outputs": [
        {
            "zip_name": "kof2003h.zip",
            "set_name": "kof2003h",
            "type": "main",
            "description": "MAME-compatible kof2003h set reconstructed from Code Mystics source files using built-in Neo Geo helpers.",
            "files": [
                "271-c1k.c1",
                "271-c2k.c2",
                "271-c3k.c3",
                "271-c4k.c4",
                "271-c5k.c5",
                "271-c6k.c6",
                "271-c7k.c7",
                "271-c8k.c8",
                "271-m1k.m1",
                "271-p1k.p1",
                "271-p2k.p2",
                "271-p3k.p3",
                "271-v1c.v1",
                "271-v2c.v2",
            ],
        }
    ],
    # Required by the current module loader. Actual file building is handled by run_custom_converter.
    "files": [],
}


def read_exact_prefix(path: Path, size: int) -> bytes:
    data = path.read_bytes()
    if len(data) < size:
        raise ValueError(f"{path.name} is too small: expected at least 0x{size:X} bytes, got 0x{len(data):X}")
    return data[:size]


def crc32_hex(data: bytes) -> str:
    return f"{binascii.crc32(data) & 0xFFFFFFFF:08x}"


def ss_unswizzle(data: bytes) -> tuple[bytes, bytes]:
    """
    Python port of Ack's ss_unswizzle.c.

    Input is Code Mystics-style swizzled sprite data.
    Output is odd/even plane streams.
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
    if len(odd) != len(even):
        raise ValueError(f"odd/even sizes differ: odd=0x{len(odd):X}, even=0x{len(even):X}")
    out = bytearray(len(odd) + len(even))
    out[0::2] = odd
    out[1::2] = even
    return bytes(out)


def split_odd_even(data: bytes) -> tuple[bytes, bytes]:
    return data[0::2], data[1::2]


def split_4_take_2(data: bytes, start: int) -> bytes:
    """Equivalent to: srec_cat data -Binary -split 4 <start> 2"""
    if start not in (0, 2):
        raise ValueError("start must be 0 or 2 for KOF2003 PROM split")
    if len(data) % 4 != 0:
        raise ValueError(f"PROM split input size must be divisible by 4; got 0x{len(data):X}")

    out = bytearray()
    for pos in range(start, len(data), 4):
        out.extend(data[pos:pos + 2])
    return bytes(out)


def add_zip_entry(zf: zipfile.ZipFile, arcname: str, data: bytes, report: list[tuple[str, int, str]]) -> None:
    zf.writestr(arcname, data)
    report.append((arcname, len(data), crc32_hex(data)))


def convert(
    source_dir: Path,
    output_zip: Path,
    *,
    show_progress: bool = False,
) -> list[tuple[str, int, str]]:
    source_dir = source_dir.resolve()
    output_zip = output_zip.resolve()

    required = ["p1.bin", "m1.bin", "v1.bin", "c1.bin"]
    missing = [name for name in required if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing required source file(s): " + ", ".join(missing))

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    report: list[tuple[str, int, str]] = []

    total_steps = 14
    step_index = 0

    def progress(output_name: str) -> None:
        nonlocal step_index
        step_index += 1

        if show_progress:
            print(f"  [{step_index}/{total_steps}] Building {output_name}")

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # V: sound data
        v_data = pcm2_unswap((source_dir / "v1.bin").read_bytes(), value=5)
        if len(v_data) < SIZE_V_TOTAL:
            raise ValueError(f"PCM2 V output too small: expected 0x{SIZE_V_TOTAL:X}, got 0x{len(v_data):X}")

        progress(f"{ROM_ID}-v1c.v1")
        add_zip_entry(zf, f"{ROM_ID}-v1c.v1", v_data[0:SIZE_V_PART], report)

        progress(f"{ROM_ID}-v2c.v2")
        add_zip_entry(zf, f"{ROM_ID}-v2c.v2", v_data[SIZE_V_PART:SIZE_V_TOTAL], report)

        # M: Z80 code
        m_data = read_exact_prefix(source_dir / "m1.bin", SIZE_M)
        m_out = cmc50_m1_encrypt(m_data)

        progress(f"{ROM_ID}-m1k.m1")
        add_zip_entry(zf, f"{ROM_ID}-m1k.m1", m_out, report)

        # P: 68K code
        p_source = read_exact_prefix(source_dir / "p1.bin", SIZE_P_SOURCE)
        p_enc_data = kof2003_p_encrypt(p_source)
        if len(p_enc_data) < SIZE_P_SOURCE:
            raise ValueError(f"PVC P output too small: expected 0x{SIZE_P_SOURCE:X}, got 0x{len(p_enc_data):X}")

        p12 = p_enc_data[:SIZE_P12]

        progress(f"{ROM_ID}-p3k.p3")
        add_zip_entry(zf, f"{ROM_ID}-p3k.p3", p_enc_data[SIZE_P12:SIZE_P12 + SIZE_P3], report)

        progress(f"{ROM_ID}-p1k.p1")
        add_zip_entry(zf, f"{ROM_ID}-p1k.p1", split_4_take_2(p12, 0), report)

        progress(f"{ROM_ID}-p2k.p2")
        add_zip_entry(zf, f"{ROM_ID}-p2k.p2", split_4_take_2(p12, 2), report)

        # C: sprites
        c_source = (source_dir / "c1.bin").read_bytes()
        odd, even = ss_unswizzle(c_source)
        crom = interleave_odd_even(odd, even)
        if len(crom) != SIZE_C_TOTAL:
            raise ValueError(f"CROM intermediate size mismatch: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(crom):X}")

        c_enc = cmc50_gfx_encrypt(crom, extra_xor=0x9D)
        if len(c_enc) < SIZE_C_TOTAL:
            raise ValueError(f"CMC50 C output too small: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(c_enc):X}")

        odd_enc, even_enc = split_odd_even(c_enc[:SIZE_C_TOTAL])
        if len(odd_enc) != SIZE_C_HALF or len(even_enc) != SIZE_C_HALF:
            raise ValueError("Encrypted C odd/even split produced unexpected sizes")

        for index, offset in [(1, 0x0000000), (3, 0x0800000), (5, 0x1000000), (7, 0x1800000)]:
            output_name = f"{ROM_ID}-c{index}k.c{index}"
            progress(output_name)
            add_zip_entry(zf, output_name, odd_enc[offset:offset + SIZE_C_PART], report)

        for index, offset in [(2, 0x0000000), (4, 0x0800000), (6, 0x1000000), (8, 0x1800000)]:
            output_name = f"{ROM_ID}-c{index}k.c{index}"
            progress(output_name)
            add_zip_entry(zf, output_name, even_enc[offset:offset + SIZE_C_PART], report)

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

    This keeps KOF2003-specific processing inside the game module while allowing
    the core to treat it as a detected game module.
    """
    _ = module_folder
    output_zip = output_folder / "kof2003h.zip"

    log.append("Custom converter: KOF2003 Code Mystics")
    log.append("  Helpers: built-in Neo Geo PCM2 + CMC50 + PVC")
    log.append(f"  Output ZIP: {output_zip}")

    report = convert(
        source_dir=source_folder,
        output_zip=output_zip,
        show_progress=True,
    )

    log.append("  Created ZIP contents:")
    for name, size, crc in report:
        log.append(f"    - {name}: size={size}, crc32={crc}")

    return True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build kof2003h.zip from Code Mystics/Amazon Prime Gaming KOF2003 source files."
    )
    parser.add_argument("--source", required=True, type=Path, help="Path to the KOF2003 Data/rom folder containing p1.bin, m1.bin, v1.bin, c1.bin.")
    parser.add_argument("--output", default=f"{ZIP_NAME}.zip", type=Path, help="Output ZIP path. Default: kof2003h.zip")
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
    print("  mame -verifyroms kof2003h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
