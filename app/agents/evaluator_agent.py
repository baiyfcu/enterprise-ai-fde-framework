from __future__ import annotations

from app.evaluation.scoring import evaluate_workflow
from app.models import BuilderPlan, DiscoveryReport, EnterpriseRequirement, EvaluationPlan, SolutionArchitecture


class EvaluatorAgent:
    def run(
        self,
        requirement: EnterpriseRequirement,
        discovery: DiscoveryReport,
        architecture: SolutionArchitecture,
        builder: BuilderPlan,
    ) -> EvaluationPlan:
        return evaluate_workflow(requirement, discovery, architecture, builder)
