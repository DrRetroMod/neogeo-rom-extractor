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

# Metal Slug X patch data:
# The JSON patch data used by this module is directly reused from
# mslug-rom-extractor by terminatorhex, with the file renamed for this project.
# See README.md -> Special thanks to terminatorhex.

# Extraction notes:
# This module was developed through source-file analysis, local testing,
# hash comparison, and comparison with public Neo Geo extraction, emulation,
# and preservation research.
#
# Metal Slug X extraction behaviour was informed by mslug-rom-extractor
# by terminatorhex. The Metal Slug X JSON patch data is directly reused
# from that project, with the file renamed for this project:
# https://github.com/terminatorhex/mslug-rom-extractor
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.


GAME = {'id': 'mslugx_dotemu',
 'title': 'Metal Slug X - Super Vehicle-001',
 'mame_set': 'mslugx',
 'source_family': 'dotemu',
 'search_folder_names': ['Metal Slug X', 'METAL SLUG X', 'mslugx'],
 'source_subfolders': ['resources/game', '.'],
 'required_source_files': ['mslugx_adpcm',
                           'mslugx_game_m68k',
                           'mslugx_game_sfix',
                           'mslugx_game_z80',
                           'mslugx_tiles',
                           'mslugx_zoom_table'],
 'notes': {'summary': 'Dotemu source layout for Metal Slug X. Requires generic Dotemu SFIX, tile re-encode, and '
                      'byte-patch operations in the core.',
           'details': ['Converted from the supplied Metal Slug Dotemu extractor style.',
                       'P1 is sliced from mslugx_game_m68k and then patched using the external JSON patch file '
                       'mslugx_250-p1.p1.json.',
                       'The patch offsets and byte values are game-specific and intentionally live in game_modules/patch_data/.',
                       'Vendor BIOS files are intentionally not emitted as a standard neogeo.zip game output.']},
 'outputs': [{'zip_name': 'mslugx.zip',
              'set_name': 'mslugx',
              'type': 'main',
              'description': 'MAME-compatible Metal Slug X - Super Vehicle-001 set reconstructed from Dotemu '
                             'source files.',
              'files': ['250-p1.p1',
                        '250-p2.ep1',
                        '250-s1.s1',
                        '250-m1.m1',
                        '250-v1.v1',
                        '250-v2.v2',
                        '250-v3.v3',
                        '250-c1.c1',
                        '250-c2.c2',
                        '250-c3.c3',
                        '250-c4.c4',
                        '250-c5.c5',
                        '250-c6.c6']}],
 'files': [{'output_name': '250-m1.m1',
            'operations': [{'type': 'slice', 'source_file': 'mslugx_game_z80', 'offset': 0, 'size': 131072}],
            'size': 131072,
            'crc32': 'fd42a842',
            'sha1': '55769bad4860f64ef53a333e0da9e073db483d6a'},
           {'output_name': '250-p1.p1',
            'operations': [{'type': 'slice', 'source_file': 'mslugx_game_m68k', 'offset': 0, 'size': 1048576},
                           {'type': 'apply_byte_patches_from_json',
                            'patch_file': 'mslugx_250-p1.p1.json'}],
            'size': 1048576,
            'crc32': '81f1f60b',
            'sha1': '4c19f2e9824e606178ac1c9d4b0516fbaa625035'},
           {'output_name': '250-p2.ep1',
            'operations': [{'type': 'slice', 'source_file': 'mslugx_game_m68k', 'offset': 1048576, 'size': 4194304}],
            'size': 4194304,
            'crc32': '1fda2e12',
            'sha1': '18aaa7a3ba8da99f78c430e9be69ccde04bc04d9'},
           {'output_name': '250-v1.v1',
            'operations': [{'type': 'slice', 'source_file': 'mslugx_adpcm', 'offset': 0, 'size': 4194304}],
            'size': 4194304,
            'crc32': 'c79ede73',
            'sha1': 'ebfcc67204ff9677cf7972fd5b6b7faabf07280c'},
           {'output_name': '250-v2.v2',
            'operations': [{'type': 'slice', 'source_file': 'mslugx_adpcm', 'offset': 4194304, 'size': 4194304}],
            'size': 4194304,
            'crc32': 'ea9aabe1',
            'sha1': '526c42ca9a388f7435569400e2f132e2724c71ff'},
           {'output_name': '250-v3.v3',
            'operations': [{'type': 'slice', 'source_file': 'mslugx_adpcm', 'offset': 8388608, 'size': 2097152}],
            'size': 2097152,
            'crc32': '2ca65102',
            'sha1': '45979d1edb1fc774a415d9386f98d7cb252a2043'},
           {'output_name': '250-s1.s1',
            'operations': [{'type': 'dotemu_sfix_reencode', 'source_file': 'mslugx_game_sfix'}],
            'size': 131072,
            'crc32': 'fb6f441d',
            'sha1': '2cc392ecde5d5afb28ddbaa1030552b48571dcfb'},
           {'output_name': '250-c1.c1',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslugx_tiles',
                            'pairs': [{'odd': '250-c1.c1', 'even': '250-c2.c2', 'size': 8388608},
                                      {'odd': '250-c3.c3', 'even': '250-c4.c4', 'size': 8388608},
                                      {'odd': '250-c5.c5', 'even': '250-c6.c6', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '09a52c6f',
            'sha1': 'c3e8a8ccdac0f8bddc4c3413277626532405fae2'},
           {'output_name': '250-c2.c2',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslugx_tiles',
                            'pairs': [{'odd': '250-c1.c1', 'even': '250-c2.c2', 'size': 8388608},
                                      {'odd': '250-c3.c3', 'even': '250-c4.c4', 'size': 8388608},
                                      {'odd': '250-c5.c5', 'even': '250-c6.c6', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '31679821',
            'sha1': '554f600a3aa09c16c13c625299b087a79d0d15c5'},
           {'output_name': '250-c3.c3',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslugx_tiles',
                            'pairs': [{'odd': '250-c1.c1', 'even': '250-c2.c2', 'size': 8388608},
                                      {'odd': '250-c3.c3', 'even': '250-c4.c4', 'size': 8388608},
                                      {'odd': '250-c5.c5', 'even': '250-c6.c6', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': 'fd602019',
            'sha1': 'c56646c62387bc1439d46610258c755beb8d7dd8'},
           {'output_name': '250-c4.c4',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslugx_tiles',
                            'pairs': [{'odd': '250-c1.c1', 'even': '250-c2.c2', 'size': 8388608},
                                      {'odd': '250-c3.c3', 'even': '250-c4.c4', 'size': 8388608},
                                      {'odd': '250-c5.c5', 'even': '250-c6.c6', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '31354513',
            'sha1': '31be8ea2498001f68ce4b06b8b90acbf2dcab6af'},
           {'output_name': '250-c5.c5',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslugx_tiles',
                            'pairs': [{'odd': '250-c1.c1', 'even': '250-c2.c2', 'size': 8388608},
                                      {'odd': '250-c3.c3', 'even': '250-c4.c4', 'size': 8388608},
                                      {'odd': '250-c5.c5', 'even': '250-c6.c6', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': 'a4b56124',
            'sha1': 'd41069856df990a1a99d39fb263c8303389d5475'},
           {'output_name': '250-c6.c6',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslugx_tiles',
                            'pairs': [{'odd': '250-c1.c1', 'even': '250-c2.c2', 'size': 8388608},
                                      {'odd': '250-c3.c3', 'even': '250-c4.c4', 'size': 8388608},
                                      {'odd': '250-c5.c5', 'even': '250-c6.c6', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '83e3e69d',
            'sha1': '39be66287696829d243fb71b3fb8b7dc2bc3298f'}]}
