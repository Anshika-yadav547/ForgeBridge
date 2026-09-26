from __future__ import annotations

import json
from pathlib import Path

from backend.architecture_analyzer import build_architecture_graph


def main() -> None:
    repository_root = Path(__file__).resolve().parent.parent

    graph = build_architecture_graph(repository_root)

    output_directory = repository_root / "architecture"
    output_directory.mkdir(exist_ok=True)

    output_file = output_directory / "graph.json"

    output_file.write_text(
        json.dumps(graph, indent=2),
        encoding="utf-8",
    )

    print(f"Architecture graph written to: {output_file}")


if __name__ == "__main__":
    main()