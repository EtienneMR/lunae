def indent(obj) -> str:
    """
    Indent each line of the str(obj) by a tab for pretty printing.
    """
    return "\n".join(f"  {l}" for l in str(obj).split("\n"))
