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

This script replaces dd, srec_cat, ss_unswizzle, and zip with Python code.
It still requires the external neo-cmc executable for CMC encryption/conversion.

Expected source files in --source:
  p1.bin
  m1.bin
  v1.bin
  c1.bin

Example:
  python3 kof2003_code_mystics_converter.py \
    --source "/path/to/source_rom_folder" \
    --neo-cmc ./neo-cmc \
    --output ./kof2003h.zip

On Windows PowerShell:
  py .\kof2003_code_mystics_converter.py `
    --source "PATH\TO\SOURCE_ROM_FOLDER" `
    --neo-cmc .\neo-cmc.exe `
    --output .\kof2003h.zip
"""

from __future__ import annotations

import argparse
import binascii
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

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
    "external_tools": {
        "neo_cmc": {
            "Darwin": ["neo-cmc-macos", "neo-cmc"],
            "Linux": ["neo-cmc-linux", "neo-cmc"],
            "Windows": ["neo-cmc.exe", "neo-cmc"],
            "default": ["neo-cmc", "neo-cmc.exe"],
        },
    },
    "notes": {
        "summary": "Code Mystics/Amazon source layout for The King of Fighters 2003. This module uses its own custom converter because it requires neo-cmc.",
        "details": [
            "The conversion logic remains game-specific inside this module.",
            "The core should only call run_custom_converter when a module provides it.",
            "Requires neo-cmc.exe or neo-cmc to be available in the extractor folder, extractor tools folder, this module's tools folder, or PATH.",
        ],
    },
    "outputs": [
        {
            "zip_name": "kof2003h.zip",
            "set_name": "kof2003h",
            "type": "main",
            "description": "MAME-compatible kof2003h set reconstructed from Code Mystics source files using neo-cmc.",
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


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


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


def find_executable(path_or_name: str) -> str:
    candidate = Path(path_or_name)
    if candidate.exists():
        return str(candidate)

    found = shutil.which(path_or_name)
    if found:
        return found

    raise FileNotFoundError(f"Could not find executable: {path_or_name}")


def run_neo_cmc(neo_cmc: str, input_file: Path, offset: int, output_file: Path, mode: str, extra: str | None = None) -> None:
    cmd = [neo_cmc, str(input_file), str(offset), str(output_file), "1", ROM_ID, mode]
    if extra is not None:
        cmd.append(extra)

    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        details = []
        if result.stdout.strip():
            details.append("stdout:\n" + result.stdout.strip())
        if result.stderr.strip():
            details.append("stderr:\n" + result.stderr.strip())
        raise RuntimeError(f"neo-cmc failed: {' '.join(cmd)}\n" + "\n".join(details))

    if not output_file.exists():
        raise RuntimeError(f"neo-cmc did not create expected output: {output_file}")


def add_zip_entry(zf: zipfile.ZipFile, arcname: str, data: bytes, report: list[tuple[str, int, str]]) -> None:
    zf.writestr(arcname, data)
    report.append((arcname, len(data), crc32_hex(data)))


def convert(source_dir: Path, output_zip: Path, neo_cmc_arg: str, keep_temp: bool) -> list[tuple[str, int, str]]:
    source_dir = source_dir.resolve()
    output_zip = output_zip.resolve()
    neo_cmc = find_executable(neo_cmc_arg)

    required = ["p1.bin", "m1.bin", "v1.bin", "c1.bin"]
    missing = [name for name in required if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing required source file(s): " + ", ".join(missing))

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    temp_root: tempfile.TemporaryDirectory[str] | None = None
    if keep_temp:
        temp_path = output_zip.parent / f"{ZIP_NAME}_temp"
        if temp_path.exists():
            shutil.rmtree(temp_path)
        temp_path.mkdir(parents=True)
    else:
        temp_root = tempfile.TemporaryDirectory(prefix=f"{ZIP_NAME}_")
        temp_path = Path(temp_root.name)

    report: list[tuple[str, int, str]] = []

    try:
        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            # V: sound data
            v_enc = temp_path / "v1enc.tmp"
            run_neo_cmc(neo_cmc, source_dir / "v1.bin", 0, v_enc, "V")
            v_data = v_enc.read_bytes()
            if len(v_data) < SIZE_V_TOTAL:
                raise ValueError(f"neo-cmc V output too small: expected 0x{SIZE_V_TOTAL:X}, got 0x{len(v_data):X}")
            add_zip_entry(zf, f"{ROM_ID}-v1c.v1", v_data[0:SIZE_V_PART], report)
            add_zip_entry(zf, f"{ROM_ID}-v2c.v2", v_data[SIZE_V_PART:SIZE_V_TOTAL], report)

            # M: Z80 code
            m_tmp = temp_path / f"{ROM_ID}-m1.tmp"
            write_bytes(m_tmp, read_exact_prefix(source_dir / "m1.bin", SIZE_M))
            m_out = temp_path / f"{ROM_ID}-m1k.m1"
            run_neo_cmc(neo_cmc, m_tmp, 0, m_out, "M")
            add_zip_entry(zf, f"{ROM_ID}-m1k.m1", m_out.read_bytes(), report)

            # P: 68K code
            p_tmp = temp_path / f"{ROM_ID}-p1.bin"
            write_bytes(p_tmp, read_exact_prefix(source_dir / "p1.bin", SIZE_P_SOURCE))
            p_enc = temp_path / "enc_prom.tmp"
            run_neo_cmc(neo_cmc, p_tmp, 0, p_enc, "P", "h")
            p_enc_data = p_enc.read_bytes()
            if len(p_enc_data) < SIZE_P_SOURCE:
                raise ValueError(f"neo-cmc P output too small: expected 0x{SIZE_P_SOURCE:X}, got 0x{len(p_enc_data):X}")
            p12 = p_enc_data[:SIZE_P12]
            add_zip_entry(zf, f"{ROM_ID}-p3k.p3", p_enc_data[SIZE_P12:SIZE_P12 + SIZE_P3], report)
            add_zip_entry(zf, f"{ROM_ID}-p1k.p1", split_4_take_2(p12, 0), report)
            add_zip_entry(zf, f"{ROM_ID}-p2k.p2", split_4_take_2(p12, 2), report)

            # C: sprites
            c_source = (source_dir / "c1.bin").read_bytes()
            odd, even = ss_unswizzle(c_source)
            crom = interleave_odd_even(odd, even)
            if len(crom) != SIZE_C_TOTAL:
                raise ValueError(f"CROM intermediate size mismatch: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(crom):X}")
            crom_tmp = temp_path / "crom.bin.tmp"
            write_bytes(crom_tmp, crom)
            c_enc_tmp = temp_path / "enc_crom.bin.tmp"
            run_neo_cmc(neo_cmc, crom_tmp, SIZE_C_TOTAL, c_enc_tmp, "C")
            c_enc = c_enc_tmp.read_bytes()
            if len(c_enc) < SIZE_C_TOTAL:
                raise ValueError(f"neo-cmc C output too small: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(c_enc):X}")
            odd_enc, even_enc = split_odd_even(c_enc[:SIZE_C_TOTAL])
            if len(odd_enc) != SIZE_C_HALF or len(even_enc) != SIZE_C_HALF:
                raise ValueError("Encrypted C odd/even split produced unexpected sizes")

            for index, offset in [(1, 0x0000000), (3, 0x0800000), (5, 0x1000000), (7, 0x1800000)]:
                add_zip_entry(zf, f"{ROM_ID}-c{index}k.c{index}", odd_enc[offset:offset + SIZE_C_PART], report)
            for index, offset in [(2, 0x0000000), (4, 0x0800000), (6, 0x1000000), (8, 0x1800000)]:
                add_zip_entry(zf, f"{ROM_ID}-c{index}k.c{index}", even_enc[offset:offset + SIZE_C_PART], report)

    finally:
        if temp_root is not None:
            temp_root.cleanup()

    return sorted(report, key=lambda item: item[0])



def find_neo_cmc_for_module(module_folder: Path) -> str:
    """
    Find neo-cmc for extractor/module use.

    Search order:
      1. Platform-specific tool names
      2. NeoGeo Extractor/tools/
      3. NeoGeo Extractor/
      4. game_modules/tools/
      5. PATH
    """
    extractor_folder = module_folder.parent

    neo_cmc_config = GAME.get("external_tools", {}).get("neo_cmc", {})

    if isinstance(neo_cmc_config, dict):
        system_name = platform.system()
        names = neo_cmc_config.get(system_name, neo_cmc_config.get("default", ["neo-cmc"]))
    else:
        names = neo_cmc_config

    candidates: list[Path] = []

    for name in names:
        candidates.extend(
            [
                extractor_folder / "tools" / name,
                extractor_folder / name,
                module_folder / "tools" / name,
            ]
        )

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)

    for name in names:
        found = shutil.which(name)
        if found:
            return found

    raise FileNotFoundError(
        "Could not find neo-cmc. Put the correct platform binary in the extractor tools folder, "
        "for example tools/neo-cmc-macos, tools/neo-cmc-linux, or tools/neo-cmc.exe."
    )


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
    neo_cmc = find_neo_cmc_for_module(module_folder)
    output_zip = output_folder / "kof2003h.zip"

    log.append("Custom converter: KOF2003 Code Mystics")
    log.append(f"  neo-cmc: {neo_cmc}")
    log.append(f"  Output ZIP: {output_zip}")

    report = convert(
        source_dir=source_folder,
        output_zip=output_zip,
        neo_cmc_arg=neo_cmc,
        keep_temp=False,
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
    parser.add_argument("--neo-cmc", default="./neo-cmc", help="Path to neo-cmc executable. Default: ./neo-cmc")
    parser.add_argument("--output", default=f"{ZIP_NAME}.zip", type=Path, help="Output ZIP path. Default: kof2003h.zip")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary files beside the output ZIP for debugging.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        report = convert(args.source, args.output, args.neo_cmc, args.keep_temp)
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
