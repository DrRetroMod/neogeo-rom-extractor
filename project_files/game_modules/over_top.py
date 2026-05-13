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
Over Top module.

Converted from extract_overtop_ngprime_conditional.py.
Game-specific details live here: source filenames, output filenames,
P1 rebuild order, sizes, CRC32/SHA1 hashes, P1 patch rule, M1 CRC-scan rule,
and C-ROM chunk assembly order.
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
    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
    "output_streams": {"odd": [0, 1], "even": [2, 3]},
}

GAME = {
    "id": "overtop",
    "title": "Over Top",
    "mame_set": "overtop",

    "search_folder_names": ["Over Top", "overtop"],
    "source_subfolders": ["Data/rom", "rom", "resources/game", "."],
    "required_source_files": ["p1.bin", "s2.bin", "m1.bin", "v1.bin", "c1.bin"],

    "notes": {
        "summary": "Over Top rebuilds P1 as top+bottom, then applies the P1 correction if needed; it also uses M1 CRC scanning and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": [
            "Converted from extract_overtop_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine overtop.",
            "The old script rebuilds 212-p1.p1 as p1.bin[0x100000:0x200000] + p1.bin[0x000000:0x100000].",
            "The old script changed byte 0x115 in the rebuilt P1 ROM to 0x00 if needed.",
            "The old script located 212-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "This module declares P1 rebuilding as concat_slices; the core needs generic support for concat_slices before this module can run fully.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [{
        "zip_name": "overtop.zip",
        "set_name": "overtop",
        "type": "main",
        "description": "MAME-compatible Over Top game set.",
        "files": ["212-p1.p1", "212-s1.s1", "212-m1.m1", "212-v1.v1", "212-c1.c1", "212-c2.c2", "212-c3.c3", "212-c4.c4", "212-c5.c5", "212-c6.c6"],
    }],

    "files": [
        {
            "output_name": "212-p1.p1",
            "operations": [
                {"type": "concat_slices", "slices": [
                    {"source_file": "p1.bin", "offset": 0x100000, "size": 0x100000},
                    {"source_file": "p1.bin", "offset": 0x000000, "size": 0x100000},
                ]},
                {"type": "patch_if_needed", "description": "Over Top P1 correction from old conditional extractor", "file_offset": 0x115, "expected_old": "02", "new": "00"},
            ],
            "size": 0x200000, "crc32": "16c063a9", "sha1": "5432869f830eed816ee5ed71c7fd39f749d15619",
        },
        {"output_name": "212-s1.s1", "operations": [{"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000}], "size": 0x020000, "crc32": "481d3ddc", "sha1": "7b0df3fc5b19f282abfd0eb5a4c6ed836a536ece"},
        {"output_name": "212-m1.m1", "operations": [{"type": "find_slice_by_crc32", "source_file": "m1.bin", "size": 0x020000, "step": 0x010000, "crc32": "fcab6191", "fallback_offset": 0x000000}], "size": 0x020000, "crc32": "fcab6191", "sha1": "488b8310b0957f0012fe50f73641b606f6ac4a57"},
        {"output_name": "212-v1.v1", "operations": [{"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x400000}], "size": 0x400000, "crc32": "013d4ef9", "sha1": "438a697c44525bdf78b54432c4f7217ab5667047"},
        {
            "output_name": "212-c1.c1",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 0}]}],
            "size": 0x400000, "crc32": "50f43087", "sha1": "e5a8c914ef8e77c7a29bffdeb18f1877b5c2fc7d",
        },
        {
            "output_name": "212-c2.c2",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 0}]}],
            "size": 0x400000, "crc32": "a5b39807", "sha1": "e98e82cf99576cb48cc5e8dc655b7e9a428c2843",
        },
        {
            "output_name": "212-c3.c3",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 1}]}],
            "size": 0x400000, "crc32": "9252ea02", "sha1": "269066e0f893d3e8e7c308528026a486c2b023a2",
        },
        {
            "output_name": "212-c4.c4",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 1}]}],
            "size": 0x400000, "crc32": "5f41a699", "sha1": "abbb162658e06a37db8475b659ece7e1270ebb49",
        },
        {
            "output_name": "212-c5.c5",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "odd", "index": 4}]}],
            "size": 0x200000, "crc32": "fc858bef", "sha1": "0031def13e7cf4a465a1eca7aa0d13d1b21427e2",
        },
        {
            "output_name": "212-c6.c6",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "even", "index": 4}]}],
            "size": 0x200000, "crc32": "0589c15e", "sha1": "b1167caf7cb61f3e05a5d342290bfe00e02e9d38",
        },
    ],
}
