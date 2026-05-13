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
King of the Monsters 2 module.

Converted from extract_kotm2_ngprime.py.

Source of extraction logic:
- old NGPrimeClaim-style King of the Monsters 2 extractor

Source of SHA1 values:
- MAME 0.287 DAT, machine kotm2

Game-specific details live here:
- source filenames
- output filenames
- offsets
- sizes
- CRC32/SHA1 hashes
- C-ROM transform parameters
- C-ROM block assembly order
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
    "id": "kotm2",
    "title": "King of the Monsters 2",
    "mame_set": "kotm2",

    "search_folder_names": [
        "King of the Monsters 2",
        "King of the Monsters 2 - The Next Thing",
        "kotm2",
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
            "King of the Monsters 2 uses standard slices plus a module-declared "
            "NeoGeo 4bpp C-ROM transform with non-linear 512 KiB block assembly."
        ),
        "details": [
            "Converted from extract_kotm2_ngprime.py without changing the old script's offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine kotm2.",
            "The old script used 512 KiB C-ROM blocks.",
            "The old script assembled c1/c2 from blocks 0, 1, 4, and 5, and c3/c4 from block 2.",
            "The old script logged block 3 as unused; this module intentionally outputs only the validated MAME files.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "kotm2.zip",
            "set_name": "kotm2",
            "type": "main",
            "description": "MAME-compatible King of the Monsters 2 game set.",
            "files": [
                "039-p1.p1",
                "039-p2.p2",
                "039-s1.s1",
                "039-m1.m1",
                "039-v2.v2",
                "039-v4.v4",
                "039-c1.c1",
                "039-c2.c2",
                "039-c3.c3",
                "039-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "039-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x080000}
            ],
            "size": 0x080000,
            "crc32": "b372d54c",
            "sha1": "b70fc6f72e16a66b6e144cc01370548e3398b8b8",
        },
        {
            "output_name": "039-p2.p2",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x080000, "size": 0x080000}
            ],
            "size": 0x080000,
            "crc32": "28661afe",
            "sha1": "6c85ff6ab334b1ca744f726f42dac211537e7315",
        },
        {
            "output_name": "039-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000}
            ],
            "size": 0x020000,
            "crc32": "63ee053a",
            "sha1": "7d4b92bd022708975b1470e8f24d1f5a712e1b94",
        },
        {
            "output_name": "039-m1.m1",
            "operations": [
                {"type": "slice", "source_file": "m1.bin", "offset": 0x000000, "size": 0x020000}
            ],
            "size": 0x020000,
            "crc32": "0c5b2ad5",
            "sha1": "15eb5ea10fecdbdbcfd06225ae6d88bb239592e7",
        },
        {
            "output_name": "039-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x200000}
            ],
            "size": 0x200000,
            "crc32": "86d34b25",
            "sha1": "89bdb614b0c63d678962da52e2f596750d20828c",
        },
        {
            "output_name": "039-v4.v4",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x200000, "size": 0x100000}
            ],
            "size": 0x100000,
            "crc32": "8fa62a0b",
            "sha1": "58ac2fdd73c542eb8178cfc4adfa0e5940183283",
        },
        {
            "output_name": "039-c1.c1",
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
            "crc32": "6d1c4aa9",
            "sha1": "4fbc9d7cb37522ec298eefbe38c75a2d050fbb4a",
        },
        {
            "output_name": "039-c2.c2",
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
            "crc32": "f7b75337",
            "sha1": "4d85f85948c3e6ed38b0b0ccda79de3ce026e2d9",
        },
        {
            "output_name": "039-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "odd", "index": 2},
                    ],
                },
            ],
            "size": 0x080000,
            "crc32": "bfc4f0b2",
            "sha1": "f4abe2b52882b966412f3b503b8f2c8f49b57968",
        },
        {
            "output_name": "039-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "even", "index": 2},
                    ],
                },
            ],
            "size": 0x080000,
            "crc32": "81c9c250",
            "sha1": "e3a34ff69081a8681b5ca895915892dcdccfa7aa",
        },
    ],
}
