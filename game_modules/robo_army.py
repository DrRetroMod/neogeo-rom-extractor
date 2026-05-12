"""
Robo Army module.

Converted from extract_roboarmy_ngprime_conditional.py.
Game-specific details live here: source filenames, output filenames,
offsets, sizes, CRC32/SHA1 hashes, P1 patch rule, M1 CRC-scan rule,
and C-ROM chunk assembly order.
"""

NEOGEO_C1_TILE_DECODE = {
    "type": "neogeo_4bpp_tile_decode",
    "source_file": "c1.bin",
    "tile_size": 128,
    "row_offsets": [[4, 0], [4, 8], [0, 0], [0, 8]],
    "output_streams": {"odd": [0, 1], "even": [2, 3]},
}

GAME = {
    "id": "roboarmy",
    "title": "Robo Army",
    "mame_set": "roboarmy",

    "search_folder_names": ["Robo Army", "roboarmy"],
    "source_subfolders": ["Data/rom", "rom", "resources/game", "."],
    "required_source_files": ["p1.bin", "s2.bin", "m1.bin", "v1.bin", "c1.bin"],

    "notes": {
        "summary": "Robo Army uses a P1 correction if needed, M1 CRC scanning, and a module-declared NeoGeo 4bpp C-ROM transform.",
        "details": [
            "Converted from extract_roboarmy_ngprime_conditional.py without changing the old script's corrected-game offsets, sizes, CRC32s, output names, or ZIP name.",
            "SHA1 values were added from the supplied MAME 0.287 DAT for machine roboarmy.",
            "The old script changed byte 0x115 in the extracted P1 ROM to 0x00 if needed.",
            "The old script located 032-m1.m1 by scanning m1.bin in 0x10000-byte steps for the expected CRC32.",
            "Included Code Mystics BIOS extraction from the old script is intentionally not part of this MAME game module.",
        ],
    },

    "outputs": [{
        "zip_name": "roboarmy.zip",
        "set_name": "roboarmy",
        "type": "main",
        "description": "MAME-compatible Robo Army game set.",
        "files": ["032-p1.p1", "032-s1.s1", "032-m1.m1", "032-v1.v1", "032-v2.v2", "032-c1.c1", "032-c2.c2", "032-c3.c3", "032-c4.c4"],
    }],

    "files": [
        {"output_name": "032-p1.p1", "operations": [{"type": "slice", "source_file": "p1.bin", "offset": 0x000000, "size": 0x080000}, {"type": "patch_if_needed", "description": "Robo Army P1 correction from old conditional extractor", "file_offset": 0x115, "expected_old": "02", "new": "00"}], "size": 0x080000, "crc32": "cd11cbd4", "sha1": "23163e3da2f07e830a7f4a02aea1cb01a54ccbf3"},
        {"output_name": "032-s1.s1", "operations": [{"type": "slice", "source_file": "s2.bin", "offset": 0x000000, "size": 0x020000}], "size": 0x020000, "crc32": "ac0daa1b", "sha1": "93bae4697dc403fce19422752a514326ccf66a91"},
        {"output_name": "032-m1.m1", "operations": [{"type": "find_slice_by_crc32", "source_file": "m1.bin", "size": 0x020000, "step": 0x010000, "crc32": "35ec952d", "fallback_offset": 0x000000}], "size": 0x020000, "crc32": "35ec952d", "sha1": "8aed30e26d7e2c70dbce5de752df416091066f7b"},
        {"output_name": "032-v1.v1", "operations": [{"type": "slice", "source_file": "v1.bin", "offset": 0x000000, "size": 0x100000}], "size": 0x100000, "crc32": "63791533", "sha1": "4479e9308cdc906b9e03b985303f4ebedd00512f"},
        {"output_name": "032-v2.v2", "operations": [{"type": "slice", "source_file": "v1.bin", "offset": 0x100000, "size": 0x100000}], "size": 0x100000, "crc32": "eb95de70", "sha1": "b34885201116d2b3bbdee15ec7b5961cf5c069e1"},
        {"output_name": "032-c1.c1", "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "odd", "index": 0}]}], "size": 0x100000, "crc32": "97984c6c", "sha1": "deea59c0892f05dc7db98cb57b3eb83688dc57f0"},
        {"output_name": "032-c2.c2", "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x100000, "chunks": [{"stream": "even", "index": 0}]}], "size": 0x100000, "crc32": "65773122", "sha1": "2c0162a8e971e5e57933e4ae16040bf824ffdefe"},
        {"output_name": "032-c3.c3", "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "odd", "index": 2}]}], "size": 0x080000, "crc32": "40adfccd", "sha1": "b11f866dd70ba0ed9123424508355cb948b19bdc"},
        {"output_name": "032-c4.c4", "operations": [NEOGEO_C1_TILE_DECODE, {"type": "assemble_chunks", "chunk_size": 0x080000, "chunks": [{"stream": "even", "index": 2}]}], "size": 0x080000, "crc32": "462571de", "sha1": "5c3d610d492f91564423873b3b434dcda700373f"},
    ],
}
