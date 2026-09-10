#!/usr/bin/env python3
"""
Convert Notion markdown export to Next.js MDX format.

This script handles:
1. Extracting title from the highest-level heading
2. Adding MDX frontmatter metadata
3. Converting bullet lists to <details>/<summary> blocks (interactive mode)
4. Downloading Notion images and updating references
"""

import re
import sys
import os
import requests
from pathlib import Path


def extract_title(content):
    """Extract the first top-level heading (# Title) as the title."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"


def extract_bullet_lists(content):
    """Extract all bullet list sections from the content."""
    lines = content.split('\n')
    bullet_sections = []
    current_section = []
    in_bullet_list = False
    start_idx = 0

    for i, line in enumerate(lines):
        is_bullet = re.match(r'^[\s]*[-*]\s+', line)

        if is_bullet:
            if not in_bullet_list:
                start_idx = i
                in_bullet_list = True
            current_section.append(line)
        else:
            if in_bullet_list and current_section:
                bullet_sections.append({
                    'content': '\n'.join(current_section),
                    'start_line': start_idx,
                    'end_line': i - 1
                })
                current_section = []
                in_bullet_list = False

    # Don't forget the last section if it ends with bullets
    if in_bullet_list and current_section:
        bullet_sections.append({
            'content': '\n'.join(current_section),
            'start_line': start_idx,
            'end_line': len(lines) - 1
        })

    return bullet_sections


def prompt_for_details_conversion(bullet_sections, content):
    """
    Interactive prompt to convert bullet lists to <details> blocks.

    Returns the converted content.
    """
    if not bullet_sections:
        return content

    lines = content.split('\n')
    replacements = []

    print("\n" + "="*60)
    print("EXPANDABLE DROPDOWN CONVERSION")
    print("="*60)
    print("\nFound bullet list sections that might be expandable dropdowns.")
    print("For each section, specify if it should be converted to <details>.\n")

    for idx, section in enumerate(bullet_sections, 1):
        print(f"\n--- Section {idx} (lines {section['start_line']}-{section['end_line']}) ---")
        print(section['content'][:200] + ("..." if len(section['content']) > 200 else ""))
        print()

        response = input(f"Convert this to expandable dropdown? (y/n): ").strip().lower()

        if response == 'y':
            summary = input("Enter the summary text (what appears when collapsed): ").strip()
            if summary:
                details_content = '\n'.join([
                    '<details>',
                    f'  <summary>{summary}</summary>',
                    '  ',
                    section['content'],
                    '</details>'
                ])
                replacements.append((
                    section['start_line'],
                    section['end_line'],
                    details_content
                ))

    # Apply replacements in reverse order to maintain line numbers
    for start_line, end_line, replacement in reversed(replacements):
        lines[start_line:end_line + 1] = [replacement]

    return '\n'.join(lines)


def add_frontmatter(content, title):
    """Add MDX frontmatter with title metadata."""
    frontmatter = f"""---
title: "{title}"
---

