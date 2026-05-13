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
The Last Blade 2 / Bakumatsu Roman - Dai Ni Maku Gekka no Kenshi module.

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
    'id': 'lastbld2',
    'title': 'The Last Blade 2 / Bakumatsu Roman - Dai Ni Maku Gekka no Kenshi',
    'mame_set': 'lastbld2',
    'search_folder_names': [
        'The Last Blade 2',
        'Last Blade 2',
        'Bakumatsu Roman - Dai Ni Maku Gekka no Kenshi',
        'lastbld2',
    ],
    'source_subfolders': [
        'Data/rom',
        'rom',
        'resources/game',
        '.',
    ],
    'required_source_files': [
        'p1.bin',
        's1.bin',
        'm1.bin',
        'v1.bin',
        'c1.bin',
    ],
    'notes': {
        'summary': 'The Last Blade 2 uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.',
        'details': [
            "Converted from extract_lastbld2_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            'SHA1 values were added from the supplied MAME 0.287 DAT for machine lastbld2.',
            'The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.',
            'The old script located 243-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.',
            'The old script allowed s2.bin or s1.bin for the S-ROM; this module uses s1.bin because the old script notes this source usually has s1.bin for Last Blade 2.',
            'Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.',
        ],
    },
    'outputs': [
        {
            'zip_name': 'lastbld2.zip',
            'set_name': 'lastbld2',
            'type': 'main',
            'description': 'MAME-compatible The Last Blade 2 game set.',
            'files': [
                '243-pg1.p1',
                '243-pg2.sp2',
                '243-s1.s1',
                '243-m1.m1',
                '243-v1.v1',
                '243-v2.v2',
                '243-v3.v3',
                '243-v4.v4',
                '243-c1.c1',
                '243-c2.c2',
                '243-c3.c3',
                '243-c4.c4',
                '243-c5.c5',
                '243-c6.c6',
            ],
        },
    ],
    'files': [
        {
            'output_name': '243-pg1.p1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'p1.bin',
                    'offset': 0x0000,
                    'size': 0x100000,
                },
                {
                    'type': 'patch_if_needed',
                    'description': 'The Last Blade 2 P1 correction from old conditional extractor',
                    'file_offset': 0x0115,
                    'expected_old': '02',
                    'new': '00',
                },
            ],
            'size': 0x100000,
            'crc32': 'af1e6554',
            'sha1': 'bd8526f60c2472937728a5d933fbd19d899f2cba',
        },
        {
            'output_name': '243-pg2.sp2',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'p1.bin',
                    'offset': 0x100000,
                    'size': 0x400000,
                },
            ],
            'size': 0x400000,
            'crc32': 'add4a30b',
            'sha1': '7db62564db49fe0218cbb35b119d62582a24d658',
        },
        {
            'output_name': '243-s1.s1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 's1.bin',
                    'offset': 0x0000,
                    'size': 0x020000,
                },
            ],
            'size': 0x020000,
            'crc32': 'c9cd2298',
            'sha1': 'a9a18b5347f9dbe29a2ccb63fd4c8fd19537bf8b',
        },
        {
            'output_name': '243-m1.m1',
            'operations': [
                {
                    'type': 'find_slice_by_crc32',
                    'source_file': 'm1.bin',
                    'offset_start': 0x0000,
                    'step': 0x010000,
                    'size': 0x020000,
                    'crc32': 'acf12d10',
                    'fallback_offset': 0x0000,
                },
            ],
            'size': 0x020000,
            'crc32': 'acf12d10',
            'sha1': '6e6b98cc1fa44f24a5168877559b0055e6957b60',
        },
        {
            'output_name': '243-v1.v1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x0000,
                    'size': 0x400000,
                },
            ],
            'size': 0x400000,
            'crc32': 'f7ee6fbb',
            'sha1': '55137bcabeeb590e40a9b8a7c07dd106e4d12a90',
        },
        {
            'output_name': '243-v2.v2',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x400000,
                    'size': 0x400000,
                },
            ],
            'size': 0x400000,
            'crc32': 'aa9e4df6',
            'sha1': 'a0b91f63e2552a8ad9e0d1af00e2c38288637161',
        },
        {
            'output_name': '243-v3.v3',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x800000,
                    'size': 0x400000,
                },
            ],
            'size': 0x400000,
            'crc32': '4ac750b2',
            'sha1': '585a154acc67bd84ea5b944686b78ed082b768d9',
        },
        {
            'output_name': '243-v4.v4',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0xC00000,
                    'size': 0x400000,
                },
            ],
            'size': 0x400000,
            'crc32': 'f5c64ba6',
            'sha1': '2eac455def8c27090862cc042f65a3a8aad88283',
        },
        {
            'output_name': '243-c1.c1',
            'operations': [
                {
                    'type': 'neogeo_4bpp_tile_decode',
                    'source_file': 'c1.bin',
                    'tile_size': 0x0080,
                    'row_offsets': [
                        [
                            0x0004,
                            0x0000,
                        ],
                        [
                            0x0004,
                            0x0008,
                        ],
                        [
                            0x0000,
                            0x0000,
                        ],
                        [
                            0x0000,
                            0x0008,
                        ],
                    ],
                    'output_streams': {
                        'odd': [
                            0x0000,
                            0x0001,
                        ],
                        'even': [
                            0x0002,
                            0x0003,
                        ],
                    },
                },
                {
                    'type': 'assemble_chunks',
                    'chunk_size': 0x800000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0000,
                        },
                    ],
                },
            ],
            'size': 0x800000,
            'crc32': '5839444d',
            'sha1': '0616921c4cce20422563578bd0e806d359508599',
        },
        {
            'output_name': '243-c2.c2',
            'operations': [
                {
                    'type': 'neogeo_4bpp_tile_decode',
                    'source_file': 'c1.bin',
                    'tile_size': 0x0080,
                    'row_offsets': [
                        [
                            0x0004,
                            0x0000,
                        ],
                        [
                            0x0004,
                            0x0008,
                        ],
                        [
                            0x0000,
                            0x0000,
                        ],
                        [
                            0x0000,
                            0x0008,
                        ],
                    ],
                    'output_streams': {
                        'odd': [
                            0x0000,
                            0x0001,
                        ],
                        'even': [
                            0x0002,
                            0x0003,
                        ],
                    },
                },
                {
                    'type': 'assemble_chunks',
                    'chunk_size': 0x800000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0000,
                        },
                    ],
                },
            ],
            'size': 0x800000,
            'crc32': 'dd087428',
            'sha1': 'ca27fdb60425664956a18c021ea465f452fb1527',
        },
        {
            'output_name': '243-c3.c3',
            'operations': [
                {
                    'type': 'neogeo_4bpp_tile_decode',
                    'source_file': 'c1.bin',
                    'tile_size': 0x0080,
                    'row_offsets': [
                        [
                            0x0004,
                            0x0000,
                        ],
                        [
                            0x0004,
                            0x0008,
                        ],
                        [
                            0x0000,
                            0x0000,
                        ],
                        [
                            0x0000,
                            0x0008,
                        ],
                    ],
                    'output_streams': {
                        'odd': [
                            0x0000,
                            0x0001,
                        ],
                        'even': [
                            0x0002,
                            0x0003,
                        ],
                    },
                },
                {
                    'type': 'assemble_chunks',
                    'chunk_size': 0x800000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0001,
                        },
                    ],
                },
            ],
            'size': 0x800000,
            'crc32': '6054cbe0',
            'sha1': 'ec2f65e9c930250ee25fd064ee5ae76a7a9c61d9',
        },
        {
            'output_name': '243-c4.c4',
            'operations': [
                {
                    'type': 'neogeo_4bpp_tile_decode',
                    'source_file': 'c1.bin',
                    'tile_size': 0x0080,
                    'row_offsets': [
                        [
                            0x0004,
                            0x0000,
                        ],
                        [
                            0x0004,
                            0x0008,
                        ],
                        [
                            0x0000,
                            0x0000,
                        ],
                        [
                            0x0000,
                            0x0008,
                        ],
                    ],
                    'output_streams': {
                        'odd': [
                            0x0000,
                            0x0001,
                        ],
                        'even': [
                            0x0002,
                            0x0003,
                        ],
                    },
                },
                {
                    'type': 'assemble_chunks',
                    'chunk_size': 0x800000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0001,
                        },
                    ],
                },
            ],
            'size': 0x800000,
            'crc32': '8bd2a9d2',
            'sha1': '0935df65cd2b0891a708bcc0f1c188148058d4b5',
        },
        {
            'output_name': '243-c5.c5',
            'operations': [
                {
                    'type': 'neogeo_4bpp_tile_decode',
                    'source_file': 'c1.bin',
                    'tile_size': 0x0080,
                    'row_offsets': [
                        [
                            0x0004,
                            0x0000,
                        ],
                        [
                            0x0004,
                            0x0008,
                        ],
                        [
                            0x0000,
                            0x0000,
                        ],
                        [
                            0x0000,
                            0x0008,
                        ],
                    ],
                    'output_streams': {
                        'odd': [
                            0x0000,
                            0x0001,
                        ],
                        'even': [
                            0x0002,
                            0x0003,
                        ],
                    },
                },
                {
                    'type': 'assemble_chunks',
                    'chunk_size': 0x800000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0002,
                        },
                    ],
                },
            ],
            'size': 0x800000,
            'crc32': '6a503dcf',
            'sha1': '23241b16d7e20f923d41186b29487ab922c7f530',
        },
        {
            'output_name': '243-c6.c6',
            'operations': [
                {
                    'type': 'neogeo_4bpp_tile_decode',
                    'source_file': 'c1.bin',
                    'tile_size': 0x0080,
                    'row_offsets': [
                        [
                            0x0004,
                            0x0000,
                        ],
                        [
                            0x0004,
                            0x0008,
                        ],
                        [
                            0x0000,
                            0x0000,
                        ],
                        [
                            0x0000,
                            0x0008,
                        ],
                    ],
                    'output_streams': {
                        'odd': [
                            0x0000,
                            0x0001,
                        ],
                        'even': [
                            0x0002,
                            0x0003,
                        ],
                    },
                },
                {
                    'type': 'assemble_chunks',
                    'chunk_size': 0x800000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0002,
                        },
                    ],
                },
            ],
            'size': 0x800000,
            'crc32': 'ec9c36d0',
            'sha1': 'e145e9e359000dda6e1dfe95a996bc6d29cfca21',
        },
    ],
}
