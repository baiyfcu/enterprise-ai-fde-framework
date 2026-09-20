from __future__ import annotations

from app.models import BuilderPlan, EnterpriseRequirement, ToolBlueprint


class BuilderAgent:
    def run(self, requirement: EnterpriseRequirement) -> BuilderPlan:
        return BuilderPlan(
            implementation_phases=[
                "第 1 周：需求确认、样例数据梳理、Mock API 与 CLI 演示",
                "第 2 周：接入真实知识库索引与权限同步",
                "第 3 周：接入真实模型 / LangGraph / MCP，并补充灰度评估",
            ],
            tool_blueprints=[
                ToolBlueprint(
                    tool_name="mock_crm_query",
                    purpose="在问答前补充客户上下文，用于个性化回复与 ROI 论证",
                    adapter_hint="替换 execute() 为 MCP/REST 适配器即可",
                ),
                ToolBlueprint(
                    tool_name="mock_ticket_create",
                    purpose="将高优先级问题转化为跟进工单，演示执行闭环",
                    adapter_hint="可映射到 ServiceNow/Jira/MCP Tool",
                ),
            ],
            mock_rag_blueprint=[
                f"为 {source} 定义 loader / chunk / retriever 接口" for source in (requirement.data_sources or ["企业知识库"])
            ],
            delivery_artifacts=["结构化发现报告", "技术方案", "实施计划", "评估计划", "交付摘要"],
        )
