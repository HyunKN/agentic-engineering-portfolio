# AI Agent Job Skill Map for the Portfolio

작성일: 2026-08-25

이 문서는 사용자의 실제 의도를 기준으로 정리한다.

- 목표는 `LocalTwin`과 `On-device Landmark Assistant`를 서로 비교하는 것이 아니다.
- 목표는 각 프로젝트의 기존 개발/ML workflow에 AEP를 붙였을 때 무엇이 좋아지는지 전후 비교를 하는 것이다.
- 최종 종합 포트폴리오는 하나지만, 구현은 별도 `localtwin-aep`와 `landmark-assistant-aep`로 분리한다. 종합 포트폴리오에는 `LT baseline -> LT + AEP`와 `LA baseline -> LA + AEP`라는 두 개의 case study가 들어간다.

현재 채용공고와 공식 문서를 보면, 회사들이 반복해서 보는 역량은 “LLM을 호출해 본 경험”이 아니라 “AI workflow를 설계, 계측, 평가, 운영할 수 있는가”에 가깝다. 이 문서는 그 역량을 포트폴리오 artifact로 바꾸기 위한 작업 목록이다.

## 1. Python + PyTorch + ML workflow

현재 채용 신호는 Python, deep learning framework, training/evaluation, model serving을 함께 본다는 점이다. 예를 들어 Beamup 공고는 strong Python coding과 rigorous model evaluation을 요구하고, PyTorch 공식 문서는 data loading, model building, training, saving을 기본 ML workflow로 설명한다.

배워야 할 것:

- Python으로 데이터, 실험, API, automation을 끝까지 연결하는 능력
- PyTorch로 train / validate / export / inference를 이어 붙이는 능력
- model artifact와 runtime artifact를 분리해서 검증하는 습관

포트폴리오에서 증명할 artifact:

- `Landmark Assistant`의 dataset snapshot, training script, eval report, export parity check, runtime benchmark
- `LocalTwin`의 backend/API test, build, smoke test, regression trace

Sources:

- https://boards.greenhouse.io/beamup/jobs/4888237101?gh_src=Ibex+Investors+job+board&utm_medium=getro.com&utm_source=Ibex+Investors+job+board
- https://docs.pytorch.org/tutorials/index.html
- https://docs.pytorch.org/tutorials/beginner/basics/intro.html

## 2. Agent frameworks: LangChain, LangGraph, AutoGen, or equivalent

현재 공고들은 LangChain, LangGraph, AutoGen, CrewAI 같은 agent framework를 실무 경험으로 묻는다. Veracyte, D&B, Acquia, DeliveryHero, Hexion, Capgemini 계열 공고가 모두 같은 방향을 말한다. LangChain 공식 문서는 agent를 model + harness로 설명하고, LangGraph 공식 문서는 long-running stateful agent workflows를 graph runtime으로 다룬다.

배워야 할 것:

- 단순 prompt chaining이 아니라 agent harness를 설계하는 능력
- router, planner, executor, verifier를 분리해 workflow로 만드는 능력
- stateful flow와 deterministic step을 섞는 능력

포트폴리오에서 증명할 artifact:

- `LT baseline`의 direct agent
- `LT + AEP`의 retrieved-context agent, routed-context agent, stateful workflow
- `LA baseline`의 direct agent
- `LA + AEP`의 retrieved-context agent, routed-context agent, stateful workflow

Sources:

- https://boards.greenhouse.io/veracyte/jobs/5189537007
- https://jobs.lever.co/dnb/b93f1c68-a572-4af7-8263-cf08ef15a521
- https://boards.greenhouse.io/acquia/jobs/8134340
- https://careers.deliveryhero.com/job/senior-ai-engineer-agentic-ai-in-berlin-germany-jid-5224
- https://careers.hexion.com/job/Columbus-Lead-Agentic-AI-Engineer-US-Remote-US-OH%2CColumbus-OH-43085/1393842500/
- https://careers.capgemini.com/job/New-York-GenAI-Agentic-AI-Developer/1412574133/
- https://docs.langchain.com/oss/python/langchain/agents
- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.langchain.com/oss/python/langgraph/graph-api

## 3. Planning, tool-calling, and memory

채용 공고들은 이제 “agent가 답을 잘하는가”보다 “agent가 어떤 도구를 언제 쓰고, 어떤 상태를 기억하며, 어디서 멈추고 사람이 개입하는가”를 본다. OpenAI의 enterprise AI Platform 포지션은 RAG, evals, monitoring, MCP/tool use, structured outputs, multi-agent workflows를 함께 요구하고, Hexion 공고는 orchestrator-executor pattern, tool calling, memory management, agent coordination을 직접 적는다. LangChain tools 문서는 외부 데이터베이스, 코드 실행, 실세계 작업을 tool로 연결하는 걸 강조하고, LangGraph persistence 문서는 checkpoint와 short-term / long-term memory를 분리해서 설명한다.

