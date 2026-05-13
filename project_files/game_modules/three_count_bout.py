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
3 Count Bout / Fire Suplex module.

This module declares the extraction data for the MAME-compatible
3countb.zip set.

Game-specific details live here:
- source filenames
- output filenames
- offsets
- sizes
- CRC32/SHA1 hashes
- C-ROM transform parameters
- C-ROM chunk assembly order
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
    "id": "3countb",
    "title": "3 Count Bout / Fire Suplex",
    "mame_set": "3countb",

    "search_folder_names": [
        "3 Count Bout",
        "3 Count Bout - Fire Suplex",
        "3 Count Bout Fire Suplex",
        "Fire Suplex",
        "3countb",
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
            "3 Count Bout uses a C-ROM/sprite transform from c1.bin before "
            "assembling the final MAME C-ROM files."
        ),
        "details": [
            "p1.bin is copied directly to 043-p1.p1.",
            "s2.bin is copied directly to 043-s1.s1.",
            "m1.bin is copied directly to 043-m1.m1.",
            "v1.bin is split into two 2 MiB V-ROM files.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout.",
            "The decoded odd/even sprite streams are then assembled into 043-c1.c1 through 043-c4.c4.",
            "This module does not define included Code Mystics BIOS extraction. It is only for the game set 3countb.zip.",
        ],
    },

    "outputs": [
        {
            "zip_name": "3countb.zip",
            "set_name": "3countb",
            "type": "main",
            "description": "MAME-compatible 3 Count Bout / Fire Suplex game set.",
            "files": [
                "043-p1.p1",
                "043-s1.s1",
                "043-m1.m1",
                "043-v1.v1",
                "043-v2.v2",
                "043-c1.c1",
                "043-c2.c2",
                "043-c3.c3",
                "043-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "043-p1.p1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x100000,
                }
            ],
            "size": 0x100000,
            "crc32": "ffbdd928",
            "sha1": "05b24655ca32723661adc5509b450824deb0c176",
        },

        {
            "output_name": "043-s1.s1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "c362d484",
            "sha1": "a3c029292572842feabe9aa8c3372628fb63978d",
        },

        {
            "output_name": "043-m1.m1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "m1.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "7eab59cb",
            "sha1": "5ae4107457e091f73960bfba39b589ae36d51ca3",
        },

        {
            "output_name": "043-v1.v1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x200000,
                }
            ],
            "size": 0x200000,
            "crc32": "63688ce8",
            "sha1": "5c6ac29a0cc0655a87cfe3ada8706838b86b86e4",
        },

        {
            "output_name": "043-v2.v2",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x200000,
                    "size": 0x200000,
                }
            ],
            "size": 0x200000,
            "crc32": "c69a827b",
            "sha1": "f5197ea87bb6573fa6aef3a1713c3679c58c1e74",
        },

        {
            "output_name": "043-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 0},
                        {"stream": "odd", "index": 2},
                    ],
                },
            ],
            "size": 0x200000,
            "crc32": "bad2d67f",
            "sha1": "04928e50ca75b7fbc52b64e816ec5701901f5893",
        },

        {
            "output_name": "043-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 0},
                        {"stream": "even", "index": 2},
                    ],
                },
            ],
            "size": 0x200000,
            "crc32": "a7fbda95",
            "sha1": "9da3c5faf22592a7eaf8df9fa6454f48c2a927ae",
        },

        {
            "output_name": "043-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 1},
                        {"stream": "odd", "index": 3},
                    ],
                },
            ],
            "size": 0x200000,
            "crc32": "f00be011",
            "sha1": "2721cdba37a511a966a2a53b9bd6240f181d920c",
        },

        {
            "output_name": "043-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 1},
                        {"stream": "even", "index": 3},
                    ],
                },
            ],
            "size": 0x200000,
            "crc32": "1887e5c0",
            "sha1": "9b915359add7c10c78d8b281b4084eceea8f0499",
        },
    ],
}