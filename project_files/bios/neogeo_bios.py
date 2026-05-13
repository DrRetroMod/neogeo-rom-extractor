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
Neo Geo BIOS collector for the NeoGeo ROM Extractor.

Current behaviour:
- scan a game's source folder after that individual game extraction completes
- match raw files by size + CRC32 + SHA1 against MAME's neogeo.zip BIOS entries
- detect Dotemu-style files containing "bios_sfix" in the filename
- re-encode matching bios_sfix files into standard sfix.sfix layout
- copy every confirmed match into that game's output/bios/unzipped folder
- rebuild that game's output/bios/neogeo.zip every run from output/bios/unzipped
- optionally maintain a shared master bios/unzipped folder
- add only newly discovered files to the master bios/unzipped folder
- rebuild master bios/neogeo.zip only when a new master BIOS file was added
- detect selected non-standard extra BIOS files such as sp_4s.bin
- copy non-standard extra BIOS files into bios/non_standard_extra_bios/unzipped
- create neogeo_with_non_standard_extra_bios.zip only when non-standard extra BIOS files are present
- include confirmed standard BIOS files plus non-standard extra BIOS files in that extra ZIP
- ignore other non-matching files

No slicing, patching, or speculative BIOS handling is performed here.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import zlib
import zipfile
from dataclasses import dataclass
from pathlib import Path


NEOGEO_BIOS_ZIP_NAME = "neogeo.zip"
NEOGEO_EXTRA_BIOS_ZIP_NAME = "neogeo_with_non_standard_extra_bios.zip"

NON_STANDARD_EXTRA_BIOS_FILES = {
    "sp_4s.bin",
}