"""
    return frontmatter + content


def extract_notion_images(content):
    """
    Extract Notion image attachments from markdown content.

    Returns list of dicts with 'attachment_id', 'filename', 'alt_text', and 'full_match'.
    """
    # Pattern: ![text](attachment:UUID:filename)
    pattern = r'!\[([^\]]*)\]\(attachment:([a-f0-9\-]+):([^\)]+)\)'
    matches = re.finditer(pattern, content)

    images = []
    for match in matches:
        images.append({
            'alt_text': match.group(1),
            'attachment_id': match.group(2),
            'filename': match.group(3),
            'full_match': match.group(0)
        })

    return images


def fetch_notion_blocks(page_id, notion_api_key):
    """Fetch all blocks from a Notion page."""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch Notion blocks: {response.status_code} - {response.text}")

    return response.json()


def find_image_url_by_attachment_id(blocks_data, attachment_id):
    """Find the signed image URL for a specific attachment ID."""
    if not blocks_data or 'results' not in blocks_data:
        return None

    for block in blocks_data['results']:
        if block['type'] == 'image':
            if block['image']['type'] == 'file':
                url = block['image']['file']['url']
                if attachment_id in url:
                    return url
            elif block['image']['type'] == 'external':
                url = block['image']['external']['url']
                if attachment_id in url:
                    return url

    return None


def generate_image_filename(attachment_id, original_filename):
    """Generate a filename using the Notion attachment ID."""
    # Get extension from original filename
    ext = Path(original_filename).suffix or '.png'

    # Use the attachment ID as the filename
    return f"{attachment_id}{ext}"


def download_notion_images(content, page_id, notion_api_key, output_dir, repo_root):
    """
    Download all Notion images and update markdown references.

    Args:
        content: Markdown content
        page_id: Notion page ID
        notion_api_key: Notion API key
        output_dir: Directory to save images (relative to repo root, e.g. "public/images")
        repo_root: Root directory of the repository

    Returns:
        Updated content with local image references
    """
    # Extract all Notion images from markdown
    images = extract_notion_images(content)

    if not images:
        return content

    print(f"\n📷 Found {len(images)} Notion image(s), downloading...")

    # Fetch blocks from Notion (single API call)
    try:
        blocks_data = fetch_notion_blocks(page_id, notion_api_key)
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch Notion blocks: {e}")
        print("   Skipping image downloads")
        return content

    # Create output directory with from-notion subfolder
    images_dir = Path(repo_root) / output_dir / "from-notion"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Download each image
    for image in images:
        attachment_id = image['attachment_id']

        # Find the signed S3 URL for this attachment
        image_url = find_image_url_by_attachment_id(blocks_data, attachment_id)

        if not image_url:
            print(f"⚠️  Warning: Could not find URL for attachment {attachment_id}")
            continue

        # Generate filename using attachment ID
        filename = generate_image_filename(attachment_id, image['filename'])
        output_path = images_dir / filename

        # Download image
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                output_path.write_bytes(response.content)
                size_kb = len(response.content) / 1024
                print(f"   ✓ Downloaded: {filename} ({size_kb:.1f}KB)")

                # Update content with local reference
                # Remove 'public/' prefix for Next.js URL (public folder is served from root)
                url_path = output_dir.replace('public/', '', 1) if output_dir.startswith('public/') else output_dir
                new_reference = f"![{image['alt_text']}](/{url_path}/from-notion/{filename})"
                content = content.replace(image['full_match'], new_reference)
            else:
                print(f"⚠️  Warning: Failed to download {filename}: HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️  Warning: Error downloading {filename}: {e}")

    return content


def convert_notion_to_mdx(input_path, output_path=None, interactive=True,
                          notion_page_id=None, notion_api_key=None, repo_root=None):
    """
    Convert a Notion markdown file to Next.js MDX format.

    Args:
        input_path: Path to input markdown file
        output_path: Path to output MDX file (optional, defaults to input path)
        interactive: Whether to prompt for details conversion (default: True)
        notion_page_id: Notion page ID for downloading images (optional)
        notion_api_key: Notion API key for downloading images (optional)
        repo_root: Repository root directory for saving images (optional)

    Returns:
        The converted content as a string
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Read the content
    content = input_file.read_text(encoding='utf-8')

    # Extract title from first heading
    title = extract_title(content)

    # Download Notion images if credentials provided
    if notion_page_id and notion_api_key and repo_root:
        content = download_notion_images(
            content, notion_page_id, notion_api_key,
            "public/images", repo_root
        )

    # Handle expandable dropdowns (interactive)
    if interactive:
        bullet_sections = extract_bullet_lists(content)
        if bullet_sections:
            content = prompt_for_details_conversion(bullet_sections, content)

    # Add frontmatter
    content = add_frontmatter(content, title)

    # Write to output file
    if output_path is None:
        output_path = input_path

    output_file = Path(output_path)
    output_file.write_text(content, encoding='utf-8')

    print(f"\n✅ Conversion complete!")
    print(f"   Title: {title}")
    print(f"   Output: {output_path}")

    return content


def load_env_file(env_path):
    """Load environment variables from .env.local file."""
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars

    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_notion_to_mdx.py <input_file> [output_file] [--page-id PAGE_ID]")
        print("\nExample:")
        print("  python convert_notion_to_mdx.py notion_export.md")
        print("  python convert_notion_to_mdx.py notion_export.md page.mdx")
        print("  python convert_notion_to_mdx.py page.mdx --page-id 1f82e4fe580280a29479cba5d8ffa898")
        print("\nNote: NOTION_API_KEY will be read from .env.local if available")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = None
    page_id = None

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--page-id' and i + 1 < len(sys.argv):
            page_id = sys.argv[i + 1]
            i += 2
        else:
            output_path = sys.argv[i]
            i += 1

    # Try to load Notion API key from .env.local
    repo_root = Path(input_path).parent
    while repo_root != repo_root.parent:
        env_file = repo_root / '.env.local'
        if env_file.exists():
            env_vars = load_env_file(env_file)
            notion_api_key = env_vars.get('NOTION_API_KEY')
            if page_id and notion_api_key:
                print(f"✓ Found Notion API key in {env_file}")
                print(f"✓ Using page ID: {page_id}")
            break
        repo_root = repo_root.parent
    else:
        notion_api_key = None
        repo_root = Path(input_path).parent

    try:
        convert_notion_to_mdx(
            input_path, output_path, interactive=True,
            notion_page_id=page_id, notion_api_key=notion_api_key,
            repo_root=repo_root
        )
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
