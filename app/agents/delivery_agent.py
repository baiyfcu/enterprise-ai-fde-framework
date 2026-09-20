from __future__ import annotations

from app.models import DeliverySummary, EnterpriseRequirement, EvaluationPlan


class DeliveryAgent:
    def run(self, requirement: EnterpriseRequirement, evaluation: EvaluationPlan) -> DeliverySummary:
        status = "满足" if evaluation.acceptance.passed else "暂不满足"
        return DeliverySummary(
            executive_summary=(
                f"针对{requirement.industry}场景的“{requirement.problem}”需求，已生成可演示的 FDE MVP，"
                f"当前验收结论为：{status}门槛。"
            ),
            next_steps=[
                "确认试点部门与样例知识文档",
                "将 Mock 工具替换为真实企业系统适配器",
                "引入人工评审与线上监控指标",
            ],
            operating_model=[
                "业务负责人提供需求与验收标准",
                "FDE 团队维护 workflow / 工具接入 / 审计",
                "安全与 IT 团队审核权限、数据边界与发布策略",
            ],
            audit_notes=[
                "本版本仅为 Mock-first 原型，不包含真实生产凭据",
                "所有敏感字段在日志中需先脱敏",
            ],
        )