# Unique ROM entries from the uploaded MAME_BIOS_287.dat machine name="neogeo".
# The DAT contains 35 entries, but sm1.sm1 is duplicated, so this table has 34 unique files.
NEOGEO_BIOS_FILES = {
    "sp-s2.sp1": {"size": 131072, "crc32": "9036d879", "sha1": "4f5ed7105b7128794654ce82b51723e16e389543"},
    "sp-s.sp1": {"size": 131072, "crc32": "c7f2fa45", "sha1": "09576ff20b4d6b365e78e6a5698ea450262697cd"},
    "sp-45.sp1": {"size": 524288, "crc32": "03cc9f6a", "sha1": "cdf1f49e3ff2bac528c21ed28449cf35b7957dc1"},
    "sp-s3.sp1": {"size": 131072, "crc32": "91b64be3", "sha1": "720a3e20d26818632aedf2c2fd16c54f213543e1"},
    "sp-u2.sp1": {"size": 131072, "crc32": "e72943de", "sha1": "5c6bba07d2ec8ac95776aa3511109f5e1e2e92eb"},
    "sp-e.sp1": {"size": 131072, "crc32": "2723a5b5", "sha1": "5dbff7531cf04886cde3ef022fb5ca687573dcb8"},
    "sp1-u2": {"size": 131072, "crc32": "62f021f4", "sha1": "62d372269e1b3161c64ae21123655a0a22ffd1bb"},
    "sp1-u4.bin": {"size": 131072, "crc32": "1179a30f", "sha1": "866817f47aa84d903d0b819d61f6ef356893d16a"},
    "sp1-u3.bin": {"size": 131072, "crc32": "2025b7a2", "sha1": "73d774746196f377111cd7aa051cc8bb5dd948b3"},
    "vs-bios.rom": {"size": 131072, "crc32": "f0e8f27d", "sha1": "ecf01eda815909f1facec62abf3594eaa8d11075"},
    "sp-j2.sp1": {"size": 131072, "crc32": "acede59c", "sha1": "b6f97acd282fd7e94d9426078a90f059b5e9dd91"},
    "sp1.jipan.1024": {"size": 131072, "crc32": "9fb0abe4", "sha1": "18a987ce2229df79a8cf6a84f968f0e42ce4e59d"},
    "japan-j3.bin": {"size": 131072, "crc32": "dff6d41f", "sha1": "e92910e20092577a4523a6b39d578a71d4de7085"},
    "sp1-j3.bin": {"size": 131072, "crc32": "fbc6d469", "sha1": "46b2b409b5b68869e367b40c846373623edb632a"},
    "sp-j3.sp1": {"size": 524288, "crc32": "486cb450", "sha1": "52c21ea817928904b80745a8c8d15cbad61e1dc1"},
    "sp-1v1_3db8c.bin": {"size": 131072, "crc32": "162f0ebe", "sha1": "fe1c6dd3dfcf97d960065b1bb46c1e11cb7bf271"},
    "uni-bios_4_0.rom": {"size": 131072, "crc32": "a7aab458", "sha1": "938a0bda7d9a357240718c2cec319878d36b8f72"},
    "uni-bios_3_3.rom": {"size": 131072, "crc32": "24858466", "sha1": "0ad92efb0c2338426635e0159d1f60b4473d0785"},
    "uni-bios_3_2.rom": {"size": 131072, "crc32": "a4e8b9b3", "sha1": "c92f18c3f1edda543d264ecd0ea915240e7c8258"},
    "uni-bios_3_1.rom": {"size": 131072, "crc32": "0c58093f", "sha1": "29329a3448c2505e1ff45ffa75e61e9693165153"},
    "uni-bios_3_0.rom": {"size": 131072, "crc32": "a97c89a9", "sha1": "97a5eff3b119062f10e31ad6f04fe4b90d366e7f"},
    "uni-bios_2_3.rom": {"size": 131072, "crc32": "27664eb5", "sha1": "5b02900a3ccf3df168bdcfc98458136fd2b92ac0"},
    "uni-bios_2_3o.rom": {"size": 131072, "crc32": "601720ae", "sha1": "1b8a72c720cdb5ee3f1d735bbcf447b09204b8d9"},
    "uni-bios_2_2.rom": {"size": 131072, "crc32": "2d50996a", "sha1": "5241a4fb0c63b1a23fd1da8efa9c9a9bd3b4279c"},
    "uni-bios_2_1.rom": {"size": 131072, "crc32": "8dabf76b", "sha1": "c23732c4491d966cf0373c65c83c7a4e88f0082c"},
    "uni-bios_2_0.rom": {"size": 131072, "crc32": "0c12c2ad", "sha1": "37bcd4d30f3892078b46841d895a6eff16dc921e"},
    "uni-bios_1_3.rom": {"size": 131072, "crc32": "b24b44a0", "sha1": "eca8851d30557b97c309a0d9f4a9d20e5b14af4e"},
    "uni-bios_1_2.rom": {"size": 131072, "crc32": "4fa698e9", "sha1": "682e13ec1c42beaa2d04473967840c88fd52c75a"},
    "uni-bios_1_2o.rom": {"size": 131072, "crc32": "e19d3ce9", "sha1": "af88ef837f44a3af2d7144bb46a37c8512b67770"},
    "uni-bios_1_1.rom": {"size": 131072, "crc32": "5dda0d84", "sha1": "4153d533c02926a2577e49c32657214781ff29b7"},
    "uni-bios_1_0.rom": {"size": 131072, "crc32": "0ce453a0", "sha1": "3b4c0cd26c176fc6b26c3a2f95143dd478f6abf9"},
    "sm1.sm1": {"size": 131072, "crc32": "94416d67", "sha1": "42f9d7ddd6c0931fd64226a60dc73602b2819dcf"},
    "000-lo.lo": {"size": 131072, "crc32": "5a86cff2", "sha1": "5992277debadeb64d1c1c64b0a92d9293eaf7e4a"},
    "sfix.sfix": {"size": 131072, "crc32": "c2ea0cfd", "sha1": "fd4a618cdcdbf849374f0a50dd8efe9dbab706c3"},
}


@dataclass(frozen=True)
class BiosMatch:
    source_path: Path
    output_name: str
    size: int
    crc32: str
    sha1: str
    data: bytes | None = None


@dataclass(frozen=True)
class BiosCollectResult:
    matches: list[BiosMatch]
    game_new_files: list[str]
    game_replaced_files: list[str]
    game_skipped_existing: list[str]
    game_conflicts: list[str]
    game_zip_rebuilt: bool
    game_extra_new_files: list[str]
    game_extra_skipped_existing: list[str]
    game_extra_zip_rebuilt: bool
    master_new_files: list[str]
    master_skipped_existing: list[str]
    master_conflicts: list[str]
    master_zip_rebuilt: bool
    master_extra_new_files: list[str]
    master_extra_skipped_existing: list[str]
    master_extra_zip_rebuilt: bool


