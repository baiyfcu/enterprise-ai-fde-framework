from __future__ import annotations

from app.models import ArchitectureDecision, EnterpriseRequirement, SolutionArchitecture


class SolutionArchitectAgent:
    def run(self, requirement: EnterpriseRequirement) -> SolutionArchitecture:
        return SolutionArchitecture(
            pattern="FastAPI + 确定性编排 + Mock-first RAG/Tools 蓝图",
            components=[
                "需求输入与结构化校验",
                "Discovery / Architect / Builder / Evaluator / Delivery Agents",
                "Mock CRM / 工单工具适配层",
                "RBAC、审计、敏感字段脱敏",
                "规则评估引擎",
            ],
            integrations=requirement.existing_systems or ["CRM", "知识库", "工单系统"],
            governance_controls=["角色权限校验", "审计事件记录", "敏感字段脱敏"],
            decisions=[
                ArchitectureDecision(name="无需真实 LLM Key", rationale="通过确定性规则和 Mock 工具保障本地可运行性。"),
                ArchitectureDecision(name="保留 MCP 适配点", rationale="工具接口统一，后续可替换为真实企业系统或 MCP Server。"),
                ArchitectureDecision(name="Mock-first RAG 蓝图", rationale="先交付检索与引用接口蓝图，再逐步接入向量库与模型。"),
            ],
        )
