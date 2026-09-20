from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class EnterpriseRequirement(BaseModel):
    industry: str
    problem: str
    users: list[str] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)
    existing_systems: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class ROIHypothesis(BaseModel):
    baseline_cost_per_month: float
    estimated_savings_per_month: float
    payback_months: float
    assumptions: list[str] = Field(default_factory=list)


class DiscoveryReport(BaseModel):
    current_state: str
    target_outcome: str
    risks: list[str] = Field(default_factory=list)
    prioritized_use_cases: list[str] = Field(default_factory=list)
    roi_hypothesis: ROIHypothesis


class ArchitectureDecision(BaseModel):
    name: str
    rationale: str


class SolutionArchitecture(BaseModel):
    pattern: str
    components: list[str] = Field(default_factory=list)
    integrations: list[str] = Field(default_factory=list)
    governance_controls: list[str] = Field(default_factory=list)
    decisions: list[ArchitectureDecision] = Field(default_factory=list)


class ToolBlueprint(BaseModel):
    tool_name: str
    purpose: str
    adapter_hint: str


class BuilderPlan(BaseModel):
    implementation_phases: list[str] = Field(default_factory=list)
    tool_blueprints: list[ToolBlueprint] = Field(default_factory=list)
    mock_rag_blueprint: list[str] = Field(default_factory=list)
    delivery_artifacts: list[str] = Field(default_factory=list)


class EvaluationScorecard(BaseModel):
    quality: int = Field(ge=0, le=100)
    safety: int = Field(ge=0, le=100)
    cost: int = Field(ge=0, le=100)
    latency: int = Field(ge=0, le=100)


class AcceptanceDecision(BaseModel):
    passed: bool
    threshold: int
    blockers: list[str] = Field(default_factory=list)


class EvaluationPlan(BaseModel):
    metrics: list[str] = Field(default_factory=list)
    test_scenarios: list[str] = Field(default_factory=list)
    scorecard: EvaluationScorecard
    acceptance: AcceptanceDecision


class DeliverySummary(BaseModel):
    executive_summary: str
    next_steps: list[str] = Field(default_factory=list)
    operating_model: list[str] = Field(default_factory=list)
    audit_notes: list[str] = Field(default_factory=list)


class AuditEvent(BaseModel):
    actor: str
    action: str
    resource: str
    outcome: Literal["success", "failure"]
    details: dict[str, Any] = Field(default_factory=dict)


class RoleBinding(BaseModel):
    role: str
    permissions: list[str]


class ToolExecutionResult(BaseModel):
    tool_name: str
    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    message: str


class FDEWorkflowResult(BaseModel):
    requirement: EnterpriseRequirement
    discovery: DiscoveryReport
    solution_architecture: SolutionArchitecture
    builder: BuilderPlan
    evaluation: EvaluationPlan
    delivery: DeliverySummary
    tool_outputs: list[ToolExecutionResult] = Field(default_factory=list)
    audit_events: list[AuditEvent] = Field(default_factory=list)
    role_binding: RoleBinding
