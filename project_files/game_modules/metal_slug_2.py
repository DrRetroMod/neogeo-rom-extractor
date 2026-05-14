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
#
# Extraction notes:
# This module was developed through source-file analysis, local testing,
# hash comparison, and comparison with public Neo Geo extraction, emulation,
# and preservation research.
#
# Metal Slug 2 extraction behaviour was informed by mslug-rom-extractor
# by terminatorhex:
# https://github.com/terminatorhex/mslug-rom-extractor
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

GAME = {'id': 'mslug2_dotemu',
 'title': 'Metal Slug 2 - Super Vehicle-001-II',
 'mame_set': 'mslug2',
 'source_family': 'dotemu',
 'search_folder_names': ['Metal Slug 2', 'METAL SLUG 2', 'mslug2'],
 'source_subfolders': ['resources/game', '.'],
 'required_source_files': ['mslug2_adpcm',
                           'mslug2_game_m68k',
                           'mslug2_game_sfix',
                           'mslug2_game_z80',
                           'mslug2_tiles',
                           'mslug2_zoom_table'],
 'notes': {'summary': 'Dotemu source layout for Metal Slug 2. Requires generic Dotemu SFIX and tile re-encode '
                      'operations in the core.',
           'details': ['Converted from the supplied Metal Slug Dotemu extractor style.',
                       'P1/P2 are sliced from mslug2_game_m68k.',
                       'Vendor BIOS files are intentionally not emitted as a standard neogeo.zip game output.']},
 'outputs': [{'zip_name': 'mslug2.zip',
              'set_name': 'mslug2',
              'type': 'main',
              'description': 'MAME-compatible Metal Slug 2 - Super Vehicle-001-II set reconstructed from '
                             'Dotemu source files.',
              'files': ['241-p1.p1',
                        '241-p2.sp2',
                        '241-s1.s1',
                        '241-m1.m1',
                        '241-v1.v1',
                        '241-v2.v2',
                        '241-c1.c1',
                        '241-c2.c2',
                        '241-c3.c3',
                        '241-c4.c4']}],
 'files': [{'output_name': '241-m1.m1',
            'operations': [{'type': 'slice', 'source_file': 'mslug2_game_z80', 'offset': 0, 'size': 131072}],
            'size': 131072,
            'crc32': '94520ebd',
            'sha1': 'f8a1551cebcb91e416f30f50581feed7f72899e9'},
           {'output_name': '241-p1.p1',
            'operations': [{'type': 'slice', 'source_file': 'mslug2_game_m68k', 'offset': 0, 'size': 1048576}],
            'size': 1048576,
            'crc32': '2a53c5da',
            'sha1': '5a6aba482cac588a6c2c51179c95b487c6e11899'},
           {'output_name': '241-p2.sp2',
            'operations': [{'type': 'slice', 'source_file': 'mslug2_game_m68k', 'offset': 1048576, 'size': 2097152}],
            'size': 2097152,
            'crc32': '38883f44',
            'sha1': 'fcf34b8c6e37774741542393b963635412484a27'},
           {'output_name': '241-v1.v1',
            'operations': [{'type': 'slice', 'source_file': 'mslug2_adpcm', 'offset': 0, 'size': 4194304}],
            'size': 4194304,
            'crc32': '99ec20e8',
            'sha1': '80597707f1fe115eed1941bb0701fc00790ad504'},
           {'output_name': '241-v2.v2',
            'operations': [{'type': 'slice', 'source_file': 'mslug2_adpcm', 'offset': 4194304, 'size': 4194304}],
            'size': 4194304,
            'crc32': 'ecb16799',
            'sha1': 'b4b4ddc680836ed55942c66d7dfe756314e02211'},
           {'output_name': '241-s1.s1',
            'operations': [{'type': 'dotemu_sfix_reencode', 'source_file': 'mslug2_game_sfix'}],
            'size': 131072,
            'crc32': 'f3d32f0f',
            'sha1': '2dc38b7dfd3ff14f64d5c0733c510b6bb8c692d0'},
           {'output_name': '241-c1.c1',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslug2_tiles',
                            'pairs': [{'odd': '241-c1.c1', 'even': '241-c2.c2', 'size': 8388608},
                                      {'odd': '241-c3.c3', 'even': '241-c4.c4', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '394b5e0d',
            'sha1': '4549926f5054ee6aa7689cf920be0327e3908a50'},
           {'output_name': '241-c2.c2',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslug2_tiles',
                            'pairs': [{'odd': '241-c1.c1', 'even': '241-c2.c2', 'size': 8388608},
                                      {'odd': '241-c3.c3', 'even': '241-c4.c4', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': 'e5806221',
            'sha1': '1e5475cfab129c77acc610f09369ca42ba5aafa5'},
           {'output_name': '241-c3.c3',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslug2_tiles',
                            'pairs': [{'odd': '241-c1.c1', 'even': '241-c2.c2', 'size': 8388608},
                                      {'odd': '241-c3.c3', 'even': '241-c4.c4', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '9f6bfa6f',
            'sha1': 'a4319b48004e723f81a980887678e3e296049a53'},
           {'output_name': '241-c4.c4',
            'operations': [{'type': 'dotemu_tiles_reencode',
                            'source_file': 'mslug2_tiles',
                            'pairs': [{'odd': '241-c1.c1', 'even': '241-c2.c2', 'size': 8388608},
                                      {'odd': '241-c3.c3', 'even': '241-c4.c4', 'size': 8388608}]}],
            'size': 8388608,
            'crc32': '7d3e306f',
            'sha1': '1499316fb381775218d897b81a6a0c3465d1a37c'}]}
