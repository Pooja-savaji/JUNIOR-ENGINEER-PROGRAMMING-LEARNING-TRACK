"""
string_utils.py
===============
Text-transformation and analysis helpers extracted from text_formatter.py.
"""

import textwrap
import re


def to_upper(text: str) -> str:
    """Return *text* converted to UPPER CASE."""
    return text.upper()


def to_lower(text: str) -> str:
    """Return *text* converted to lower case."""
    return text.lower()


def to_title_case(text: str) -> str:
    """Return *text* in Title Case."""
    return text.title()


def to_camel_case(text: str) -> str:
    """Convert a space- or underscore-separated string to camelCase.

    Example: "hello world" -> "helloWorld"
    """
    words = re.split(r"[\s_]+", text.strip())
    if not words:
        return ""
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def to_snake_case(text: str) -> str:
    """Convert a string to snake_case.

    Example: "Hello World" -> "hello_world"
    """
    return re.sub(r"[\s]+", "_", text.strip().lower())


def to_kebab_case(text: str) -> str:
    """Convert a string to kebab-case.

    Example: "Hello World" -> "hello-world"
    """
    return re.sub(r"[\s_]+", "-", text.strip().lower())


def generate_slug(text: str) -> str:
    """Generate a URL-friendly slug from *text*.

    Removes non-alphanumeric characters and replaces spaces with hyphens.
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")


def wrap_text(text: str, width: int = 60) -> str:
    """Wrap *text* to at most *width* characters per line."""
    return textwrap.fill(text, width=width)


def analyze_text(text: str) -> dict:
    """Return a dict with basic statistics about *text*.

    Keys: characters, words, sentences, paragraphs, unique_words
    """
    words = text.split()
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    unique_words = set(w.lower().strip(".,!?;:\"'") for w in words)
    return {
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "unique_words": len(unique_words),
    }
