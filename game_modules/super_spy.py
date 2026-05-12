"""
The Super Spy module.

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
    'id': 'superspy',
    'title': 'The Super Spy',
    'mame_set': 'superspy',
    'search_folder_names': [
        'The Super Spy',
        'Super Spy',
        'superspy',
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
        'summary': 'The Super Spy uses conditional P1 patching, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.',
        'details': [
            "Converted from extract_superspy_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            'SHA1 values were added from the supplied MAME 0.287 DAT for machine superspy.',
            'The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.',
            'The old script writes the P2 file as sp2.p2, not 011-p2.sp2.',
            'The old script located 011-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.',
            'Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.',
        ],
    },
    'outputs': [
        {
            'zip_name': 'superspy.zip',
            'set_name': 'superspy',
            'type': 'main',
            'description': 'MAME-compatible The Super Spy game set.',
            'files': [
                '011-p1.p1',
                'sp2.p2',
                '011-s1.s1',
                '011-m1.m1',
                '011-v11.v11',
                '011-v12.v12',
                '011-v21.v21',
                '011-c1.c1',
                '011-c2.c2',
                '011-c3.c3',
                '011-c4.c4',
            ],
        },
    ],
    'files': [
        {
            'output_name': '011-p1.p1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'p1.bin',
                    'offset': 0x0000,
                    'size': 0x080000,
                },
                {
                    'type': 'patch_if_needed',
                    'description': 'The Super Spy P1 correction from old conditional extractor',
                    'file_offset': 0x0115,
                    'expected_old': '02',
                    'new': '00',
                },
            ],
            'size': 0x080000,
            'crc32': 'c7f944b5',
            'sha1': 'da7560e09187c68f1d9f7656218497b4464c56c9',
        },
        {
            'output_name': 'sp2.p2',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'p1.bin',
                    'offset': 0x080000,
                    'size': 0x020000,
                },
            ],
            'size': 0x020000,
            'crc32': '811a4faf',
            'sha1': '8169dfaf79f52d80ecec402ce1b1ab9cafb7ebdd',
        },
        {
            'output_name': '011-s1.s1',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 's2.bin',
                    'offset': 0x0000,
                    'size': 0x020000,
                },
            ],
            'size': 0x020000,
            'crc32': 'ec5fdb96',
            'sha1': '8003028025ac7bf531e568add6ba66c02d0b7e84',
        },
        {
            'output_name': '011-m1.m1',
            'operations': [
                {
                    'type': 'find_slice_by_crc32',
                    'source_file': 'm1.bin',
                    'offset_start': 0x0000,
                    'step': 0x010000,
                    'size': 0x040000,
                    'crc32': 'ca661f1b',
                    'fallback_offset': 0x0000,
                },
            ],
            'size': 0x040000,
            'crc32': 'ca661f1b',
            'sha1': '4e3cb57db716ec48487c1b070c3a55a5faf40856',
        },
        {
            'output_name': '011-v11.v11',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x0000,
                    'size': 0x100000,
                },
            ],
            'size': 0x100000,
            'crc32': '5c674d5c',
            'sha1': 'd7b9beddeb247b584cea9ca6c43ec6869809b673',
        },
        {
            'output_name': '011-v12.v12',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x100000,
                    'size': 0x080000,
                },
            ],
            'size': 0x080000,
            'crc32': '9f513d5a',
            'sha1': '37b04962f0b8e2a74abd35c407337a6151dc4e95',
        },
        {
            'output_name': '011-v21.v21',
            'operations': [
                {
                    'type': 'slice',
                    'source_file': 'v1.bin',
                    'offset': 0x180000,
                    'size': 0x080000,
                },
            ],
            'size': 0x080000,
            'crc32': '426cd040',
            'sha1': 'b2b45189837c8287223c2b8bd4df9525b72a3f16',
        },
        {
            'output_name': '011-c1.c1',
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
            'crc32': 'cae7be57',
            'sha1': '43b35b349594535689c358d9f324adda55e5281a',
        },
        {
            'output_name': '011-c2.c2',
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
            'crc32': '9e29d986',
            'sha1': 'b417763bad1acf76116cd56f4203c2d2677e22e5',
        },
        {
            'output_name': '011-c3.c3',
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
            'crc32': '14832ff2',
            'sha1': '1179792d773d97d5e45e7d8f009051d362d72e24',
        },
        {
            'output_name': '011-c4.c4',
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
            'crc32': 'b7f63162',
            'sha1': '077a81b2bb0a8f17c9df6945078608f74432877a',
        },
    ],
}
