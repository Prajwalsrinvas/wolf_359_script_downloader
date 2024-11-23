# 🚀 Wolf 359 Script Downloader

Welcome to the [Wolf 359](https://wolf359.fm/) Script Downloader! This tool helps you explore the amazing world of Wolf 359 through its official scripts, whether you're caught up or still making your way through the series.

## About Wolf 359

Wolf 359 is a brilliant radio drama that follows the dysfunctional crew of the U.S.S. Hephaestus space station. Set 7.8 light years from Earth, the crew faces daily life-or-death emergencies while searching for signs of alien life—and discovers there might be more to their mission than they thought.

## Features

- 📥 Downloads [episode scripts](https://wolf359.fm/extras) from the official Wolf 359 website
- 🔖 Combines multiple episodes into a single, bookmarked PDF
- 📝 Converts scripts to markdown format for easy text analysis
- ⚡ Caches downloaded scripts to avoid unnecessary downloads
- 🛡️ Flexible episode range selection to avoid spoilers
- 🤖 LLM-friendly output format

## Installation

```bash
# Clone the repository
git clone https://github.com/Prajwalsrinvas/wolf_359_script_downloader.git

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Download all episodes
python wolf_359_script_downloader.py

# Download a specific range of episodes (great for avoiding spoilers!)
python wolf_359_script_downloader.py --start_episode 5 --end_episode 15

# Download episodes up to a certain point
python wolf_359_script_downloader.py --end_episode 28

# Convert to markdown for LLM analysis
python wolf_359_script_downloader.py --start_episode 5 --end_episode 15 --convert_markdown
```

### Output Files

The script creates two types of files:
- `wolf359_episodes_X_to_Y.pdf`: Combined PDF with bookmarks
- `wolf359_episodes_X_to_Y.md`: Markdown version (if requested)

### Caching

Downloaded scripts are cached in the `wolf_359_scripts` directory. This means:
- No unnecessary downloads when experimenting with different episode ranges
- Faster execution on subsequent runs
- Less load on the Wolf 359 website servers

## Fun Things You Can Do!

### 1. Episode Discussion Companion
Download specific story arcs or seasons:
```bash
# Download Season 1 (Episodes 1-12)
python wolf_359_script_downloader.py --start_episode 1 --end_episode 12 --convert_markdown

# Track a specific story arc
python wolf_359_script_downloader.py --start_episode 15 --end_episode 20 --convert_markdown
```

### 2. LLM Analysis
Use the markdown output with your favorite LLM to:
- Get episode summaries
- Track character development
- Analyze plot points
- Search for specific scenes or dialogue
- Create episode guides

Example prompts for your LLM:
- "Summarize the key events in episodes 10-15"
- "Track Eiffel's character development throughout these episodes"
- "What are all the mentions of Plant Monster?"
- "Create a timeline of important events"

### 3. Study the Craft
Use the scripts to study:
- Radio drama writing techniques
- Character development
- Plot structure
- Dialogue writing

## Technical Details

The script:
1. Loads episode URLs from the included `episode_urls.json`
2. Downloads PDFs with appropriate delays to be nice to the server
3. Combines them into a single PDF with bookmarks
4. Optionally converts to markdown for text analysis

## Credits

Wolf 359 is created by Gabriel Urbina, Sarah Shachat, and Zach Valenti. All rights to the scripts and content belong to the original creators. Visit [wolf359.fm](https://wolf359.fm) for more information about the show.

This tool is a fan project designed to help listeners explore and enjoy the amazing world of Wolf 359. Please support the official release!

---

*"Dear listeners..." - Doug Eiffel, probably*