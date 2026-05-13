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

This script replaces dd, split, cat, srec_cat, ss_unswizzle, and zip with
Python code. It still requires the external neo-cmc executable for CMC
encryption/conversion.

Expected source files in --source:
  p1.bin
  m1.bin
  v1.bin
  c1.bin
  s2.bin

Example, Windows PowerShell:
  py .\mslug4_code_mystics_converter.py `
    --source "PATH\TO\Metal Slug 4\Data\rom" `
    --neo-cmc .\neo-cmc.exe `
    --output .\mslug4h.zip

Example, macOS/Linux:
  python3 ./mslug4_code_mystics_converter.py \
    --source "/path/to/Metal Slug 4/Data/rom" \
    --neo-cmc ./neo-cmc \
    --output ./mslug4h.zip
"""

from __future__ import annotations

import argparse
import binascii
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

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
    "external_tools": {
        "neo_cmc": {
            "Darwin": ["neo-cmc-macos", "neo-cmc"],
            "Linux": ["neo-cmc-linux", "neo-cmc"],
            "Windows": ["neo-cmc.exe", "neo-cmc"],
            "default": ["neo-cmc", "neo-cmc.exe"],
        },
    },
    "notes": {
        "summary": "Code Mystics/Amazon source layout for Metal Slug 4. This module uses its own custom converter because it requires neo-cmc.",
        "details": [
            "The conversion logic remains game-specific inside this module.",
            "The core should only call run_custom_converter when a module provides it.",
            "Requires the correct platform neo-cmc binary in the extractor tools folder, extractor folder, game_modules/tools folder, or PATH.",
        ],
    },
    "outputs": [
        {
            "zip_name": "mslug4h.zip",
            "set_name": "mslug4h",
            "type": "main",
            "description": "MAME-compatible mslug4h set reconstructed from Code Mystics source files using neo-cmc.",
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


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


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


def find_executable(path_or_name: str) -> str:
    candidate = Path(path_or_name)
    if candidate.exists():
        return str(candidate)

    found = shutil.which(path_or_name)
    if found:
        return found

    raise FileNotFoundError(f"Could not find executable: {path_or_name}")


def run_neo_cmc(neo_cmc: str, input_file: Path, offset: int, output_file: Path, mode: str) -> None:
    cmd = [neo_cmc, str(input_file), str(offset), str(output_file), "1", ROM_ID, mode]
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

    required = ["p1.bin", "m1.bin", "v1.bin", "c1.bin", "s2.bin"]
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
            # S: fixed/text data. The shell script takes this from s2.bin, not s1.bin.
            add_zip_entry(zf, f"{ROM_ID}-s1d.s1", read_exact_prefix(source_dir / "s2.bin", SIZE_S), report)

            # V: sound sample data.
            v_enc = temp_path / "v1enc.tmp"
            run_neo_cmc(neo_cmc, source_dir / "v1.bin", 0, v_enc, "V")
            v_data = v_enc.read_bytes()
            if len(v_data) < SIZE_V_TOTAL:
                raise ValueError(
                    f"neo-cmc V output too small: expected 0x{SIZE_V_TOTAL:X}, got 0x{len(v_data):X}"
                )
            add_zip_entry(zf, f"{ROM_ID}-v1.v1", v_data[0:SIZE_V_PART], report)
            add_zip_entry(zf, f"{ROM_ID}-v2.v2", v_data[SIZE_V_PART:SIZE_V_TOTAL], report)

            # M: Z80 code. Shell script uses first 64 KiB from m1.bin, then 64 KiB of 0xFF padding.
            m_dec = read_exact_prefix(source_dir / "m1.bin", SIZE_M_PREFIX) + (b"\xFF" * SIZE_M_PAD)
            m_tmp = temp_path / f"{ROM_ID}-m1d.m1"
            write_bytes(m_tmp, m_dec)
            m_out = temp_path / f"{ROM_ID}-m1.m1"
            run_neo_cmc(neo_cmc, m_tmp, 0, m_out, "M")
            add_zip_entry(zf, f"{ROM_ID}-m1.m1", m_out.read_bytes(), report)

            # P: 68K program code. No neo-cmc step in the Metal Slug 4 shell script.
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

            c_dec_tmp = temp_path / "c_dec.tmp"
            c_enc_tmp = temp_path / "c_enc.tmp"
            write_bytes(c_dec_tmp, c_dec)
            run_neo_cmc(neo_cmc, c_dec_tmp, 0, c_enc_tmp, "C")
            c_enc = c_enc_tmp.read_bytes()
            if len(c_enc) < SIZE_C_TOTAL:
                raise ValueError(
                    f"neo-cmc C output too small: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(c_enc):X}"
                )

            odd_enc, even_enc = split_odd_even(c_enc[:SIZE_C_TOTAL])
            if len(odd_enc) < SIZE_C_HALF or len(even_enc) < SIZE_C_HALF:
                raise ValueError("Encrypted C odd/even split produced unexpected sizes")

            for index, offset in [(1, 0x0000000), (3, 0x0800000), (5, 0x1000000)]:
                add_zip_entry(zf, f"{ROM_ID}-c{index}.c{index}", odd_enc[offset:offset + SIZE_C_PART], report)
            for index, offset in [(2, 0x0000000), (4, 0x0800000), (6, 0x1000000)]:
                add_zip_entry(zf, f"{ROM_ID}-c{index}.c{index}", even_enc[offset:offset + SIZE_C_PART], report)

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

    This keeps Metal Slug 4-specific processing inside the game module while allowing
    the core to treat it as a detected game module.
    """
    neo_cmc = find_neo_cmc_for_module(module_folder)
    output_zip = output_folder / "mslug4h.zip"

    log.append("Custom converter: Metal Slug 4 Code Mystics")
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
        description="Build mslug4h.zip from Code Mystics/Amazon Prime Gaming Metal Slug 4 source files."
    )
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="Path to the Metal Slug 4 Data/rom folder containing p1.bin, m1.bin, v1.bin, c1.bin, s2.bin.",
    )
    parser.add_argument(
        "--neo-cmc",
        default="./neo-cmc",
        help="Path to neo-cmc executable. On Windows, usually .\\neo-cmc.exe. Default: ./neo-cmc",
    )
    parser.add_argument("--output", default=f"{ZIP_NAME}.zip", type=Path, help="Output ZIP path. Default: mslug4h.zip")
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
    print("  mame -verifyroms mslug4h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
