def string_sanitizer(string: str):
    """Clean text from forbidden characters."""
    return string.replace("\n", "\\n")
