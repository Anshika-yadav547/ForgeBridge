
from schemas import AgentFinding
from integrated_analyzer import analyze_machine


def analyze_question(question: str) -> dict:
    findings = [
        AgentFinding(
            agent="LegacyCodeAgent",
            language="C",
            finding=(
                "Temperature at or above 85C activates the alarm "
                "and disables production."
            ),
            sources=[
                "legacy/AUTOFACTORY-2005/src/alarm.c",
                "legacy/AUTOFACTORY-2005/src/temperature.c",
            ],
            status="supported-by-sources",
        ),
    ]

    integrated = analyze_machine()
    history = integrated["historical_analysis"]
    history_finding = AgentFinding(**history)
    findings.append(history_finding)

    return {
        "question": question,
        "answer": (
            "Machine 7 stops because its temperature reaches or exceeds "
            "the 85C safety limit. The alarm activates and production is disabled."
        ),
        "agents": findings,
    }
