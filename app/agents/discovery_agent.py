from __future__ import annotations

from app.models import DiscoveryReport, EnterpriseRequirement, ROIHypothesis


class DiscoveryAgent:
    def run(self, requirement: EnterpriseRequirement) -> DiscoveryReport:
        automation_targets = [
            f"面向{user}的知识问答助手" for user in (requirement.users[:2] or ["业务团队"]) 
        ]
        assumptions = [
            "当前知识查询主要依赖人工检索与跨系统问询",
            "企业愿意先以 Mock-first 方式验证价值，再接真实系统",
            f"核心数据源包括：{', '.join(requirement.data_sources or ['企业知识库'])}",
        ]
        baseline_cost = max(12000.0, 3000.0 * max(1, len(requirement.users)))
        savings = round(baseline_cost * 0.35, 2)
        payback = round(3 * baseline_cost / max(savings, 1), 1)
        return DiscoveryReport(
            current_state=f"{requirement.industry}场景下，{requirement.problem} 依赖人工流程与分散系统协同。",
            target_outcome="在不接入真实模型密钥的前提下，演示可交付的 AI 闭环，缩短需求到原型时间。",
            risks=[
                "真实知识库质量与权限边界尚未验证",
                "Mock 工具调用不能替代生产可用性测试",
                *([f"约束需要纳入方案：{c}" for c in requirement.constraints[:2]]),
            ],
            prioritized_use_cases=automation_targets,
            roi_hypothesis=ROIHypothesis(
                baseline_cost_per_month=baseline_cost,
                estimated_savings_per_month=savings,
                payback_months=payback,
                assumptions=assumptions,
            ),
        )
