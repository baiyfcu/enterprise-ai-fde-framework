# 企业 AI 落地 FDE 框架 MVP

这是一个 **Mock-first** 的企业 AI 落地（FDE, Forward Deployed Engineering）框架原型，用于演示从 **需求发现 → ROI 评估 → 技术方案 → Agent/RAG 构建蓝图 → 评估与交付** 的完整闭环。

> 目标不是伪装成生产级平台，而是提供一个 **无需真实 LLM API Key、可本地启动、可演示结构化交付结果** 的最小可运行版本。

## 1. 能力概览

- **确定性 FDE workflow**：不依赖模型调用，直接根据结构化需求生成交付物。
- **结构化 Agent 输出**：Discovery、Solution Architect、Builder、Evaluator、Delivery 全部使用 Pydantic 模型。
- **Mock-first 工具闭环**：内置模拟 CRM 查询、模拟工单创建，并保留统一工具接口，便于后续接入 MCP/REST。
- **治理能力**：基础 RBAC、审计事件、敏感字段脱敏。
- **规则评估**：质量 / 安全 / 成本 / 延迟评分，附带验收门槛判断。
- **本地演示方式**：FastAPI + CLI + Docker。

## 2. 目录结构

```text
app/
├── api/              # FastAPI 路由
├── agents/           # Discovery / Architect / Builder / Evaluator / Delivery
├── orchestration/    # 确定性 FDE workflow
├── integrations/     # Mock 企业工具与后续 MCP 适配接口
├── evaluation/       # 规则评分与验收
├── governance/       # RBAC / 审计 / 脱敏
examples/             # 示例需求输入
tests/                # 单元测试
```

## 3. 快速启动

### 3.1 本地 Python 方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python -m app.cli
uvicorn app.main:app --reload
```

启动后访问：

- OpenAPI 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/api/health`

### 3.2 Docker 方式

```bash
cp .env.example .env
docker compose up --build
```

说明：

- `.env.example` 是模板文件；`docker-compose.yml` 默认读取实际运行时配置 `.env`。
- 如果你希望使用其他文件名，可复制出一份并同步调整 `docker-compose.yml` 中的 `env_file`。

## 4. 架构说明

### 4.1 工作流

```text
企业需求输入
  -> Discovery Agent（问题定义 / ROI 假设）
  -> Solution Architect Agent（架构与治理设计）
  -> Builder Agent（Mock-first Agent/RAG/Tools 蓝图）
  -> Evaluator Agent（规则评分与验收判断）
  -> Delivery Agent（交付摘要与下一步建议）
```

### 4.2 示例场景

当前内置示例为：

- **企业知识库问答**
- **Mock CRM 上下文查询**
- **Mock 工单创建**

其中 RAG 仅提供蓝图与接口思路，不声称已经实现生产级检索增强。

## 5. API 示例

### 5.1 查询示例用例

```bash
curl http://127.0.0.1:8000/api/examples
```

### 5.2 查询工具清单

```bash
curl http://127.0.0.1:8000/api/tools
```

### 5.3 运行一次 FDE workflow

```bash
curl -X POST "http://127.0.0.1:8000/api/workflow/run" \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "制造业",
    "problem": "客服团队无法快速回答产品知识问题，并需要联动 CRM 与工单系统",
    "users": ["客服专员", "售后经理"],
    "data_sources": ["产品手册", "FAQ 文档", "历史工单"],
    "existing_systems": ["CRM", "工单系统", "企业知识库"],
    "constraints": ["不能暴露客户敏感信息", "优先本地演示，不依赖外部 API Key"]
  }'
```

## 6. CLI 示例

```bash
python -m app.cli
```

将打印完整 JSON 结构化交付结果，包括：

- 发现报告与 ROI 假设
- 架构方案
- 实施计划与工具蓝图
- 评估计划与验收判断
- 交付摘要
- 工具执行结果与审计事件

## 7. 示例输入与输出

- 示例输入：`examples/knowledge_base_demo.json`
- 输出：CLI 或 `/api/workflow/run` 返回的 JSON

## 8. 生产化接入建议

如果后续要从 MVP 演进到生产版本，建议按以下顺序接入：

1. **LangGraph**：把当前确定性 workflow 替换为可观测、可恢复的状态图编排。
2. **真实模型**：为 Discovery / Architect / Builder 等 Agent 增加 LLM 推理能力，但保留结构化输出约束。
3. **MCP / 企业系统**：将 `app/integrations/tools.py` 中的统一工具接口映射到 MCP Server、REST API、数据库或消息系统。
4. **真实 RAG**：补充文档加载、切分、embedding、检索、权限过滤、引用回溯。
5. **治理增强**：加入更细粒度 RBAC、审批流、密钥管理、数据分级与观测告警。

## 9. 边界与安全注意事项

- 本仓库 **不包含任何真实 API Key**，也不要求配置外部服务。
- 当前工具调用、知识检索、ROI 测算均为 **Mock / 规则驱动示例**。
- 敏感字段应在日志、审计、提示词上下文中统一先脱敏。
- 生产接入前，需要补充真实身份认证、授权、速率限制、日志留存与合规审查。
- 不应将本 MVP 视为生产级 RAG、MCP 或 Agent 平台，只应作为 FDE 交付蓝图和演示原型。

## 10. 已知限制与下一步

### 已知限制

- 没有接入真实 LLM，因此输出是确定性模板化结果。
- 没有实现真实向量检索或企业权限同步。
- Mock 工具仅用于展示接口契约与闭环，不代表真实系统可靠性。

### 下一步建议

- 对接试点企业知识文档与 FAQ 数据。
- 增加更细的 ROI 参数模型与人工确认节点。
- 把工具接口扩展为 MCP Adapter 与可观测调用链。
- 为生产接入补充身份认证、缓存、监控、回滚与 A/B 评估。
