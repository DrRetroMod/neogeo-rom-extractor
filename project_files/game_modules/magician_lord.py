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
Magician Lord module.

Converted from extract_maglord_ngprime_dual.py.

This module declares only the corrected MAME-clean maglord.zip output.
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
    "id": "maglord",
    "title": "Magician Lord",
    "mame_set": "maglord",
    "search_folder_names": ["Magician Lord", "maglord"],
    "source_subfolders": ["Data/rom", "rom", "resources/game", "."],
    "required_source_files": ["p1.bin", "s2.bin", "m1.bin", "v1.bin", "c1.bin"],
    "notes": {
        "summary": "Magician Lord requires the old script's P1 correction at file offset 0x115 before final MAME validation passes.",
        "details": [
            "Converted from extract_maglord_ngprime_dual.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine maglord.",
            "The old script changed byte 0x115 in the extracted 005-pg1.p1 to 0x00 for the corrected MAME-clean output.",
            "The old script handled m1.bin conditionally: if 256 KiB, use it directly; if 320 KiB or larger, use offset 0x10000 for 256 KiB; otherwise if at least 256 KiB, use the first 256 KiB.",
            "v1.bin is split into three 512 KiB V-ROM files, matching the old extractor.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout, then assembled into 005-c1.c1 through 005-c6.c6.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },
    "outputs": [{
        "zip_name": "maglord.zip",
        "set_name": "maglord",
        "type": "main",
        "description": "MAME-compatible Magician Lord game set.",
        "files": [
            "005-pg1.p1", "005-s1.s1", "005-m1.m1",
            "005-v11.v11", "005-v21.v21", "005-v22.v22",
            "005-c1.c1", "005-c2.c2", "005-c3.c3", "005-c4.c4", "005-c5.c5", "005-c6.c6",
        ],
    }],
    "files": [
        {
            "output_name": "005-pg1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x080000},
                {"type": "patch_if_needed", "description": "P1 correction from old extractor", "file_offset": 0x115, "expected_old": "02", "new": "00"},
            ],
            "size": 0x080000,
            "crc32": "bd0a492d",
            "sha1": "d043d3710cf2b0d2b3798008e65e4c7c3ead1af3",
        },
        {
            "output_name": "005-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000},
            ],
            "size": 0x020000,
            "crc32": "1c5369a2",
            "sha1": "db0dba0a7dced6c9ca929c5abda491b05d84199c",
        },
        {
            "output_name": "005-m1.m1",
            "operations": [
                {
                    "type": "conditional_slice",
                    "source_file": "m1.bin",
                    "choices": [
                        {"description": "m1.bin is 256 KiB; use whole file", "if_size": 0x040000, "offset": 0x000000, "size": 0x040000},
                        {"description": "m1.bin is 320 KiB or larger; use offset 0x10000 for 256 KiB", "minimum_size": 0x050000, "offset": 0x010000, "size": 0x040000},
                        {"description": "m1.bin is at least 256 KiB but below 320 KiB; use first 256 KiB", "minimum_size": 0x040000, "max_source_size": 0x04FFFF, "offset": 0x000000, "size": 0x040000},
                    ],
                },
            ],
            "size": 0x040000,
            "crc32": "26259f0f",
            "sha1": "4f3e500093d61585048767dbd9fa09b3911a05d6",
        },
        {
            "output_name": "005-v11.v11",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x080000},
            ],
            "size": 0x080000,
            "crc32": "cc0455fd",
            "sha1": "a8ff4270e7705e263d25ff0b301f503bccea7e59",
        },
        {
            "output_name": "005-v21.v21",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x080000, "size": 0x080000},
            ],
            "size": 0x080000,
            "crc32": "f94ab5b7",
            "sha1": "2c16985102e3585e08622d8c54ac5c60425b9ff8",
        },
        {
            "output_name": "005-v22.v22",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x100000, "size": 0x080000},
            ],
            "size": 0x080000,
            "crc32": "232cfd04",
            "sha1": "61b66a9decbbd1f500a8c186615e7fd077c6861e",
        },
        {
            "output_name": "005-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "odd", "index": 0}]},
            ],
            "size": 0x080000,
            "crc32": "806aee34",
            "sha1": "3c32a0edbbddb694495b510c13979c44b83de8bc",
        },
        {
            "output_name": "005-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "even", "index": 0}]},
            ],
            "size": 0x080000,
            "crc32": "34aa9a86",
            "sha1": "cec97e1ff7f91158040c629ba75742db82c4ae5e",
        },
        {
            "output_name": "005-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "odd", "index": 1}]},
            ],
            "size": 0x080000,
            "crc32": "c4c2b926",
            "sha1": "478bfafca21f5a1338808251a06ab405e6a9e65f",
        },
        {
            "output_name": "005-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "even", "index": 1}]},
            ],
            "size": 0x080000,
            "crc32": "9c46dcf4",
            "sha1": "4c05f3dc25777a87578ce09a6cefb3a4cebf3266",
        },
        {
            "output_name": "005-c5.c5",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "odd", "index": 2}]},
            ],
            "size": 0x080000,
            "crc32": "69086dec",
            "sha1": "7fa47f4a765948813ebf366168275dcc3c42e951",
        },
        {
            "output_name": "005-c6.c6",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "even", "index": 2}]},
            ],
            "size": 0x080000,
            "crc32": "ab7ac142",
            "sha1": "e6ad2843947d35d8e913d2666f87946c1ba7944f",
        },
    ],
}
