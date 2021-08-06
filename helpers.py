def sanitize_string(string: str):
    """Clean text from forbidden characters."""
    return string.replace("\n", "\\n")
