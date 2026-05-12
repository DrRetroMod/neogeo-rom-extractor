"""
Samurai Shodown IV - Amakusa's Revenge / Samurai Spirits - Amakusa Kourin module.

This module declares game-specific extraction data only.
"""

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
    "id": "samsho4",
    "title": "Samurai Shodown IV - Amakusa's Revenge / Samurai Spirits - Amakusa Kourin",
    "mame_set": "samsho4",

    "search_folder_names": [
        "Samurai Shodown IV",
        "Samurai Shodown 4",
        "Samurai Spirits - Amakusa Kourin",
        "Samurai Shodown IV - Amakusa's Revenge",
        "samsho4",
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
        "summary": "Samurai Shodown IV uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": [
            "Converted from extract_samsho4_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine samsho4.",
            "The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.",
            "The old script located 222-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "samsho4.zip",
            "set_name": "samsho4",
            "type": "main",
            "description": "MAME-compatible Samurai Shodown IV - Amakusa's Revenge / Samurai Spirits - Amakusa Kourin game set.",
            "files": [
                "222-p1.p1",
                "222-p2.sp2",
                "222-s1.s1",
                "222-m1.m1",
                "222-v1.v1",
                "222-v2.v2",
                "222-v3.v3",
                "222-c1.c1",
                "222-c2.c2",
                "222-c3.c3",
                "222-c4.c4",
                "222-c5.c5",
                "222-c6.c6",
                "222-c7.c7",
                "222-c8.c8",
            ],
        }
    ],

    "files": [
        {
            "output_name": "222-p1.p1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x100000,
                },
{
                    "type": "patch_if_needed",
                    "description": "Samurai Shodown IV P1 correction from old conditional extractor",
                    "file_offset": 0x000115,
                    "expected_old": "02",
                    "new": "00",
                }
            ],
            "size": 0x100000,
            "crc32": "1a5cb56d",
            "sha1": "9a0a5a1c7c5d428829f22d3d17f7033d43a51b5b",
        },

        {
            "output_name": "222-p2.sp2",
            "operations": [
{
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x100000,
                    "size": 0x400000,
                }
            ],
            "size": 0x400000,
            "crc32": "b023cd8b",
            "sha1": "35b4cec9858225f90acdfa16ed8a3017d0d08327",
        },

        {
            "output_name": "222-s1.s1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "8d3d3bf9",
            "sha1": "9975ed9b458bdd14e23451d2534153f68a5e4e6c",
        },

        {
            "output_name": "222-m1.m1",
            "operations": [
{
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "offset_start": 0x000000,
                    "step": 0x010000,
                    "size": 0x020000,
                    "crc32": "7615bc1b",
                    "fallback_offset": 0x000000,
                }
            ],
            "size": 0x020000,
            "crc32": "7615bc1b",
            "sha1": "b936f7b341f6fe0921b4c41049734684583e3596",
        },

        {
            "output_name": "222-v1.v1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x400000,
                }
            ],
            "size": 0x400000,
            "crc32": "7d6ba95f",
            "sha1": "03cb4e0d770e0b332b07b64cacef624460b84c78",
        },

        {
            "output_name": "222-v2.v2",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x400000,
                    "size": 0x400000,
                }
            ],
            "size": 0x400000,
            "crc32": "6c33bb5d",
            "sha1": "fd5d4e08a962dd0d22c52c91bad5ec7f23cfb901",
        },

        {
            "output_name": "222-v3.v3",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x800000,
                    "size": 0x200000,
                }
            ],
            "size": 0x200000,
            "crc32": "831ea8c0",
            "sha1": "f2987b7d09bdc4311e972ce8a9ab7ca9802db4db",
        },

        {
            "output_name": "222-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "odd", "index": 0},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "68f2ed95",
            "sha1": "c0a02df012cd25bcfe341770ea861a80294148cb",
        },

        {
            "output_name": "222-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "even", "index": 0},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "a6e9aff0",
            "sha1": "15addca49951ed53fa3c000c8d7cd327d012a620",
        },

        {
            "output_name": "222-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "odd", "index": 1},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "c91b40f4",
            "sha1": "dcda45e0336204e3e024de08edfd0a3217bc1fdd",
        },

        {
            "output_name": "222-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "even", "index": 1},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "359510a4",
            "sha1": "b6642677ebdff7788263266402080272b8a66b15",
        },

        {
            "output_name": "222-c5.c5",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "odd", "index": 2},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "9cfbb22d",
            "sha1": "789c32f917d0c6e38601cd390a7bf9d803131a4a",
        },

        {
            "output_name": "222-c6.c6",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "even", "index": 2},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "685efc32",
            "sha1": "db21ba1c7e3631ce0f1cb6f503ae7e0e043ff71b",
        },

        {
            "output_name": "222-c7.c7",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "odd", "index": 3},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "d0f86f0d",
            "sha1": "32502d71c2ab1469c492b6b382bf2bb3f85981d9",
        },

        {
            "output_name": "222-c8.c8",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x400000,
                    "chunks": [
                        {"stream": "even", "index": 3},
                    ],
                }
            ],
            "size": 0x400000,
            "crc32": "adfc50e3",
            "sha1": "7d7ee874355b5aa75ad9c9a5c9c3df98d098d85e",
        }
    ],
}
