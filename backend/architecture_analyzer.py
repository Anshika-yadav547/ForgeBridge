from __future__ import annotations

import re
from pathlib import Path

from backend.dependency_graph import DependencyGraph


C_SOURCE_SUFFIXES = {".c"}
C_HEADER_SUFFIXES = {".h"}

INCLUDE_PATTERN = re.compile(
    r'^\s*#\s*include\s*[<"]([^">]+)[">]',
    re.MULTILINE,
)
FUNCTION_DEFINITION_PATTERN = re.compile(
    r"(?m)^[\t ]*"
    r"(?:static[\t ]+)?"
    r"(?:void|int|float|double|char|MachineStatus)"
    r"[\t ]+"
    r"([A-Za-z_][A-Za-z0-9_]*)"
    r"[\t ]*\([^;{}]*\)"
    r"[\t \r\n]*\{"
)
FUNCTION_CALL_PATTERN = re.compile(
    r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\("
)
COBOL_SOURCE_SUFFIXES = {".cbl", ".cob"}

COBOL_PROGRAM_ID_PATTERN = re.compile(
    r"\bPROGRAM-ID\.\s*([A-Z0-9-]+)\.?",
    re.IGNORECASE,
)
COBOL_PARAGRAPH_PATTERN = re.compile(
    r"(?m)^[ \t]{7}([A-Z][A-Z0-9-]*)\.[ \t]*$",
    re.IGNORECASE,
)
COBOL_CALL_PATTERN = re.compile(
    r'\bCALL\s+["\']([A-Z0-9-]+)["\']',
    re.IGNORECASE,
)

COBOL_COPY_PATTERN = re.compile(
    r"\bCOPY\s+([A-Z0-9-]+)",
    re.IGNORECASE,
)
def repository_relative(path: Path, repository_root: Path) -> str:
    return path.relative_to(repository_root).as_posix()


def discover_c_files(
    repository_root: Path,
    graph: DependencyGraph,
) -> list[Path]:
    legacy_root = repository_root / "legacy" / "AUTOFACTORY-2005"
    discovered: list[Path] = []

    for path in sorted(legacy_root.rglob("*")):
        if not path.is_file():
            continue

        relative = repository_relative(path, repository_root)

        if path.suffix.lower() in C_SOURCE_SUFFIXES:
            graph.add_node(
                node_id=relative,
                node_type="c_file",
                label=path.name,
            )
            discovered.append(path)

        elif path.suffix.lower() in C_HEADER_SUFFIXES:
            graph.add_node(
                node_id=relative,
                node_type="header",
                label=path.name,
            )
            discovered.append(path)

    return discovered
def discover_cobol_files(
    repository_root: Path,
    graph: DependencyGraph,
) -> list[Path]:
    legacy_root = repository_root / "legacy" / "AUTOFACTORY-2005"
    discovered: list[Path] = []

    for path in sorted(legacy_root.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in COBOL_SOURCE_SUFFIXES:
            continue

        relative = repository_relative(path, repository_root)

        graph.add_node(
            node_id=relative,
            node_type="cobol_file",
            label=path.name,
        )

        discovered.append(path)

    return discovered
def extract_cobol_programs(
    cobol_files: list[Path],
    repository_root: Path,
    graph: DependencyGraph,
) -> None:
    for source_path in cobol_files:
        source_id = repository_relative(
            source_path,
            repository_root,
        )

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        match = COBOL_PROGRAM_ID_PATTERN.search(content)

        if match is None:
            continue

        program_name = match.group(1).upper()
        program_id = f"{source_id}::{program_name}"

        graph.add_node(
            node_id=program_id,
            node_type="cobol_program",
            label=program_name,
        )

        graph.add_edge(
            source=source_id,
            target=program_id,
            kind="contains",
        )
def extract_cobol_paragraph_bodies(
    content: str,
) -> list[tuple[str, str]]:
    matches = list(COBOL_PARAGRAPH_PATTERN.finditer(content))
    paragraphs: list[tuple[str, str]] = []

    for index, match in enumerate(matches):
        paragraph_name = match.group(1).upper()
        body_start = match.end()

        if index + 1 < len(matches):
            body_end = matches[index + 1].start()
        else:
            body_end = len(content)

        body = content[body_start:body_end]
        paragraphs.append((paragraph_name, body))

    return paragraphs
def extract_cobol_paragraphs_and_performs(
    cobol_files: list[Path],
    repository_root: Path,
    graph: DependencyGraph,
) -> None:
    for source_path in cobol_files:
        source_id = repository_relative(
            source_path,
            repository_root,
        )

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        paragraphs = extract_cobol_paragraph_bodies(content)
        for paragraph_name, _ in paragraphs:
            paragraph_id = f"{source_id}::{paragraph_name}"

            graph.add_node(
                node_id=paragraph_id,
                node_type="cobol_paragraph",
                label=paragraph_name,
            )

            graph.add_edge(
                source=source_id,
                target=paragraph_id,
                kind="contains",
            )

        for paragraph_name, body in paragraphs:
            source_paragraph_id = f"{source_id}::{paragraph_name}"

            performed_names = re.findall(
                r"\bPERFORM\s+([A-Z][A-Z0-9-]*)",
                body,
                flags=re.IGNORECASE,
            )

            for performed_name in performed_names:
                target_paragraph_id = (
                    f"{source_id}::{performed_name.upper()}"
                )

                graph.add_edge(
                    source=source_paragraph_id,
                    target=target_paragraph_id,
                    kind="performs",
                )
def extract_cobol_calls_and_copies(
    cobol_files: list[Path],
    repository_root: Path,
    graph: DependencyGraph,
) -> None:
    for source_path in cobol_files:
        source_id = repository_relative(
            source_path,
            repository_root,
        )

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        called_programs = COBOL_CALL_PATTERN.findall(content)

        for program_name in called_programs:
            target_id = (
                f"external_cobol_program::{program_name.upper()}"
            )

            graph.add_node(
                node_id=target_id,
                node_type="external_cobol_program",
                label=program_name.upper(),
            )

            graph.add_edge(
                source=source_id,
                target=target_id,
                kind="calls_program",
            )

        copybooks = COBOL_COPY_PATTERN.findall(content)

        for copybook_name in copybooks:
            target_id = f"copybook::{copybook_name.upper()}"

            graph.add_node(
                node_id=target_id,
                node_type="copybook",
                label=copybook_name.upper(),
            )

            graph.add_edge(
                source=source_id,
                target=target_id,
                kind="copies",
            )


def resolve_include(
    include_name: str,
    source_path: Path,
    repository_root: Path,
) -> Path | None:
    legacy_root = repository_root / "legacy" / "AUTOFACTORY-2005"

    candidates = [
        source_path.parent / include_name,
        legacy_root / "include" / include_name,
        legacy_root / "src" / include_name,
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate

    return None


def extract_c_includes(
    c_files: list[Path],
    repository_root: Path,
    graph: DependencyGraph,
) -> None:
    for source_path in c_files:
        source_id = repository_relative(source_path, repository_root)

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        include_names = INCLUDE_PATTERN.findall(content)

        for include_name in include_names:
            target_path = resolve_include(
                include_name=include_name,
                source_path=source_path,
                repository_root=repository_root,
            )

            if target_path is None:
                continue

            target_id = repository_relative(
                target_path,
                repository_root,
            )

            graph.add_edge(
                source=source_id,
                target=target_id,
                kind="includes",
            )
def extract_c_function_definitions(
    c_files: list[Path],
    repository_root: Path,
    graph: DependencyGraph,
) -> None:
    for source_path in c_files:
        if source_path.suffix.lower() not in C_SOURCE_SUFFIXES:
            continue

        source_id = repository_relative(
            source_path,
            repository_root,
        )

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        function_names = FUNCTION_DEFINITION_PATTERN.findall(
            content,
        )

        for function_name in function_names:
            function_id = f"{source_id}::{function_name}"

            graph.add_node(
                node_id=function_id,
                node_type="function",
                label=f"{function_name}()",
            )

            graph.add_edge(
                source=source_id,
                target=function_id,
                kind="contains",
            )
def function_body_start(content: str, function_name: str) -> int | None:
    pattern = re.compile(
        r"(?:static\s+)?"
        r"(?:void|int|float|double|char|MachineStatus)"
        r"\s+"
        + re.escape(function_name)
        + r"\s*\([^;{}]*\)\s*\{"
    )

    match = pattern.search(content)

    if match is None:
        return None

    return match.end()


def extract_braced_body(content: str, body_start: int) -> str:
    depth = 1
    index = body_start

    while index < len(content) and depth > 0:
        character = content[index]

        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1

        index += 1

    return content[body_start:index - 1]
def extract_c_function_calls(
    c_files: list[Path],
    repository_root: Path,
    graph: DependencyGraph,
) -> None:
    definitions: dict[str, str] = {}

    for source_path in c_files:
        if source_path.suffix.lower() not in C_SOURCE_SUFFIXES:
            continue

        source_id = repository_relative(
            source_path,
            repository_root,
        )

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        for function_name in FUNCTION_DEFINITION_PATTERN.findall(content):
            definitions[function_name] = f"{source_id}::{function_name}"

    ignored_names = {
        "if",
        "for",
        "while",
        "switch",
        "return",
        "sizeof",
    }

    for source_path in c_files:
        if source_path.suffix.lower() not in C_SOURCE_SUFFIXES:
            continue

        source_id = repository_relative(
            source_path,
            repository_root,
        )

        content = source_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        function_names = FUNCTION_DEFINITION_PATTERN.findall(content)

        for function_name in function_names:
            body_start = function_body_start(
                content=content,
                function_name=function_name,
            )

            if body_start is None:
                continue

            body = extract_braced_body(
                content=content,
                body_start=body_start,
            )

            source_function = f"{source_id}::{function_name}"

            for called_name in FUNCTION_CALL_PATTERN.findall(body):
                if called_name in ignored_names:
                    continue

                target_function = definitions.get(called_name)

                if target_function is None:
                    continue

                if source_function == target_function:
                    continue

                graph.add_edge(
                    source=source_function,
                    target=target_function,
                    kind="calls_heuristic",
                )
def build_architecture_graph(repository_root: Path) -> dict:
    graph = DependencyGraph()

    c_files = discover_c_files(
        repository_root=repository_root,
        graph=graph,
    )
    cobol_files = discover_cobol_files(
    repository_root=repository_root,
    graph=graph,
    )

    extract_c_includes(
        c_files=c_files,
        repository_root=repository_root,
        graph=graph,
    )

    extract_c_function_definitions(
        c_files=c_files,
        repository_root=repository_root,
        graph=graph,
    )
    extract_c_function_calls(
        c_files=c_files,
        repository_root=repository_root,
        graph=graph,
    )
    extract_cobol_programs(
    cobol_files=cobol_files,
    repository_root=repository_root,
    graph=graph,
    )
    extract_cobol_paragraphs_and_performs(
    cobol_files=cobol_files,
    repository_root=repository_root,
    graph=graph,
)
    extract_cobol_calls_and_copies(
    cobol_files=cobol_files,
    repository_root=repository_root,
    graph=graph,
)

    return graph.to_dict()
if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    result = build_architecture_graph(root)

    print("Nodes:")
    for node in result["nodes"]:
        print(
            f"- {node['type']}: "
            f"{node['id']}"
        )

    print("\nEdges:")
    for edge in result["edges"]:
        print(
            f"- {edge['source']} "
            f"--{edge['kind']}--> "
            f"{edge['target']}"
        )