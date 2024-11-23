import argparse
import json
import time
from pathlib import Path
from random import randrange

import PyPDF2
import requests
from pdfminer.high_level import extract_text
from tqdm import tqdm


def load_episode_urls():
    """Load episode URLs from JSON file."""
    config_path = Path("episode_urls.json")
    if not config_path.exists():
        raise FileNotFoundError("episode_urls.json not found")

    with open(config_path, "r") as f:
        urls = json.load(f)
    return urls


def natural_sort_key(episode_num):
    """Create a key for natural sorting of episode numbers."""
    if episode_num == "12_13":
        return 12.5  # Place between 12 and 13
    return float(episode_num)


def setup_directories():
    """Create cache directory if it doesn't exist."""
    cache_dir = Path("wolf_359_scripts")
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_episode_filename(episode_num, url):
    """Generate filename for an episode."""
    return f"episode_{str(episode_num).zfill(2)}_{Path(url).name}"


def download_episode(url, output_path, session):
    """Download a single episode if it doesn't exist."""
    if output_path.exists():
        return "Cached"

    response = session.get(url, stream=True)
    response.raise_for_status()
    time.sleep(randrange(1, 4))
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return "Downloaded"


def should_include_episode(episode_num, start_episode, end_episode):
    """Determine if an episode should be included based on episode range."""
    if episode_num == "12_13":
        return start_episode <= 12 and end_episode >= 12
    episode_float = float(episode_num)
    return start_episode <= episode_float <= end_episode


def download_episodes(start_episode, end_episode, cache_dir, episode_urls):
    """Download all episodes within the specified range."""
    downloaded_files = []
    filtered_episodes = {
        k: v
        for k, v in episode_urls.items()
        if should_include_episode(k, start_episode, end_episode)
    }

    with requests.Session() as session:
        with tqdm(total=len(filtered_episodes), desc="Downloading episodes") as pbar:
            for episode_num in sorted(filtered_episodes.keys(), key=natural_sort_key):
                url = filtered_episodes[episode_num]
                filename = get_episode_filename(episode_num, url)
                output_path = cache_dir / filename

                try:
                    status = download_episode(url, output_path, session)
                    downloaded_files.append((episode_num, output_path))
                    pbar.set_description(f"Episode {episode_num} ({status})")
                except requests.RequestException as e:
                    print(f"\nError downloading episode {episode_num}: {e}")
                    continue

                pbar.update(1)

    # Sort files by episode number and return tuples of (episode_num, path)
    return sorted(downloaded_files, key=lambda x: natural_sort_key(x[0]))


def combine_pdfs(episode_files, output_path):
    """Combine multiple PDFs into one file with bookmarks."""
    merger = PyPDF2.PdfMerger()

    with tqdm(total=len(episode_files), desc="Combining PDFs") as pbar:
        current_page = 0
        for episode_num, pdf_file in episode_files:
            try:
                # Add file and create bookmark
                bookmark_title = f"Episode {episode_num}"
                merger.append(pdf_file, import_outline=True)
                merger.add_outline_item(bookmark_title, current_page)

                # Update current page number
                with open(pdf_file, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    current_page += len(pdf_reader.pages)

                pbar.update(1)
            except Exception as e:
                print(f"\nError processing {pdf_file}: {e}")
                continue

    merger.write(str(output_path))
    merger.close()


def convert_to_markdown(pdf_path, markdown_path):
    """Convert PDF to markdown format."""
    try:
        print("Converting PDF to markdown... This may take a while.")
        text = extract_text(str(pdf_path))
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Created markdown file: {markdown_path}")
    except Exception as e:
        print(f"Error converting to markdown: {e}")


def main():
    parser = argparse.ArgumentParser(description="Wolf 359 Script Combiner")
    parser.add_argument(
        "--start_episode",
        type=int,
        default=1,
        help="Starting episode number (default: 1)",
    )
    parser.add_argument("--end_episode", type=int, help="Ending episode number")
    parser.add_argument(
        "--convert_markdown", action="store_true", help="Convert final PDF to markdown"
    )
    args = parser.parse_args()

    try:
        # Load episode URLs
        episode_urls = load_episode_urls()

        # Setup cache directory
        cache_dir = setup_directories()

        # Set end episode if not provided
        end_episode = (
            args.end_episode
            if args.end_episode
            else max(natural_sort_key(ep) for ep in episode_urls.keys())
        )

        # Validate episode range
        max_available = max(natural_sort_key(ep) for ep in episode_urls.keys())
        if args.start_episode < 1 or end_episode > max_available:
            print(f"Error: Episode range must be between 1 and {int(max_available)}")
            return

        if args.start_episode > end_episode:
            print("Error: Start episode cannot be greater than end episode")
            return

        # Download/cache episodes and get sorted list of files
        episode_files = download_episodes(
            args.start_episode, end_episode, cache_dir, episode_urls
        )

        if not episode_files:
            print("No files were downloaded. Exiting.")
            return

        # Combine PDFs - save in current directory
        combined_pdf = Path(
            f"wolf359_episodes_{args.start_episode}_to_{int(end_episode)}.pdf"
        )
        combine_pdfs(episode_files, combined_pdf)

        # Convert to markdown if requested - save in current directory
        if args.convert_markdown:
            markdown_path = Path(
                f"wolf359_episodes_{args.start_episode}_to_{int(end_episode)}.md"
            )
            convert_to_markdown(combined_pdf, markdown_path)

        print("Processing complete!")
        print(f"Combined PDF saved as: {combined_pdf}")
        if args.convert_markdown:
            print(f"Markdown version saved as: {markdown_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure episode_urls.json is in the same directory as the script.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
