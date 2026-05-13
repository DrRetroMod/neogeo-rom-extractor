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
Ghost Pilots module.

Converted from extract_gpilots_ngprime.py.

Source of extraction logic:
- old NGPrimeClaim-style Ghost Pilots extractor

Source of SHA1 values:
- MAME 0.287 DAT, machine gpilots

Game-specific details live here:
- source filenames
- output filenames
- offsets
- sizes
- CRC32/SHA1 hashes
- P1 patch rule
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
    "id": "gpilots",
    "title": "Ghost Pilots",
    "mame_set": "gpilots",

    "search_folder_names": [
        "Ghost Pilots",
        "gpilots",
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
            "Ghost Pilots uses p1.bin/s2.bin/m1.bin/v1.bin slices, a P1 byte correction, "
            "and a module-declared NeoGeo 4bpp C-ROM transform from c1.bin."
        ),
        "details": [
            "Converted from extract_gpilots_ngprime.py without changing the old script's offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine gpilots.",
            "The old script changed byte offset 277 / 0x115 in the extracted 020-p1.p1 to 0x00 before CRC validation.",
            "p1.bin is split into 020-p1.p1 and 020-p2.p2, matching the old extractor.",
            "v1.bin is split into 020-v11.v11, 020-v12.v12, and 020-v21.v21, matching the old extractor.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout, then assembled into 020-c1.c1 through 020-c4.c4.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "gpilots.zip",
            "set_name": "gpilots",
            "type": "main",
            "description": "MAME-compatible Ghost Pilots game set.",
            "files": [
                "020-p1.p1",
                "020-p2.p2",
                "020-s1.s1",
                "020-m1.m1",
                "020-v11.v11",
                "020-v12.v12",
                "020-v21.v21",
                "020-c1.c1",
                "020-c2.c2",
                "020-c3.c3",
                "020-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "020-p1.p1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x080000,
                },
                {
                    "type": "patch_if_needed",
                    "description": "Ghost Pilots P1 correction from old extractor",
                    "file_offset": 0x115,
                    "expected_old": "02",
                    "new": "00",
                },
            ],
            "size": 0x080000,
            "crc32": "e6f2fe64",
            "sha1": "50ab82517e077727d97668a4df2b9b96d2e78ab6",
        },
        {
            "output_name": "020-p2.p2",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x080000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "edcb22ac",
            "sha1": "505d2db38ae999b7d436e8f2ff56b81796d62b54",
        },
        {
            "output_name": "020-s1.s1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "a6d83d53",
            "sha1": "9a8c092f89521cc0b27a385aa72e29cbaca926c5",
        },
        {
            "output_name": "020-m1.m1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "m1.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "48409377",
            "sha1": "0e212d2c76856a90b2c2fdff675239525972ac43",
        },
        {
            "output_name": "020-v11.v11",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x100000,
                }
            ],
            "size": 0x100000,
            "crc32": "1b526c8b",
            "sha1": "2801868d2badcf8aaf5d490e010e4049d81d7bc1",
        },
        {
            "output_name": "020-v12.v12",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x100000,
                    "size": 0x080000,
                }
            ],
            "size": 0x080000,
            "crc32": "4a9e6f03",
            "sha1": "d3ac11f333b03d8a318921bdaefb14598e289a14",
        },
        {
            "output_name": "020-v21.v21",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x180000,
                    "size": 0x080000,
                }
            ],
            "size": 0x080000,
            "crc32": "7abf113d",
            "sha1": "5b2a0e70f2eaf4638b44702dacd4cb17838fb1d5",
        },
        {
            "output_name": "020-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 0},
                    ],
                },
            ],
            "size": 0x100000,
            "crc32": "bd6fe78e",
            "sha1": "50b704862cd79d64fa488e621b079f6e413c33bc",
        },
        {
            "output_name": "020-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 0},
                    ],
                },
            ],
            "size": 0x100000,
            "crc32": "5f4a925c",
            "sha1": "71c5ef8141234daaa7025427a6c65e79766973a5",
        },
        {
            "output_name": "020-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 1},
                    ],
                },
            ],
            "size": 0x100000,
            "crc32": "d1e42fd0",
            "sha1": "f0d476aebbdc2ce008f5f0783be86d295b24aa44",
        },
        {
            "output_name": "020-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 1},
                    ],
                },
            ],
            "size": 0x100000,
            "crc32": "edde439b",
            "sha1": "79be7b10ecdab54c2f77062b8f5fda0e299fa982",
        },
    ],
}
