from schemas import AgentFinding


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
        AgentFinding(
            agent="HistoryAgent",
            language=None,
            finding=(
                "The fictional temperature limit changed from 90C to 85C "
                "after a Machine 7 thermal-stop investigation."
            ),
            sources=[
                "legacy/AUTOFACTORY-2005/tickets/BUG-187.txt",
                "legacy/AUTOFACTORY-2005/CHANGELOG.txt",
                "legacy/AUTOFACTORY-2005/docs/maintenance_notes.txt",
            ],
            status="supported-by-sources",
        ),
    ]

    return {
        "question": question,
        "answer": (
            "Machine 7 stops because its temperature reaches or exceeds "
            "the 85C safety limit. The alarm activates and production is disabled."
        ),
        "agents": findings,
    }