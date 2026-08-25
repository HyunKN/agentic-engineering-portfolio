# AI Agent 직무 역량 개발 계획

작성일: 2026-08-24

## 1. 목표 직무와 이 프로젝트의 역할

이 추가 프로젝트의 목적은 LangChain이나 LangGraph 사용 경험을 한 줄 추가하는 것이 아니다.

목표는 다음 역량을 실제 source, trace, evaluator, metric과 failure evidence로 보여줄 수 있는 **Applied AI / AI Agent Engineer**가 되는 것이다.

```text
AI/ML foundation
+ LLM application engineering
+ Agent orchestration
+ RAG and context engineering
+ evaluation and observability
+ production reliability
```

LocalTwin AEP와 Landmark Assistant AEP는 서로 다른 학습 역할을 가진다.

- LocalTwin AEP: 제품 개발 Agent의 Context, Tool, workflow, 검증, 배포와 운영
- Landmark Assistant AEP: ML workflow Agent의 데이터, 실험, metric, artifact와 serving decision

비교 단위는 `LT 기존 방식 vs LT AEP`, `LA 기존 방식 vs LA AEP`다. LT와 LA의 점수를 직접 비교하지 않는다.

## 2. 채용공고에서 반복되는 역량과 증명 방법

첨부된 채용공고 이미지와 2026-08-24 기준 현재 공고 조사에서 반복된 항목을 학습 목표로 변환했다. 상세 출처는 [AI Agent 채용 역량 조사](../research/AI_AGENT_JOB_SKILLS.md)에 정리한다.

| 역량 영역 | 배워야 할 지식 | LocalTwin AEP에서의 실습 | Landmark AEP에서의 실습 | 포트폴리오 증거 |
| --- | --- | --- | --- | --- |
| Python·backend | typing, Pydantic schema, async I/O, API, timeout, retry, error contract | code/test/git Tool API와 runner | dataset·experiment·artifact Tool API | typed Tool contract, API test, failure handling |
| Tool / Function Calling | structured output, schema 설계, Tool selection, 권한과 side effect | read/search/test/build Tool과 변경 승인 | dataset 검사, metric 집계, experiment 제안, artifact gate | Tool schema, 허용/차단 정책, 실패 trace |
| RAG | ingestion, chunking, embedding, BM25/vector/hybrid retrieval, metadata filter | architecture·task·git·failure 문맥 검색 | experiment log·model card·dataset·artifact evidence 검색 | retrieval dataset, Recall@K/MRR, citation·grounding 검사 |
| Agent orchestration | planning, state, memory, checkpoint, retry, Human-in-the-loop | Analyze→Retrieve→Plan→Edit→Verify→Recover | Evidence→Propose→Approve→Run/Simulate→Evaluate→Decide | LangGraph state diagram, resume·approval·recovery 시나리오 |
| Evaluation | baseline, dataset, deterministic evaluator, calibrated LLM judge, regression | Task success, regression, diff scope, token·시간·개입 | invalid proposal, leakage 탐지, artifact selection, GPU iteration | versioned eval dataset, automated harness, holdout report |
| Observability / LLMOps | trace/span, prompt/version, token, latency, cost, feedback, drift | LLM·Tool·retrieval·verification trace | decision·experiment·artifact lineage와 W&B 연결 | trace dashboard, failure taxonomy, cost/latency report |
| ML / PyTorch | dataset split, training/evaluation, variance, model selection, export | 필요한 ML 개념은 소비자 관점에서 검증 | 기존 PyTorch·W&B·ONNX evidence를 AEP gate로 연결 | reproducible metric, provenance, model/artifact decision |
| Production engineering | secrets, sandbox, authz, rate limit, cache, concurrency, CI/CD | 실제 repo Tool의 최소권한 실행과 안전한 patch | 비싼 학습 실행 전 approval와 resource budget | threat boundary, retry/idempotency test, deployment runbook |
| 연구 분석·재현 | 공식 문서·논문 읽기, 작은 재현, baseline·limitation 보고 | Agent/RAG technique를 LT Task에 제한 재현 | experiment-planning/evaluation technique를 LA Task에 재현 | reproduction note, code, negative result와 적용 판단 |

## 3. 도구 학습 원칙

채용공고에 나열된 모든 framework와 vector DB를 한 번씩 만지는 방식은 피한다.

### 깊게 다룰 것

- Python과 FastAPI/Pydantic 기반 Tool·runner 구현
- LangChain의 model, Tool과 retrieval integration
- LangGraph의 state, persistence, Human-in-the-loop와 failure recovery
- RAG ingestion부터 retrieval evaluation까지의 전체 pipeline
- offline eval dataset, regression harness와 trace observability

### 하나를 선택해 끝까지 운영할 것

- Vector store: Qdrant 또는 PostgreSQL/pgvector 중 하나
- Agent observability: LangSmith 또는 Langfuse 중 하나
- ML experiment tracking: 기존 Landmark evidence와 연결되는 W&B

Chroma, Qdrant, Weaviate를 모두 사용하는 것이 목표가 아니다. chunking·embedding·filter·hybrid retrieval을 선택한 이유와 retrieval 품질을 설명할 수 있어야 한다.

### 비교 학습만 할 것

- AutoGen, PydanticAI와 다른 Agent framework는 architecture와 trade-off를 비교한다.
- LocalTwin AEP의 주 runtime이 LangGraph라면 같은 기능을 AutoGen으로 중복 구현하지 않는다.
- 멀티 Agent는 역할 분리만으로 품질이나 비용 이점이 확인될 때만 추가한다.

## 4. LocalTwin AEP 학습 순서

LocalTwin AEP를 먼저 완성한다.

### LT-0 — Baseline과 계측