def _file_hashes(path: Path) -> tuple[int, str, str]:
    """Return (size, crc32_hex, sha1_hex) for path."""
    crc = 0
    sha1 = hashlib.sha1()
    size = 0

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            size += len(chunk)
            crc = zlib.crc32(chunk, crc)
            sha1.update(chunk)

    return size, f"{crc & 0xFFFFFFFF:08x}", sha1.hexdigest()

def _data_hashes(data: bytes) -> tuple[int, str, str]:
    return (
        len(data),
        f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        hashlib.sha1(data).hexdigest(),
    )


def dotemu_sfix_reencode_source_bytes(data: bytes) -> bytes:
    if len(data) % 32 != 0:
        raise ValueError(
            f"Dotemu SFIX source size must be divisible by 32, got {len(data)}"
        )

    output = bytearray()
    buffer = bytearray(32)

    for i in range(0, len(data), 32):
        for j in range(0, 8):
            buffer[0 + j] = data[i + j * 4 + 2]
            buffer[8 + j] = data[i + j * 4 + 3]
            buffer[16 + j] = data[i + j * 4]
            buffer[24 + j] = data[i + j * 4 + 1]

        output.extend(buffer)

    return bytes(output)


def _try_bios_sfix_reencode(path: Path) -> BiosMatch | None:
    if "bios_sfix" not in path.name.lower():
        return None

    try:
        source_data = path.read_bytes()
        reencoded = dotemu_sfix_reencode_source_bytes(source_data)
    except ValueError:
        return None

    size, crc32, sha1 = _data_hashes(reencoded)
    expected = NEOGEO_BIOS_FILES["sfix.sfix"]

    if (
        size == int(expected["size"])
        and crc32 == str(expected["crc32"]).lower()
        and sha1 == str(expected["sha1"]).lower()
    ):
        return BiosMatch(
            source_path=path,
            output_name="sfix.sfix",
            size=size,
            crc32=crc32,
            sha1=sha1,
            data=reencoded,
        )

    return None

def _build_lookup() -> dict[tuple[int, str, str], str]:
    """Map (size, crc32, sha1) to the correct neogeo.zip member filename."""
    lookup: dict[tuple[int, str, str], str] = {}
    for output_name, meta in NEOGEO_BIOS_FILES.items():
        key = (int(meta["size"]), str(meta["crc32"]).lower(), str(meta["sha1"]).lower())
        lookup[key] = output_name
    return lookup


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _same_confirmed_bios(path: Path, bios_name: str) -> bool:
    """Return True if path currently contains the expected confirmed BIOS data for bios_name."""
    if not path.is_file():
        return False
    expected = NEOGEO_BIOS_FILES[bios_name]
    size, crc32, sha1 = _file_hashes(path)
    return (
        size == int(expected["size"])
        and crc32 == str(expected["crc32"]).lower()
        and sha1 == str(expected["sha1"]).lower()
    )


def scan_for_neogeo_bios(
    scan_root: str | os.PathLike[str],
    *skip_dirs: str | os.PathLike[str] | None,
) -> list[BiosMatch]:
    """
    Scan scan_root recursively and return confirmed neogeo.zip BIOS matches.

    Any skip_dirs provided are ignored, so repeated runs do not scan their own output folders.
    """
    root = Path(scan_root).resolve()
    resolved_skip_dirs = [Path(d).resolve() for d in skip_dirs if d is not None]
    lookup = _build_lookup()
    matches_by_name: dict[str, BiosMatch] = {}

    if not root.exists():
        return []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(_is_inside(path, skip_dir) for skip_dir in resolved_skip_dirs):
            continue

        # Avoid treating zipped output as a raw BIOS file.
        if path.name.lower() == NEOGEO_BIOS_ZIP_NAME:
            continue

        sfix_match = _try_bios_sfix_reencode(path)
        if sfix_match is not None:
            matches_by_name.setdefault("sfix.sfix", sfix_match)
            continue

        size, crc32, sha1 = _file_hashes(path)
        output_name = lookup.get((size, crc32, sha1))
        if not output_name:
            continue

        # Deduplicate by final MAME BIOS filename. First valid source wins.
        matches_by_name.setdefault(
            output_name,
            BiosMatch(
                source_path=path,
                output_name=output_name,
                size=size,
                crc32=crc32,
                sha1=sha1,
            ),
        )

    return [matches_by_name[name] for name in sorted(matches_by_name)]


