from app.governance.masking import mask_sensitive_data
from app.integrations.tools import MockCRMQueryTool, MockTicketCreateTool
from app.models import EnterpriseRequirement
from app.orchestration import workflow as workflow_module
from app.orchestration.workflow import FDEWorkflow


def sample_requirement() -> EnterpriseRequirement:
    return EnterpriseRequirement(
        industry="零售",
        problem="门店支持团队需要统一知识问答入口",
        users=["店长", "运营", "客服"],
        data_sources=["SOP", "培训手册"],
        existing_systems=["CRM", "知识库"],
        constraints=["需要审计", "客户邮箱不可明文展示"],
    )


def test_workflow_returns_structured_result():
    result = FDEWorkflow().run(sample_requirement())

    assert result.discovery.roi_hypothesis.estimated_savings_per_month > 0
    assert result.solution_architecture.pattern.startswith("FastAPI")
    assert result.builder.tool_blueprints[0].tool_name == "mock_crm_query"
    assert result.evaluation.scorecard.safety >= result.evaluation.acceptance.threshold
    assert result.delivery.next_steps
    assert len(result.audit_events) == 2


def test_mask_sensitive_data_redacts_nested_values():
    payload = {"email": "user@example.com", "nested": {"token": "abc", "ok": "value"}}
    masked = mask_sensitive_data(payload)

    assert masked["email"] == "***REDACTED***"
    assert masked["nested"]["token"] == "***REDACTED***"
    assert masked["nested"]["ok"] == "value"


def test_workflow_resolves_tools_by_name(monkeypatch):
    monkeypatch.setattr(
        workflow_module,
        "get_tool_catalog",
        lambda: [MockTicketCreateTool(), MockCRMQueryTool()],
    )

    result = FDEWorkflow().run(sample_requirement())

    assert result.tool_outputs[0].tool_name == "mock_crm_query"
    assert result.tool_outputs[1].tool_name == "mock_ticket_create"
