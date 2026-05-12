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
Art of Fighting 3 - The Path of the Warrior / Ryuuko no Ken Gaiden module.

Converted from extract_aof3_ngprime_dual.py.

Source of extraction logic:
- old dual-output AOF3 NGPrimeClaim-style extractor

Source of SHA1 values:
- MAME 0.287 DAT, machine aof3

This module declares only the corrected MAME-clean aof3.zip output.
The old script's separate original Amazon/Code Mystics P1 preservation ZIP is not
included, matching the current framework decision to output only the validated
MAME-compatible game ZIP.
"""

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
    "id": "aof3",
    "title": "Art of Fighting 3 - The Path of the Warrior / Ryuuko no Ken Gaiden",
    "mame_set": "aof3",

    "search_folder_names": [
        "Art of Fighting 3",
        "Art of Fighting 3 - The Path of The",
        "Art of Fighting 3 - The Path of the Warrior",
        "Art of Fighting 3 - The Path of the Warrior - Ryuuko no Ken Gaiden",
        "Art of Fighting 3 - The Path of the Warrior / Ryuuko no Ken Gaiden",
        "Art of Fighting 3 / Ryuuko no Ken Gaiden",
        "Ryuuko no Ken Gaiden",
        "aof3",
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
        "summary": (
            "AOF3 requires the old script's P1 correction at file offset 0x115 "
            "before the final MAME CRC32/SHA1 validation passes."
        ),
        "details": [
            "Converted from extract_aof3_ngprime_dual.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine aof3.",
            "The old script changed byte 0x115 in the extracted 096-p1.p1 from 0x02 to 0x00 for the corrected MAME-clean output.",
            "The old script also created a separate original P1 preservation ZIP; this module intentionally outputs only aof3.zip.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout, then assembled into 096-c1.c1 through 096-c8.c8.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "aof3.zip",
            "set_name": "aof3",
            "type": "main",
            "description": "MAME-compatible Art of Fighting 3 game set.",
            "files": [
                "096-p1.p1",
                "096-p2.sp2",
                "096-s1.s1",
                "096-m1.m1",
                "096-v1.v1",
                "096-v2.v2",
                "096-v3.v3",
                "096-c1.c1",
                "096-c2.c2",
                "096-c3.c3",
                "096-c4.c4",
                "096-c5.c5",
                "096-c6.c6",
                "096-c7.c7",
                "096-c8.c8",
            ],
        }
    ],

    "files": [
        {
            "output_name": "096-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x100000},
                {
                    "type": "patch_if_needed",
                    "description": "AOF3 P1 correction from old dual-output extractor",
                    "file_offset": 0x115,
                    "expected_old": "02",
                    "new": "00",
                },
            ],
            "size": 0x100000,
            "crc32": "9edb420d",
            "sha1": "150d80707325ece351c72c21c6186cfb5996adba",
        },
        {
            "output_name": "096-p2.sp2",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x100000, "size": 0x200000},
            ],
            "size": 0x200000,
            "crc32": "4d5a2602",
            "sha1": "4c26d6135d2877d9c38169662033e9d0cc24d943",
        },
        {
            "output_name": "096-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x20000},
            ],
            "size": 0x20000,
            "crc32": "cc7fd344",
            "sha1": "2c6846cf8ea61fb192ba181dbccb63594d572c0e",
        },
        {
            "output_name": "096-m1.m1",
            "operations": [
                {"type": "slice", "source_file": "m1.bin", "offset": 0x000000, "size": 0x20000},
            ],
            "size": 0x20000,
            "crc32": "cb07b659",
            "sha1": "940b379957c2987d7ab0443cb80c3ff58f6ba559",
        },
        {
            "output_name": "096-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x200000},
            ],
            "size": 0x200000,
            "crc32": "e2c32074",
            "sha1": "69426e7e63fc31a73d1cd056cc9ae6a2c4499407",
        },
        {
            "output_name": "096-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x200000, "size": 0x200000},
            ],
            "size": 0x200000,
            "crc32": "a290eee7",
            "sha1": "e66a98cd9740188bf999992b417f8feef941cede",
        },
        {
            "output_name": "096-v3.v3",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x400000, "size": 0x200000},
            ],
            "size": 0x200000,
            "crc32": "199d12ea",
            "sha1": "a883bf34e685487705a8dafdd0b8db15eb360e80",
        },
        {
            "output_name": "096-c1.c1",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 0}]}],
            "size": 0x400000,
            "crc32": "f17b8d89",
            "sha1": "7180df23f7c7a964b0835fda76970b12f0aa9ea8",
        },
        {
            "output_name": "096-c2.c2",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 0}]}],
            "size": 0x400000,
            "crc32": "3840c508",
            "sha1": "55adc7cd26fec3e4dbd779df6701bc6eaba41b84",
        },
        {
            "output_name": "096-c3.c3",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 1}]}],
            "size": 0x400000,
            "crc32": "55f9ee1e",
            "sha1": "fbe1b7891beae66c5fcbc7e36168dc1b460ede91",
        },
        {
            "output_name": "096-c4.c4",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 1}]}],
            "size": 0x400000,
            "crc32": "585b7e47",
            "sha1": "d50ea91397fc53d86470ff5b493a44d57c010306",
        },
        {
            "output_name": "096-c5.c5",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 2}]}],
            "size": 0x400000,
            "crc32": "c75a753c",
            "sha1": "fc977f8710816a369a5d0d49ee84059380e93fb7",
        },
        {
            "output_name": "096-c6.c6",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 2}]}],
            "size": 0x400000,
            "crc32": "9a9d2f7a",
            "sha1": "a89a713bfcd93974c9acb21ce699d365b08e7e39",
        },
        {
            "output_name": "096-c7.c7",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "odd", "index": 6}]}],
            "size": 0x200000,
            "crc32": "51bd8ab2",
            "sha1": "c8def9c64de64571492b5b7e14b794e3c18f1393",
        },
        {
            "output_name": "096-c8.c8",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "even", "index": 6}]}],
            "size": 0x200000,
            "crc32": "9a34f99c",
            "sha1": "fca72d95ec42790a7f1e771a1e25dbc5bec5fc19",
        },
    ],
}
