"""
Last Resort module.

Converted from extract_lresort_ngprime.py.

Source of extraction logic:
- old NGPrimeClaim-style Last Resort extractor

Source of SHA1 values:
- MAME 0.287 DAT, machine lresort

Game-specific details live here:
- source filenames
- output filenames
- offsets
- sizes
- CRC32/SHA1 hashes
- conditional M1 handling
- C-ROM transform parameters
- C-ROM chunk assembly order
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
    "id": "lresort",
    "title": "Last Resort",
    "mame_set": "lresort",

    "search_folder_names": [
        "Last Resort",
        "lresort",
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
            "Last Resort uses standard slices, conditional M1 handling, and a "
            "module-declared NeoGeo 4bpp C-ROM transform from c1.bin."
        ),
        "details": [
            "Converted from extract_lresort_ngprime.py without changing the old script's offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine lresort.",
            "The old script did not blindly follow a 65536-byte M1 JSON entry; it outputs the 131072-byte MAME M1 file.",
            "If m1.bin is 128 KiB, the whole file is used. If m1.bin is 192 KiB or larger, offset 0x10000 for 128 KiB is used.",
            "v1.bin is split into two 1 MiB V-ROM files, matching the old extractor.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout, then assembled into 024-c1.c1 through 024-c4.c4.",
            "The old script could create a manual-review ZIP if CRC validation failed; this module outputs only the validated MAME lresort.zip when all files pass.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "lresort.zip",
            "set_name": "lresort",
            "type": "main",
            "description": "MAME-compatible Last Resort game set.",
            "files": [
                "024-p1.p1",
                "024-s1.s1",
                "024-m1.m1",
                "024-v1.v1",
                "024-v2.v2",
                "024-c1.c1",
                "024-c2.c2",
                "024-c3.c3",
                "024-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "024-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x080000}
            ],
            "size": 0x080000,
            "crc32": "89c4ab97",
            "sha1": "3a1817c427185ea1b44fe52f009c00b0a9007c85",
        },
        {
            "output_name": "024-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000}
            ],
            "size": 0x020000,
            "crc32": "5cef5cc6",
            "sha1": "9ec305007bdb356e9f8f279beae5e2bcb3f2cf7b",
        },
        {
            "output_name": "024-m1.m1",
            "operations": [
                {
                    "type": "conditional_slice",
                    "source_file": "m1.bin",
                    "choices": [
                        {
                            "description": "m1.bin is already 128 KiB; use whole file",
                            "if_size": 0x020000,
                            "offset": 0x000000,
                            "size": 0x020000,
                        },
                        {
                            "description": "m1.bin is 192 KiB or larger; use offset 0x10000 for 128 KiB",
                            "minimum_size": 0x030000,
                            "offset": 0x010000,
                            "size": 0x020000,
                        },
                    ],
                }
            ],
            "size": 0x020000,
            "crc32": "cec19742",
            "sha1": "ab6c6ba7737e68d2420a0617719c6d4c89039c45",
        },
        {
            "output_name": "024-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x100000}
            ],
            "size": 0x100000,
            "crc32": "efdfa063",
            "sha1": "e4609ecbcc1c820758f229da5145f51285b50555",
        },
        {
            "output_name": "024-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x100000, "size": 0x100000}
            ],
            "size": 0x100000,
            "crc32": "3c7997c0",
            "sha1": "8cb7e8e69892b19d318978370dbc510d51b06a69",
        },
        {
            "output_name": "024-c1.c1",
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
            "crc32": "3617c2dc",
            "sha1": "8de2643a618272f8aa1c705363edb007f4a5f5b7",
        },
        {
            "output_name": "024-c2.c2",
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
            "crc32": "3f0a7fd8",
            "sha1": "d0c9c7a9dde9ce175fb243d33ec11fa719d0158c",
        },
        {
            "output_name": "024-c3.c3",
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
            "crc32": "e9f745f8",
            "sha1": "bbe6141da28b0db7bf5cf321d69b7e613e2414d7",
        },
        {
            "output_name": "024-c4.c4",
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
            "crc32": "7382fefb",
            "sha1": "e916dec5bb5462eb9ae9711f08c7388937abb980",
        },
    ],
}
