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
Metal Slug 3 Dotemu / Steam-style standalone converter.

Builds a MAME-style mslug3.zip from Dotemu source files:
  mslug3_tiles
  mslug3_adpcm
  mslug3_game_z80
  mslug3_game_m68k

This module replaces the previous external prog.exe, tileswap.exe, and
 tiles2crom.exe steps with Python-side logic:
  - SMA/P-ROM encryption is ported from the supplied prog.c/bitswap.h source.
  - Dotemu tile re-encoding is adapted from mslug-rom-extractor.py.
    Note: sfix_reencode() is not applied to mslug3_tiles; that helper is for S-ROM/SFIX data.
  - bcut.exe, BSwap.exe, copy /b, Compress-Archive, and CRC validation are
    replaced with Python slicing, interleaving, zip, and CRC code.

Important CMC note:
  Metal Slug 3 uses CMC42 graphics encryption with key 0xAD. This version uses
  the pure-Python cmc42_gfx_encrypt helper from neogeo/cmc.py, so neo-cmc.exe is
  no longer required.

Standalone examples:
  python3 metal_slug_3.py --source "/path/to/Metal Slug 3/resources/game" --output ./mslug3.zip
  py .\metal_slug_3.py --source "C:\\Path\\To\\Metal Slug 3\\resources\\game" --output .\mslug3.zip
