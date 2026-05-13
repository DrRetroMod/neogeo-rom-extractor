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

# Extraction notes:
# This module was developed through source-file analysis, local testing,
# hash comparison, and comparison with public Neo Geo extraction, emulation,
# and preservation research.
#
# Twinkle Star Sprites extraction behaviour was informed by mslug-rom-extractor
# by terminatorhex:
# https://github.com/terminatorhex/mslug-rom-extractor
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

GAME = {'id': 'twinspri_dotemu',
 'title': 'Twinkle Star Sprites',
 'mame_set': 'twinspri',
 'source_family': 'dotemu',
 'search_folder_names': ['Twinkle Star Sprites', 'twinspri'],
 'source_subfolders': ['resources/game', '.'],
 'required_source_files': ['twinspri_game_m68k',
                           'twinspri_game_z80',
                           'twinspri_game_sfix',
                           'twinspri_adpcm',
                           'twinspri_tiles'],
 'notes': {'summary': 'Dotemu/Amazon source layout for Twinkle Star Sprites. Requires generic Dotemu SFIX and tile '
                      're-encode operations in the core.',
           'details': ['P1 uses the two 1 MiB halves of twinspri_game_m68k reversed, matching the supplied adaptation.',
                       'Vendor BIOS files are intentionally not emitted as a standard neogeo.zip game output.']},
 'outputs': [{'zip_name': 'twinspri.zip',
              'set_name': 'twinspri',
              'type': 'main',
              'description': 'MAME-compatible Twinkle Star Sprites set reconstructed from Dotemu source files.',
              'files': ['224-p1.p1',
                        '224-m1.m1',
                        '224-s1.s1',
                        '224-v1.v1',
                        '224-v2.v2',
                        '224-c1.c1',
                        '224-c2.c2',
                        '224-c3.c3',
                        '224-c4.c4']}],
 'files': [{'output_name': '224-p1.p1',
            'operations': [{'type': 'concat_slices',
                            'slices': [{'source_file': 'twinspri_game_m68k', 'offset': 1048576, 'size': 1048576},
                                       {'source_file': 'twinspri_game_m68k', 'offset': 0, 'size': 1048576}]}],
            'size': 2097152,
            'crc32': '7697e445',
            'sha1': '5b55ca120f77a931d40719b14e0bfc8cac1d628c'},
           {'output_name': '224-m1.m1',
            'operations': [{'type': 'slice', 'source_file': 'twinspri_game_z80', 'offset': 0, 'size': 131072}],
            'size': 131072,
            'crc32': '364d6f96',
            'sha1': '779b95a6476089b71f48c8368d9043ee1dba9032'},
           {'output_name': '224-s1.s1',
            'operations': [{'type': 'dotemu_sfix_reencode', 'source_file': 'twinspri_game_sfix'}],
            'size': 131072,
            'crc32': 'eeed5758',
            'sha1': '24e48f396716e145b692468762cf595fb7267873'},
           {'output_name': '224-v1.v1',
            'operations': [{'type': 'slice', 'source_file': 'twinspri_adpcm', 'offset': 0, 'size': 4194304}],
            'size': 4194304,
            'crc32': 'ff57f088',
            'sha1': '1641989b8aac899dbd68aa2332bcdf9b90b33564'},
           {'output_name': '224-v2.v2',
            'operations': [{'type': 'slice', 'source_file': 'twinspri_adpcm', 'offset': 4194304, 'size': 2097152}],
            'size': 2097152,
            'crc32': '7ad26599',
            'sha1': '822030037b7664795bf3d64e1452d0aecc22497e'},
           {'output_name': '224-c1.c1',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'twinspri_tiles',
                            'pairs': [{'odd': '224-c1.c1', 'even': '224-c2.c2', 'size': 4194304},
                                      {'odd': '224-c3.c3', 'even': '224-c4.c4', 'size': 1048576}]}],
            'size': 4194304,
            'crc32': 'f7da64ab',
            'sha1': '587a10ed9235c9046a3523fe80feba07764fac9b'},
           {'output_name': '224-c2.c2',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'twinspri_tiles',
                            'pairs': [{'odd': '224-c1.c1', 'even': '224-c2.c2', 'size': 4194304},
                                      {'odd': '224-c3.c3', 'even': '224-c4.c4', 'size': 1048576}]}],
            'size': 4194304,
            'crc32': '4c09bbfb',
            'sha1': 'e781aafba3bdefb7ed152826f4c3eb441735331c'},
           {'output_name': '224-c3.c3',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'twinspri_tiles',
                            'pairs': [{'odd': '224-c1.c1', 'even': '224-c2.c2', 'size': 4194304},
                                      {'odd': '224-c3.c3', 'even': '224-c4.c4', 'size': 1048576}]}],
            'size': 1048576,
            'crc32': 'c59e4129',
            'sha1': '93f02d1b4fbb152a9d336494fbff0d7642921de5'},
           {'output_name': '224-c4.c4',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'twinspri_tiles',
                            'pairs': [{'odd': '224-c1.c1', 'even': '224-c2.c2', 'size': 4194304},
                                      {'odd': '224-c3.c3', 'even': '224-c4.c4', 'size': 1048576}]}],
            'size': 1048576,
            'crc32': 'b5532e53',
            'sha1': '7d896c25ba97f6e5d43c13d4df4ba72964a976ed'}]}
