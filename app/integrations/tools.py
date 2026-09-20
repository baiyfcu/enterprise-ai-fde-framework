from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.models import ToolExecutionResult


class EnterpriseTool(ABC):
    name: str
    description: str
    adapter_type: str = "mcp-compatible"

    @abstractmethod
    def execute(self, payload: dict[str, Any]) -> ToolExecutionResult:
        raise NotImplementedError

    def metadata(self) -> dict[str, str]:
        return {
            "name": self.name,
            "description": self.description,
            "adapter_type": self.adapter_type,
        }


class MockCRMQueryTool(EnterpriseTool):
    name = "mock_crm_query"
    description = "查询模拟 CRM 中的客户与工单摘要"

    def execute(self, payload: dict[str, Any]) -> ToolExecutionResult:
        account = payload.get("account", "示例客户")
        return ToolExecutionResult(
            tool_name=self.name,
            success=True,
            data={
                "account": account,
                "open_opportunities": 2,
                "active_tickets": 3,
                "last_contact": "2026-09-10",
            },
            message="已返回模拟 CRM 摘要",
        )


class MockTicketCreateTool(EnterpriseTool):
    name = "mock_ticket_create"
    description = "创建模拟工单，验证 Agent 到企业工具的闭环"

    def execute(self, payload: dict[str, Any]) -> ToolExecutionResult:
        title = payload.get("title", "AI MVP 跟进")
        owner = payload.get("owner", "fde-team")
        return ToolExecutionResult(
            tool_name=self.name,
            success=True,
            data={"ticket_id": "TICKET-1001", "title": title, "owner": owner, "status": "created"},
            message="已创建模拟工单",
        )


def get_tool_catalog() -> list[EnterpriseTool]:
    return [MockCRMQueryTool(), MockTicketCreateTool()]
