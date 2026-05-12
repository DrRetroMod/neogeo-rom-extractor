"""
Top Hunter - Roddy & Cathy module.

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
    'id': 'tophuntr',
    'title': 'Top Hunter - Roddy & Cathy',
    'mame_set': 'tophuntr',
    'search_folder_names': [
        'Top Hunter',
        'Top Hunter - Roddy & Cathy',
        'tophuntr',
    ],
    'source_subfolders': [
        'Data/rom',
        'rom',
        'resources/game',
        '.',
    ],
    'required_source_files': [
        'p1.bin',
        's2.bin',
        'm1.bin',
        'v1.bin',
        'c1.bin',
    ],
    'notes': {
        'summary': 'Top Hunter uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.',
        'details': [
            "Converted from extract_tophuntr_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            'SHA1 values were added from the supplied MAME 0.287 DAT for machine tophuntr.',
            'The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.',
            'The old script located 046-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.',
            'Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.',
        ],
    },
    'outputs': [
        {
            'zip_name': 'tophuntr.zip',
            'set_name': 'tophuntr',
            'type': 'main',
            'description': 'MAME-compatible Top Hunter game set.',
            'files': [
                '046-p1.p1',
                '046-p2.sp2',
                '046-s1.s1',
                '046-m1.m1',
                '046-v1.v1',
                '046-v2.v2',
                '046-v3.v3',
                '046-v4.v4',
                '046-c1.c1',
                '046-c2.c2',
                '046-c3.c3',
                '046-c4.c4',
                '046-c5.c5',
                '046-c6.c6',
                '046-c7.c7',
                '046-c8.c8',
            ],
        },
    ],
    'files': [
        {
            'output_name': '046-p1.p1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'p1.bin',
                    'offset': 0x0000,
                    'size': 0x100000,
                },
                {
                    'type': 'patch_if_needed',
                    'description': 'Top Hunter P1 correction from old conditional extractor',
                    'file_offset': 0x0115,
                    'expected_old': '02',
                    'new': '00',
                },
            ],
            'size': 0x100000,
            'crc32': '69fa9e29',
            'sha1': '9a40a16163193bb506a32bd34f6323b25ec69622',
        },
        {
            'output_name': '046-p2.sp2',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'p1.bin',
                    'offset': 0x100000,
                    'size': 0x100000,
                },
            ],
            'size': 0x100000,
            'crc32': 'f182cb3e',
            'sha1': '6b4e0af5d4e623f0682f37ff5c69e5b705e20028',
        },
        {
            'output_name': '046-s1.s1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 's2.bin',
                    'offset': 0x0000,
                    'size': 0x020000,
                },
            ],
            'size': 0x020000,
            'crc32': '14b01d7b',
            'sha1': '618ce75c25d6cc86a3b46bd64a0aa34ab82f75ae',
        },
        {
            'output_name': '046-m1.m1',
            'operations': [
                {
                    'type': 'find_slice_by_crc32',
                    'source_file': 'm1.bin',
                    'offset_start': 0x0000,
                    'step': 0x010000,
                    'size': 0x020000,
                    'crc32': '3f84bb9f',
                    'fallback_offset': 0x0000,
                },
            ],
            'size': 0x020000,
            'crc32': '3f84bb9f',
            'sha1': '07446040871d11da3c2217ee9d1faf8c3cae7420',
        },
        {
            'output_name': '046-v1.v1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x0000,
                    'size': 0x100000,
                },
            ],
            'size': 0x100000,
            'crc32': 'c1f9c2db',
            'sha1': 'bed95a76afefa46503a12e0f0a9787c4c967ac50',
        },
        {
            'output_name': '046-v2.v2',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x100000,
                    'size': 0x100000,
                },
            ],
            'size': 0x100000,
            'crc32': '56254a64',
            'sha1': '1cf049cb4c414419859d2c8ee714317a35a85251',
        },
        {
            'output_name': '046-v3.v3',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x200000,
                    'size': 0x100000,
                },
            ],
            'size': 0x100000,
            'crc32': '58113fb1',
            'sha1': '40972982a63c7adecef840f9882f4165da723ab6',
        },
        {
            'output_name': '046-v4.v4',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x300000,
                    'size': 0x100000,
                },
            ],
            'size': 0x100000,
            'crc32': '4f54c187',
            'sha1': '63a76949301b83bdd44aa1a4462f642ab9ca3c0b',
        },
        {
            'output_name': '046-c1.c1',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0000,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': 'fa720a4a',
            'sha1': '364913b9fa40d46e4e39ae3cdae914cfd0de137d',
        },
        {
            'output_name': '046-c2.c2',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0000,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': 'c900c205',
            'sha1': '50274e79aa26f334eb806288688b30720bade883',
        },
        {
            'output_name': '046-c3.c3',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0001,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': '880e3c25',
            'sha1': 'b6974af0c833b766866919b6f15b6f8cef82530d',
        },
        {
            'output_name': '046-c4.c4',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0001,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': '7a2248aa',
            'sha1': '8af0b26025a54e3b91604dd24a3c1c518fbd8536',
        },
        {
            'output_name': '046-c5.c5',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0002,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': '4b735e45',
            'sha1': '2f8b46388c4696aee6a97e1e21cdadf6b142b01a',
        },
        {
            'output_name': '046-c6.c6',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0002,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': '273171df',
            'sha1': '9c35832221e016c12ef1ed71da167f565daaf86c',
        },
        {
            'output_name': '046-c7.c7',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'odd',
                            'index': 0x0003,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': '12829c4c',
            'sha1': 'ac5f3d848d7116fc35c97f53a72c85e049dd3a2f',
        },
        {
            'output_name': '046-c8.c8',
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
                    'chunk_size': 0x100000,
                    'chunks': [
                        {
                            'stream': 'even',
                            'index': 0x0003,
                        },
                    ],
                },
            ],
            'size': 0x100000,
            'crc32': 'c944e03d',
            'sha1': 'be23999b8ce09ee15ba500ce4d5e2a82a4f58d9b',
        },
    ],
}
