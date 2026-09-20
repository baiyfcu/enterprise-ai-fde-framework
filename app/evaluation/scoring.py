from __future__ import annotations

from app.models import AcceptanceDecision, BuilderPlan, DiscoveryReport, EnterpriseRequirement, EvaluationPlan, EvaluationScorecard, SolutionArchitecture


def evaluate_workflow(
    requirement: EnterpriseRequirement,
    discovery: DiscoveryReport,
    architecture: SolutionArchitecture,
    builder: BuilderPlan,
) -> EvaluationPlan:
    quality = min(100, 55 + len(discovery.prioritized_use_cases) * 10 + len(architecture.components) * 3)
    safety = 60
    if requirement.constraints:
        safety += min(20, len(requirement.constraints) * 5)
    if architecture.governance_controls:
        safety += 10
    cost = max(50, 90 - len(builder.implementation_phases) * 8)
    latency = max(55, 85 - len(builder.tool_blueprints) * 7)

    scorecard = EvaluationScorecard(
        quality=quality,
        safety=min(100, safety),
        cost=cost,
        latency=latency,
    )
    threshold = 70
    blockers: list[str] = []
    if scorecard.quality < threshold:
        blockers.append("质量分不足，需补充高价值场景或知识数据")
    if scorecard.safety < threshold:
        blockers.append("安全分不足，需补充权限、脱敏或审计控制")
    if not requirement.data_sources:
        blockers.append("缺少明确数据源，无法进入真实 RAG 实施阶段")

    return EvaluationPlan(
        metrics=["quality", "safety", "cost", "latency"],
        test_scenarios=[
            "企业知识库问答",
            "CRM 上下文查询",
            "高优先级问题自动创建工单",
            "敏感字段脱敏与审计记录",
        ],
        scorecard=scorecard,
        acceptance=AcceptanceDecision(passed=not blockers, threshold=threshold, blockers=blockers),
    )