배워야 할 것:

- planning을 자연어 한 번으로 끝내지 않고 실행 가능한 task graph로 바꾸는 능력
- tool schema를 좁혀서 불필요한 context와 실패를 줄이는 능력
- checkpoint, memory, human approval을 workflow로 설계하는 능력

포트폴리오에서 증명할 artifact:

- `task router`와 `planner` 노드
- `tool registry`와 `allowed / forbidden context` 정의
- `checkpointed run trace`와 `human intervention log`

Sources:

- https://openai.com/careers/software-engineer-enterprise-ai-platform-san-francisco/
- https://openai.com/careers/customer-enablement-lead-builder-san-francisco/
- https://careers.hexion.com/job/Columbus-Lead-Agentic-AI-Engineer-US-Remote-US-OH%2CColumbus-OH-43085/1393842500/
- https://docs.langchain.com/oss/python/langchain/tools
- https://docs.langchain.com/oss/python/langchain/context-engineering
- https://docs.langchain.com/oss/python/concepts/memory
- https://docs.langchain.com/oss/python/langgraph/persistence

## 4. RAG, vector DB, embeddings

이 분야는 거의 모든 공고가 공통으로 본다. Tavily는 RAG와 real-time reasoning을 전면에 두고, D&B와 Xsolla는 vector database와 retrieval architecture를 요구한다. Decathlon 공고는 agentic RAG, semantic caching, context window optimization, request routing, deterministic metrics까지 함께 본다. Qdrant, Chroma, Weaviate 공식 문서는 embeddings, vector search, retrieval, hybrid search를 데이터 구조와 API 수준에서 다룬다.

배워야 할 것:

- chunking, embedding, vector index, reranking, hybrid retrieval을 구분하는 능력
- project context를 “전부 읽기”가 아니라 “필요한 것만 검색하기”로 바꾸는 능력
- retrieval quality를 실제 task success와 연결하는 능력

포트폴리오에서 증명할 artifact:

- `LocalTwin`의 docs / issues / commit / code retrieval index
- `Landmark Assistant`의 paper / dataset / experiment retrieval index
- retrieval precision / recall / hit-rate / context reduction report

Sources:

- https://boards.greenhouse.io/tavily/jobs/4952166101
- https://jobs.lever.co/dnb/a8078a50-4713-45ee-b8e1-aa276a41b9e6
- https://jobs.lever.co/xsolla/4522b069-a0ed-47cc-9219-1382ab544d2d
- https://boards.greenhouse.io/decathlontechnologyen/jobs/4952375101
- https://qdrant.tech/documentation/overview/vector-search/
- https://docs.trychroma.com/docs/overview/introduction
- https://docs.weaviate.io/weaviate

## 5. Evaluation harness, datasets, and metrics

여기서 채용 시장이 가장 명확해진다. Beamup은 baseline, cross-validation, error analysis, agent behavior evaluation을 요구하고, Decathlon은 LLM test framework, golden datasets, deterministic metrics, JSON schema validation을 요구한다. D&B와 OpenAI 계열 공고도 eval frameworks, monitoring, and production tradeoffs를 강하게 본다. Langfuse 공식 문서는 eval을 repeatable check로 정의하고, production traces와 datasets, human feedback를 연결한다.

배워야 할 것:

- benchmark task를 직접 정의하고 frozen dataset으로 만드는 능력
- success / failure / regression을 같은 evaluator로 재현하는 능력
- 숫자를 만들기 전에 baseline과 control condition을 고정하는 습관

포트폴리오에서 증명할 artifact:

- `LT-01`, `LA-01` 같은 task set
- hidden evaluator와 trace schema
- success rate, regression-free success, token, time, human intervention report

Sources:

- https://boards.greenhouse.io/beamup/jobs/4888237101?gh_src=Ibex+Investors+job+board&utm_medium=getro.com&utm_source=Ibex+Investors+job+board
- https://boards.greenhouse.io/decathlontechnologyen/jobs/4952375101
- https://jobs.lever.co/dnb/b93f1c68-a572-4af7-8263-cf08ef15a521
- https://openai.com/careers/software-engineer-enterprise-ai-platform-san-francisco/
- https://langfuse.com/docs/evaluation/overview

## 6. Observability, tracing, and prompt versioning

Acquia 공고는 LangFuse를 직접 언급하면서 tracing, prompt versioning, evaluation, performance benchmarking을 요구한다. Langfuse 공식 문서도 traces, latency, costs, datasets, evaluation, dashboards를 한 흐름으로 묶는다. Anduril 공고는 agent behavior의 observability, reproducibility, and evaluation을 명시한다. 이건 단순 디버깅이 아니라 “왜 이 agent가 그렇게 행동했는지”를 재현 가능하게 만드는 역량이다.

