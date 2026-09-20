from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_and_catalog_endpoints():
    assert client.get("/api/health").json() == {"status": "ok"}
    assert len(client.get("/api/examples").json()) >= 1
    assert len(client.get("/api/tools").json()) == 2


def test_run_workflow_endpoint():
    payload = {
        "industry": "金融",
        "problem": "知识查询耗时长",
        "users": ["坐席"],
        "data_sources": ["制度文档"],
        "existing_systems": ["CRM"],
        "constraints": ["必须记录审计日志"]
    }
    response = client.post("/api/workflow/run", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["role_binding"]["role"] == "fde_admin"
    assert body["tool_outputs"][1]["data"]["status"] == "created"


def test_run_workflow_endpoint_blocks_create_for_query_only_role(monkeypatch):
    monkeypatch.setenv("DEFAULT_ROLE", "solution_architect")
    payload = {
        "industry": "金融",
        "problem": "知识查询耗时长",
        "users": ["坐席"],
        "data_sources": ["制度文档"],
        "existing_systems": ["CRM"],
        "constraints": ["必须记录审计日志"],
    }

    response = client.post("/api/workflow/run", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["role_binding"]["role"] == "solution_architect"
    assert body["tool_outputs"][0]["success"] is True
    assert body["tool_outputs"][1]["success"] is False
    assert "没有创建企业工单的权限" in body["tool_outputs"][1]["message"]


def test_run_workflow_endpoint_falls_back_for_invalid_role(monkeypatch):
    monkeypatch.setenv("DEFAULT_ROLE", "invalid-role")
    payload = {
        "industry": "金融",
        "problem": "知识查询耗时长",
        "users": ["坐席"],
        "data_sources": ["制度文档"],
        "existing_systems": ["CRM"],
        "constraints": ["必须记录审计日志"],
    }

    response = client.post("/api/workflow/run", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["role_binding"]["role"] == "analyst"
    assert body["tool_outputs"][1]["success"] is False
