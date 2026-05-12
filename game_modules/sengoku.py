"""
Sengoku / Sengoku Denshou module.

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
    "id": "sengoku",
    "title": "Sengoku / Sengoku Denshou",
    "mame_set": "sengoku",

    "search_folder_names": [
        "Sengoku",
        "Sengoku Denshou",
        "sengoku",
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
        "summary": "Sengoku uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": [
            "Converted from extract_sengoku_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine sengoku.",
            "The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.",
            "The old script located 017-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "sengoku.zip",
            "set_name": "sengoku",
            "type": "main",
            "description": "MAME-compatible Sengoku / Sengoku Denshou game set.",
            "files": [
                "017-p1.p1",
                "017-p2.p2",
                "017-s1.s1",
                "017-m1.m1",
                "017-v1.v1",
                "017-v2.v2",
                "017-c1.c1",
                "017-c2.c2",
                "017-c3.c3",
                "017-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "017-p1.p1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x080000,
                },
{
                    "type": "patch_if_needed",
                    "description": "Sengoku P1 correction from old conditional extractor",
                    "file_offset": 0x000115,
                    "expected_old": "02",
                    "new": "00",
                }
            ],
            "size": 0x080000,
            "crc32": "f8a63983",
            "sha1": "7a10ecb2f0fd8315641374c065d2602107b09e72",
        },

        {
            "output_name": "017-p2.p2",
            "operations": [
{
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x080000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "3024bbb3",
            "sha1": "88892e1292dd60f35a76f9a22e623d4f0f9693cc",
        },

        {
            "output_name": "017-s1.s1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                }
            ],
            "size": 0x020000,
            "crc32": "b246204d",
            "sha1": "73dce64c61fb5bb7e836a8e60f081bb77d80d281",
        },

        {
            "output_name": "017-m1.m1",
            "operations": [
{
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "offset_start": 0x000000,
                    "step": 0x010000,
                    "size": 0x020000,
                    "crc32": "9b4f34c6",
                    "fallback_offset": 0x000000,
                }
            ],
            "size": 0x020000,
            "crc32": "9b4f34c6",
            "sha1": "7f3a51f47fcbaa598f5c76bc66e2c53c8dfd852d",
        },

        {
            "output_name": "017-v1.v1",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x100000,
                }
            ],
            "size": 0x100000,
            "crc32": "23663295",
            "sha1": "9374a5d9f3de8e6a97c11f07d8b4485ac9d55edb",
        },

        {
            "output_name": "017-v2.v2",
            "operations": [
{
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x100000,
                    "size": 0x100000,
                }
            ],
            "size": 0x100000,
            "crc32": "f61e6765",
            "sha1": "1c9b287996947319eb3d288c3d82932cf01039db",
        },

        {
            "output_name": "017-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 0},
                    ],
                }
            ],
            "size": 0x100000,
            "crc32": "b4eb82a1",
            "sha1": "79879e2ea78c07d04c88dc9a1ad59604b7a078be",
        },

        {
            "output_name": "017-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 0},
                    ],
                }
            ],
            "size": 0x100000,
            "crc32": "d55c550d",
            "sha1": "6110f693aa23710939c04153cf5af26493e4a03f",
        },

        {
            "output_name": "017-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 1},
                    ],
                }
            ],
            "size": 0x100000,
            "crc32": "ed51ef65",
            "sha1": "e8a8d86e24454948e51a75c883bc6e4091cbf820",
        },

        {
            "output_name": "017-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
{
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 1},
                    ],
                }
            ],
            "size": 0x100000,
            "crc32": "f4f3c9cb",
            "sha1": "8faafa89dbd0345218f71f891419d2e4e7578200",
        }
    ],
}