def rebuild_neogeo_zip(bios_output_dir: str | os.PathLike[str]) -> Path | None:
    """
    Rebuild bios/neogeo.zip from confirmed loose BIOS files in bios/unzipped.

    Returns the zip path if at least one BIOS file is present, otherwise None.
    """
    bios_dir = Path(bios_output_dir)
    loose_bios_dir = bios_dir / "unzipped"

    present_files = [
        name
        for name in sorted(NEOGEO_BIOS_FILES)
        if (loose_bios_dir / name).is_file()
        and _same_confirmed_bios(loose_bios_dir / name, name)
    ]

    zip_path = bios_dir / NEOGEO_BIOS_ZIP_NAME

    if not present_files:
        if zip_path.exists():
            zip_path.unlink()
        return None

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as zf:
        for name in present_files:
            zf.write(loose_bios_dir / name, arcname=name)

    return zip_path

def scan_for_non_standard_extra_bios(
    scan_root: str | os.PathLike[str],
    *skip_dirs: str | os.PathLike[str] | None,
) -> list[Path]:
    root = Path(scan_root).resolve()
    resolved_skip_dirs = [Path(d).resolve() for d in skip_dirs if d is not None]
    matches_by_name: dict[str, Path] = {}

    if not root.exists():
        return []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(_is_inside(path, skip_dir) for skip_dir in resolved_skip_dirs):
            continue

        name = path.name.lower()

        if name in NON_STANDARD_EXTRA_BIOS_FILES:
            matches_by_name.setdefault(name, path)

    return [matches_by_name[name] for name in sorted(matches_by_name)]


def _copy_extra_bios_files(
    extra_paths: list[Path],
    bios_dir: Path,
) -> tuple[list[str], list[str]]:
    extra_unzipped_dir = bios_dir / "non_standard_extra_bios" / "unzipped"
    extra_unzipped_dir.mkdir(parents=True, exist_ok=True)

    new_files: list[str] = []
    skipped_existing: list[str] = []

    for source_path in extra_paths:
        destination = extra_unzipped_dir / source_path.name

        if destination.exists():
            source_size, source_crc32, source_sha1 = _file_hashes(source_path)
            dest_size, dest_crc32, dest_sha1 = _file_hashes(destination)

            if (
                source_size == dest_size
                and source_crc32 == dest_crc32
                and source_sha1 == dest_sha1
            ):
                skipped_existing.append(source_path.name)
                continue

        shutil.copy2(source_path, destination)
        new_files.append(source_path.name)

    return new_files, skipped_existing


def rebuild_neogeo_extra_zip(bios_output_dir: str | os.PathLike[str]) -> Path | None:
    bios_dir = Path(bios_output_dir)
    loose_bios_dir = bios_dir / "unzipped"
    extra_unzipped_dir = bios_dir / "non_standard_extra_bios" / "unzipped"
    zip_path = bios_dir / NEOGEO_EXTRA_BIOS_ZIP_NAME

    standard_files = [
        name
        for name in sorted(NEOGEO_BIOS_FILES)
        if (loose_bios_dir / name).is_file()
        and _same_confirmed_bios(loose_bios_dir / name, name)
    ]

    extra_files = [
        path
        for path in sorted(extra_unzipped_dir.glob("*"))
        if path.is_file()
    ]

    if not extra_files:
        if zip_path.exists():
            zip_path.unlink()
        return None

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as zf:
        for name in standard_files:
            zf.write(loose_bios_dir / name, arcname=name)

        for path in extra_files:
            zf.write(path, arcname=path.name)

    return zip_path

def _write_or_copy_match(match: BiosMatch, destination: Path) -> None:
    if match.data is not None:
        destination.write_bytes(match.data)
    else:
        shutil.copy2(match.source_path, destination)

