from __future__ import annotations

import json
from pathlib import Path

from app.models import EnterpriseRequirement
from app.orchestration.workflow import FDEWorkflow


def load_example_requirement() -> EnterpriseRequirement:
    example_path = Path(__file__).resolve().parent.parent / "examples" / "knowledge_base_demo.json"
    return EnterpriseRequirement.model_validate_json(example_path.read_text(encoding="utf-8"))


def main() -> None:
    workflow = FDEWorkflow()
    result = workflow.run(load_example_requirement())
    print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
