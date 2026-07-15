import shlex


def parse_redirects(parts: list[str]) -> tuple[list[str], str | None, str | None]:
    result = []
    stdout_file = None
    stderr_file = None
    stdout_append = False
    stderr_append = False
    i = 0

    while i < len(parts):
        if parts[i] in (">", "1>"):
            stdout_file = parts[i + 1]
            i += 2
        elif parts[i] == "2>":
            stderr_file = parts[i + 1]
            i += 2
        elif parts[i] in (">>", "1>>"):
            stdout_file = parts[i + 1]
            stdout_append = True
            i += 2
        elif parts[i] == "2>>":
            stderr_file = parts[i + 1]
            stderr_append = True
            i += 2
        else:
            result.append(parts[i])
            i += 1

    return result, stdout_file, stderr_file, stdout_append, stderr_append


def parse_input(line, home):
    parts = shlex.split(line)

    if not parts:
        return "", [], None, None, False, False

    parts, stdout_file, stderr_file, stdout_append, stderr_append = parse_redirects(
        parts
    )

    parts = [
        part.replace("~", home) if part.startswith("~") else part for part in parts
    ]
    if stdout_file and stdout_file.startswith("~"):
        stdout_file = stdout_file.replace("~", home)
    if stderr_file and stderr_file.startswith("~"):
        stderr_file = stderr_file.replace("~", home)

    return parts[0], parts[1:], stdout_file, stderr_file, stdout_append, stderr_append
