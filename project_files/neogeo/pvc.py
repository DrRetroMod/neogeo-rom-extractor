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
Neo Geo PVC P-ROM helpers used by KOF2003.

This is a Python-side helper for the NeoGeo ROM Extractor. It mirrors the
KOF2003 P-ROM transform behaviour used by the MAME-derived PVC protection code.

Original reference files used for this helper:
  prot_pvc.cpp
  prot_pvc.h

The original uploaded reference source carried BSD-3-Clause notices from MAME.
Keep appropriate attribution in the project NOTICE/credits.
"""

# Implementation notes:
# This module implements Neo Geo processing behaviour researched through
# public Neo Geo tooling, emulator documentation, and related extraction
# workflows.
#
# See README.md -> Credits and Acknowledgements for full project-wide credits.

from __future__ import annotations


KOF2003_XOR1 = bytes([
    0x3B, 0x6A, 0xF7, 0xB7, 0xE8, 0xA9, 0x20, 0x99,
    0x9F, 0x39, 0x34, 0x0C, 0xC3, 0x9A, 0xA5, 0xC8,
    0xB8, 0x18, 0xCE, 0x56, 0x94, 0x44, 0xE3, 0x7A,
    0xF7, 0xDD, 0x42, 0xF0, 0x18, 0x60, 0x92, 0x9F,
])

KOF2003_XOR2 = bytes([
    0x2F, 0x02, 0x60, 0xBB, 0x77, 0x01, 0x30, 0x08,
    0xD8, 0x01, 0xA0, 0xDF, 0x37, 0x0A, 0xF0, 0x65,
    0x28, 0x03, 0xD0, 0x23, 0xD3, 0x03, 0x70, 0x42,
    0xBB, 0x06, 0xF0, 0x28, 0xBA, 0x0F, 0xF0, 0x7A,
])


def _bitswap(value: int, *bits: int) -> int:
    out = 0
    for bit in bits:
        out = (out << 1) | ((value >> bit) & 1)
    return out


def _check_min_size(data: bytes | bytearray, minimum: int, label: str) -> None:
    if len(data) < minimum:
        raise ValueError(f"{label} must be at least 0x{minimum:X} bytes; got 0x{len(data):X}")


def kof2003_p_decrypt(data: bytes) -> bytes:
    """
    Decrypt KOF2003 P-ROM data.

    Mirrors pvc_prot_device::kof2003_decrypt_68k().

    Input size expected by the original routine: at least 0x900000 bytes.
    Output size: 0x800000 bytes.
    """
    _check_min_size(data, 0x900000, "KOF2003 encrypted P data")

    rom = bytearray(data[:0x900000])
    buf = bytearray(0x900000)

    for i in range(0x100000):
        rom[0x800000 + i] ^= rom[0x100002 | i]

    for i in range(0x100000):
        rom[i] ^= KOF2003_XOR1[i % 0x20]

    for i in range(0x100000, 0x800000):
        rom[i] ^= KOF2003_XOR2[i % 0x20]

    for i in range(0x100000, 0x800000, 4):
        rom16 = rom[i + 1] | (rom[i + 2] << 8)
        rom16 = _bitswap(rom16, 15, 14, 13, 12, 5, 4, 7, 6, 9, 8, 11, 10, 3, 2, 1, 0)
        rom[i + 1] = rom16 & 0xFF
        rom[i + 2] = (rom16 >> 8) & 0xFF

    for i in range(0x0100000 // 0x10000):
        ofst = (i & 0xF0) + _bitswap(i & 0x0F, 7, 6, 5, 4, 0, 1, 2, 3)
        buf[i * 0x10000:(i + 1) * 0x10000] = rom[ofst * 0x10000:(ofst + 1) * 0x10000]

    for i in range(0x100000, 0x900000, 0x100):
        ofst = (
            (i & 0xF000FF)
            + ((i & 0x000F00) ^ 0x00800)
            + (_bitswap((i & 0x0FF000) >> 12, 4, 5, 6, 7, 1, 0, 3, 2) << 12)
        )
        buf[i:i + 0x100] = rom[ofst:ofst + 0x100]

    rom[0x000000:0x100000] = buf[0x000000:0x100000]
    rom[0x100000:0x200000] = buf[0x800000:0x900000]
    rom[0x200000:0x900000] = buf[0x100000:0x800000]

    return bytes(rom[:0x800000])


def kof2003_p_encrypt(data: bytes) -> bytes:
    """
    Encrypt KOF2003 P-ROM data.

    Mirrors pvc_prot_device::kof2003_encrypt_68k().

    Input size expected by the original routine: at least 0x800000 bytes.
    Output size: 0x900000 bytes.
    """
    _check_min_size(data, 0x800000, "KOF2003 decrypted P data")

    rom = bytearray(0x900000)
    buf = bytearray(0x900000)

    buf[0:0x800000] = data[:0x800000]
    buf[0x800000:0x900000] = b"\xFF" * 0x100000

    rom[0x000000:0x100000] = buf[0x000000:0x100000]
    rom[0x800000:0x900000] = buf[0x100000:0x200000]
    rom[0x100000:0x800000] = buf[0x200000:0x900000]

    for i in range(0x100000, 0x900000, 0x100):
        ofst = (
            (i & 0xF000FF)
            + ((i & 0x000F00) ^ 0x00800)
            + (_bitswap((i & 0x0FF000) >> 12, 4, 5, 6, 7, 1, 0, 3, 2) << 12)
        )
        buf[i:i + 0x100] = rom[ofst:ofst + 0x100]

    for i in range(0x0100000 // 0x10000):
        ofst = (i & 0xF0) + _bitswap(i & 0x0F, 7, 6, 5, 4, 0, 1, 2, 3)
        buf[i * 0x10000:(i + 1) * 0x10000] = rom[ofst * 0x10000:(ofst + 1) * 0x10000]

    rom[:] = buf

    for i in range(0x100000, 0x800000, 4):
        rom16 = rom[i + 1] | (rom[i + 2] << 8)
        rom16 = _bitswap(rom16, 15, 14, 13, 12, 5, 4, 7, 6, 9, 8, 11, 10, 3, 2, 1, 0)
        rom[i + 1] = rom16 & 0xFF
        rom[i + 2] = (rom16 >> 8) & 0xFF

    for i in range(0x100000):
        rom[i] ^= KOF2003_XOR1[i % 0x20]

    for i in range(0x100000, 0x800000):
        rom[i] ^= KOF2003_XOR2[i % 0x20]

    for i in range(0x100000):
        rom[0x800000 + i] ^= rom[0x100002 | i]

    return bytes(rom[:0x900000])