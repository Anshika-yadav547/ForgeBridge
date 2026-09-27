from pathlib import Path

from backend.affected_files import get_temperature_affected_files
from backend.architecture_analyzer import build_architecture_graph


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_c_files_are_discovered():
    graph = build_architecture_graph(REPOSITORY_ROOT)

    node_ids = {
        node["id"]
        for node in graph["nodes"]
    }

    assert "legacy/AUTOFACTORY-2005/src/main.c" in node_ids
    assert "legacy/AUTOFACTORY-2005/src/alarm.c" in node_ids
    assert "legacy/AUTOFACTORY-2005/src/temperature.c" in node_ids
    assert "legacy/AUTOFACTORY-2005/include/factory.h" in node_ids


def test_c_include_edges_are_extracted():
    graph = build_architecture_graph(REPOSITORY_ROOT)

    edge_tuples = {
        (
            edge["source"],
            edge["target"],
            edge["kind"],
        )
        for edge in graph["edges"]
    }

    assert (
        "legacy/AUTOFACTORY-2005/src/alarm.c",
        "legacy/AUTOFACTORY-2005/include/factory.h",
        "includes",
    ) in edge_tuples


def test_c_function_definitions_are_extracted():
    graph = build_architecture_graph(REPOSITORY_ROOT)

    node_ids = {
        node["id"]
        for node in graph["nodes"]
    }

    assert (
        "legacy/AUTOFACTORY-2005/src/alarm.c::evaluate_machine"
        in node_ids
    )

    assert (
        "legacy/AUTOFACTORY-2005/src/temperature.c::"
        "temperature_exceeds_limit"
        in node_ids
    )


def test_c_runtime_call_edges_are_extracted():
    graph = build_architecture_graph(REPOSITORY_ROOT)

    edge_tuples = {
        (
            edge["source"],
            edge["target"],
            edge["kind"],
        )
        for edge in graph["edges"]
    }

    assert (
        "legacy/AUTOFACTORY-2005/src/main.c::main",
        "legacy/AUTOFACTORY-2005/src/alarm.c::evaluate_machine",
        "calls_heuristic",
    ) in edge_tuples

    assert (
        "legacy/AUTOFACTORY-2005/src/alarm.c::evaluate_machine",
        "legacy/AUTOFACTORY-2005/src/temperature.c::"
        "temperature_exceeds_limit",
        "calls_heuristic",
    ) in edge_tuples


def test_cobol_program_is_extracted():
    graph = build_architecture_graph(REPOSITORY_ROOT)

    node_ids = {
        node["id"]
        for node in graph["nodes"]
    }

    cobol_file = (
        "legacy/AUTOFACTORY-2005/cobol/MACHINE-STATUS.cbl"
    )

    assert cobol_file in node_ids
    assert f"{cobol_file}::MACHINE-STATUS" in node_ids


def test_cobol_perform_relationship_is_extracted():
    graph = build_architecture_graph(REPOSITORY_ROOT)

    edge_tuples = {
        (
            edge["source"],
            edge["target"],
            edge["kind"],
        )
        for edge in graph["edges"]
    }

    cobol_file = (
        "legacy/AUTOFACTORY-2005/cobol/MACHINE-STATUS.cbl"
    )

    assert (
        f"{cobol_file}::MAIN-LOGIC",
        f"{cobol_file}::CHECK-TEMPERATURE",
        "performs",
    ) in edge_tuples


def test_temperature_affected_files_are_returned():
    affected_files = get_temperature_affected_files(
        REPOSITORY_ROOT,
    )

    affected_paths = {
        item["path"]
        for item in affected_files
    }

    assert (
        "legacy/AUTOFACTORY-2005/src/alarm.c"
        in affected_paths
    )

    assert (
        "legacy/AUTOFACTORY-2005/src/temperature.c"
        in affected_paths
    )


    assert (
        "legacy/AUTOFACTORY-2005/tickets/BUG-187.txt"
        in affected_paths
    )