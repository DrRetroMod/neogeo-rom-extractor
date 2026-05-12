"""
Alpha Mission II / ASO II - Last Guardian module.

Converted from extract_alpham2_ngprime.py.

Source of extraction logic:
- old NGPrimeClaim-style Alpha Mission II extractor

Source of SHA1 values:
- MAME 0.287 DAT, machine alpham2

Game-specific details live here:
- source filenames
- output filenames
- offsets
- sizes
- CRC32/SHA1 hashes
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
    "id": "alpham2",
    "title": "Alpha Mission II / ASO II - Last Guardian",
    "mame_set": "alpham2",

    "search_folder_names": [
        "Alpha Mission II",
        "Alpha Mission 2",
        "ASO II",
        "ASO II - Last Guardian",
        "Alpha Mission II - ASO II - Last Guardian",
        "alpham2",
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
            "Alpha Mission II uses p1.bin/s2.bin/m1.bin/v1.bin slices and a "
            "module-declared NeoGeo 4bpp C-ROM transform from c1.bin."
        ),
        "details": [
            "Converted from extract_alpham2_ngprime.py without changing the old script's offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine alpham2.",
            "m1.bin is sliced from offset 0x10000 for 0x20000 bytes, matching the old extractor.",
            "p1.bin is split into 007-p1.p1 and 007-p2.p2, matching the old extractor.",
            "v1.bin is split into two 1 MiB V-ROM files, matching the old extractor.",
            "c1.bin is decoded using the module-declared NeoGeo 4bpp tile layout, then assembled into 007-c1.c1 through 007-c4.c4.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [
        {
            "zip_name": "alpham2.zip",
            "set_name": "alpham2",
            "type": "main",
            "description": "MAME-compatible Alpha Mission II / ASO II game set.",
            "files": [
                "007-p1.p1",
                "007-p2.p2",
                "007-s1.s1",
                "007-m1.m1",
                "007-v1.v1",
                "007-v2.v2",
                "007-c1.c1",
                "007-c2.c2",
                "007-c3.c3",
                "007-c4.c4",
            ],
        }
    ],

    "files": [
        {
            "output_name": "007-p1.p1",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x00000, "size": 0x80000},
            ],
            "size": 0x80000,
            "crc32": "5b266f47",
            "sha1": "8afbf995989f47ad93fea1f31a884afc7228b53a",
        },
        {
            "output_name": "007-p2.p2",
            "operations": [
                {"type": "slice", "source_file": "p1.bin", "offset": 0x80000, "size": 0x20000},
            ],
            "size": 0x20000,
            "crc32": "eb9c1044",
            "sha1": "65d3416dcd96663bc4e7cefe90ecb7c1eafb2dda",
        },
        {
            "output_name": "007-s1.s1",
            "operations": [
                {"type": "slice", "source_file": "s2.bin", "offset": 0x00000, "size": 0x20000},
            ],
            "size": 0x20000,
            "crc32": "85ec9acf",
            "sha1": "39a11974438ad36a2cc84307151b31474c3c5518",
        },
        {
            "output_name": "007-m1.m1",
            "operations": [
                {"type": "slice", "source_file": "m1.bin", "offset": 0x10000, "size": 0x20000},
            ],
            "size": 0x20000,
            "crc32": "28dfe2cd",
            "sha1": "1a1a99fb917c6c8db591e3be695ce03f843ee1df",
        },
        {
            "output_name": "007-v1.v1",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x100000},
            ],
            "size": 0x100000,
            "crc32": "cd5db931",
            "sha1": "b59f9f2df29f49470312a6cd20f5669b6aaf51ff",
        },
        {
            "output_name": "007-v2.v2",
            "operations": [
                {"type": "slice", "source_file": "v1.bin", "offset": 0x100000, "size": 0x100000},
            ],
            "size": 0x100000,
            "crc32": "63e9b574",
            "sha1": "1ade4cd0b15c84dd4a0fb7f7abf0885eef3a3f71",
        },
        {
            "output_name": "007-c1.c1",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 0}]},
            ],
            "size": 0x100000,
            "crc32": "8fba8ff3",
            "sha1": "1a682292e99eb91b0edb9771c44bc5e762867e98",
        },
        {
            "output_name": "007-c2.c2",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 0}]},
            ],
            "size": 0x100000,
            "crc32": "4dad2945",
            "sha1": "ac85a146276537fed124bda892bb93ff549f1d93",
        },
        {
            "output_name": "007-c3.c3",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x80000, "chunks": [{"stream": "odd", "index": 2}]},
            ],
            "size": 0x80000,
            "crc32": "68c2994e",
            "sha1": "4f8dfc6e5188942e03b853a2c9f0ea6138dec791",
        },
        {
            "output_name": "007-c4.c4",
            "operations": [
                NEOGEO_C1_TILE_DECODE,
                {"type": "assemble_chunks", "chunk_size": 0x80000, "chunks": [{"stream": "even", "index": 2}]},
            ],
            "size": 0x80000,
            "crc32": "7d588349",
            "sha1": "a5ed789d7bbc25be5c5b2d99883b64d379c103a2",
        },
    ],
}
