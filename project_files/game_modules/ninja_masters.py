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
Ninja Master's - Haoh-ninpo-cho module.

Converted from extract_ninjamas_ngprime_dual.py.
Game-specific details live here: source filenames, output filenames,
offsets, sizes, CRC32/SHA1 hashes, P1 patch rule, M1 CRC-scan rule,
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
    "id": "ninjamas",
    "title": "Ninja Master's - Haoh-ninpo-cho",
    "mame_set": "ninjamas",

    "search_folder_names": [
        "Ninja Master's",
        "Ninja Masters",
        "Ninja Master's - Haoh-ninpo-cho",
        "Ninja Masters - Haoh-ninpo-cho",
        "ninjamas",
    ],

    "source_subfolders": ["Data/rom", "rom", "resources/game", "."],

    "required_source_files": ["p1.bin", "s2.bin", "m1.bin", "v1.bin", "c1.bin"],

    "notes": {
        "summary": "Ninja Master's uses a P1 correction, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": [
            "Converted from extract_ninjamas_ngprime_dual.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine ninjamas.",
            "The old script changed byte 0x115 in the extracted 217-p1.p1 to 0x00 for the corrected MAME-clean output.",
            "The old script located 217-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "The old script also created a separate original P1 preservation ZIP; this module intentionally outputs only ninjamas.zip.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "ninjamas.zip",
            "set_name": "ninjamas",
            "type": "main",
            "description": "MAME-compatible Ninja Master's game set.",
            "files": [
                "217-p1.p1", "217-p2.sp2", "217-s1.s1", "217-m1.m1",
                "217-v1.v1", "217-v2.v2",
                "217-c1.c1", "217-c2.c2", "217-c3.c3", "217-c4.c4",
                "217-c5.c5", "217-c6.c6", "217-c7.c7", "217-c8.c8",
            ],
        }
    ],

    "files": [
        {
            "output_name": "217-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x100000},
                {"type": "patch_if_needed", "description": "Ninja Master's P1 correction from old dual-output extractor", "file_offset": 0x115, "expected_old": "02", "new": "00"},
            ],
            "size": 0x100000, "crc32": "3e97ed69", "sha1": "336bcae375a5109945d11356503bf0d9f4a9a50a",
        },
        {
            "output_name": "217-p2.sp2",
            "operations": [{"type": "slice", "source_file": "p1.bin", "offset": 0x100000, "size": 0x200000}],
            "size": 0x200000, "crc32": "191fca88", "sha1": "e318e5931704779bbe461719a5eeeba89bd83a5d",
        },
        {
            "output_name": "217-s1.s1",
            "operations": [{"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000}],
            "size": 0x020000, "crc32": "8ff782f0", "sha1": "90099c154357042ba658d4ef6abe4d9335bb7172",
        },
        {
            "output_name": "217-m1.m1",
            "operations": [{"type": "find_slice_by_crc32", "source_file": "m1.bin", "size": 0x020000, "step": 0x010000, "crc32": "d00fb2af", "fallback_offset": 0x000000}],
            "size": 0x020000, "crc32": "d00fb2af", "sha1": "6bcaa52e1641cc24288e1f22f4dc98e8d8921b90",
        },
        {
            "output_name": "217-v1.v1",
            "operations": [{"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x400000}],
            "size": 0x400000, "crc32": "1c34e013", "sha1": "5368e413d2188c4fd063b6bb7d5f498ff83ea812",
        },
        {
            "output_name": "217-v2.v2",
            "operations": [{"type": "slice", "source_file": "v1.bin", "offset": 0x400000, "size": 0x200000}],
            "size": 0x200000, "crc32": "22f1c681", "sha1": "09da03b2e63d180e55173ff25e8735c4162f027b",
        },
        {
            "output_name": "217-c1.c1",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 0}]}],
            "size": 0x400000, "crc32": "5fe97bc4", "sha1": "d76c955d83baa2b9fd24222a9b2852947b7b92f0",
        },
        {
            "output_name": "217-c2.c2",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 0}]}],
            "size": 0x400000, "crc32": "886e0d66", "sha1": "d407e1525e4ebe996e14f6e5c0396a10f736a50d",
        },
        {
            "output_name": "217-c3.c3",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 1}]}],
            "size": 0x400000, "crc32": "59e8525f", "sha1": "19f602c71545d6c021dc72e112d3a8b8efe7a9b7",
        },
        {
            "output_name": "217-c4.c4",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 1}]}],
            "size": 0x400000, "crc32": "8521add2", "sha1": "0d1a6f2979302c4c282e31ff334d2d887aec74f7",
        },
        {
            "output_name": "217-c5.c5",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 2}]}],
            "size": 0x400000, "crc32": "fb1896e5", "sha1": "777a8caa9ebdbddf89e3d5ab650c94a55228ce54",
        },
        {
            "output_name": "217-c6.c6",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 2}]}],
            "size": 0x400000, "crc32": "1c98c54b", "sha1": "cb1cad161d9b9f2f5a7cf8ae4d6d35b51acf90f5",
        },
        {
            "output_name": "217-c7.c7",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "odd", "index": 3}]}],
            "size": 0x400000, "crc32": "8b0ede2e", "sha1": "ea632ac98291ddac95441b7fe2349974b2da8a42",
        },
        {
            "output_name": "217-c8.c8",
            "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x400000, "chunks": [{"stream": "even", "index": 3}]}],
            "size": 0x400000, "crc32": "a085bb61", "sha1": "6a3e9e6ba96072b8849b407f2b24103dc0852259",
        },
    ],
}
