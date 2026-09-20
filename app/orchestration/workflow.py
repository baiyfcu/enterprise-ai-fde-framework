from __future__ import annotations

from app.agents.builder_agent import BuilderAgent
from app.agents.delivery_agent import DeliveryAgent
from app.agents.discovery_agent import DiscoveryAgent
from app.agents.evaluator_agent import EvaluatorAgent
from app.agents.solution_architect_agent import SolutionArchitectAgent
from app.governance.audit import build_audit_event
from app.governance.masking import mask_sensitive_data
from app.governance.rbac import resolve_role_binding
from app.integrations.tools import get_tool_catalog
from app.models import (
    AcceptanceDecision,
    BuilderPlan,
    DeliverySummary,
    DiscoveryReport,
    EnterpriseRequirement,
    EvaluationPlan,
    EvaluationScorecard,
    FDEWorkflowResult,
    ROIHypothesis,
    RoleBinding,
    SolutionArchitecture,
    ToolExecutionResult,
)


class FDEWorkflow:
    def __init__(self) -> None:
        self.discovery_agent = DiscoveryAgent()
        self.architect_agent = SolutionArchitectAgent()
        self.builder_agent = BuilderAgent()
        self.evaluator_agent = EvaluatorAgent()
        self.delivery_agent = DeliveryAgent()

    def run(self, requirement: EnterpriseRequirement, role: str = "fde_admin") -> FDEWorkflowResult:
        role_binding = resolve_role_binding(role)
        if "workflow:run" not in role_binding.permissions:
            return self._build_workflow_denied_result(requirement, role_binding)
        discovery = self.discovery_agent.run(requirement)
        architecture = self.architect_agent.run(requirement)
        builder = self.builder_agent.run(requirement)
        evaluation = self.evaluator_agent.run(requirement, discovery, architecture, builder)
        delivery = self.delivery_agent.run(requirement, evaluation)

        tools = {tool.name: tool for tool in get_tool_catalog()}
        query_tool = tools.get("mock_crm_query")
        create_tool = tools.get("mock_ticket_create")
        tool_outputs = []

        if query_tool is None:
            tool_outputs.append(
                ToolExecutionResult(
                    tool_name="mock_crm_query",
                    success=False,
                    message="必需工具缺失：mock_crm_query",
                )
            )
        elif "tool:query" in role_binding.permissions:
            tool_outputs.append(query_tool.execute({"account": requirement.industry}))
        else:
            tool_outputs.append(
                ToolExecutionResult(
                    tool_name="mock_crm_query",
                    success=False,
                    message="当前角色没有查询企业工具的权限",
                )
            )

        if create_tool is None:
            tool_outputs.append(
                ToolExecutionResult(
                    tool_name="mock_ticket_create",
                    success=False,
                    message="必需工具缺失：mock_ticket_create",
                )
            )
        elif "tool:create" in role_binding.permissions:
            tool_outputs.append(
                create_tool.execute(
                    {"title": f"{requirement.industry} AI MVP PoC 跟进", "owner": role_binding.role}
                )
            )
        else:
            tool_outputs.append(
                ToolExecutionResult(
                    tool_name="mock_ticket_create",
                    success=False,
                    message="当前角色没有创建企业工单的权限",
                )
            )

        sanitized_requirement = mask_sensitive_data(requirement.model_dump())
        tool_outcome = "success" if all(tool.success for tool in tool_outputs) else "failure"
        audit_events = [
            build_audit_event(
                actor=role_binding.role,
                action="workflow.run",
                resource="fde_workflow",
                outcome=tool_outcome,
                requirement=sanitized_requirement,
            ),
            build_audit_event(
                actor=role_binding.role,
                action="tool.batch_execute",
                resource="tool_batch",
                outcome=tool_outcome,
                tool_count=len(tool_outputs),
                executed_tools=[
                    {"tool_name": tool.tool_name, "success": tool.success, "message": tool.message}
                    for tool in tool_outputs
                ],
            ),
        ]

        return FDEWorkflowResult(
            requirement=requirement,
            discovery=discovery,
            solution_architecture=architecture,
            builder=builder,
            evaluation=evaluation,
            delivery=delivery,
            tool_outputs=tool_outputs,
            audit_events=audit_events,
            role_binding=role_binding,
        )

    def _build_workflow_denied_result(
        self,
        requirement: EnterpriseRequirement,
        role_binding: RoleBinding,
    ) -> FDEWorkflowResult:
        return FDEWorkflowResult(
            requirement=requirement,
            discovery=DiscoveryReport(
                current_state="当前角色未被授权执行 FDE workflow。",
                target_outcome="申请具备 workflow:run 权限的角色后重试。",
                risks=["未授权执行，未生成业务分析结果。"],
                prioritized_use_cases=[],
                roi_hypothesis=ROIHypothesis(
                    baseline_cost_per_month=0,
                    estimated_savings_per_month=0,
                    payback_months=0,
                    assumptions=[],
                ),
            ),
            solution_architecture=SolutionArchitecture(
                pattern="未执行",
                components=[],
                integrations=[],
                governance_controls=[],
                decisions=[],
            ),
            builder=BuilderPlan(
                implementation_phases=[],
                tool_blueprints=[],
                mock_rag_blueprint=[],
                delivery_artifacts=[],
            ),
            evaluation=EvaluationPlan(
                metrics=["quality", "safety", "cost", "latency"],
                test_scenarios=[],
                scorecard=EvaluationScorecard(quality=0, safety=0, cost=0, latency=0),
                acceptance=AcceptanceDecision(
                    passed=False,
                    threshold=70,
                    blockers=["当前角色缺少 workflow:run 权限"],
                ),
            ),
            delivery=DeliverySummary(
                executive_summary="未授权执行 workflow，因此未生成交付方案。",
                next_steps=["切换到具备 workflow:run 权限的角色。"],
                operating_model=[],
                audit_notes=["本次请求被 RBAC 拒绝。"],
            ),
            tool_outputs=[],
            audit_events=[
                build_audit_event(
                    actor=role_binding.role,
                    action="workflow.run",
                    resource="fde_workflow",
                    outcome="failure",
                    reason="missing workflow:run permission",
                )
            ],
            role_binding=role_binding,
        )
