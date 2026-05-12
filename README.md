# NeoGeo ROM Extractor

A modular, preservation-focused Python extractor for rebuilding verified Neo Geo ROM ZIPs from supported legally owned PC releases.

This project is designed to help users extract ROM data from game releases they already own, then rebuild emulator-ready Neo Geo ROM ZIPs using per-game extraction modules.

## Project Status

This project is in active development.

Supported games are added through individual game modules in the `game_modules/` folder. Each module defines the source layout, expected file slices, output names, hashes, and any game-specific extraction behaviour required for that title.

## Currently Supported Games

The following game modules are currently included:

- Alpha Mission II
- Art of Fighting 3
- Crossed Swords
- Ghost Pilots
- King of the Monsters 2
- Last Blade 2
- Last Resort
- Magician Lord
- Mutation Nation
- Ninja Commando
- Ninja Master's
- Over Top
- Robo Army
- Samurai Shodown IV
- Sengoku
- Sengoku 2
- Soccer Brawl
- Super Sidekicks
- The Super Spy
- Three Count Bout
- Top Hunter

## Features

- Modular per-game extraction system
- General-purpose extraction core
- Game-specific logic kept inside game modules
- Hash-based file verification
- Output ZIP creation for supported Neo Geo titles
- Designed for preservation and personal-use extraction workflows
- No ROMs, BIOS files, or copyrighted game assets included

## Supported Sources

This extractor is intended for supported PC releases of Neo Geo games, such as legally purchased storefront releases where the required source data is available locally.

Support varies per game. Each supported title requires a matching game module.

## Project Structure

```text
NeoGeo ROM Extractor/
├── neogeo_extractor.py
├── game_modules/
│   ├── __init__.py
│   ├── alpha_mission_ii.py
│   ├── art_of_fighting_3.py
│   ├── crossed_swords.py
│   └── ...
├── .gitignore
├── README.md
└── LICENSE
```

## Requirements

- Python 3.10 or newer recommended
- A legally owned supported game release
- Local access to the required source files for that game

No ROMs or copyrighted files are provided by this project.

## Basic Usage

Run the extractor from the command line:

```bash
python3 neogeo_extractor.py
```

Depending on the current version of the script, you may need to provide a source folder and output folder.

Example on macOS or Linux:

```bash
python3 neogeo_extractor.py /path/to/source/files /path/to/output
```

Example on Windows:

```powershell
python neogeo_extractor.py "C:\Path\To\Source\Files" "C:\Path\To\Output"
```

## Game Modules

Each game module lives in:

```text
game_modules/
```

Game-specific information belongs in the relevant module, not in the core extractor.

Examples of game-specific data include:

- source filenames
- ROM slice offsets
- expected CRC32 values
- expected SHA-256 values, where used
- output ROM names
- patch rules
- game-specific quirks
- notes about unusual source layouts

The main extractor should remain as generic as possible.

## Output

The extractor creates rebuilt ROM ZIPs for supported games when the source files match the expected data.

Where applicable, the extractor may also create preservation-oriented secondary outputs, such as original/unmodified file ZIPs, if a supported source requires patching or correction.

Output files are generated locally and are not included in this repository.

## Verification

This project is verification-focused.

Where possible, extracted files are checked against expected hashes before final ZIP creation. If source files do not match the expected data, the extractor should fail rather than silently creating incorrect output.

## What This Project Does Not Include

This repository does not include:

- Neo Geo ROMs
- Neo Geo BIOS files
- MAME ROM sets
- game executables
- Steam, GOG, or Amazon game data
- copyrighted assets
- decryption keys
- tools for downloading games
- instructions for piracy

## License

This project is released under the license specified in the `LICENSE` file.

If no license has been added yet, all rights are reserved by default. Add a license before allowing public reuse, modification, or redistribution of the code.

Recommended options:

- **MIT License** — simple and permissive
- **GPLv3** — requires modified versions to remain open source
- **Apache 2.0** — permissive, with explicit patent language

Choose the license that matches how you want others to use the project.

## Disclaimer

This project is provided for educational, preservation, and personal backup purposes.

The author is not responsible for how users obtain, use, distribute, or handle copyrighted material. Users are responsible for complying with all applicable laws in their own country or region.

## Contributing

Contributions may be considered once the project structure has stabilised.

Useful contributions include:

- new game modules
- hash verification improvements
- clearer error messages
- documentation improvements
- testing against legally owned releases

Do not submit ROMs, BIOS files, copyrighted game data, or proprietary assets.

## Suggested GitHub Topics

```text
neogeo neo-geo snk rom-extractor rom-extraction game-preservation digital-preservation python emulation-tools arcade retro-gaming mame
```

## Legal Notice

This project does **not** include, distribute, download, or provide access to ROMs, BIOS files, game executables, game data, or any other copyrighted assets.

You must provide your own legally obtained source files.

This tool is intended for users who own the relevant games and want to extract their own local copies for personal use, preservation, backup, or emulator compatibility.

Do not use this project to obtain, distribute, or share copyrighted game data that you do not have the legal right to use.

The author does not endorse piracy or copyright infringement.