def _copy_matches_to_game_bios(
    matches: list[BiosMatch],
    game_bios_dir: Path,
) -> tuple[list[str], list[str], list[str], list[str]]:
    """
    Copy all confirmed matches into the per-game BIOS folder.

    Per-game output should reflect what this game/source provided. If the same confirmed
    BIOS file is already present, it is skipped. If a same-named bad/conflicting file is
    present, it is replaced by the confirmed match and recorded.
    """
    game_new_files: list[str] = []
    game_replaced_files: list[str] = []
    game_skipped_existing: list[str] = []
    game_conflicts: list[str] = []

    game_loose_bios_dir = game_bios_dir / "unzipped"
    game_loose_bios_dir.mkdir(parents=True, exist_ok=True)

    for match in matches:
        destination = game_loose_bios_dir / match.output_name
        if destination.exists():
            if _same_confirmed_bios(destination, match.output_name):
                game_skipped_existing.append(match.output_name)
                continue
            game_conflicts.append(match.output_name)
            _write_or_copy_match(match, destination)
            game_replaced_files.append(match.output_name)
            continue

        _write_or_copy_match(match, destination)
        game_new_files.append(match.output_name)

    return game_new_files, game_replaced_files, game_skipped_existing, game_conflicts


def _copy_matches_to_master_bios(
    matches: list[BiosMatch],
    master_bios_dir: Path,
) -> tuple[list[str], list[str], list[str]]:
    """
    Copy only newly discovered confirmed matches into the master BIOS folder.

    The master folder accumulates files over many game runs. Existing confirmed files are
    skipped. Same-name conflicts are not overwritten.
    """
    master_new_files: list[str] = []
    master_skipped_existing: list[str] = []
    master_conflicts: list[str] = []

    master_loose_bios_dir = master_bios_dir / "unzipped"
    master_loose_bios_dir.mkdir(parents=True, exist_ok=True)

    for match in matches:
        destination = master_loose_bios_dir / match.output_name
        if destination.exists():
            if _same_confirmed_bios(destination, match.output_name):
                master_skipped_existing.append(match.output_name)
            else:
                master_conflicts.append(match.output_name)
            continue

        _write_or_copy_match(match, destination)
        master_new_files.append(match.output_name)

    return master_new_files, master_skipped_existing, master_conflicts


def collect_neogeo_bios(
    scan_root: str | os.PathLike[str],
    game_bios_output_dir: str | os.PathLike[str],
    master_bios_output_dir: str | os.PathLike[str] | None = None,
    *,
    verbose: bool = True,
) -> BiosCollectResult:
    """
    Collect confirmed raw Neo Geo BIOS files after one individual game extraction.

    Per-game behaviour:
      - copy every confirmed BIOS file found from scan_root into game_bios_output_dir
      - rebuild game_bios_output_dir/neogeo.zip every run

    Master behaviour, if master_bios_output_dir is provided:
      - copy only confirmed BIOS files not already present in the master folder
      - rebuild master_bios_output_dir/neogeo.zip only if at least one new file was added
      - do not overwrite same-name conflicts

    Non-matching files are ignored. Code Mystics-only candidates are intentionally ignored
    in this phase unless they match the confirmed DAT hashes in NEOGEO_BIOS_FILES.
    """
    game_bios_dir = Path(game_bios_output_dir)
    master_bios_dir = Path(master_bios_output_dir) if master_bios_output_dir is not None else None

    matches = scan_for_neogeo_bios(scan_root, game_bios_dir, master_bios_dir)

    extra_paths = scan_for_non_standard_extra_bios(scan_root, game_bios_dir, master_bios_dir)

    game_new_files, game_replaced_files, game_skipped_existing, game_conflicts = _copy_matches_to_game_bios(
        matches,
        game_bios_dir,
    )
    game_zip_path = rebuild_neogeo_zip(game_bios_dir)
    game_zip_rebuilt = game_zip_path is not None

    game_extra_new_files, game_extra_skipped_existing = _copy_extra_bios_files(
        extra_paths,
        game_bios_dir,
    )
    game_extra_zip_path = rebuild_neogeo_extra_zip(game_bios_dir)
    game_extra_zip_rebuilt = game_extra_zip_path is not None

    master_new_files: list[str] = []
    master_skipped_existing: list[str] = []
    master_conflicts: list[str] = []
    master_zip_rebuilt = False
    master_extra_new_files: list[str] = []
    master_extra_skipped_existing: list[str] = []
    master_extra_zip_rebuilt = False

    if master_bios_dir is not None:
        master_new_files, master_skipped_existing, master_conflicts = _copy_matches_to_master_bios(matches, master_bios_dir)

        master_extra_new_files, master_extra_skipped_existing = _copy_extra_bios_files(
            extra_paths,
            master_bios_dir,
        )

        if master_new_files:
            master_zip_path = rebuild_neogeo_zip(master_bios_dir)
            master_zip_rebuilt = master_zip_path is not None

        if master_new_files or master_extra_new_files:
            master_extra_zip_path = rebuild_neogeo_extra_zip(master_bios_dir)
            master_extra_zip_rebuilt = master_extra_zip_path is not None

    result = BiosCollectResult(
        matches=matches,
        game_new_files=game_new_files,
        game_replaced_files=game_replaced_files,
        game_skipped_existing=game_skipped_existing,
        game_conflicts=game_conflicts,
        game_zip_rebuilt=game_zip_rebuilt,
        game_extra_new_files=game_extra_new_files,
        game_extra_skipped_existing=game_extra_skipped_existing,
        game_extra_zip_rebuilt=game_extra_zip_rebuilt,
        master_new_files=master_new_files,
        master_skipped_existing=master_skipped_existing,
        master_conflicts=master_conflicts,
        master_zip_rebuilt=master_zip_rebuilt,
        master_extra_new_files=master_extra_new_files,
        master_extra_skipped_existing=master_extra_skipped_existing,
        master_extra_zip_rebuilt=master_extra_zip_rebuilt,
    )

    if verbose:
        _print_result(scan_root, game_bios_dir, master_bios_dir, result)

    return result


