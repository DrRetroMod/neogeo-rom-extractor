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
Super Sidekicks / Tokuten Ou module.

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
    "id": "ssideki",
    "title": "Super Sidekicks / Tokuten Ou",
    "mame_set": "ssideki",

    "search_folder_names": [
        "Super Sidekicks",
        "Tokuten Ou",
        "ssideki",
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
        "summary": "Super Sidekicks uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform with 512 KiB block assembly.",
        "details": [
            "Converted from extract_ssideki_ngprime_corrected.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine ssideki.",
            "The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.",
            "The old script located 052-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "The old script assembled C1/C2 from decoded 512 KiB blocks 0, 1, 4, and 5.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "ssideki.zip",
            "set_name": "ssideki",
            "type": "main",
            "description": "MAME-compatible Super Sidekicks / Tokuten Ou game set.",
            "files": [
                "052-p1.p1",
                "052-s1.s1",
                "052-m1.m1",
                "052-v1.v1",
                "052-c1.c1",
                "052-c2.c2",
            ],
        }
    ],

    "files": [
        {
            "output_name": "052-p1.p1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x080000,
                },
                {
                    "type": "patch_if_needed",
                    "description": "Super Sidekicks P1 correction from old corrected extractor",
                    "file_offset": 0x000115,
                    "expected_old": "02",
                    "new": "00",
                },
            ],
            "size": 0x080000,
            "crc32": "9cd97256",
            "sha1": "1c780b711137fd79cc81b01941e84f3d59e0071f",
        },

        {
            "output_name": "052-s1.s1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                },
            ],
            "size": 0x020000,
            "crc32": "97689804",
            "sha1": "fa8dab3b3353d7115a0368f3fc749950c0186fbc",
        },

        {
            "output_name": "052-m1.m1",
            "operations": [
                {
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "offset_start": 0x000000,
                    "step": 0x010000,
                    "size": 0x020000,
                    "crc32": "49f17d2d",
                    "fallback_offset": 0x000000,
                },
            ],
            "size": 0x020000,
            "crc32": "49f17d2d",
            "sha1": "70971fcf71ae3a6b2e26e7ade8063941fb178ae5",
        },

        {
            "output_name": "052-v1.v1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x200000,
                },
            ],
            "size": 0x200000,
            "crc32": "22c097a5",
            "sha1": "328c4e6db0a026f54a633cff1443a3f964a8daea",
        },

        {
            "output_name": "052-c1.c1",
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
                },
            ],
            "size": 0x200000,
            "crc32": "53e1c002",
            "sha1": "2125b1be379ea7933893ffb1cd65d6c4bf8b03bd",
        },

        {
            "output_name": "052-c2.c2",
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
                },
            ],
            "size": 0x200000,
            "crc32": "776a2d1f",
            "sha1": "bca0bac87443e9e78c623d284f6cc96cc9c9098f",
        }
    ],
}
