from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    label: str


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str


class DependencyGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: set[Edge] = set()

    def add_node(self, node_id: str, node_type: str, label: str) -> None:
        self._nodes[node_id] = Node(
            id=node_id,
            type=node_type,
            label=label,
        )

    def add_edge(self, source: str, target: str, kind: str) -> None:
        self._edges.add(
            Edge(
                source=source,
                target=target,
                kind=kind,
            )
        )

    def to_dict(self) -> dict:
        return {
            "nodes": [
                asdict(node)
                for node in sorted(
                    self._nodes.values(),
                    key=lambda item: item.id,
                )
            ],
            "edges": [
                asdict(edge)
                for edge in sorted(
                    self._edges,
                    key=lambda item: (
                        item.source,
                        item.target,
                        item.kind,
                    ),
                )
            ],
        }