def _print_result(
    scan_root: str | os.PathLike[str],
    game_bios_dir: Path,
    master_bios_dir: Path | None,
    result: BiosCollectResult,
) -> None:
    print()
    print("Neo Geo BIOS scan:")
    print(f"  Scan root: {Path(scan_root)}")
    print(f"  Game BIOS folder: {game_bios_dir}")
    print(f"  Confirmed BIOS matches found this pass: {len(result.matches)}")
    print(f"  Game BIOS files copied: {len(result.game_new_files)}")
    print(f"  Game BIOS files already present: {len(result.game_skipped_existing)}")
    print(f"  Game neogeo.zip rebuilt: {'yes' if result.game_zip_rebuilt else 'no'}")
    print(f"  Game non-standard extra BIOS files copied: {len(result.game_extra_new_files)}")
    print(f"  Game non-standard extra BIOS files already present: {len(result.game_extra_skipped_existing)}")
    print(f"  Game neogeo_with_non_standard_extra_bios.zip rebuilt: {'yes' if result.game_extra_zip_rebuilt else 'no'}")

    if result.game_replaced_files:
        print("  Warning: replaced conflicting files in game BIOS folder:")
        for name in result.game_replaced_files:
            print(f"    - {name}")

    if master_bios_dir is not None:
        print(f"  Master BIOS folder: {master_bios_dir}")
        print(f"  Master BIOS new files added: {len(result.master_new_files)}")
        print(f"  Master BIOS files already present: {len(result.master_skipped_existing)}")
        print(f"  Master neogeo.zip rebuilt: {'yes' if result.master_zip_rebuilt else 'no'}")
        print(f"  Master non-standard extra BIOS new files added: {len(result.master_extra_new_files)}")
        print(f"  Master non-standard extra BIOS files already present: {len(result.master_extra_skipped_existing)}")
        print(f"  Master neogeo_with_non_standard_extra_bios.zip rebuilt: {'yes' if result.master_extra_zip_rebuilt else 'no'}")

        if result.master_conflicts:
            print("  Warning: same-name conflicts in master BIOS folder were not overwritten:")
            for name in result.master_conflicts:
                print(f"    - {name}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Collect confirmed Neo Geo BIOS files into bios/neogeo.zip.")
    parser.add_argument("scan_root", nargs="?", default=".", help="Folder to scan recursively. Default: current folder.")
    parser.add_argument(
        "--game-bios-dir",
        default=None,
        help="Per-game BIOS output folder. Default: <scan_root>/bios",
    )
    parser.add_argument(
        "--master-bios-dir",
        default=None,
        help="Optional master BIOS output folder. Only rebuilt when new master files are added.",
    )
    args = parser.parse_args()

    scan_root = Path(args.scan_root).resolve()
    game_bios_dir = Path(args.game_bios_dir).resolve() if args.game_bios_dir else scan_root / "bios"
    master_bios_dir = Path(args.master_bios_dir).resolve() if args.master_bios_dir else None

    collect_neogeo_bios(
        scan_root=scan_root,
        game_bios_output_dir=game_bios_dir,
        master_bios_output_dir=master_bios_dir,
        verbose=True,
    )
