import shlex


def parse_stdout_redirect(parts: list[str]) -> tuple[list[str], str | None]:
    result = []
    stdout_file = None
    i = 0

    while i < len(parts):
        if parts[i] in (">", "1>"):
            stdout_file = parts[i + 1]
            i += 2
        else:
            result.append(parts[i])
            i += 1

    return result, stdout_file


def parse_input(line, home):
    parts = shlex.split(line)

    if not parts:
        return "", [], None

    parts, stdout_file = parse_stdout_redirect(parts)

    parts = [
        part.replace("~", home) if part.startswith("~") else part
        for part in parts
    ]
    if stdout_file and stdout_file.startswith("~"):
        stdout_file = stdout_file.replace("~", home)

    return parts[0], parts[1:], stdout_file
