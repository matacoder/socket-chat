async def string_sanitizer(string: str):
    return string.replace("\n", "\\n")
