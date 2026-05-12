"""
Soccer Brawl module.

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
    "id": "socbrawl",
    "title": "Soccer Brawl",
    "mame_set": "socbrawl",

    "search_folder_names": [
        "Soccer Brawl",
        "socbrawl",
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
        "summary": "Soccer Brawl uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": [
            "Converted from extract_socbrawl_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine socbrawl.",
            "The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.",
            "The old script located 031-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "socbrawl.zip",
            "set_name": "socbrawl",
            "type": "main",
            "description": "MAME-compatible Soccer Brawl game set.",
            "files": [
                "031-pg1.p1",
                "031-s1.s1",
                "031-m1.m1",
                "031-v1.v1",
                "031-v2.v2",
                "031-c1.c1",
                "031-c2.c2",
                "031-c3.c3",
                "031-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "031-pg1.p1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "p1.bin",
                    "offset": 0x000000,
                    "size": 0x080000,
                },
                {
                    "type": "patch_if_needed",
                    "description": "Soccer Brawl P1 correction from old conditional extractor",
                    "file_offset": 0x000115,
                    "expected_old": "02",
                    "new": "00",
                },
            ],
            "size": 0x080000,
            "crc32": "17f034a7",
            "sha1": "2e66c7bd93a08efe63c4894494db50bbf58f60e4",
        },

        {
            "output_name": "031-s1.s1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "s2.bin",
                    "offset": 0x000000,
                    "size": 0x020000,
                },
            ],
            "size": 0x020000,
            "crc32": "4c117174",
            "sha1": "26e52c4f628338a9aa1c159517cdf873f738fb98",
        },

        {
            "output_name": "031-m1.m1",
            "operations": [
                {
                    "type": "find_slice_by_crc32",
                    "source_file": "m1.bin",
                    "offset_start": 0x000000,
                    "step": 0x010000,
                    "size": 0x020000,
                    "crc32": "cb37427c",
                    "fallback_offset": 0x000000,
                },
            ],
            "size": 0x020000,
            "crc32": "cb37427c",
            "sha1": "99efe9600ebeda48331f396e3203c7588bdb7d24",
        },

        {
            "output_name": "031-v1.v1",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x000000,
                    "size": 0x100000,
                },
            ],
            "size": 0x100000,
            "crc32": "cc78497e",
            "sha1": "895bd647150fae9b2259ef043ed681f4c4de66ea",
        },

        {
            "output_name": "031-v2.v2",
            "operations": [
                {
                    "type": "slice",
                    "source_file": "v1.bin",
                    "offset": 0x100000,
                    "size": 0x100000,
                },
            ],
            "size": 0x100000,
            "crc32": "dda043c6",
            "sha1": "08165a59700ab6b1e523079dd2a3549e520cc594",
        },

        {
            "output_name": "031-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "odd", "index": 0},
                    ],
                },
            ],
            "size": 0x100000,
            "crc32": "bd0a4eb8",
            "sha1": "b67988cb3e550d083e81c9bd436da55b242785ed",
        },

        {
            "output_name": "031-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x100000,
                    "chunks": [
                        {"stream": "even", "index": 0},
                    ],
                },
            ],
            "size": 0x100000,
            "crc32": "efde5382",
            "sha1": "e42789c8d87ee3d4549d0a903e990c03338cbbd8",
        },

        {
            "output_name": "031-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "odd", "index": 2},
                    ],
                },
            ],
            "size": 0x080000,
            "crc32": "580f7f33",
            "sha1": "f4f95a7c8de00e1366a723fc4cd0e8c1905af636",
        },

        {
            "output_name": "031-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {
                    "type": "assemble_chunks",
                    "chunk_size": 0x080000,
                    "chunks": [
                        {"stream": "even", "index": 2},
                    ],
                },
            ],
            "size": 0x080000,
            "crc32": "ed297de8",
            "sha1": "616f8fa4c86231f3e79faf9f69f8bb909cbc35f0",
        }
    ],
}
