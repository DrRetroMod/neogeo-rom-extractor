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
Game module for Kizuna Encounter - Super Tag Battle / Fu'un Super Tag Battle.

Source layout: Code Mystics/Amazon style files:
  p1.bin, m1.bin, v1.bin, c1.bin, s2.bin

Converted from the standalone kizuna_code_mystics_converter.py.
"""

GAME = {
    "id": "kizuna",
    "title": "Kizuna Encounter - Super Tag Battle / Fu'un Super Tag Battle",
    "mame_set": "kizuna",
    "source_family": "code_mystics",
    "search_folder_names": [
        "Kizuna Encounter - Super Tag Battle",
        "Kizuna Encounter",
        "Kizuna",
        "Fu'un Super Tag Battle",
        "Fuun Super Tag Battle",
        "kizuna",
    ],
    "source_subfolders": ["Data/rom", "rom", "."],
    "required_source_files": [
        "p1.bin",
        "m1.bin",
        "v1.bin",
        "c1.bin",
        "s2.bin",
    ],
    "notes": {
        "summary": "Code Mystics/Amazon source layout for Kizuna Encounter - Super Tag Battle.",
        "details": [
            "Converted from the supplied standalone Kizuna Code Mystics converter.",
            "P1 is rebuilt by concatenating the second 1 MiB half of p1.bin before the first 1 MiB half.",
            "S1 is copied from s2.bin and renamed to 216-s1.s1.",
            "Sprite data is decoded from c1.bin using the same generic NeoGeo 4bpp tile decode operation used by the core.",
            "This module emits kizuna.zip only; BIOS extraction is intentionally separate.",
        ],
    },
    "outputs": [
        {
            "zip_name": "kizuna.zip",
            "set_name": "kizuna",
            "type": "main",
            "description": "MAME-compatible Kizuna Encounter - Super Tag Battle set reconstructed from Code Mystics source files.",
            "files": [
                "216-p1.p1",
                "216-s1.s1",
                "216-m1.m1",
                "059-v1.v1",
                "216-v2.v2",
                "059-v3.v3",
                "216-v4.v4",
                "059-c1.c1",
                "059-c2.c2",
                "216-c3.c3",
                "216-c4.c4",
                "059-c5.c5",
                "059-c6.c6",
                "059-c7.c7",
                "059-c8.c8",
            ],
        }
    ],
    "files": [
        {
            "output_name": "216-p1.p1",
            "operations": [
                {
                    "type": "concat_slices",
                    "slices": [
                        {"source_file": "p1.bin", "offset": 0x100000, "size": 0x100000},
                        {"source_file": "p1.bin", "offset": 0x000000, "size": 0x100000},
                    ],
                }
            ],
            "size": 0x200000,
            "crc32": "75d2b3de",
            "sha1": "ee778656c26828935ee2a2bfd0ce5a22aa681c10",
        },
        {
            "output_name": "216-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0, "size": 0x20000}
            ],
            "size": 0x20000,
            "crc32": "efdc72d7",
            "sha1": "be37cbf1852e2e4c907cc799b754b538544b6703",
        },
        {
            "output_name": "216-m1.m1",
            "operations": [
                {"type": "slice", "source_file": "m1.bin", "offset": 0, "size": 0x20000}
            ],
            "size": 0x20000,
            "crc32": "1b096820",
            "sha1": "72852e78c620038f8dafde5e54e02e418c31be9c",
        },
        {
            "output_name": "059-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x200000}
            ],
            "size": 0x200000,
            "crc32": "530c50fd",
            "sha1": "29401cee7f7d2c199c7cb58092e86b28205e81ad",
        },
        {
            "output_name": "216-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x200000, "size": 0x200000}
            ],
            "size": 0x200000,
            "crc32": "03667a8d",
            "sha1": "3b0475e553a49f8788f32b0c84f82645cc6b4273",
        },
        {
            "output_name": "059-v3.v3",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x400000, "size": 0x200000}
            ],
            "size": 0x200000,
            "crc32": "7038c2f9",
            "sha1": "c1d6f86b24feba03fe009b58199d2eeabe572f4e",
        },
        {
            "output_name": "216-v4.v4",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x600000, "size": 0x200000}
            ],
            "size": 0x200000,
            "crc32": "31b99bd6",
            "sha1": "5871751f8e9e6b98337472c22b5e1c7ede0a9311",
        },
        {
            "output_name": "059-c1.c1",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "odd", "index": 0}]},
            ],
            "size": 0x200000,
            "crc32": "763ba611",
            "sha1": "d3262e0332c894ee149c5963f882cc5e5562ee57",
        },
        {
            "output_name": "059-c2.c2",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "even", "index": 0}]},
            ],
            "size": 0x200000,
            "crc32": "e05e8ca6",
            "sha1": "986a9b16ff92bc101ab567d2d01348e093abea9a",
        },
        {
            "output_name": "216-c3.c3",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x200000,
                    "chunks": [
                        {"stream": "odd", "index": 2},
                        {"stream": "odd", "index": 3},
                    ],
                },
            ],
            "size": 0x400000,
            "crc32": "665c9f16",
            "sha1": "7ec781a49a462f395b450460b29493f55134eac2",
        },
        {
            "output_name": "216-c4.c4",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x200000,
                    "chunks": [
                        {"stream": "even", "index": 2},
                        {"stream": "even", "index": 3},
                    ],
                },
            ],
            "size": 0x400000,
            "crc32": "7f5d03db",
            "sha1": "365ed266c121f4df0bb76898955a8ae0e668a216",
        },
        {
            "output_name": "059-c5.c5",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "odd", "index": 4}]},
            ],
            "size": 0x200000,
            "crc32": "59013f9e",
            "sha1": "5bf48fcc450da72a8c4685f6e3887e67eae49988",
        },
        {
            "output_name": "059-c6.c6",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "even", "index": 4}]},
            ],
            "size": 0x200000,
            "crc32": "1c8d5def",
            "sha1": "475d89a5c4922a9f6bd756d23c2624d57b6e9d62",
        },
        {
            "output_name": "059-c7.c7",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "odd", "index": 6}]},
            ],
            "size": 0x200000,
            "crc32": "c88f7035",
            "sha1": "c29a428b741f4fe7b71a3bc23c87925b6bc1ca8f",
        },
        {
            "output_name": "059-c8.c8",
            "operations": [
                {
                    "type": "neogeo_4bpp_tile_decode",
                    "source_file": "c1.bin",
                    "tile_size": 128,
                    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
                    "output_streams": {"odd": [0, 1], "even": [2, 3]},
                },
                {"type": "assemble_chunks", "chunk_size": 0x200000, "chunks": [{"stream": "even", "index": 6}]},
            ],
            "size": 0x200000,
            "crc32": "484ce3ba",
            "sha1": "4f21ed20ce6e2b67e2b079404599310c94f591ff",
        },
    ],
}
