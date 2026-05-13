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
Crossed Swords module.

Converted from extract_crsword_ngprime_dual.py.

Source of extraction logic:
- old dual-output Crossed Swords NGPrimeClaim-style extractor

Source of SHA1 values:
- MAME 0.287 DAT, machine crsword

This module declares only the corrected MAME-clean crsword.zip output.
The old script's separate original Amazon/Code Mystics P1 preservation ZIP is not
included, matching the current framework decision to output only the validated
MAME-compatible game ZIP.

Note: this module preserves the old script's conditional m1.bin handling using
operation type "conditional_slice". The core must support that generic operation
before this module can fully run if your m1.bin is the 192 KiB form. If your
m1.bin is already 128 KiB, the first conditional branch is equivalent to a
normal offset-0 slice.
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
    "id": "crsword",
    "title": "Crossed Swords",
    "mame_set": "crsword",

    "search_folder_names": [
        "Crossed Swords",
        "crsword",
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
            "Crossed Swords requires the old script's P1 correction at file "
            "offset 0x115 before final MAME validation passes."
        ),
        "details": [
            "Converted from extract_crsword_ngprime_dual.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine crsword.",
            "The old script changed byte 0x115 in the extracted 037-p1.p1 to 0x00 for the corrected MAME-clean output.",
            "The original unpatched P1 CRC32 in the old script was e9e2e51c; the old byte at 0x115 is 0x02 when compared to the corrected CRC32 e7f2553c.",
            "The old script handled m1.bin conditionally: if 128 KiB, use it directly; if at least 192 KiB, use offset 0x10000 for 128 KiB.",
            "The old script also created a separate original P1 preservation ZIP; this module intentionally outputs only crsword.zip.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout, then assembled into 037-c1.c1 through 037-c4.c4.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "crsword.zip",
            "set_name": "crsword",
            "type": "main",
            "description": "MAME-compatible Crossed Swords game set.",
            "files": [
                "037-p1.p1",
                "037-s1.s1",
                "037-m1.m1",
                "037-v1.v1",
                "037-c1.c1",
                "037-c2.c2",
                "037-c3.c3",
                "037-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "037-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x80000},
                {
                    "type": "patch_if_needed",
                    "description": "Crossed Swords P1 correction from old dual-output extractor",
                    "file_offset": 0x115,
                    "expected_old": "02",
                    "new": "00",
                },
            ],
            "size": 0x80000,
            "crc32": "e7f2553c",
            "sha1": "8469ecb900477feed05ae3311fe9515019bbec2a",
        },
        {
            "output_name": "037-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x20000},
            ],
            "size": 0x20000,
            "crc32": "74651f27",
            "sha1": "bff7ff2429d2be82c1647abac2ee45b339b3b310",
        },
        {
            "output_name": "037-m1.m1",
            "operations": [
                {
                    "type": "conditional_slice",
                    "source_file": "m1.bin",
                    "choices": [
                        {"if_size": 0x20000, "offset": 0x00000, "size": 0x20000},
                        {"minimum_size": 0x30000, "offset": 0x10000, "size": 0x20000},
                    ],
                },
            ],
            "size": 0x20000,
            "crc32": "9504b2c6",
            "sha1": "9ce8e681b9df6eacd0d23a36bad836bd5074233d",
        },
        {
            "output_name": "037-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x100000},
            ],
            "size": 0x100000,
            "crc32": "61fedf65",
            "sha1": "98f31d1e23bf7c1f7844e67f14707a704134042e",
        },
        {
            "output_name": "037-c1.c1",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 0}]}],
            "size": 0x100000,
            "crc32": "09df6892",
            "sha1": "df2579dcf9c9dc88d461212cb74de106be2983c1",
        },
        {
            "output_name": "037-c2.c2",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 0}]}],
            "size": 0x100000,
            "crc32": "ac122a78",
            "sha1": "7bfa4d29b7d7d9443f64d81caeafa74fe05c606e",
        },
        {
            "output_name": "037-c3.c3",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 1}]}],
            "size": 0x100000,
            "crc32": "9d7ed1ca",
            "sha1": "2bbd25dc3a3f825d0af79a418f06a23a1bf03cc0",
        },
        {
            "output_name": "037-c4.c4",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 1}]}],
            "size": 0x100000,
            "crc32": "4a24395d",
            "sha1": "943f911f40985db901eaef4c28dfcda299fca73e",
        },
    ],
}
