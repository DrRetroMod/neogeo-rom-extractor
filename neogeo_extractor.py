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
NeoGeo MAME ROM Extractor - Core Script

Expected structure:

NeoGeo Games Root/
├─ NeoGeo Extractor/
│  ├─ neogeo_extractor.py
│  ├─ game_modules/
│  │  ├─ __init__.py
│  │  └─ three_count_bout.py
│  ├─ temp/
│  ├─ extracted_neogeo/
│  ├─ backups/
│  │  ├─ temp/
│  │  └─ extracted_neogeo/
│  ├─ failed/
│  └─ batch_logs/
│
├─ 3 Count Bout/
├─ Metal Slug 4/
└─ other game folders...

Path rule:

SCRIPT_DIR = the folder containing this script.
SCAN_ROOT  = the parent folder above the extractor folder.

This version supports:
- loading Python game modules
- menu
- command-line arguments
- recursive source detection
- dry-run mode
- module listing
- per-game temp folders
- per-game output folders
- timestamped backups
- slice operations
- concat_slices operations
- generic NeoGeo 4bpp tile decode operations
- conditional_slice operations
- find_slice_by_crc32 operations
- Dotemu SFIX re-encode operations
- Dotemu tile re-encode operations
- assemble_chunks operations
- CRC32 + SHA1 validation
- normal compressed ZIP creation
- existing source ZIP collection from all top-level folders during batch extraction
- per-game logs
"""

from __future__ import annotations

import argparse
import binascii
import hashlib
import importlib.util
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


# ------------------------------------------------------------
# Root paths
# ------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
SCAN_ROOT = SCRIPT_DIR.parent

MODULES_DIR = SCRIPT_DIR / "game_modules"
TEMP_DIR = SCRIPT_DIR / "temp"
OUTPUT_DIR = SCRIPT_DIR / "extracted_neogeo"

BACKUPS_DIR = SCRIPT_DIR / "backups"
FAILED_DIR = SCRIPT_DIR / "failed"
BATCH_LOGS_DIR = SCRIPT_DIR / "batch_logs"

IGNORED_DIR_NAMES = {
    "game_modules",
    "temp",
    "extracted_neogeo",
    "backups",
    "failed",
    "batch_logs",
    "__pycache__",
    ".git",
    "_backups",
    "_failed",
    "_batch_logs",
}


# ------------------------------------------------------------
# Data containers
# ------------------------------------------------------------

@dataclass
class GameModule:
    module_path: Path
    module_name: str
    game: dict[str, Any]


@dataclass
class DetectionResult:
    game_id: str
    title: str
    found: bool
    method: str | None = None
    game_folder: Path | None = None
    source_folder: Path | None = None
    reason: str | None = None


@dataclass
class FileBuildResult:
    output_name: str
    success: bool
    output_path: Path | None = None
    reason: str | None = None


@dataclass
class GameProcessResult:
    game_id: str
    title: str
    success: bool
    status: str
    output_folder: Path | None = None
    log_path: Path | None = None
    reason: str | None = None


@dataclass
class ExistingZipCollectionResult:
    game_id: str
    title: str
    copied_count: int
    skipped_reason: str | None = None
    output_folder: Path | None = None
    log_path: Path | None = None
    copied_files: list[Path] | None = None


# ------------------------------------------------------------
# Basic helpers
# ------------------------------------------------------------

def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H%M%S")


def normalize_name(value: str) -> str:
    return value.casefold().replace("_", " ").replace("-", " ").strip()


def sanitize_folder_name(value: str) -> str:
    replacements = {
        "/": "-",
        "\\": "-",
        ":": " -",
        "*": "",
        "?": "",
        '"': "'",
        "<": "(",
        ">": ")",
        "|": "-",
    }

    cleaned = value

    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)

    cleaned = " ".join(cleaned.split())
    cleaned = cleaned.strip(" .")

    return cleaned or "Unknown Game"


def ensure_base_folders() -> None:
    MODULES_DIR.mkdir(exist_ok=True)
    TEMP_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    BACKUPS_DIR.mkdir(exist_ok=True)
    FAILED_DIR.mkdir(exist_ok=True)
    BATCH_LOGS_DIR.mkdir(exist_ok=True)

    init_file = MODULES_DIR / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")


def backup_existing_folder(folder: Path, backup_root: Path) -> Path | None:
    if not folder.exists():
        return None

    backup_root.mkdir(parents=True, exist_ok=True)

    backup_name = f"{folder.name} - {timestamp()}"
    backup_path = backup_root / backup_name

    counter = 2
    while backup_path.exists():
        backup_path = backup_root / f"{backup_name} ({counter})"
        counter += 1

    shutil.move(str(folder), str(backup_path))
    return backup_path


def read_bytes_from_file(path: Path) -> bytes:
    with path.open("rb") as f:
        return f.read()


def write_bytes_to_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)


def crc32_hex(data: bytes) -> str:
    return f"{binascii.crc32(data) & 0xFFFFFFFF:08x}"


def sha1_hex(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def hex_to_bytes(value: str) -> bytes:
    clean = value.replace(" ", "").replace("0x", "").replace(",", "").strip()
    if len(clean) % 2 != 0:
        raise ValueError(f"Invalid hex byte string: {value}")
    return bytes.fromhex(clean)


def validate_data(data: bytes, file_entry: dict[str, Any], log: list[str]) -> bool:
    expected_size = int(file_entry["size"])
    expected_crc32 = str(file_entry["crc32"]).casefold()
    expected_sha1 = str(file_entry["sha1"]).casefold()

    actual_size = len(data)
    actual_crc32 = crc32_hex(data)
    actual_sha1 = sha1_hex(data)

    size_ok = actual_size == expected_size
    crc_ok = actual_crc32 == expected_crc32
    sha1_ok = actual_sha1 == expected_sha1

    log.append(f"  Size:  {'OK' if size_ok else 'FAIL'} expected {expected_size}, got {actual_size}")
    log.append(f"  CRC32: {'OK' if crc_ok else 'FAIL'} expected {expected_crc32}, got {actual_crc32}")
    log.append(f"  SHA1:  {'OK' if sha1_ok else 'FAIL'} expected {expected_sha1}, got {actual_sha1}")

    return size_ok and crc_ok and sha1_ok


def unique_destination_path(destination_folder: Path, filename: str) -> Path:
    destination = destination_folder / filename

    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix

    counter = 2
    while True:
        candidate = destination_folder / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


# ------------------------------------------------------------
# Module loading
# ------------------------------------------------------------

def load_game_modules() -> list[GameModule]:
    ensure_base_folders()

    modules: list[GameModule] = []

    for module_path in sorted(MODULES_DIR.glob("*.py")):
        if module_path.name == "__init__.py":
            continue

        module_name = module_path.stem

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            print(f"WARNING: Could not load module spec: {module_path.name}")
            continue

        loaded_module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(loaded_module)
        except Exception as error:
            print(f"WARNING: Failed to import {module_path.name}: {error}")
            continue

        game = getattr(loaded_module, "GAME", None)

        if not isinstance(game, dict):
            print(f"WARNING: {module_path.name} has no valid GAME dictionary.")
            continue

        required_keys = ["id", "title", "files", "outputs"]
        missing_keys = [key for key in required_keys if key not in game]

        if missing_keys:
            print(
                f"WARNING: {module_path.name} missing required GAME keys: "
                f"{', '.join(missing_keys)}"
            )
            continue

        modules.append(
            GameModule(
                module_path=module_path,
                module_name=module_name,
                game=game,
            )
        )

    return modules


# ------------------------------------------------------------
# Recursive folder scanning
# ------------------------------------------------------------

def iter_candidate_folders() -> list[Path]:
    candidates: list[Path] = []

    for path in SCAN_ROOT.rglob("*"):
        if not path.is_dir():
            continue

        relative_parts = path.relative_to(SCAN_ROOT).parts

        if not relative_parts:
            continue

        if relative_parts[0] == SCRIPT_DIR.name:
            continue

        if any(part in IGNORED_DIR_NAMES for part in relative_parts):
            continue

        candidates.append(path)

    return candidates


def calculate_required_source_sizes(game: dict[str, Any]) -> dict[str, int]:
    """
    Calculate minimum source-file sizes required by declared slice-style operations.

    This is generic. It reads the module's declared operations and prevents
    fallback detection from choosing another NeoGeo game's folder just because
    it has the same generic source filenames.
    """
    required_sizes: dict[str, int] = {}

    for file_entry in game.get("files", []):
        for operation in file_entry.get("operations", []):
            op_type = str(operation.get("type"))

            if op_type == "slice":
                source_file = str(operation["source_file"])
                offset = int(operation.get("offset", 0))
                size = int(operation["size"])
                required = offset + size

                required_sizes[source_file] = max(
                    required_sizes.get(source_file, 0),
                    required,
                )

            elif op_type == "concat_slices":
                for slice_def in operation.get("slices", []):
                    source_file = str(slice_def["source_file"])
                    offset = int(slice_def.get("offset", 0))
                    size = int(slice_def["size"])
                    required = offset + size

                    required_sizes[source_file] = max(
                        required_sizes.get(source_file, 0),
                        required,
                    )

            elif op_type == "conditional_slice":
                source_file = str(operation["source_file"])
                choices = operation.get("choices")
                if choices is None:
                    choices = operation.get("cases", [])

                for choice in choices:
                    offset = int(choice.get("offset", 0))
                    size = int(choice["size"])
                    required = offset + size

                    required_sizes[source_file] = max(
                        required_sizes.get(source_file, 0),
                        required,
                    )

            elif op_type in {
                "neogeo_4bpp_tile_decode",
                "assemble_chunks",
                "patch_if_needed",
                "find_slice_by_crc32",
                "dotemu_sfix_reencode",
                "dotemu_tiles_reencode",
            }:
                continue

    return required_sizes


def source_folder_has_required_files_and_sizes(
    source_folder: Path,
    required_source_files: list[str],
    required_source_sizes: dict[str, int],
) -> tuple[bool, str | None]:
    for filename in required_source_files:
        path = source_folder / filename

        if not path.is_file():
            return False, f"Missing required file: {filename}"

        required_size = required_source_sizes.get(filename)

        if required_size is not None:
            actual_size = path.stat().st_size

            if actual_size < required_size:
                return (
                    False,
                    f"{filename} too small: need at least {required_size} bytes, got {actual_size}",
                )

    return True, None


# ------------------------------------------------------------
# Source detection
# ------------------------------------------------------------

def detect_game_source(module: GameModule, candidate_folders: list[Path]) -> DetectionResult:
    game = module.game

    game_id = str(game["id"])
    title = str(game["title"])

    search_folder_names = [
        normalize_name(str(name))
        for name in game.get("search_folder_names", [])
    ]

    source_subfolders = [
        Path(str(subfolder))
        for subfolder in game.get("source_subfolders", ["."])
    ]

    required_source_files = [
        str(filename)
        for filename in game.get("required_source_files", [])
    ]

    required_source_sizes = calculate_required_source_sizes(game)

    # Pass 1: folder-name matching.
    if search_folder_names:
        for folder in candidate_folders:
            folder_name = normalize_name(folder.name)

            if folder_name not in search_folder_names:
                continue

            for source_subfolder in source_subfolders:
                possible_source_folder = folder / source_subfolder

                if not possible_source_folder.is_dir():
                    continue

                if required_source_files:
                    ok, _reason = source_folder_has_required_files_and_sizes(
                        possible_source_folder,
                        required_source_files,
                        required_source_sizes,
                    )

                    if not ok:
                        continue

                return DetectionResult(
                    game_id=game_id,
                    title=title,
                    found=True,
                    method="folder-name match",
                    game_folder=folder,
                    source_folder=possible_source_folder,
                )

    # Pass 2: optional required-source-file and source-size fallback.
    # This is disabled by default because many NeoGeo games use the same
    # generic source filenames and can falsely match another game's folder.
    if game.get("allow_required_file_fallback", False) and required_source_files:
        for folder in candidate_folders:
            ok, _reason = source_folder_has_required_files_and_sizes(
                folder,
                required_source_files,
                required_source_sizes,
            )

            if not ok:
                continue

            return DetectionResult(
                game_id=game_id,
                title=title,
                found=True,
                method="required-source-file and source-size match",
                game_folder=folder.parent,
                source_folder=folder,
            )

    return DetectionResult(
        game_id=game_id,
        title=title,
        found=False,
        reason="No matching folder or source folder containing all required source files with valid minimum sizes was found.",
    )


def detect_all_games(modules: list[GameModule]) -> list[DetectionResult]:
    candidate_folders = iter_candidate_folders()
    return [
        detect_game_source(module, candidate_folders)
        for module in modules
    ]


# ------------------------------------------------------------
# Existing source ZIP collection
# ------------------------------------------------------------

def collect_existing_zips_for_game(
    module: GameModule,
    detection: DetectionResult,
    log: list[str] | None = None,
    *,
    verbose: bool = False,
) -> ExistingZipCollectionResult:
    game = module.game
    game_id = str(game["id"])
    title = str(game["title"])
    safe_title = sanitize_folder_name(title)

    if not detection.found or detection.game_folder is None:
        reason = detection.reason or "Game source was not detected."
        if log is not None:
            log.append("")
            log.append("Existing ZIP collection: SKIPPED")
            log.append(f"Reason: {reason}")
        return ExistingZipCollectionResult(
            game_id=game_id,
            title=title,
            copied_count=0,
            skipped_reason=reason,
        )

    game_folder = detection.game_folder
    existing_zip_output_folder = OUTPUT_DIR / safe_title

    candidate_zips = sorted(
        path
        for path in game_folder.rglob("*.zip")
        if path.is_file()
        and not any(part in IGNORED_DIR_NAMES for part in path.relative_to(game_folder).parts)
    )

    has_neogeo_zip = any(path.name.casefold() == "neogeo.zip" for path in candidate_zips)

    if not has_neogeo_zip:
        reason = "No neogeo.zip found under detected game folder; skipped ZIP collection."
        if log is not None:
            log.append("")
            log.append("Existing ZIP collection: SKIPPED")
            log.append(f"Scan root: {game_folder}")
            log.append(f"Reason: {reason}")
        if verbose:
            print("  Existing ZIPs: skipped, no neogeo.zip found")
        return ExistingZipCollectionResult(
            game_id=game_id,
            title=title,
            copied_count=0,
            skipped_reason=reason,
            output_folder=existing_zip_output_folder,
        )

    backup_existing_folder(existing_zip_output_folder, BACKUPS_DIR / "extracted_neogeo")

    existing_zip_output_folder.mkdir(parents=True, exist_ok=True)

    copied_files: list[Path] = []
    lines: list[str] = []

    lines.append("Existing ZIP Collection Log")
    lines.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"Game ID: {game_id}")
    lines.append(f"Title:   {title}")
    lines.append(f"Source game folder: {game_folder}")
    lines.append(f"Output folder:      {existing_zip_output_folder}")
    lines.append("")
    lines.append("Rule:")
    lines.append("  neogeo.zip was found, so all .zip files under the detected game folder were copied.")
    lines.append("  These ZIPs were copied from the source game folder.")
    lines.append("  These ZIPs were not generated or validated by this extractor.")
    lines.append("")
    lines.append("Copied ZIP files:")

    if log is not None:
        log.append("")
        log.append("Existing ZIP collection: RUN")
        log.append(f"Scan root: {game_folder}")
        log.append("Trigger: neogeo.zip found")
        log.append("Copied files:")

    for source_zip in candidate_zips:
        destination_zip = unique_destination_path(existing_zip_output_folder, source_zip.name)
        shutil.copy2(source_zip, destination_zip)
        copied_files.append(destination_zip)

        try:
            relative_source = source_zip.relative_to(game_folder)
        except ValueError:
            relative_source = source_zip

        lines.append(f"  - {relative_source} -> {destination_zip.name}")

        if log is not None:
            log.append(f"  - {relative_source} -> {destination_zip}")

    if not copied_files:
        lines.append("  none")

    log_path = existing_zip_output_folder / "existing ZIP collection log.txt"
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if verbose:
        print(f"  Existing ZIPs: copied {len(copied_files)} file(s)")

    return ExistingZipCollectionResult(
        game_id=game_id,
        title=title,
        copied_count=len(copied_files),
        output_folder=existing_zip_output_folder,
        log_path=log_path,
        copied_files=copied_files,
    )


def collect_existing_zips_for_detected_games(modules: list[GameModule]) -> list[ExistingZipCollectionResult]:
    candidate_folders = iter_candidate_folders()
    results: list[ExistingZipCollectionResult] = []

    print()
    print("Collecting existing ZIPs from detected game folders.")
    print("Rule: only copy ZIPs when neogeo.zip is found under that game folder.")

    for module in modules:
        detection = detect_game_source(module, candidate_folders)
        title = str(module.game["title"])

        print()
        print(f"Checking: {title}")

        if not detection.found:
            print(f"  Status: SKIPPED")
            print(f"  Reason: {detection.reason}")
            results.append(
                ExistingZipCollectionResult(
                    game_id=str(module.game["id"]),
                    title=title,
                    copied_count=0,
                    skipped_reason=detection.reason,
                )
            )
            continue

        result = collect_existing_zips_for_game(
            module,
            detection,
            log=None,
            verbose=True,
        )
        results.append(result)

    write_existing_zip_collection_log(results)

    print()
    print("Existing ZIP collection finished.")

    return results


def write_existing_zip_collection_log(results: list[ExistingZipCollectionResult]) -> Path:
    BATCH_LOGS_DIR.mkdir(parents=True, exist_ok=True)

    log_path = BATCH_LOGS_DIR / f"Existing ZIP collection - {timestamp()}.txt"

    lines: list[str] = []
    lines.append("Existing ZIP Collection Batch Log")
    lines.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("Rule:")
    lines.append("  For each detected game folder, copy ZIPs only if neogeo.zip exists under that folder.")
    lines.append("  Copied ZIPs are source/vendor ZIPs, not generated or validated extractor output.")
    lines.append("")

    for result in results:
        lines.append(result.title)

        if result.copied_count > 0:
            lines.append(f"  Status: COPIED {result.copied_count} file(s)")
            if result.output_folder:
                lines.append(f"  Output folder: {result.output_folder}")
            if result.log_path:
                lines.append(f"  Log: {result.log_path}")
        else:
            lines.append("  Status: SKIPPED")
            if result.skipped_reason:
                lines.append(f"  Reason: {result.skipped_reason}")

        lines.append("")

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log_path

def iter_top_level_scan_folders() -> list[Path]:
    """
    Return top-level folders under SCAN_ROOT that are not extractor/framework folders.

    This is used by the global existing-ZIP collector. It deliberately does
    not require a game module, because the point of that collector is to find
    vendor/source ZIPs in all folders when neogeo.zip is present.
    """
    folders: list[Path] = []

    for path in sorted(SCAN_ROOT.iterdir()):
        if not path.is_dir():
            continue

        if path.name == SCRIPT_DIR.name:
            continue

        if path.name in IGNORED_DIR_NAMES:
            continue

        folders.append(path)

    return folders


def find_zip_files_under(folder: Path) -> list[Path]:
    """
    Find ZIP files below a folder while skipping framework-style folders.
    """
    zip_files: list[Path] = []

    for path in folder.rglob("*.zip"):
        if not path.is_file():
            continue

        try:
            relative_parts = path.relative_to(folder).parts
        except ValueError:
            relative_parts = path.parts

        if any(part in IGNORED_DIR_NAMES for part in relative_parts):
            continue

        zip_files.append(path)

    return sorted(zip_files)


def collect_existing_zips_from_folder(
    source_root: Path,
    output_title: str,
    *,
    verbose: bool = False,
) -> ExistingZipCollectionResult:
    """
    Scan one top-level source folder.

    Rule:
      - If neogeo.zip exists anywhere below source_root, copy every .zip found
        below source_root.
      - If neogeo.zip is not found, copy nothing.

    The output folder name is based on output_title, normally the top-level
    folder name for module-free global scans.
    """
    safe_title = sanitize_folder_name(output_title)
    existing_zip_output_folder = OUTPUT_DIR / safe_title

    candidate_zips = find_zip_files_under(source_root)
    has_neogeo_zip = any(path.name.casefold() == "neogeo.zip" for path in candidate_zips)

    if not has_neogeo_zip:
        reason = "No neogeo.zip found; skipped ZIP collection."
        if verbose:
            print("  Existing ZIPs: skipped, no neogeo.zip found")
        return ExistingZipCollectionResult(
            game_id=source_root.name,
            title=output_title,
            copied_count=0,
            skipped_reason=reason,
            output_folder=existing_zip_output_folder,
        )

    backup_existing_folder(existing_zip_output_folder, BACKUPS_DIR / "extracted_neogeo")
    existing_zip_output_folder.mkdir(parents=True, exist_ok=True)

    copied_files: list[Path] = []
    lines: list[str] = []

    lines.append("Existing ZIP Collection Log")
    lines.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"Source root:   {source_root}")
    lines.append(f"Output title:  {output_title}")
    lines.append(f"Output folder: {existing_zip_output_folder}")
    lines.append("")
    lines.append("Rule:")
    lines.append("  neogeo.zip was found, so all .zip files under this source folder were copied.")
    lines.append("  These ZIPs were copied from the source game folder.")
    lines.append("  These ZIPs were not generated or validated by this extractor.")
    lines.append("")
    lines.append("Copied ZIP files:")

    for source_zip in candidate_zips:
        destination_zip = unique_destination_path(existing_zip_output_folder, source_zip.name)
        shutil.copy2(source_zip, destination_zip)
        copied_files.append(destination_zip)

        try:
            relative_source = source_zip.relative_to(source_root)
        except ValueError:
            relative_source = source_zip

        lines.append(f"  - {relative_source} -> {destination_zip.name}")

    log_path = existing_zip_output_folder / "existing ZIP collection log.txt"
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if verbose:
        print(f"  Existing ZIPs: copied {len(copied_files)} file(s)")

    return ExistingZipCollectionResult(
        game_id=source_root.name,
        title=output_title,
        copied_count=len(copied_files),
        output_folder=existing_zip_output_folder,
        log_path=log_path,
        copied_files=copied_files,
    )


def collect_existing_zips_from_all_folders() -> list[ExistingZipCollectionResult]:
    """
    Global existing-ZIP collector.

    This scans every top-level folder under SCAN_ROOT, not just folders that
    have game modules. It is intentionally gated by neogeo.zip.
    """
    results: list[ExistingZipCollectionResult] = []

    print()
    print("Collecting existing ZIPs from all top-level folders.")
    print("Rule: if neogeo.zip is found under a folder, copy all ZIPs from that folder.")

    for folder in iter_top_level_scan_folders():
        print()
        print(f"Checking folder: {folder.name}")

        result = collect_existing_zips_from_folder(
            folder,
            folder.name,
            verbose=True,
        )
        results.append(result)

    write_existing_zip_collection_log(results)

    print()
    print("Existing ZIP collection finished.")

    return results



# ------------------------------------------------------------
# Generic NeoGeo tile/sprite helpers
# ------------------------------------------------------------

def neogeo_4bpp_tile_decode(
    source_data: bytes,
    *,
    tile_size: int,
    row_offsets: list[tuple[int, int]],
    output_streams: dict[str, list[int]],
) -> dict[str, bytes]:
    """
    Generic NeoGeo 4bpp tile decoder.

    The game module declares:
      - tile_size
      - row_offsets
      - output_streams

    Important:
    output_streams controls the byte order written per decoded row.
    Example:
      "odd":  [0, 1]
      "even": [2, 3]

    That means:
      odd receives plane0, plane1, plane0, plane1...
      even receives plane2, plane3, plane2, plane3...

    The core remains generic; the module declares the layout.
    """
    if tile_size <= 0:
        raise ValueError(f"Invalid tile_size: {tile_size}")

    if len(source_data) % tile_size != 0:
        raise ValueError(
            f"Source size is not divisible by tile_size: "
            f"source={len(source_data)}, tile_size={tile_size}"
        )

    if len(row_offsets) != 4:
        raise ValueError(
            f"row_offsets must contain exactly 4 entries, got {len(row_offsets)}"
        )

    for stream_name, planes in output_streams.items():
        for plane in planes:
            if plane < 0 or plane > 3:
                raise ValueError(
                    f"Invalid plane {plane} in output stream {stream_name}"
                )

    streams = {
        stream_name: bytearray()
        for stream_name in output_streams
    }

    total_tiles = len(source_data) // tile_size

    for tile_index in range(total_tiles):
        tile_start = tile_index * tile_size
        tile = source_data[tile_start:tile_start + tile_size]

        for block in range(4):
            base_offset, row_block = row_offsets[block]

            for row in range(8):
                planes = [0, 0, 0, 0]
                offset = base_offset + (row_block * 8) + (row * 8)

                if offset + 4 > len(tile):
                    raise ValueError(
                        f"Tile decode offset out of range: "
                        f"tile={tile_index}, block={block}, row={row}, offset={offset}"
                    )

                for i in range(3, -1, -1):
                    b = tile[offset + i]

                    planes[0] = (planes[0] << 1) | ((b >> 4) & 0x1)
                    planes[0] = (planes[0] << 1) | ((b >> 0) & 0x1)

                    planes[1] = (planes[1] << 1) | ((b >> 5) & 0x1)
                    planes[1] = (planes[1] << 1) | ((b >> 1) & 0x1)

                    planes[2] = (planes[2] << 1) | ((b >> 6) & 0x1)
                    planes[2] = (planes[2] << 1) | ((b >> 2) & 0x1)

                    planes[3] = (planes[3] << 1) | ((b >> 7) & 0x1)
                    planes[3] = (planes[3] << 1) | ((b >> 3) & 0x1)

                for stream_name, plane_indexes in output_streams.items():
                    for plane_index in plane_indexes:
                        streams[stream_name].append(planes[plane_index])

    return {
        stream_name: bytes(data)
        for stream_name, data in streams.items()
    }


# ------------------------------------------------------------
# Operation engine
# ------------------------------------------------------------

def resolve_source_file(source_folder: Path, operation: dict[str, Any]) -> Path:
    source_file = Path(str(operation["source_file"]))

    if source_file.is_absolute():
        return source_file

    source_subfolder = operation.get("source_subfolder")

    if source_subfolder:
        return source_folder / str(source_subfolder) / source_file

    return source_folder / source_file


def run_slice_operation(source_folder: Path, operation: dict[str, Any], log: list[str]) -> bytes:
    source_path = resolve_source_file(source_folder, operation)

    offset = int(operation.get("offset", 0))
    size = int(operation["size"])
    required_size = offset + size

    log.append(f"  Operation: slice")
    log.append(f"    Source file: {source_path}")
    log.append(f"    Offset:      0x{offset:08X}")
    log.append(f"    Size:        {size} bytes")

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    actual_source_size = source_path.stat().st_size

    if actual_source_size < required_size:
        raise ValueError(
            f"Source file too small: {source_path} "
            f"needs at least {required_size} bytes, got {actual_source_size}"
        )

    with source_path.open("rb") as f:
        f.seek(offset)
        return f.read(size)


def run_concat_slices_operation(
    source_folder: Path,
    operation: dict[str, Any],
    log: list[str],
) -> bytes:
    log.append("  Operation: concat_slices")

    slices = operation["slices"]
    output = bytearray()

    for index, slice_def in enumerate(slices, start=1):
        source_path = resolve_source_file(source_folder, slice_def)

        offset = int(slice_def.get("offset", 0))
        size = int(slice_def["size"])
        required_size = offset + size

        log.append(f"    Slice {index}:")
        log.append(f"      Source file: {source_path}")
        log.append(f"      Offset:      0x{offset:08X}")
        log.append(f"      Size:        {size} bytes")

        if not source_path.is_file():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        actual_source_size = source_path.stat().st_size

        if actual_source_size < required_size:
            raise ValueError(
                f"Source file too small: {source_path} "
                f"needs at least {required_size} bytes, got {actual_source_size}"
            )

        with source_path.open("rb") as f:
            f.seek(offset)
            output.extend(f.read(size))

    return bytes(output)


def run_conditional_slice_operation(
    source_folder: Path,
    operation: dict[str, Any],
    log: list[str],
) -> bytes:
    source_path = resolve_source_file(source_folder, operation)

    log.append("  Operation: conditional_slice")
    log.append(f"    Source file: {source_path}")

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    source_size = source_path.stat().st_size
    log.append(f"    Source size: {source_size} bytes")

    choices = operation.get("choices")
    if choices is None:
        choices = operation.get("cases")

    if choices is None:
        raise ValueError("conditional_slice operation must define choices or cases")

    for choice in choices:
        if_size = choice.get("if_size")
        minimum_size = choice.get("minimum_size")
        min_source_size = choice.get("min_source_size")
        max_source_size = choice.get("max_source_size")

        if if_size is not None and source_size != int(if_size):
            continue

        if minimum_size is not None and source_size < int(minimum_size):
            continue

        if min_source_size is not None and source_size < int(min_source_size):
            continue

        if max_source_size is not None and source_size > int(max_source_size):
            continue

        offset = int(choice.get("offset", 0))
        size = int(choice["size"])
        required_size = offset + size

        log.append(f"    Matched choice: {choice.get('description', 'unnamed choice')}")
        log.append(f"    Offset:         0x{offset:08X}")
        log.append(f"    Size:           {size} bytes")

        if source_size < required_size:
            raise ValueError(
                f"Source file too small: {source_path} "
                f"needs at least {required_size} bytes, got {source_size}"
            )

        with source_path.open("rb") as f:
            f.seek(offset)
            return f.read(size)

    raise ValueError(
        f"No conditional_slice choice matched source size {source_size} "
        f"for {source_path}"
    )


def dotemu_sfix_reencode_source_bytes(data: bytes) -> bytes:
    """
    Re-encode Dotemu SFIX/source text-layer data into NeoGeo SFIX layout.

    Dotemu stores each 32-byte block in a different byte order. This converts
    each 32-byte block into the MAME/NeoGeo expected order.
    """
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


def run_dotemu_sfix_reencode_operation(
    source_folder: Path,
    operation: dict[str, Any],
    log: list[str],
) -> bytes:
    source_path = resolve_source_file(source_folder, operation)

    log.append("  Operation: dotemu_sfix_reencode")
    log.append(f"    Source file: {source_path}")

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    source_data = read_bytes_from_file(source_path)
    output = dotemu_sfix_reencode_source_bytes(source_data)

    log.append(f"    Source size: {len(source_data)} bytes")
    log.append(f"    Output size: {len(output)} bytes")

    return output


def dotemu_tiles_reencode_pair_data(pair_data: bytes) -> tuple[bytes, bytes]:
    """
    Re-encode one Dotemu tile pair block into NeoGeo odd/even C-ROM data.

    The source pair_data should be exactly odd_size + even_size bytes. For a
    C1/C2 pair where each output is 8 MiB, pair_data is 16 MiB.
    """
    if len(pair_data) % 128 != 0:
        raise ValueError(
            f"Dotemu tile pair data size must be divisible by 128, got {len(pair_data)}"
        )

    odd = bytearray()
    even = bytearray()

    def col_to_neogeo(column: list[list[int]]) -> None:
        for row in column:
            bp0 = 0
            bp1 = 0
            bp2 = 0
            bp3 = 0

            pixels = bytearray()

            for value in row:
                pixels.append(value & 0x0F)
                pixels.append(value >> 4)

            for pixel_index in range(0, 8):
                pixel = pixels[pixel_index]

                bp0 |= (pixel & 1) << (7 - pixel_index)
                bp1 |= ((pixel >> 1) & 1) << (7 - pixel_index)
                bp2 |= ((pixel >> 2) & 1) << (7 - pixel_index)
                bp3 |= ((pixel >> 3) & 1) << (7 - pixel_index)

            odd.append(bp0)
            odd.append(bp1)
            even.append(bp2)
            even.append(bp3)

    for tile_offset in range(0, len(pair_data), 128):
        left_column: list[list[int]] = []
        right_column: list[list[int]] = []
        build_row: list[int] = []

        for byte_index in range(0, 128):
            value = pair_data[tile_offset + byte_index]

            if ((byte_index // 4) % 2) == 0:
                build_row.append(value)

                if len(build_row) == 4:
                    left_column.append(build_row[:])
                    build_row.clear()
            else:
                build_row.append(value)

                if len(build_row) == 4:
                    right_column.append(build_row[:])
                    build_row.clear()

        col_to_neogeo(right_column)
        col_to_neogeo(left_column)

    return bytes(odd), bytes(even)


def run_dotemu_tiles_reencode_operation(
    source_folder: Path,
    operation: dict[str, Any],
    output_name: str,
    log: list[str],
) -> bytes:
    source_path = resolve_source_file(source_folder, operation)

    log.append("  Operation: dotemu_tiles_reencode")
    log.append(f"    Source file: {source_path}")
    log.append(f"    Requested output: {output_name}")

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    source_data = read_bytes_from_file(source_path)
    pairs = operation["pairs"]

    log.append(f"    Source size: {len(source_data)} bytes")
    log.append(f"    Pair count:   {len(pairs)}")

    position = 0

    for pair in pairs:
        odd_name = str(pair["odd"])
        even_name = str(pair["even"])
        output_size = int(pair["size"])

        pair_size = output_size * 2
        pair_end = position + pair_size

        log.append(f"    Pair: {odd_name} / {even_name}")
        log.append(f"      Output size each: {output_size} bytes")
        log.append(f"      Source range:     0x{position:08X}-0x{pair_end - 1:08X}")

        if pair_end > len(source_data):
            raise ValueError(
                f"Dotemu tile source too small for pair {odd_name}/{even_name}: "
                f"needs {pair_end} bytes, got {len(source_data)}"
            )

        pair_data = source_data[position:pair_end]
        position = pair_end

        if output_name not in {odd_name, even_name}:
            continue

        odd_data, even_data = dotemu_tiles_reencode_pair_data(pair_data)

        if len(odd_data) != output_size:
            raise ValueError(
                f"Unexpected odd output size for {odd_name}: "
                f"expected {output_size}, got {len(odd_data)}"
            )

        if len(even_data) != output_size:
            raise ValueError(
                f"Unexpected even output size for {even_name}: "
                f"expected {output_size}, got {len(even_data)}"
            )

        if output_name == odd_name:
            log.append(f"      Returning odd output: {odd_name}")
            return odd_data

        log.append(f"      Returning even output: {even_name}")
        return even_data

    raise ValueError(
        f"dotemu_tiles_reencode did not define requested output file: {output_name}"
    )


def run_find_slice_by_crc32_operation(
    source_folder: Path,
    operation: dict[str, Any],
    log: list[str],
) -> bytes:
    source_path = resolve_source_file(source_folder, operation)

    offset_start = int(operation.get("offset_start", 0))
    offset_end = operation.get("offset_end")
    step = int(operation.get("step", 0x10000))
    size = int(operation["size"])
    expected_crc32 = str(operation["crc32"]).casefold()

    log.append("  Operation: find_slice_by_crc32")
    log.append(f"    Source file:     {source_path}")
    log.append(f"    Offset start:    0x{offset_start:08X}")
    log.append(f"    Step:            0x{step:08X}")
    log.append(f"    Slice size:      {size} bytes")
    log.append(f"    Expected CRC32:  {expected_crc32}")

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    source_data = read_bytes_from_file(source_path)
    source_size = len(source_data)

    if offset_end is None:
        offset_end_int = source_size - size
    else:
        offset_end_int = int(offset_end)

    if offset_end_int < offset_start:
        raise ValueError(
            f"Invalid find_slice_by_crc32 range: start={offset_start}, end={offset_end_int}"
        )

    for offset in range(offset_start, offset_end_int + 1, step):
        end = offset + size

        if end > source_size:
            continue

        candidate = source_data[offset:end]
        got_crc32 = crc32_hex(candidate)

        log.append(f"    Candidate offset 0x{offset:08X}: CRC32 {got_crc32}")

        if got_crc32 == expected_crc32:
            log.append(f"    Result: MATCH at offset 0x{offset:08X}")
            return candidate

    raise ValueError(
        f"No slice found in {source_path} matching CRC32 {expected_crc32}"
    )


def build_streams_for_file(
    source_folder: Path,
    file_entry: dict[str, Any],
    log: list[str],
) -> dict[str, bytes]:
    streams: dict[str, bytes] = {}

    for operation in file_entry["operations"]:
        op_type = str(operation["type"])

        if op_type == "neogeo_4bpp_tile_decode":
            source_path = resolve_source_file(source_folder, operation)

            tile_size = int(operation["tile_size"])

            row_offsets = [
                tuple(item)
                for item in operation["row_offsets"]
            ]

            output_streams = {
                str(stream_name): [int(plane) for plane in planes]
                for stream_name, planes in operation["output_streams"].items()
            }

            log.append("  Operation: neogeo_4bpp_tile_decode")
            log.append(f"    Source file:    {source_path}")
            log.append(f"    Tile size:      {tile_size}")
            log.append(f"    Row offsets:    {row_offsets}")
            log.append(f"    Output streams: {output_streams}")

            if not source_path.is_file():
                raise FileNotFoundError(f"Source file not found: {source_path}")

            source_data = read_bytes_from_file(source_path)

            generated_streams = neogeo_4bpp_tile_decode(
                source_data,
                tile_size=tile_size,
                row_offsets=row_offsets,
                output_streams=output_streams,
            )

            for name, data in generated_streams.items():
                streams[name] = data
                log.append(f"    Generated stream: {name} ({len(data)} bytes)")

        elif op_type == "slice":
            # Direct slice-only files are handled elsewhere.
            continue

        elif op_type == "concat_slices":
            # Direct concat-slices files are handled elsewhere.
            continue

        elif op_type == "conditional_slice":
            # Direct conditional-slice files are handled elsewhere.
            continue

        elif op_type == "find_slice_by_crc32":
            # Direct find-slice files are handled elsewhere.
            continue

        elif op_type == "dotemu_sfix_reencode":
            # Direct Dotemu SFIX files are handled elsewhere.
            continue

        elif op_type == "dotemu_tiles_reencode":
            # Direct Dotemu tile files are handled elsewhere.
            continue

        elif op_type == "assemble_chunks":
            # Assembly is handled later once all streams are known.
            continue

        elif op_type == "patch_if_needed":
            # Patch is handled after validation failure.
            continue

        else:
            raise NotImplementedError(f"Unsupported operation type: {op_type}")

    return streams


def run_assemble_chunks_operation(
    operation: dict[str, Any],
    streams: dict[str, bytes],
    log: list[str],
) -> bytes:
    chunk_size = int(operation["chunk_size"])
    chunks = operation["chunks"]

    output = bytearray()

    log.append("  Operation: assemble_chunks")
    log.append(f"    Chunk size: {chunk_size} bytes")

    for chunk in chunks:
        stream_name = str(chunk["stream"])
        index = int(chunk["index"])

        if stream_name not in streams:
            raise ValueError(f"Stream not available for assemble_chunks: {stream_name}")

        stream = streams[stream_name]
        start = index * chunk_size
        end = start + chunk_size

        if len(stream) < end:
            raise ValueError(
                f"Stream {stream_name} too small for chunk {index}: "
                f"needs {end} bytes, got {len(stream)}"
            )

        log.append(f"    Add: stream={stream_name}, index={index}, range=0x{start:08X}-0x{end - 1:08X}")
        output.extend(stream[start:end])

    return bytes(output)


def apply_patch_if_needed(
    data: bytes,
    file_entry: dict[str, Any],
    log: list[str],
) -> bytes | None:
    operations = file_entry.get("operations", [])
    patch_operations = [
        operation
        for operation in operations
        if str(operation.get("type")) == "patch_if_needed"
    ]

    if not patch_operations:
        log.append("  Patch: no patch rule declared")
        return None

    patched = bytearray(data)

    log.append("  Patch: attempting declared patch rule(s)")

    for patch in patch_operations:
        description = str(patch.get("description", "Unnamed patch"))
        file_offset = int(patch["file_offset"])
        expected_old = hex_to_bytes(str(patch["expected_old"]))
        new_bytes = hex_to_bytes(str(patch["new"]))

        old_end = file_offset + len(expected_old)

        if old_end > len(patched):
            log.append(f"    FAIL: patch out of range: {description}")
            return None

        actual_old = bytes(patched[file_offset:old_end])

        log.append(f"    Description:        {description}")
        log.append(f"    File offset:        0x{file_offset:08X}")
        log.append(f"    Expected old bytes: {expected_old.hex()}")
        log.append(f"    Actual old bytes:   {actual_old.hex()}")
        log.append(f"    New bytes:          {new_bytes.hex()}")

        if actual_old != expected_old:
            log.append("    Result: old bytes did not match; patch refused")
            return None

        patched[file_offset:file_offset + len(new_bytes)] = new_bytes
        log.append("    Result: patch applied")

    return bytes(patched)


def build_file_data(
    source_folder: Path,
    file_entry: dict[str, Any],
    log: list[str],
) -> bytes:
    operations = file_entry["operations"]
    operation_types = [str(operation["type"]) for operation in operations]

    if operation_types.count("slice") == 1 and "assemble_chunks" not in operation_types:
        slice_operation = next(
            operation for operation in operations
            if operation["type"] == "slice"
        )
        return run_slice_operation(source_folder, slice_operation, log)

    if operation_types.count("concat_slices") == 1 and "assemble_chunks" not in operation_types:
        concat_operation = next(
            operation for operation in operations
            if operation["type"] == "concat_slices"
        )
        return run_concat_slices_operation(
            source_folder,
            concat_operation,
            log,
        )

    if operation_types.count("conditional_slice") == 1 and "assemble_chunks" not in operation_types:
        conditional_slice_operation = next(
            operation for operation in operations
            if operation["type"] == "conditional_slice"
        )
        return run_conditional_slice_operation(
            source_folder,
            conditional_slice_operation,
            log,
        )

    if operation_types.count("find_slice_by_crc32") == 1 and "assemble_chunks" not in operation_types:
        find_slice_operation = next(
            operation for operation in operations
            if operation["type"] == "find_slice_by_crc32"
        )
        return run_find_slice_by_crc32_operation(
            source_folder,
            find_slice_operation,
            log,
        )

    if operation_types.count("dotemu_sfix_reencode") == 1 and "assemble_chunks" not in operation_types:
        sfix_operation = next(
            operation for operation in operations
            if operation["type"] == "dotemu_sfix_reencode"
        )
        return run_dotemu_sfix_reencode_operation(
            source_folder,
            sfix_operation,
            log,
        )

    if operation_types.count("dotemu_tiles_reencode") == 1 and "assemble_chunks" not in operation_types:
        tile_operation = next(
            operation for operation in operations
            if operation["type"] == "dotemu_tiles_reencode"
        )
        return run_dotemu_tiles_reencode_operation(
            source_folder,
            tile_operation,
            str(file_entry["output_name"]),
            log,
        )

    streams = build_streams_for_file(source_folder, file_entry, log)

    assembled_data: bytes | None = None

    for operation in operations:
        op_type = str(operation["type"])

        if op_type == "assemble_chunks":
            assembled_data = run_assemble_chunks_operation(operation, streams, log)

    if assembled_data is None:
        raise ValueError(f"No output-producing operation found for {file_entry['output_name']}")

    return assembled_data


# ------------------------------------------------------------
# Extraction engine
# ------------------------------------------------------------

def write_game_notes(game: dict[str, Any], log: list[str]) -> None:
    notes = game.get("notes")

    if not isinstance(notes, dict):
        return

    summary = notes.get("summary")
    details = notes.get("details", [])

    log.append("Module notes:")

    if summary:
        log.append(f"  Summary: {summary}")

    if details:
        log.append("  Details:")
        for detail in details:
            log.append(f"    - {detail}")

    log.append("")


def build_single_file(
    source_folder: Path,
    temp_game_folder: Path,
    file_entry: dict[str, Any],
    log: list[str],
) -> FileBuildResult:
    output_name = str(file_entry["output_name"])
    output_path = temp_game_folder / "zip_staging" / output_name

    log.append("")
    log.append(f"File: {output_name}")

    try:
        data = build_file_data(source_folder, file_entry, log)

        log.append("  Initial validation:")
        initial_ok = validate_data(data, file_entry, log)

        if not initial_ok:
            patched_data = apply_patch_if_needed(data, file_entry, log)

            if patched_data is None:
                return FileBuildResult(
                    output_name=output_name,
                    success=False,
                    reason="Initial validation failed and no valid patch was applied.",
                )

            log.append("  Patched validation:")
            patched_ok = validate_data(patched_data, file_entry, log)

            if not patched_ok:
                return FileBuildResult(
                    output_name=output_name,
                    success=False,
                    reason="Patched data failed validation.",
                )

            data = patched_data
            log.append("  Final file used in ZIP: patched version")
        else:
            log.append("  Final file used in ZIP: unmodified extracted version")

        write_bytes_to_file(output_path, data)

        return FileBuildResult(
            output_name=output_name,
            success=True,
            output_path=output_path,
        )

    except Exception as error:
        log.append(f"  ERROR: {error}")
        return FileBuildResult(
            output_name=output_name,
            success=False,
            reason=str(error),
        )


def create_zip(
    output_folder: Path,
    output_def: dict[str, Any],
    built_files: dict[str, Path],
    log: list[str],
) -> bool:
    zip_name = str(output_def["zip_name"])
    zip_path = output_folder / zip_name
    required_files = [str(name) for name in output_def["files"]]

    log.append("")
    log.append(f"Creating ZIP: {zip_name}")

    missing = [
        name
        for name in required_files
        if name not in built_files
    ]

    if missing:
        log.append("  FAIL: missing built files:")
        for name in missing:
            log.append(f"    - {name}")
        return False

    if zip_path.exists():
        preserved_name = f"existing source {zip_name}"
        preserved_path = unique_destination_path(output_folder, preserved_name)
        shutil.move(str(zip_path), str(preserved_path))
        log.append(f"  Existing ZIP preserved before writing generated ZIP: {preserved_path.name}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in required_files:
            source_path = built_files[name]
            zf.write(source_path, arcname=name)
            log.append(f"  Added: {name}")

    log.append(f"  ZIP written: {zip_path}")
    return True


def process_game(
    module: GameModule,
    *,
    collect_existing_zips: bool = False,
    backup_output: bool = True,
) -> GameProcessResult:
    game = module.game
    game_id = str(game["id"])
    title = str(game["title"])
    safe_title = sanitize_folder_name(title)

    candidate_folders = iter_candidate_folders()
    detection = detect_game_source(module, candidate_folders)

    log: list[str] = []
    log.append(f"NeoGeo MAME ROM Extractor Log")
    log.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    log.append("")
    log.append(f"Game ID: {game_id}")
    log.append(f"Title:   {title}")
    log.append(f"Module:  {module.module_path}")
    log.append("")

    write_game_notes(game, log)

    if not detection.found:
        log.append("Detection: NOT FOUND")
        log.append(f"Reason: {detection.reason}")

        failed_folder = FAILED_DIR / f"{safe_title} - {timestamp()}"
        failed_folder.mkdir(parents=True, exist_ok=True)

        log_path = failed_folder / f"{safe_title} extraction log.txt"
        log_path.write_text("\n".join(log) + "\n", encoding="utf-8")

        return GameProcessResult(
            game_id=game_id,
            title=title,
            success=False,
            status="NOT FOUND",
            output_folder=failed_folder,
            log_path=log_path,
            reason=detection.reason,
        )

    assert detection.source_folder is not None

    log.append("Detection: FOUND")
    log.append(f"Found by:      {detection.method}")
    log.append(f"Game folder:   {detection.game_folder}")
    log.append(f"Source folder: {detection.source_folder}")
    log.append("")

    temp_game_folder = TEMP_DIR / safe_title
    output_game_folder = OUTPUT_DIR / safe_title

    backup_existing_folder(temp_game_folder, BACKUPS_DIR / "temp")
    if backup_output:
        backup_existing_folder(output_game_folder, BACKUPS_DIR / "extracted_neogeo")

    temp_game_folder.mkdir(parents=True, exist_ok=True)
    (temp_game_folder / "zip_staging").mkdir(parents=True, exist_ok=True)

    output_game_folder.mkdir(parents=True, exist_ok=True)

    if collect_existing_zips:
        print("  Checking existing source ZIPs before extraction")
        collect_existing_zips_for_game(
            module,
            detection,
            log,
            verbose=True,
        )

    built_files: dict[str, Path] = {}
    failed_files: list[FileBuildResult] = []

    total_files = len(game["files"])

    for file_index, file_entry in enumerate(game["files"], start=1):
        output_name = str(file_entry.get("output_name", "UNKNOWN"))

        print(f"  [{file_index}/{total_files}] Building {output_name}")

        result = build_single_file(
            source_folder=detection.source_folder,
            temp_game_folder=temp_game_folder,
            file_entry=file_entry,
            log=log,
        )

        if result.success and result.output_path is not None:
            built_files[result.output_name] = result.output_path
        else:
            failed_files.append(result)

    if failed_files:
        log.append("")
        log.append("Result: FAILED")
        log.append("Failed files:")

        for result in failed_files:
            log.append(f"  - {result.output_name}: {result.reason}")

        failed_folder = FAILED_DIR / f"{safe_title} - {timestamp()}"
        failed_folder.mkdir(parents=True, exist_ok=True)

        log_path = failed_folder / f"{safe_title} extraction log.txt"
        log_path.write_text("\n".join(log) + "\n", encoding="utf-8")

        # Move failed output folder away if it exists and is empty/partial.
        # Existing ZIP collection for a failed game remains under failed output backup/logs
        # only if it was already included in the output folder backup before this run.
        if output_game_folder.exists():
            shutil.rmtree(output_game_folder, ignore_errors=True)

        return GameProcessResult(
            game_id=game_id,
            title=title,
            success=False,
            status="FAILED",
            output_folder=failed_folder,
            log_path=log_path,
            reason="One or more files failed to build or validate.",
        )

    zip_success = True

    for output_def in game["outputs"]:
        if not create_zip(output_game_folder, output_def, built_files, log):
            zip_success = False

    if not zip_success:
        log.append("")
        log.append("Result: FAILED")
        log.append("Reason: ZIP creation failed.")

        failed_folder = FAILED_DIR / f"{safe_title} - {timestamp()}"
        failed_folder.mkdir(parents=True, exist_ok=True)

        log_path = failed_folder / f"{safe_title} extraction log.txt"
        log_path.write_text("\n".join(log) + "\n", encoding="utf-8")

        if output_game_folder.exists():
            shutil.rmtree(output_game_folder, ignore_errors=True)

        return GameProcessResult(
            game_id=game_id,
            title=title,
            success=False,
            status="FAILED",
            output_folder=failed_folder,
            log_path=log_path,
            reason="ZIP creation failed.",
        )

    log.append("")
    log.append("Result: SUCCESS")

    log_path = output_game_folder / f"{safe_title} extraction log.txt"
    log_path.write_text("\n".join(log) + "\n", encoding="utf-8")

    return GameProcessResult(
        game_id=game_id,
        title=title,
        success=True,
        status="SUCCESS",
        output_folder=output_game_folder,
        log_path=log_path,
    )


# ------------------------------------------------------------
# Display / reporting
# ------------------------------------------------------------

def print_paths() -> None:
    print()
    print("Paths:")
    print(f"  Extractor folder: {SCRIPT_DIR}")
    print(f"  Scan root:        {SCAN_ROOT}")
    print(f"  Modules folder:   {MODULES_DIR}")
    print(f"  Temp folder:      {TEMP_DIR}")
    print(f"  Output folder:    {OUTPUT_DIR}")
    print(f"  Backups folder:   {BACKUPS_DIR}")
    print(f"  Failed folder:    {FAILED_DIR}")
    print(f"  Batch logs folder:{BATCH_LOGS_DIR}")
    print()


def print_modules(modules: list[GameModule]) -> None:
    if not modules:
        print("No valid game modules found.")
        print(f"Expected modules in: {MODULES_DIR}")
        return

    print()
    print("Installed game modules:")
    print()

    for index, module in enumerate(modules, start=1):
        game = module.game
        game_id = game.get("id", "UNKNOWN")
        title = game.get("title", "UNKNOWN TITLE")
        mame_set = game.get("mame_set", "")

        suffix = f" [{mame_set}]" if mame_set else ""

        print(f"  [{index}] {title}{suffix}")
        print(f"      id:     {game_id}")
        print(f"      module: {module.module_path.name}")
        print()

    print()


def print_detection_results(results: list[DetectionResult]) -> None:
    print()
    print("Detection results:")
    print()

    for result in results:
        print(result.title)

        if result.found:
            print("  Status:        FOUND")
            print(f"  Found by:      {result.method}")
            print(f"  Game folder:   {result.game_folder}")
            print(f"  Source folder: {result.source_folder}")
        else:
            print("  Status:        NOT FOUND")
            print(f"  Reason:        {result.reason}")

        print()


def write_batch_log(results: list[GameProcessResult]) -> Path:
    batch_folder = BATCH_LOGS_DIR
    batch_folder.mkdir(parents=True, exist_ok=True)

    log_path = batch_folder / f"NeoGeo batch extraction - {timestamp()}.txt"

    lines: list[str] = []
    lines.append("NeoGeo Batch Extraction Log")
    lines.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")

    for status in ["SUCCESS", "FAILED", "NOT FOUND"]:
        matching = [result for result in results if result.status == status]

        lines.append(f"{status}:")
        if matching:
            for result in matching:
                lines.append(f"  - {result.title}")
                if result.reason:
                    lines.append(f"      Reason: {result.reason}")
                if result.log_path:
                    lines.append(f"      Log: {result.log_path}")
        else:
            lines.append("  none")
        lines.append("")

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log_path


# ------------------------------------------------------------
# Extraction wrappers
# ------------------------------------------------------------

def extract_one_game(module: GameModule) -> None:
    print()
    print(f"Processing: {module.game['title']}")

    result = process_game(module)

    print()
    print(f"Status: {result.status}")

    if result.reason:
        print(f"Reason: {result.reason}")

    if result.output_folder:
        print(f"Output folder: {result.output_folder}")

    if result.log_path:
        print(f"Log: {result.log_path}")


def extract_all_games(modules: list[GameModule]) -> None:
    if not modules:
        print("No valid game modules found.")
        return

    print()
    print("Batch extraction started.")
    print("Existing ZIP collection will run first across all top-level folders.")
    print("Rule: if neogeo.zip is found under a folder, copy all ZIPs from that folder.")

    collect_existing_zips_from_all_folders()

    results: list[GameProcessResult] = []

    for module in modules:
        print()
        print(f"Processing: {module.game['title']}")

        result = process_game(module, collect_existing_zips=False, backup_output=False)
        results.append(result)

        print(f"  Status: {result.status}")
        if result.reason:
            print(f"  Reason: {result.reason}")

    batch_log = write_batch_log(results)

    print()
    print("Batch extraction finished.")
    print(f"Batch log: {batch_log}")


# ------------------------------------------------------------
# Interactive menu
# ------------------------------------------------------------

def interactive_menu(modules: list[GameModule]) -> None:
    while True:
        print()
        print("NeoGeo MAME ROM Extractor")
        print()
        print("[1] Extract one game")
        print("[2] Extract all detected games")
        print("[3] Dry run / detect available games only")
        print("[4] List installed game modules")
        print("[5] Show paths")
        print("[6] Collect existing ZIPs from all folders")
        print("[Q] Quit")
        print()

        choice = input("Choose option: ").strip().casefold()

        if choice == "q":
            return

        if choice == "1":
            choose_one_game_menu(modules)
            continue

        if choice == "2":
            extract_all_games(modules)
            continue

        if choice == "3":
            results = detect_all_games(modules)
            print_detection_results(results)
            continue

        if choice == "4":
            print_modules(modules)
            continue

        if choice == "5":
            print_paths()
            continue

        if choice == "6":
            collect_existing_zips_from_all_folders()
            continue

        print("Invalid option.")


def choose_one_game_menu(modules: list[GameModule]) -> None:
    """
    Menu for selecting a single detected game.

    This only lists modules whose source folders are actually found.
    """
    if not modules:
        print("No valid game modules found.")
        return

    print()
    print("Scanning for detected games...")

    candidate_folders = iter_candidate_folders()

    detected_items: list[tuple[GameModule, DetectionResult]] = []

    for module in modules:
        result = detect_game_source(module, candidate_folders)

        if result.found:
            detected_items.append((module, result))

    if not detected_items:
        print()
        print("No detected games found.")
        print("Use dry-run to see which modules are not being found.")
        return

    detected_items.sort(
        key=lambda item: normalize_name(str(item[0].game.get("title", "")))
    )

    print()
    print("Detected games:")
    print()

    for index, (module, result) in enumerate(detected_items, start=1):
        title = module.game.get("title", "UNKNOWN TITLE")
        game_id = module.game.get("id", "UNKNOWN")
        print(f"[{index}] {title} ({game_id})")
        print(f"    Source: {result.source_folder}")
        print()

    print("[Q] Back")
    print()

    choice = input("Choose game: ").strip().casefold()

    if choice == "q":
        return

    try:
        selected_index = int(choice)
    except ValueError:
        print("Invalid option.")
        return

    if selected_index < 1 or selected_index > len(detected_items):
        print("Invalid option.")
        return

    selected_module, _selected_detection = detected_items[selected_index - 1]
    extract_one_game(selected_module)


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="NeoGeo modular ROM extractor framework."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan for available game sources without extracting.",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Extract all detected games.",
    )

    parser.add_argument(
        "--game",
        metavar="GAME_ID",
        help="Extract one game by module GAME id, for example: --game 3countb",
    )

    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="List installed game modules.",
    )

    parser.add_argument(
        "--show-paths",
        action="store_true",
        help="Show important framework paths.",
    )

    parser.add_argument(
        "--collect-existing-zips",
        action="store_true",
        help="Collect existing source ZIPs from all top-level folders without extracting.",
    )

    return parser.parse_args()


def find_module_by_id(modules: list[GameModule], game_id: str) -> GameModule | None:
    wanted = game_id.casefold()

    for module in modules:
        current_id = str(module.game.get("id", "")).casefold()

        if current_id == wanted:
            return module

    return None


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main() -> int:
    ensure_base_folders()

    args = parse_args()
    modules = load_game_modules()

    if args.show_paths:
        print_paths()
        return 0

    if args.list_modules:
        print_modules(modules)
        return 0

    if args.collect_existing_zips:
        collect_existing_zips_from_all_folders()
        return 0

    if args.dry_run:
        results = detect_all_games(modules)
        print_detection_results(results)
        return 0

    if args.all:
        extract_all_games(modules)
        return 0

    if args.game:
        module = find_module_by_id(modules, args.game)

        if module is None:
            print(f"No module found with id: {args.game}")
            print_modules(modules)
            return 1

        extract_one_game(module)
        return 0

    interactive_menu(modules)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