"""

# Extraction notes:
# This module was developed by translating the supplied convert_mslug3_dotemu.py
# flow and replacing the available external helper steps with Python-side code.
#
# Remaining external helper:
# - none for CMC; CMC42 is handled by neogeo/cmc.py.
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

from __future__ import annotations

import argparse
import binascii
import sys
import zipfile
from pathlib import Path

from neogeo.cmc import MSLUG3_GFX_KEY, cmc42_gfx_encrypt

ROM_ID = "256"
ZIP_NAME = "mslug3"
SCRIPT_VERSION = "mslug3-python-direct-tiles-cmc42-v2026-05-14g"

SIZE_P_SOURCE = 0x900000
SIZE_SMA = 0x040000
SIZE_P_PART = 0x400000
SIZE_M = 0x020000
SIZE_V_PART = 0x400000
SIZE_V_TOTAL = 0x1000000
SIZE_C_PART = 0x800000
SIZE_C_TOTAL = 0x4000000
SIZE_C_HALF = 0x2000000
CMC42_GFX_KEY = 0xAD

REQUIRED_SOURCE_FILES = [
    "mslug3_tiles",
    "mslug3_adpcm",
    "mslug3_game_z80",
    "mslug3_game_m68k",
]

EXPECTED_CRCS = {
    "256-c1.c1": 0x5A79C34E,
    "256-c2.c2": 0x944C362C,
    "256-c3.c3": 0x6E69D36F,
    "256-c4.c4": 0x0B755B4EB,
    "256-c5.c5": 0x7AACAB47,
    "256-c6.c6": 0xC698FD5D,
    "256-c7.c7": 0xCFCEDDD2,
    "256-c8.c8": 0x4D9BE34C,
    "256-m1.bin": 0xEAEEC116,
    "256-p1.bin": 0xB07EDFD5,
    "256-p2.bin": 0x6097C26B,
    "256-sma.bin": 0x9CD55736,
    "256-v1.v1": 0xF2690241,
    "256-v2.v2": 0x7E2A10BD,
    "256-v3.v3": 0x0EAEC17C,
    "256-v4.v4": 0x9B4B22D4,
}

GAME = {
    "id": "mslug3_dotemu",
    "title": "Metal Slug 3",
    "mame_set": "mslug3",
    "source_family": "dotemu",
    "module_type": "custom_converter",
    "search_folder_names": [
        "Metal Slug 3",
        "METAL SLUG 3",
        "mslug3",
    ],
    "source_subfolders": ["resources/game", "Resources/game", "game", "."],
    "required_source_files": REQUIRED_SOURCE_FILES,
    "notes": {
        "summary": "Dotemu source layout for Metal Slug 3. This module uses a custom converter with Python-side SMA/PROM and tile conversion.",
        "details": [
            "The conversion logic remains game-specific inside this module.",
            "The core should only call run_custom_converter when a module provides it.",
            "prog.exe, tileswap.exe, and tiles2crom.exe are not required by this module.",
            "CMC42 C-ROM encryption is handled by the shared neogeo.cmc helper.",
        ],
    },
    "outputs": [
        {
            "zip_name": "mslug3.zip",
            "set_name": "mslug3",
            "type": "main",
            "description": "MAME-style mslug3 set reconstructed from Dotemu source files.",
            "files": list(EXPECTED_CRCS.keys()),
        }
    ],
    # Required by the current module loader. Actual file building is handled by run_custom_converter.
    "files": [],
}


def crc32_hex(data: bytes) -> str:
    return f"{binascii.crc32(data) & 0xFFFFFFFF:08x}"


def crc32_int(data: bytes) -> int:
    return binascii.crc32(data) & 0xFFFFFFFF


def read_exact_prefix(path: Path, size: int) -> bytes:
    data = path.read_bytes()
    if len(data) < size:
        raise ValueError(f"{path.name} is too small: expected at least 0x{size:X} bytes, got 0x{len(data):X}")
    return data[:size]


def bitswap(value: int, *bits: int) -> int:
    out = 0
    for bit in bits:
        out = (out << 1) | ((value >> bit) & 1)
    return out


def get_u16le(data: bytearray, word_index: int) -> int:
    off = word_index * 2
    return data[off] | (data[off + 1] << 8)


def set_u16le(data: bytearray, word_index: int, value: int) -> None:
    off = word_index * 2
    data[off] = value & 0xFF
    data[off + 1] = (value >> 8) & 0xFF


# prog.c table rows for type 3 / mslug3, crypt=1 / encrypt.
_MSLUG3_P1_DATA_SWAP_ENCRYPT = (4, 13, 10, 5, 14, 3, 2, 6, 8, 0, 1, 15, 12, 7, 11, 9)
_MSLUG3_P2_ADDRESS_SWAP_ENCRYPT = (15, 11, 8, 1, 13, 4, 6, 7, 3, 10, 2, 9, 5, 14, 0, 12)
_MSLUG3_P2_ADDRESS_OFFSET = 0x800000


def mslug3_sma_encrypt(p1_decrypted: bytes) -> tuple[bytes, bytes, bytes]:
    """
    Python port of the mslug3 encrypt path from the supplied prog.c.

    Input mirrors prog.exe's p1_decrypted file.
    Returns:
      256-sma.bin data
      256-p1.bin data
      256-p2.bin data
    """
    if len(p1_decrypted) < SIZE_P_SOURCE:
        raise ValueError(
            f"mslug3_game_m68k is too small for SMA encryption: expected at least 0x{SIZE_P_SOURCE:X}, got 0x{len(p1_decrypted):X}"
        )

    src = bytearray(p1_decrypted[:SIZE_P_SOURCE])
    base_words = 0x100000 // 2

    # prog.c: data bitswap over src + 0x100000 for 0x800000 bytes.
    a = _MSLUG3_P1_DATA_SWAP_ENCRYPT
    for i in range(0x800000 // 2):
        word_index = base_words + i
        value = get_u16le(src, word_index)
        set_u16le(src, word_index, bitswap(value, *a))

    # prog.c: per-0x10000-byte P2 address block scramble over src + 0x100000.
    c = _MSLUG3_P2_ADDRESS_SWAP_ENCRYPT
    words_per_block = 0x010000 // 2
    total_words = _MSLUG3_P2_ADDRESS_OFFSET // 2

    for i in range(0, total_words, words_per_block):
        block = [get_u16le(src, base_words + i + j) for j in range(words_per_block)]
        for j in range(words_per_block):
            source_index = bitswap(j, 23, 22, 21, 20, 19, 18, 17, 16, *c)
            set_u16le(src, base_words + i + j, block[source_index])

    sma = bytes(src[0x0C0000:0x100000])
    p1 = bytes(src[0x100000:0x500000])
    p2 = bytes(src[0x500000:0x900000])

    if len(sma) != SIZE_SMA or len(p1) != SIZE_P_PART or len(p2) != SIZE_P_PART:
        raise ValueError("Unexpected SMA/P output size after encryption")

    return sma, p1, p2


def sfix_reencode_data(data: bytes) -> bytes:
    """
    Python equivalent of sfix_reencode().

    This is intentionally not used for mslug3_tiles. It is retained only for
    reference/debugging, because sfix_reencode() is for S-ROM/SFIX-style data.

    Reorganises every 32-byte block from:
      cdab cdab ...
    into grouped a/b/c/d planes, matching the helper logic from
    mslug-rom-extractor.py.
    """
    if len(data) % 32 != 0:
        raise ValueError(f"sfix-style reencode input must be a multiple of 32 bytes; got 0x{len(data):X}")

    output = bytearray()
    for i in range(0, len(data), 32):
        block = data[i:i + 32]
        buffer = bytearray(32)
        for j in range(8):
            buffer[0 + j] = block[j * 4 + 2]
            buffer[8 + j] = block[j * 4 + 3]
            buffer[16 + j] = block[j * 4 + 0]
            buffer[24 + j] = block[j * 4 + 1]
        output.extend(buffer)
    return bytes(output)


def dotemu_tiles_to_crom_chunks(data: bytes, crom_size: int, chunk_count: int) -> list[bytes]:
    """
    Byte-oriented adaptation of tiles_reencode() from mslug-rom-extractor.py.

    Returns C chunks in order:
      c1, c2, c3, c4, c5, c6, c7, c8
    for Metal Slug 3.
    """
    expected = crom_size * chunk_count
    if len(data) != expected:
        raise ValueError(f"mslug3_tiles size mismatch: expected 0x{expected:X}, got 0x{len(data):X}")
    if len(data) % 128 != 0:
        raise ValueError(f"mslug3_tiles size must be a multiple of 128 bytes, got 0x{len(data):X}")

    outa = bytearray()
    outb = bytearray()

    def col_to_neogeo(col: list[list[int]]) -> None:
        for row in col:
            bp0 = bp1 = bp2 = bp3 = 0
            pixels = bytearray()
            for b in row:
                pixels.append(b & 0x0F)
                pixels.append(b >> 4)
            for p in range(8):
                bp0 |= (pixels[p] & 1) << (7 - p)
                bp1 |= ((pixels[p] >> 1) & 1) << (7 - p)
                bp2 |= ((pixels[p] >> 2) & 1) << (7 - p)
                bp3 |= ((pixels[p] >> 3) & 1) << (7 - p)
            outa.append(bp0)
            outa.append(bp1)
            outb.append(bp2)
            outb.append(bp3)

    for tile in range(0, len(data), 128):
        left_col: list[list[int]] = []
        right_col: list[list[int]] = []
        row_buffer: list[int] = []

        for byte_index in range(128):
            row_buffer.append(data[tile + byte_index])
            if len(row_buffer) == 4:
                if ((byte_index // 4) % 2) == 0:
                    left_col.append(row_buffer[:])
                else:
                    right_col.append(row_buffer[:])
                row_buffer.clear()

        col_to_neogeo(right_col)
        col_to_neogeo(left_col)

    chunks: list[bytes] = []
    for i in range(chunk_count // 2):
        chunks.append(bytes(outa[i * crom_size:(i + 1) * crom_size]))
        chunks.append(bytes(outb[i * crom_size:(i + 1) * crom_size]))

    for index, chunk in enumerate(chunks, start=1):
        if len(chunk) != crom_size:
            raise ValueError(f"C{index} chunk size mismatch: expected 0x{crom_size:X}, got 0x{len(chunk):X}")

    return chunks


def interleave_odd_even(odd: bytes, even: bytes) -> bytes:
    if len(odd) != len(even):
        raise ValueError(f"odd/even sizes differ: odd=0x{len(odd):X}, even=0x{len(even):X}")
    out = bytearray(len(odd) + len(even))
    out[0::2] = odd
    out[1::2] = even
    return bytes(out)


def split_odd_even(data: bytes) -> tuple[bytes, bytes]:
    if len(data) % 2:
        raise ValueError(f"Cannot split odd-sized data: 0x{len(data):X}")
    return data[0::2], data[1::2]


def split_chunks(data: bytes, chunk_size: int, count: int) -> list[bytes]:
    expected = chunk_size * count
    if len(data) != expected:
        raise ValueError(f"split input size mismatch: expected 0x{expected:X}, got 0x{len(data):X}")
    return [data[i * chunk_size:(i + 1) * chunk_size] for i in range(count)]


def encrypt_crom_cmc42(crom: bytes) -> bytes:
    """Encrypt C-ROM data using the pure-Python CMC42 helper."""
    if len(crom) != SIZE_C_TOTAL:
        raise ValueError(f"CROM intermediate size mismatch: expected 0x{SIZE_C_TOTAL:X}, got 0x{len(crom):X}")
    return cmc42_gfx_encrypt(crom, extra_xor=MSLUG3_GFX_KEY)


def build_crom_outputs(source_dir: Path, module_folder: Path | None, explicit_neo_cmc: Path | None = None, progress: bool = False) -> dict[str, bytes]:
    # Important correction:
    # tiles_reencode() from mslug-rom-extractor.py already represents the Dotemu
    # tile-to-NeoGeo C-ROM conversion path for sprite data. sfix_reencode() is for
    # S-ROM/SFIX data and must NOT be applied to mslug3_tiles.
    if progress:
        print("  [C1] Reading mslug3_tiles", flush=True)
    tile_data = (source_dir / "mslug3_tiles").read_bytes()
    if progress:
        print("  [C2] Applying tiles_reencode-style Dotemu tile conversion", flush=True)
    c_chunks = dotemu_tiles_to_crom_chunks(tile_data, SIZE_C_PART, 8)

    odd = b"".join([c_chunks[0], c_chunks[2], c_chunks[4], c_chunks[6]])
    even = b"".join([c_chunks[1], c_chunks[3], c_chunks[5], c_chunks[7]])
    if len(odd) != SIZE_C_HALF or len(even) != SIZE_C_HALF:
        raise ValueError("Unexpected odd/even C chunk sizes before CMC42 encryption")

    if progress:
        print("  [C3] Interleaving odd/even into crom.bin data", flush=True)
    crom = interleave_odd_even(odd, even)
    if progress:
        print("  [C4] Running pure-Python CMC42 encryption", flush=True)
    encrypted = encrypt_crom_cmc42(crom)
    if progress:
        print("  [C5] Splitting encrypted C data into final ROM chunks", flush=True)
    odd_enc, even_enc = split_odd_even(encrypted)

    odd_chunks = split_chunks(odd_enc, SIZE_C_PART, 4)
    even_chunks = split_chunks(even_enc, SIZE_C_PART, 4)

    return {
        "256-c1.c1": odd_chunks[0],
        "256-c2.c2": even_chunks[0],
        "256-c3.c3": odd_chunks[1],
        "256-c4.c4": even_chunks[1],
        "256-c5.c5": odd_chunks[2],
        "256-c6.c6": even_chunks[2],
        "256-c7.c7": odd_chunks[3],
        "256-c8.c8": even_chunks[3],
    }


def build_roms(source_dir: Path, module_folder: Path | None = None, explicit_neo_cmc: Path | None = None, progress: bool = False) -> dict[str, bytes]:
    source_dir = source_dir.resolve()
    missing = [name for name in REQUIRED_SOURCE_FILES if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError("Missing required source file(s): " + ", ".join(missing))

    output: dict[str, bytes] = {}

    # P/SMA: replaces prog.exe.
    if progress:
        print("  [P] Building encrypted P/SMA ROMs", flush=True)
    sma, p1, p2 = mslug3_sma_encrypt(read_exact_prefix(source_dir / "mslug3_game_m68k", SIZE_P_SOURCE))
    output["256-sma.bin"] = sma
    output["256-p1.bin"] = p1
    output["256-p2.bin"] = p2

    # M and V: direct copy/split, matching the original MS3 conversion flow.
    if progress:
        print("  [M/V] Copying full M1 and splitting V ROMs", flush=True)
    output["256-m1.bin"] = (source_dir / "mslug3_game_z80").read_bytes()
    v_data = read_exact_prefix(source_dir / "mslug3_adpcm", SIZE_V_TOTAL)
    output["256-v1.v1"] = v_data[0x000000:0x400000]
    output["256-v2.v2"] = v_data[0x400000:0x800000]
    output["256-v3.v3"] = v_data[0x800000:0xC00000]
    output["256-v4.v4"] = v_data[0xC00000:0x1000000]

    # C: replaces tileswap.exe, tiles2crom.exe, and neo-cmc.exe using Python helpers.
    if progress:
        print("  [C] Building C ROMs", flush=True)
    output.update(build_crom_outputs(source_dir, module_folder, explicit_neo_cmc, progress=progress))

    return output


def validate_roms(roms: dict[str, bytes]) -> list[tuple[str, int, str]]:
    report: list[tuple[str, int, str]] = []
    bad: list[str] = []

    for name, expected_crc in EXPECTED_CRCS.items():
        data = roms.get(name)
        if data is None:
            bad.append(f"{name}: missing")
            continue
        actual_crc = crc32_int(data)
        report.append((name, len(data), f"{actual_crc:08x}"))
        if actual_crc != expected_crc:
            bad.append(f"{name}: got {actual_crc:08X}, expected {expected_crc:08X}")

    if bad:
        raise ValueError("CRC validation failed:\n  " + "\n  ".join(bad))

    return sorted(report, key=lambda item: item[0])


def write_zip(output_zip: Path, roms: dict[str, bytes]) -> None:
    output_zip = output_zip.resolve()
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in EXPECTED_CRCS.keys():
            zf.writestr(name, roms[name])


def convert(
    source_dir: Path,
    output_zip: Path,
    *,
    module_folder: Path | None = None,
    explicit_neo_cmc: Path | None = None,
    show_progress: bool = False,
) -> list[tuple[str, int, str]]:
    if show_progress:
        print("  [1/4] Building ROM data", flush=True)
    roms = build_roms(source_dir, module_folder, explicit_neo_cmc, progress=show_progress)

    if show_progress:
        print("  [2/4] Validating CRCs", flush=True)
    report = validate_roms(roms)

    if show_progress:
        print("  [3/4] Writing ZIP", flush=True)
    write_zip(output_zip, roms)

    if show_progress:
        print("  [4/4] Complete", flush=True)
    return report


def run_custom_converter(
    *,
    source_folder: Path,
    output_folder: Path,
    module_folder: Path,
    log: list[str],
) -> bool:
    """
    Custom converter hook for neogeo_extractor.py.
    """
    output_zip = output_folder / "mslug3.zip"

    log.append("Custom converter: Metal Slug 3 Dotemu")
    log.append("  Helpers: Python SMA/PROM + Python Dotemu tile conversion")
    log.append("  Helpers: Python CMC42 C-ROM encryption via neogeo.cmc")
    log.append(f"  Output ZIP: {output_zip}")

    report = convert(
        source_dir=source_folder,
        output_zip=output_zip,
        module_folder=module_folder,
        show_progress=True,
    )

    log.append("  Created ZIP contents:")
    for name, size, crc in report:
        log.append(f"    - {name}: size={size}, crc32={crc}")

    return True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build mslug3.zip from Dotemu Metal Slug 3 source files.")
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="Folder containing mslug3_tiles, mslug3_adpcm, mslug3_game_z80, and mslug3_game_m68k.",
    )
    parser.add_argument("--output", default=f"{ZIP_NAME}.zip", type=Path, help="Output ZIP path. Default: mslug3.zip")
    parser.add_argument("--neo-cmc", default=None, type=Path, help="Ignored compatibility option; CMC42 is now pure Python")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    print(f"Metal Slug 3 converter version: {SCRIPT_VERSION}", flush=True)
    args = parse_args(argv)

    try:
        report = convert(
            source_dir=args.source,
            output_zip=args.output,
            module_folder=Path(__file__).resolve().parent,
            explicit_neo_cmc=args.neo_cmc,
            show_progress=True,
        )
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
    print("  mame -verifyroms mslug3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
