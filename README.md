# NeoGeo ROM Extractor 

A modular, preservation-focused Python extractor for rebuilding verified Neo Geo ROM ZIPs from supported legally owned PC releases.

This project is designed to help users extract ROM data from game releases they already own, then rebuild emulator-ready Neo Geo ROM ZIPs using per-game extraction modules.

## Project Status 

This project is in active development.

Supported games are added through individual game modules in the `game_modules/` folder. Each module defines the source layout, expected file slices, output names, hashes, and any game-specific extraction behaviour required for that title.

## Currently Supported Games 

The following games are supported (29 in total so far):

- 3 Count Bout
- Alpha Mission II
- Art of Fighting 3
- Crossed Swords
- Ghost Pilots
- King of the Monsters 2
- Kizuna Encounter - Super Tag Battle
- Last Resort
- Magician Lord
- Metal Slug
- Metal Slug 2
- Metal Slug 3?? (Currently Working On, Not Yet Implimented)
- Metal Slug 4
- Metal Slug X
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
- The King of Fighters 2003
- The Last Blade
- The Last Blade 2
- The Super Spy
- Top Hunter
- Twinkle Star Sprites

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
- expected SHA1 values
- output ROM names
- patch rules
- game-specific quirks
- notes about unusual source layouts

The main extractor should remain as generic as possible.

## Output 

The extractor creates rebuilt ROM ZIPs for supported games when the source files match the expected data.

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

## Credits and Acknowledgements

This project was informed by, adapted from, or cross-checked against earlier Neo Geo extraction, conversion, preservation, and emulation work.

Some sources were used as direct implementation references. Others were used for research, comparison, testing, or validation only. Inclusion here does not necessarily mean that code from that source is included in this repository.

### Projects and code references

The following projects were useful while developing this extractor:

- [NGPrimeClaim](https://github.com/Lx32/NGPrimeClaim) by Lx32
- [mslug-rom-extractor](https://github.com/terminatorhex/mslug-rom-extractor) by terminatorhex
- [goNCommand](https://github.com/lioneltrs/goNCommand) by Lionel Cordesses

Where code, logic, offsets, extraction layouts, patch behaviour, conversion behaviour, or command-line workflows have been adapted from these projects, credit should also remain in the relevant source files or game modules.

### Research notes and discussions

The following public notes, blog posts, scripts, and discussions were also used for research, comparison, or cross-checking:

- [goNCommand issue #13](https://github.com/lioneltrs/goNCommand/issues/13)
- alhumbra’s notes: https://milkchoco.info/archives/8695
- scrap-a’s notes: http://blog.livedoor.jp/scrap_a/archives/37910430.html
- Tomasz Bednarz’s related work and notes, 2023
- Lionel Cordesses’ KOF 2003 extraction/build script work, 2025

These references were especially useful for understanding The King of Fighters 2003, CMC-related processing, encrypted Neo Geo content, and ROM-set reconstruction.

### Tools, algorithms, and reimplemented processing

Some extraction steps use, reproduce, or reimplement behaviour from earlier tools, scripts, or commercial release workflows.

- `neo-cmc` is used or referenced for CMC-related Neo Geo processing.
- `tileswap` logic is used or reimplemented for graphics/tile data rearrangement where required.
- `tiles2crom` logic is used or reimplemented for converting tile data into Neo Geo C-ROM-compatible output where required.
- `unswizzle` logic was initially based largely on NGPrimeClaim and has been adapted for this project.
- For Metal Slug 3, parts of the Python implementation were developed by studying and replacing the behaviour of the original `prog.exe` workflow from the legally obtained release.

Where these behaviours are implemented in this repository, the relevant source files should also include local credit comments explaining which external project, tool, script, or workflow informed that implementation.

This project does not redistribute `prog.exe`, commercial game executables, ROMs, BIOS files, encryption keys, or copyrighted game assets.

### Emulator and validation references

Extracted files are checked against known emulator-compatible ROM layouts, names, sizes, and hashes where possible. Thanks are due to the contributors and maintainers of:

- [MAME](https://www.mamedev.org/)
- [FBNeo](https://github.com/finalburnneo/FBNeo)

Their ROM definitions, naming conventions, hash records, and long-term hardware documentation work are important validation references for this project.

### Affiliation disclaimer

This repository is not affiliated with, endorsed by, or maintained by SNK, Amazon, GOG, Steam, DotEmu, Code Mystics, MAME, FBNeo, Lx32, terminatorhex, Lionel Cordesses, Shigeshigeru, alhumbra, scrap-a, Tomasz Bednarz, or any other referenced project, contributor, publisher, distributor, or rights holder.

Use of a source as a reference does not necessarily mean this repository contains code from that source. Some sources were used only for comparison, verification, or background research.

Any mistakes, omissions, or project-specific implementation choices in this repository are my own.

### Affiliation disclaimer for credited sources (new)

This repository is not affiliated with, endorsed by, or maintained by SNK, Amazon, GOG, Steam, DotEmu, Code Mystics, MAME, FBNeo, Lx32, terminatorhex, Lionel Cordesses, Shigeshigeru, alhumbra, scrap-a, Tomasz Bednarz, or any other referenced project, contributor, publisher, distributor, or rights holder.

Use of a source as a reference does not necessarily mean this repository contains code from that source. Some sources were used only for comparison, verification, or background research.

Any mistakes, omissions, or project-specific implementation choices in this repository are my own.

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

## License (GPLv3) 

This project is released under the GPLv3 license, specified in the `LICENSE` file.

You may use, modify, and redistribute this extractor, but if you redistribute it or modify versions, you must keep it under GPLv3 and provide the source code.
