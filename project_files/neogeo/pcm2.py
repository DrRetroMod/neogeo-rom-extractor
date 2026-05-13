#!/usr/bin/env python3

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
Neo Geo PCM2 V-ROM transform helpers.

This is a small Python port of the PCM2 address/data transforms from the
uploaded MAME-derived neo-cmc source. The original source files carried
BSD-3-Clause notices from MAME contributors S. Smith, David Haywood, and
Fabio Priuli. Preserve those credits in the project NOTICE/credits.
"""

# Implementation notes:
# This module implements Neo Geo processing behaviour researched through
# public Neo Geo tooling, emulator documentation, and related extraction
# workflows.
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

from __future__ import annotations


def _validate_pcm2(data: bytes | bytearray, value: int) -> None:
    if value <= 0 or value % 4 != 0:
        raise ValueError(f"PCM2 value must be a positive multiple of 4; got {value}")
    if len(data) % 2 != 0:
        raise ValueError(f"PCM2 data size must be even; got 0x{len(data):X}")


def pcm2_encrypt(data: bytes | bytearray, *, value: int) -> bytes:
    """
    PCM2 encrypt transform used by Metal Slug 4 V-ROM data.

    Metal Slug 4 uses value=8.
    """
    _validate_pcm2(data, value)
    out = bytearray(data)
    words_per_block = value // 2
    xor_words = value // 4

    for byte_base in range(0, len(out), value):
        block = out[byte_base:byte_base + value]
        if len(block) < value:
            break

        words = [bytes(block[i:i + 2]) for i in range(0, value, 2)]
        new_words = [b"\x00\x00"] * words_per_block

        for j in range(words_per_block):
            new_words[j ^ xor_words] = words[j]

        out[byte_base:byte_base + value] = b"".join(new_words)

    return bytes(out)


def pcm2_decrypt(data: bytes | bytearray, *, value: int) -> bytes:
    """
    Inverse of pcm2_encrypt().
    """
    _validate_pcm2(data, value)
    out = bytearray(data)
    words_per_block = value // 2
    xor_words = value // 4

    for byte_base in range(0, len(out), value):
        block = out[byte_base:byte_base + value]
        if len(block) < value:
            break

        words = [bytes(block[i:i + 2]) for i in range(0, value, 2)]
        new_words = [b"\x00\x00"] * words_per_block

        for j in range(words_per_block):
            new_words[j] = words[j ^ xor_words]

        out[byte_base:byte_base + value] = b"".join(new_words)

    return bytes(out)


def _bitswap(value: int, width: int, *order: int) -> int:
    if len(order) != width:
        raise ValueError(f"bitswap order width mismatch: expected {width}, got {len(order)}")
    out = 0
    for bit in order:
        out = (out << 1) | ((value >> bit) & 1)
    return out


_PCM2_SWAP_ADDRS = (
    (0x000000, 0xA5000),
    (0xFFCE20, 0x01000),
    (0xFE2CF6, 0x4E001),
    (0xFFAC28, 0xC2000),
    (0xFEB2C0, 0x0A000),
    (0xFF14EA, 0xA7001),
    (0xFFB440, 0x02000),
)

_PCM2_SWAP_XOR = (
    (0xF9, 0xE0, 0x5D, 0xF3, 0xEA, 0x92, 0xBE, 0xEF),
    (0xC4, 0x83, 0xA8, 0x5F, 0x21, 0x27, 0x64, 0xAF),
    (0xC3, 0xFD, 0x81, 0xAC, 0x6D, 0xE7, 0xBF, 0x9E),
    (0xC3, 0xFD, 0x81, 0xAC, 0x6D, 0xE7, 0xBF, 0x9E),
    (0xCB, 0x29, 0x7D, 0x43, 0xD2, 0x3A, 0xC2, 0xB4),
    (0x4B, 0xA4, 0x63, 0x46, 0xF0, 0x91, 0xEA, 0x62),
    (0x4B, 0xA4, 0x63, 0x46, 0xF0, 0x91, 0xEA, 0x62),
)


def pcm2_swap(data: bytes | bytearray, *, value: int) -> bytes:
    """
    Later PCM2 swap transform used by some titles, including KOF2003 with value=5.

    This mirrors pcm2_prot_device::swap(). It operates on the first 0x1000000
    bytes, matching the original helper behaviour.
    """
    if not 0 <= value < len(_PCM2_SWAP_ADDRS):
        raise ValueError(f"PCM2 swap value out of range: {value}")
    if len(data) < 0x1000000:
        raise ValueError(f"PCM2 swap requires at least 0x1000000 bytes; got 0x{len(data):X}")

    out = bytearray(data)
    buf = bytes(out[:0x1000000])
    addr_add, addr_xor = _PCM2_SWAP_ADDRS[value]
    xor_table = _PCM2_SWAP_XOR[value]

    for i in range(0x1000000):
        j = _bitswap(i, 24, 23, 22, 21, 20, 19, 18, 17, 0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16)
        j ^= addr_xor
        d = (i + addr_add) & 0xFFFFFF
        out[j] = buf[d] ^ xor_table[j & 0x07]

    return bytes(out)


def pcm2_unswap(data: bytes | bytearray, *, value: int) -> bytes:
    """
    Inverse of pcm2_swap().
    """
    if not 0 <= value < len(_PCM2_SWAP_ADDRS):
        raise ValueError(f"PCM2 swap value out of range: {value}")
    if len(data) < 0x1000000:
        raise ValueError(f"PCM2 unswap requires at least 0x1000000 bytes; got 0x{len(data):X}")

    out = bytearray(data)
    buf = bytes(out[:0x1000000])
    addr_add, addr_xor = _PCM2_SWAP_ADDRS[value]
    xor_table = _PCM2_SWAP_XOR[value]

    for i in range(0x1000000):
        j = _bitswap(i, 24, 23, 22, 21, 20, 19, 18, 17, 0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16)
        j ^= addr_xor
        d = (i + addr_add) & 0xFFFFFF
        out[d] = buf[j] ^ xor_table[j & 0x07]

    return bytes(out)
