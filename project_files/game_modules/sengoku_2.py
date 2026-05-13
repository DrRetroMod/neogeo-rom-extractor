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
Sengoku 2 / Sengoku Denshou 2 module.

This module declares game-specific extraction data only.
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
    "id": "sengoku2",
    "title": "Sengoku 2 / Sengoku Denshou 2",
    "mame_set": "sengoku2",

    "search_folder_names": [
        "Sengoku 2",
        "Sengoku Denshou 2",
        "Sengoku2",
        "sengoku2",
    ],

    "source_subfolders": [
        "Data/rom",
        "rom",
        "resources/game",
        ".",
    ],

    "required_source_files": [
        "p1.bin",
        "s2.bin",
        "m1.bin",
        "v1.bin",
        "c1.bin",
    ],

    "notes": {
        "summary": "Sengoku 2 uses conditional P1 patching, M1 CRC scanning, and a 512 KiB C-ROM block layout declared in this module.",
        "details": [
            "Converted from extract_sengoku2_ngprime_corrected.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine sengoku2.",
            "The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.",
            "The old script located 040-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "The old script assembled C1/C2 from 512 KiB blocks 0,1,4,5 and C3/C4 from block 2.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "sengoku2.zip",
            "set_name": "sengoku2",
            "type": "main",
            "description": "MAME-compatible Sengoku 2 / Sengoku Denshou 2 game set.",
            "files": [
                "040-p1.p1",
                "040-s1.s1",
                "040-m1.m1",
                "040-v1.v1",
                "040-v2.v2",
                "040-c1.c1",
                "040-c2.c2",
                "040-c3.c3",
                "040-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "040-p1.p1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x100000,
                },
{
                    "type": "patch_if_needed",
                    "description": "Sengoku 2 P1 correction from old corrected extractor",
                    "file_offset": 0x000115,
                    "expected_old": "02",
                    "new": "00",
                }
            ],
            "size": 0x100000,
            "crc32": "6dde02c2",
            "sha1": "e432e63feb88c71629ec96aa84650dcfe356a551",
        },

        {
            "output_name": "040-s1.s1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "cd9802a3",
            "sha1": "f685d4638f4f68e7e3f101c0c39128454536721b",
        },

        {
            "output_name": "040-m1.m1",
            "operations": [
{
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "offset_start": 0x000000,
                    "step": 0x010000,
                    "size": 0x020000,
                    "crc32": "d4de4bca",
                    "fallback_offset": 0x000000,
                }
            ],
            "size": 0x020000,
            "crc32": "d4de4bca",
            "sha1": "ecf604d06f01d40b04e285facef66a6ae2d35661",
        },

        {
            "output_name": "040-v1.v1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x200000,
                }
            ],
            "size": 0x200000,
            "crc32": "71cb4b5d",
            "sha1": "56d9aca1d476c19c7d0f707176a8fed53e0189b7",
        },

        {
            "output_name": "040-v2.v2",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x200000,
                    "size": 0x100000,
                }
            ],
            "size": 0x100000,
            "crc32": "c5cece01",
            "sha1": "923a3377dac1919e8c3d9ab316902250caa4785f",
        },

        {
            "output_name": "040-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "odd", "index": 0},
                        {"stream": "odd", "index": 1},
                        {"stream": "odd", "index": 4},
                        {"stream": "odd", "index": 5},
                    ],
                }
            ],
            "size": 0x200000,
            "crc32": "faa8ea99",
            "sha1": "714575e57ea1990612f960ec42b38d2e157ad400",
        },

        {
            "output_name": "040-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "even", "index": 0},
                        {"stream": "even", "index": 1},
                        {"stream": "even", "index": 4},
                        {"stream": "even", "index": 5},
                    ],
                }
            ],
            "size": 0x200000,
            "crc32": "87d0ec65",
            "sha1": "23645e0cf859fb4cec3745b3846ca0ef64c689fb",
        },

        {
            "output_name": "040-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "odd", "index": 2},
                    ],
                }
            ],
            "size": 0x080000,
            "crc32": "24b5ba80",
            "sha1": "29d58a6b56bd24ee2046a8d45e023b4d7ab7685b",
        },

        {
            "output_name": "040-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "even", "index": 2},
                    ],
                }
            ],
            "size": 0x080000,
            "crc32": "1c9e9930",
            "sha1": "d017474873750a7602b7708c663d29b25ef7bb63",
        }
    ],
}
