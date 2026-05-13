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
Mutation Nation module.

Converted from extract_mutnat_ngprime_conditional.py.

This module declares only the corrected MAME-clean mutnat.zip output.
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
    "id": "mutnat",
    "title": "Mutation Nation",
    "mame_set": "mutnat",
    "search_folder_names": ["Mutation Nation", "mutnat"],
    "source_subfolders": ["Data/rom", "rom", "resources/game", "."],
    "required_source_files": ["p1.bin", "s2.bin", "m1.bin", "v1.bin", "c1.bin"],
    "notes": {
        "summary": "Mutation Nation uses a P1 correction if needed, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": ["Converted from extract_mutnat_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.", 'SHA1 values were added from the supplied MAME 0.287 DAT for machine mutnat.', 'The old script changed byte 0x115 in the extracted P1 ROM to 0x00 for the corrected MAME-clean output if needed.', 'The old script located the M1 ROM by scanning m1.bin in 0x10000-byte steps for the expected CRC32.', 'This module declares that as find_slice_by_crc32; the core needs generic support for that operation before this module can run fully.', 'c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout.', 'Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.'],
    },
    "outputs": [{
        "zip_name": "mutnat.zip",
        "set_name": "mutnat",
        "type": "main",
        "description": "MAME-compatible Mutation Nation game set.",
        "files": ['014-p1.p1', '014-s1.s1', '014-m1.m1', '014-v1.v1', '014-v2.v2', '014-c1.c1', '014-c2.c2', '014-c3.c3', '014-c4.c4'],
    }],
    "files": [
        {
            "output_name": "014-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x080000},
                {"type": "patch_if_needed", "description": "P1 correction from old extractor", "file_offset": 0x115, "expected_old": "02", "new": "00"},
            ],
            "size": 0x080000,
            "crc32": "6f1699c8",
            "sha1": "87206f67a619dede7959230f9ff3701b8b78957a",
        },
        {
            "output_name": "014-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000},
            ],
            "size": 0x020000,
            "crc32": "99419733",
            "sha1": "b2524af8704941acc72282aa1d62fd4c93e3e822",
        },
        {
            "output_name": "014-m1.m1",
            "operations": [
                {
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "size": 0x020000,
                    "step": 0x010000,
                    "crc32": "b6683092",
                    "fallback_offset": 0x000000,
                },
            ],
            "size": 0x020000,
            "crc32": "b6683092",
            "sha1": "623ec7ec2915fb077bf65b4a16c815e071c25259",
        },
        {
            "output_name": "014-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x100000},
            ],
            "size": 0x100000,
            "crc32": "25419296",
            "sha1": "c9fc04987c4e0875d276e1a0fb671740b6f548ad",
        },
        {
            "output_name": "014-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x100000, "size": 0x100000},
            ],
            "size": 0x100000,
            "crc32": "0de53d5e",
            "sha1": "467f6040da3dfb1974785e95e14c3f608a93720a",
        },
        {
            "output_name": "014-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 0}]},
            ],
            "size": 0x100000,
            "crc32": "5e4381bf",
            "sha1": "d429a5e09dafd2fb99495658b3652eecbf58f91b",
        },
        {
            "output_name": "014-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 0}]},
            ],
            "size": 0x100000,
            "crc32": "69ba4e18",
            "sha1": "b3369190c47771a790c7adffa958ff55d90e758b",
        },
        {
            "output_name": "014-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 1}]},
            ],
            "size": 0x100000,
            "crc32": "890327d5",
            "sha1": "47f97bf120a8480758e1f3bb8982be4c5325c036",
        },
        {
            "output_name": "014-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 1}]},
            ],
            "size": 0x100000,
            "crc32": "e4002651",
            "sha1": "17e53a5f4708866a120415bf24f3b89621ad0bcc",
        },
    ],
}
