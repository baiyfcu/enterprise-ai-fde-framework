from __future__ import annotations

from fastapi import APIRouter

from app.config import get_default_role
from app.integrations.tools import get_tool_catalog
from app.models import EnterpriseRequirement
from app.orchestration.workflow import FDEWorkflow

router = APIRouter()
workflow = FDEWorkflow()

EXAMPLE_USE_CASES = [
    {
        "name": "企业知识库问答 + CRM 上下文",
        "industry": "制造业",
        "problem": "客服无法快速查询产品知识与客户状态",
    },
    {
        "name": "内部 IT 支持 Copilot",
        "industry": "互联网",
        "problem": "员工服务台问题重复、升级链路长",
    },
]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/examples")
def list_examples() -> list[dict[str, str]]:
    return EXAMPLE_USE_CASES


@router.get("/tools")
def list_tools() -> list[dict[str, str]]:
    return [tool.metadata() for tool in get_tool_catalog()]


@router.post("/workflow/run")
def run_workflow(requirement: EnterpriseRequirement):
    return workflow.run(requirement=requirement, role=get_default_role())