- 기존 Direct Agent workflow를 재현한다.
- token, elapsed time, Tool call, human intervention, patch와 evaluator result를 저장한다.
- LT-01 fixture와 hidden evaluator의 정답 누출을 차단한다.

### LT-1 — Tool Calling

- repository search/read, git evidence, test와 diff 검사를 typed Tool로 만든다.
- read-only와 write Tool을 분리하고 side effect와 timeout을 기록한다.

### LT-2 — Retrieval / RAG

- deterministic path/keyword retrieval을 첫 baseline으로 둔다.
- BM25와 embedding retrieval을 같은 dataset으로 평가한다.
- architecture, task, failure log와 git evidence에 source citation을 남긴다.

### LT-3 — Routing

- request를 frontend, API, data, deploy, security 등으로 분류한다.
- 필요한 Context와 Tool schema만 제공했을 때 token과 오류가 줄어드는지 측정한다.

### LT-4 — Stateful Workflow

- V1에서 실제로 반복된 실패에만 LangGraph state와 recovery edge를 추가한다.
- checkpoint/resume, approval, retry budget과 terminal failure를 시험한다.

### LT-5 — Evaluation·Observability·운영

- versioned eval dataset과 holdout을 만든다.
- trace, retrieval, Tool failure, latency, token과 cost를 관측한다.
- prompt/model 변경에 대한 regression gate와 실패 feedback loop를 만든다.

## 5. Landmark Assistant AEP 학습 순서

LocalTwin 실험 설계가 안정된 뒤 별도 저장소에서 시작한다. LocalTwin 코드를 복사하지 않고, 검증된 측정 원칙만 가져간다.

1. 기존 ML 의사결정 workflow와 evidence gap을 baseline으로 고정한다.
2. experiment log, dataset fingerprint, model card와 artifact contract retrieval을 만든다.
3. experiment proposal을 structured schema와 deterministic gate로 검사한다.
4. 학습·export 같은 고비용 작업 전에 Human approval과 resource budget을 둔다.
5. W&B run, aggregate metric, artifact checksum과 serving decision을 하나의 trace로 연결한다.
6. 잘못된 실험 제안, leakage 탐지, 불필요한 iteration과 검증되지 않은 claim 차단을 평가한다.

처음부터 전체 학습을 반복하지 않는다. 기존 52-run evidence와 의도적 fixture로 evaluator를 먼저 검증한 뒤, 필요한 경우에만 작은 재현 학습을 수행한다.

## 6. 반드시 남길 포트폴리오 산출물

- 두 AEP의 architecture와 trust boundary
- versioned Task/eval dataset과 holdout 분리
- Agent state와 Tool contract source
- RAG corpus manifest, retrieval benchmark와 failure case
- raw trace, token·latency·cost와 human intervention 기록
- 자동 evaluator와 human rubric의 일치·불일치 분석
- checkpoint/resume, Tool failure와 approval 시나리오
- 성공 사례뿐 아니라 효과가 없거나 악화된 ablation
- framework·vector DB·observability 도구를 선택한 Decision Record
- 다른 사람이 재현할 수 있는 runbook

## 7. 피해야 할 포트폴리오 표현

```text
LangGraph를 사용했다.
Vector DB를 구축했다.
멀티 Agent 시스템을 만들었다.
생산성이 크게 향상됐다.
```

대신 측정 후 다음처럼 말할 수 있어야 한다.

```text
LT holdout N개에서 retrieval configuration별 Task success와 token을 비교했다.
retrieval evaluator로 관련 문서 Recall@K와 잘못된 context 비율을 측정했다.
LangGraph recovery edge가 필요한 failure class와 필요하지 않은 Task를 분리했다.
LA experiment gate가 fingerprint 불일치와 검증되지 않은 artifact 선택을 얼마나 차단했는지 측정했다.
```

## 8. 현재 보유 역량과 추가 확보할 역량

### 이미 근거가 있는 것

- LocalTwin의 full-stack product, data, test, security와 deployment 경험
- Landmark의 Python/PyTorch, experiment matrix, W&B, metric 해석, ONNX와 mobile handoff 경험
- 실제 실패와 제한 사항을 문서·test·artifact contract로 남긴 경험

### 이번 AEP에서 새로 증명해야 하는 것

- 직접 구현한 Tool Calling Agent runtime
- 평가된 RAG pipeline과 Context routing
- LangGraph state, memory, Human-in-the-loop와 recovery
- Agent 전용 eval dataset·harness와 holdout
- LangSmith/Langfuse 등으로 수집한 production-shaped trace와 debugging evidence
- Agent cost, latency, reliability와 security trade-off
- 최신 agentic workflow를 분석하고 재현한 기록

## 9. 바로 다음 학습 작업

새 `localtwin-aep` 저장소에서 LT-01을 대상으로 `Baseline 계측 → typed Tool → deterministic evaluator`까지의 첫 vertical slice를 만든다.

첫 slice에는 vector DB, LangGraph와 multi-agent를 넣지 않는다. baseline trace와 evaluator가 안정된 뒤 하나씩 추가해야 각 기술의 효과와 학습 결과를 설명할 수 있다.

## 참고 근거

- [넥스트증권 AI Agent Engineer](https://nextsecurities.career.greetinghr.com/ko/o/195433)
- [핀다 AI Agent 개발자](https://finda.career.greetinghr.com/ko/o/187418)
- [매드엔진 AI Agent Engineer](https://madngine.career.greetinghr.com/ko/o/214921)
- [Shoplive AI Engineer](https://shoplive.career.greetinghr.com/ko/o/175840)
- [LangGraph 공식 overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangSmith 공식 evaluation 문서](https://docs.langchain.com/langsmith/evaluation)
- [Microsoft AutoGen AgentChat 공식 문서](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html)
