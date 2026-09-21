"""Comprehensive Text Formatter and String Utilities in Pure Python.

Covers: string manipulation methods, casing transformations, slugification,
word-wrapping, alignment formatting, and lexical analysis statistics.
"""

import re
from typing import Dict, List


def to_title_case(text: str) -> str:
    """Format string to Title Case while keeping standard small words lowercase."""
    small_words = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on", "or", "the", "to", "up"}
    words = text.strip().split()
    if not words:
        return ""

    result = []
    for i, word in enumerate(words):
        w_lower = word.lower()
        if i == 0 or i == len(words) - 1 or w_lower not in small_words:
            result.append(word.capitalize())
        else:
            result.append(w_lower)
    return " ".join(result)


def to_camel_case(text: str) -> str:
    """Convert text to camelCase (e.g. 'hello world' -> 'helloWorld')."""
    words = re.sub(r"[^a-zA-Z0-9]+", " ", text).split()
    if not words:
        return ""
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase (e.g. 'hello world' -> 'HelloWorld')."""
    words = re.sub(r"[^a-zA-Z0-9]+", " ", text).split()
    return "".join(w.capitalize() for w in words)


def to_snake_case(text: str) -> str:
    """Convert text to snake_case (e.g. 'Hello World!' -> 'hello_world')."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", " ", text).strip()
    return "_".join(cleaned.lower().split())


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case (e.g. 'Hello World!' -> 'hello-world')."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", " ", text).strip()
    return "-".join(cleaned.lower().split())


def generate_slug(text: str) -> str:
    """Generate a clean, URL-safe slug from a heading or title."""
    return to_kebab_case(text)


def wrap_text(text: str, width: int = 60) -> str:
    """Wrap text to a specified maximum column width preserving whole words."""
    words = text.split()
    if not words:
        return ""

    lines: List[str] = []
    current_line: List[str] = []
    current_length = 0

    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)


def analyze_text(text: str) -> Dict[str, object]:
    """Perform lexical analysis returning counts and estimates."""
    clean = text.strip()
    if not clean:
        return {
            "characters_with_spaces": 0,
            "characters_without_spaces": 0,
            "words": 0,
            "sentences": 0,
            "lines": 0,
            "estimated_reading_time_sec": 0,
        }

    words = clean.split()
    sentences = [s for s in re.split(r"[.!?]+", clean) if s.strip()]
    lines = clean.splitlines()

    word_count = len(words)
    # Average adult reading speed: ~200-250 words per minute (~3.5 words/sec)
    reading_time_sec = round((word_count / 200) * 60)

    return {
        "characters_with_spaces": len(text),
        "characters_without_spaces": len(text.replace(" ", "").replace("\n", "")),
        "words": word_count,
        "sentences": len(sentences),
        "lines": len(lines),
        "estimated_reading_time_sec": reading_time_sec,
    }


def run_text_formatter_cli():
    """Interactive CLI menu for text operations."""
    print("=" * 55)
    print("           🔤 PYTHON TEXT FORMATTER               ")
    print("=" * 55)

    sample_text = "The quick brown fox jumps over the lazy dog."

    while True:
        print("\nOperations:")
        print("  1. 🔠 Transform Casing (Title, Camel, Snake, Kebab, Pascal)")
        print("  2. 🔗 Generate URL Slug")
        print("  3. 📐 Wrap Text to Width")
        print("  4. 📊 Analyze Text Statistics")
        print("  0. 🚪 Exit")

        choice = input("\nEnter choice (0-4): ").strip()

        if choice == "0":
            print("\nThank you for using Text Formatter! Goodbye! 👋\n")
            break

        text_input = input("\nEnter text to format (or press Enter for sample): ").strip()
        text = text_input if text_input else sample_text

        if choice == "1":
            print("\n" + "=" * 50)
            print("                 CASING TRANSFORMS                ")
            print("=" * 50)
            print(f"Original    : {text}")
            print(f"Title Case  : {to_title_case(text)}")
            print(f"camelCase   : {to_camel_case(text)}")
            print(f"PascalCase  : {to_pascal_case(text)}")
            print(f"snake_case  : {to_snake_case(text)}")
            print(f"kebab-case  : {to_kebab_case(text)}")
            print("=" * 50)

        elif choice == "2":
            slug = generate_slug(text)
            print(f"\nSlug: {slug}")

        elif choice == "3":
            try:
                width_in = input("Enter column width (default 40): ").strip()
                width = int(width_in) if width_in else 40
                wrapped = wrap_text(text, width)
                print(f"\nWrapped at {width} columns:")
                print("-" * width)
                print(wrapped)
                print("-" * width)
            except ValueError:
                print("[Error] Please enter a valid integer for width.")

        elif choice == "4":
            stats = analyze_text(text)
            print("\n" + "=" * 45)
            print("               TEXT ANALYSIS              ")
            print("=" * 45)
            print(f"Characters (with spaces)    : {stats['characters_with_spaces']}")
            print(f"Characters (without spaces) : {stats['characters_without_spaces']}")
            print(f"Total Words                 : {stats['words']}")
            print(f"Sentences                   : {stats['sentences']}")
            print(f"Lines                       : {stats['lines']}")
            print(f"Est. Reading Time           : ~{stats['estimated_reading_time_sec']}s")
            print("=" * 45)


if __name__ == "__main__":
    run_text_formatter_cli()