배워야 할 것:

- prompt / tool / retrieval / output을 trace로 남기는 능력
- latency, token, cost, failure reason을 함께 보는 습관
- experiment result를 나중에 다시 검증할 수 있게 보존하는 능력

포트폴리오에서 증명할 artifact:

- run trace viewer
- prompt version history
- token / cost / latency dashboard
- failure taxonomy와 replay 가능한 trace bundle

Sources:

- https://boards.greenhouse.io/acquia/jobs/8134340
- https://boards.greenhouse.io/andurilindustries/jobs/5112335007?gh_jid=5112335007
- https://langfuse.com/docs
- https://langfuse.com/docs/observability/overview

## 7. Latest research analysis and reproduction

채용 공고들은 최신 AI 연구를 읽는 수준이 아니라, agent workflow와 model behavior를 분석하고 재현할 수 있는지를 본다. Beamup은 agent behavior evaluation을, Anduril은 reproducibility를, OpenAI는 practical AI systems experience를 요구한다. 이 포트폴리오에서는 논문 리뷰 자체보다 “이 연구 아이디어를 내 프로젝트에 어떻게 재현 가능한 task로 옮길 것인가”가 핵심이다.

배워야 할 것:

- 논문/블로그/공식 문서를 읽고 실험 설계로 바꾸는 능력
- ablation을 설계하고 “무엇이 실제로 효과를 냈는지” 분리하는 능력
- 실패한 재현도 포트폴리오 증거로 남기는 태도

포트폴리오에서 증명할 artifact:

- `AEP baseline -> retrieval -> routing -> stateful workflow` ablation
- 각 프로젝트별 mini reproduction note
- 성공 사례와 실패 사례를 같이 남긴 decision record

Sources:

- https://boards.greenhouse.io/beamup/jobs/4888237101?gh_src=Ibex+Investors+job+board&utm_medium=getro.com&utm_source=Ibex+Investors+job+board
- https://boards.greenhouse.io/andurilindustries/jobs/5112335007?gh_jid=5112335007
- https://openai.com/careers/software-engineer-enterprise-ai-platform-san-francisco/
- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.langchain.com/oss/python/langchain/context-engineering

## 8. 이 포트폴리오에서 최종적으로 보여줄 역량

이 프로젝트를 끝내면 보여줄 수 있어야 하는 것은 “AI를 써봤다”가 아니라 다음이다.

- Python 기반 AI system을 끝까지 설계하고 운영할 수 있다.
- LangChain / LangGraph / AutoGen 류의 agent framework를 목적에 맞게 선택할 수 있다.
- RAG, vector DB, embeddings, retrieval quality를 task success와 연결할 수 있다.
- planning, tool-calling, memory, human-in-the-loop를 workflow로 설계할 수 있다.
- eval harness, dataset, metric, observability를 실제 run 단위로 계측할 수 있다.
- 최신 agentic workflow 연구를 읽고 재현 가능한 engineering task로 바꿀 수 있다.

## 9. 추천 학습 순서

1. baseline Task, eval dataset과 trace schema부터 고정한다.
   - 이유: 측정이 없으면 RAG나 Agent framework의 개선도 증명할 수 없다.
2. typed Tool Calling과 deterministic retrieval을 구현한다.
   - 이유: Agent 행동과 기존 keyword/path search의 기준선을 먼저 이해해야 한다.
3. BM25·embedding RAG와 retrieval evaluation을 붙인다.
   - 이유: 거의 모든 AI engineer 공고가 공통으로 요구하지만 vector DB 사용 자체가 아니라 검색 품질을 증명해야 한다.
4. planning, memory, observability와 eval feedback loop를 붙인다.
   - 이유: prompt, Tool, retrieval, token, latency와 failure를 함께 재현해야 한다.
5. LangGraph로 stateful workflow를 붙인다.
   - 이유: 재시도, 복구, 승인, 장기 task에만 필요한 복잡도를 그때 추가하면 된다.
6. PyTorch / training / export / parity를 Landmark 쪽에서 다진다.
   - 이유: ML engineering 채용 신호를 직접 증명할 수 있다.
7. 마지막으로 최신 연구 재현과 ablation을 정리한다.
   - 이유: “읽었다”가 아니라 “내 workflow에 옮겼다”는 증거가 된다.

## 10. 한 줄 결론

이 추가 프로젝트의 목표는 두 프로젝트를 비교하는 게 아니다.

`LocalTwin`과 `Landmark Assistant` 각각의 기존 workflow 위에 AEP를 얹어서, 채용공고가 실제로 요구하는 AI Agent 역량을 “설계-구현-평가-재현”까지 보여주는 것이 목표다.
