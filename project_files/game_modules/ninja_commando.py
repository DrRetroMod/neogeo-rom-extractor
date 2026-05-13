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

"""
Ninja Commando module.

Converted from extract_ncommand_ngprime_dual.py.

This module declares only the corrected MAME-clean ncommand.zip output.
The old script's separate original Amazon/Code Mystics P1 preservation ZIP and included BIOS ZIP are intentionally not part of this MAME game module.
"""

# Extraction notes:
# This module was developed through source-file analysis, local testing,
# hash comparison, and comparison with public Neo Geo extraction, emulation,
# and preservation research.
#
# Extraction behaviour in this module was informed in part by NGPrimeClaim
# by Lx32:
# https://github.com/Lx32/NGPrimeClaim
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

NEOGEO_C1_TILE_DECODE = {
    "type": "neogeo_4bpp_tile_decode",
    "source_file": "c1.bin",
    "tile_size": 128,
    "row_offsets": [
        [4, 0],
        [4, 8],
        [0, 0],
        [0, 8],
    ],
    "output_streams": {
        "odd": [0, 1],
        "even": [2, 3],
    },
}


GAME = {
    "id": "ncommand",
    "title": "Ninja Commando",
    "mame_set": "ncommand",
    "search_folder_names": ["Ninja Commando", "ncommand"],
    "source_subfolders": ["Data/rom", "rom", "resources/game", "."],
    "required_source_files": ["p1.bin", "s2.bin", "m1.bin", "v1.bin", "c1.bin"],
    "notes": {
        "summary": "Ninja Commando uses a P1 correction if needed, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": ["Converted from extract_ncommand_ngprime_dual.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.", 'SHA1 values were added from the supplied MAME 0.287 DAT for machine ncommand.', 'The old script changed byte 0x115 in the extracted P1 ROM to 0x00 for the corrected MAME-clean output if needed.', 'The old script located the M1 ROM by scanning m1.bin in 0x10000-byte steps for the expected CRC32.', 'This module declares that as find_slice_by_crc32; the core needs generic support for that operation before this module can run fully.', 'c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout.', 'Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.'],
    },
    "outputs": [{
        "zip_name": "ncommand.zip",
        "set_name": "ncommand",
        "type": "main",
        "description": "MAME-compatible Ninja Commando game set.",
        "files": ['050-p1.p1', '050-s1.s1', '050-m1.m1', '050-v1.v1', '050-v2.v2', '050-c1.c1', '050-c2.c2', '050-c3.c3', '050-c4.c4'],
    }],
    "files": [
        {
            "output_name": "050-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x100000},
                {"type": "patch_if_needed", "description": "P1 correction from old extractor", "file_offset": 0x115, "expected_old": "02", "new": "00"},
            ],
            "size": 0x100000,
            "crc32": "4e097c40",
            "sha1": "43311a7ca14a14dcd4a99d8576a12e897b078643",
        },
        {
            "output_name": "050-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000},
            ],
            "size": 0x020000,
            "crc32": "db8f9c8e",
            "sha1": "11cb82cf3c4d0fc2da5df0c26410a64808093610",
        },
        {
            "output_name": "050-m1.m1",
            "operations": [
                {
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "size": 0x020000,
                    "step": 0x010000,
                    "crc32": "6fcf07d3",
                    "fallback_offset": 0x000000,
                },
            ],
            "size": 0x020000,
            "crc32": "6fcf07d3",
            "sha1": "e9ecff4bfec1f5964bf06645f75d80d611b6231c",
        },
        {
            "output_name": "050-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x100000},
            ],
            "size": 0x100000,
            "crc32": "23c3ab42",
            "sha1": "b6c59bb180f1aa34c95f3ec923f3aafb689d57b0",
        },
        {
            "output_name": "050-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x100000, "size": 0x080000},
            ],
            "size": 0x080000,
            "crc32": "80b8a984",
            "sha1": "950cf0e78ceffa4037663f1086fbbc88588f49f2",
        },
        {
            "output_name": "050-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 0}]},
            ],
            "size": 0x100000,
            "crc32": "87421a0a",
            "sha1": "1d8faaf03778f7c5b062554d7333bbd3f0ca12ad",
        },
        {
            "output_name": "050-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 0}]},
            ],
            "size": 0x100000,
            "crc32": "c4cf5548",
            "sha1": "ef9eca5aeff9dda2209a050c2af00ed8979ae2bc",
        },
        {
            "output_name": "050-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 1}]},
            ],
            "size": 0x100000,
            "crc32": "03422c1e",
            "sha1": "920e5015aebe2ffc5ce43a52365c7f0a705f3b9e",
        },
        {
            "output_name": "050-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 1}]},
            ],
            "size": 0x100000,
            "crc32": "0845eadb",
            "sha1": "3c71a02bf0e07a5381846bb6d75bbe7dd546adea",
        },
    ],
}
