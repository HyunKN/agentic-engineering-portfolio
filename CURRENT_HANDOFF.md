# Handoff: AI-assisted Engineering Portfolio

작성일: 2026-08-24
현재 primary host: 이 노트북의 Codex Desktop
작업 폴더: 이 repository의 root

## 1. 사용자의 목표

기존 프로젝트를 단순 복습하거나 최신 framework로 포장하는 것이 아니다.

LocalTwin과 On-device Landmark Assistant의 실제 코드·문서·commit·실험 기록을 각각 controlled engineering task로 바꾼다. 각 프로젝트에서 기존의 ad-hoc AI 사용 방식과 프로젝트 전용 AEP를 비교하고, 성공률, token·비용, 시간, 사람 개입과 품질을 실제 run에서 측정한다.

LocalTwin과 Landmark Assistant를 서로 비교하지 않는다. 두 프로젝트는 서로 다른 lifecycle에서 AI Agent 역량을 학습하고 증명하는 독립 Case Study다.

대상 lifecycle:

- LocalTwin: Software Product Engineering
- On-device Landmark Assistant: ML Model Development & Deployment

## 2. 실험 원칙

- 과거 token, 시간과 개선률을 추측하지 않는다.
- 같은 Task, starting state, model, tool budget과 evaluator를 사용한다.
- 정답 commit, pristine fixture와 future fix를 Agent context에서 차단한다.
- 제품 성능, 모델 성능과 Agent workflow 성능을 분리한다.
- LangChain은 구현 수단이지 실험 변수 자체가 아니다.
- V0 Direct, V1A Retrieval, V1B Routing, V2 Stateful Workflow를 단계적으로 비교한다.
- LangGraph는 V1B 결과에서 상태·복구 loop의 필요성이 확인된 Task에만 사용한다.
- V0/V1A/V1B/V2 비교는 같은 프로젝트의 같은 Task 안에서만 한다.
- LocalTwin AEP와 Landmark AEP의 Tool, Context, Workflow와 evaluator는 별도로 설계한다.
- 공통 Core는 먼저 만들지 않고 실제 중복이 확인된 뒤에만 추출한다.
- 개인, Agent, 팀과 외부 모델·서비스의 기여를 분리하되 근거 없는 퍼센트는 만들지 않는다.

## 3. 이 노트북에서 확인한 경로

- LocalTwin: [HyunKN/hub-fork@8ac6178](https://github.com/HyunKN/hub-fork/tree/8ac6178ed41c3056b4353cc2449791a335051dd5)
- Landmark 원천 작업: 별도 로컬 작업본이며 공개 저장소는 아직 연결하지 않음
- Portfolio planning: 이 repository
- LocalTwin AEP: 아직 생성하지 않음. 별도 `localtwin-aep` 저장소로 만들 예정
- Landmark AEP: 아직 생성하지 않음. 별도 `landmark-assistant-aep` 저장소로 만들 예정

`.env`, credential 값과 비공개 model/data 내용은 출력하거나 외부로 옮기지 않는다.

## 4. 완료한 조사와 재현

### LocalTwin

- `main`, HEAD `8ac6178ed41c3056b4353cc2449791a335051dd5`, clean, 531 tracked files, 751 commits를 확인했다.
- `.harness/tasks` 73개와 `.harness/runs` 75개를 확인했다.
- web test file 48개와 API test file 26개를 확인했지만 전체 suite와 production build는 다시 실행하지 않았다.
- `python -B scripts/check_docs_index.py`는 통과했다.
- `python -B scripts/check_docs_html.py`는 다음 기존 오류를 재현했다.

```text
docs/wiki/doc-viewer.html: document tree is missing docs/issues/industry-taxonomy-and-map-performance.md
```

- SQLite를 read-only URI로 조회해 `store_points` 537,489, `store_market_links` 4,548을 확인했다.
- DB의 store/sales/flow metrics는 `20251`~`20254` 4개 분기다.
- 현재 web의 `market-analysis.json`은 `20251` 한 분기, 12개 상권·업종 조합이다.
- 공식 Agent evaluation entry와 run trace는 없다.
- 73개 Task Packet 중 `Owner`가 있는 것은 51개이고 22개는 누락되어 있다. 현재 기록만으로 개인·Agent 기여율을 계산할 수 없다.
- 자세한 source → test → deploy → commit 연결은 `LOCALTWIN_EVIDENCE_MAP.md`에 있다.

### On-device Landmark Assistant

- 공개 portfolio repository 원격 `main` HEAD는 `823ccdabc56bd512cb77d8e498f172cdd0f116db`다.
- 임시 clone에서 portfolio test 13개와 metadata contract test 3개가 통과했다.
- 노트북 raw W&B export 52개는 `40 main + 12 screening` 구성과 일치했다.
- 공개 8개 aggregate metric을 raw 52-run summary에서 8/8 다시 확인했다.
- training source 10개, Sprint 1 prototype source 16개와 team-app integration contract/script/patch의 commit provenance를 대조했다.
- 52개 run은 23-class fingerprint를 공유하지만, 노트북에 남은 실제 split manifest는 이전 22-class다.
- 원본 ONNX/checkpoint와 artifact validation JSON은 현재 조사 범위에 없다.
- S4는 validation 평균 1위이고 S3가 실제 FP16 handoff다. 배포 기준의 가중치를 명시한 최종 Decision Record가 필요하다.

### 두 Pilot의 manual reproduction

- LT-01: 위 LocalTwin docs HTML 실패를 base commit에서 재현했다.
- LA-01: 공개 manifest의 `class_count 23 -> 22` drift fixture에서 contract test 3개 중 1개 실패, portfolio test 13개 통과를 재현했다.
- LA-01 fixture는 drift 적용 후 새 root commit으로 만들어 pristine history와 정답 diff가 노출되지 않게 해야 한다.

## 5. 현재 기준 문서

- `README.md`: 전체 진행 지도와 다음 작업
- `PORTFOLIO_THESIS.md`: 연구 질문과 주장 제한
- `EVIDENCE_AUDIT.md`: 확인된 사실과 공백
- `LOCALTWIN_EVIDENCE_MAP.md`: LocalTwin source·test·deploy·commit 근거 지도
- `BENCHMARK_V1.md`: configuration, metric, LT-01/LA-01 pilot 계약
- `docs/strategy/AI_SKILL_ROADMAP.md`: 채용 목표 역량과 AEP 산출물 연결
- `docs/research/AI_AGENT_JOB_SKILLS.md`: 현재 채용공고와 공식 문서 조사
- `tasks/BACKLOG.md`: 전체 작업 ID, 상태, 선후관계와 체크리스트
- `docs/project-management/TASK_WORKFLOW.md`: GitHub Project·Issue·Milestone 운영 규칙
- `docs/research/GITHUB_TASK_TRACKING.md`: GitHub 공식 기능과 권장 구조 조사
- `docs/project-management/ISSUE_AUTHORING_AI_WORKFLOW.md`: AI Issue JSON draft, validation, preview와 apply 절차
- `docs/project-management/AGENT_WORKFLOWS_ARCHITECTURE.md`: portfolio 운영용 workflow module의 경계와 구조
- `docs/project-management/EVALUATION_PACKET_WORKFLOW.md`: 외부 Web AI 검토용 immutable evidence packet 절차
- `governance/PUBLIC_EVIDENCE_POLICY.md`: 공개할 evidence와 제외할 민감정보 기준
- `CURRENT_HANDOFF.md`: 현재 작업 상태

Portfolio planning은 공개 [agentic-engineering-portfolio](https://github.com/HyunKN/agentic-engineering-portfolio)의 `main`과 연결됐다. 이 repository에는 공통 AEP runner를 구현하지 않는다. GitHub Project와 초기 Issue 전환이 끝날 때까지 `tasks/BACKLOG.md`를 임시 source of truth로 사용한다.

AI가 작성하는 Issue는 `agent_workflows.issue_authoring` module로 검증한다. 2026-08-27에 이 workflow를 이용해 parent Issue `#4`~`#9`의 손상된 줄바꿈을 복구했고 GitHub round-trip을 확인했다.

외부 Web AI 검토 자료는 `agent_workflows.evaluation_packet` module로 만든다. 이 module은 고정 Git commit의 명시적 source allowlist만 복사하고 SHA256 manifest, 질문, 알려진 공백과 제외 사유를 기록한다. 두 module의 local path·secret pattern 검사는 `agent_workflows.publication_safety`가 공유한다. 이들은 portfolio 운영 자동화이며 LocalTwin/LA 전용 AEP runtime의 공통 Core가 아니다.

첫 packet `agent-workflows-v1`을 만든 뒤 실제 Issue 재적용에서 duplicate parent 오류를 발견했고 `a9ff6f56d1f1b8e3a847836417b27c66a9eb79c2`에서 idempotent 처리와 regression test를 추가했다. `v1`은 역사적 snapshot으로 보존한다. 최신 `evaluation_packets/agent-workflows-v2`는 이 수정 commit의 source 13개와 생성 문서 3개를 담고 있으며 총 17개 file(MANIFEST 포함)의 SHA256 검증이 통과했다. 외부 AI review는 아직 실행하지 않았으며 결과가 생기면 `reviews/agent-workflows-v2/`에 원문과 사람의 triage를 분리해 저장한다.

## 6. 바로 다음 작업

1. GitHub Project OAuth scope를 확보하고 `FND-009`를 완료한다.
2. `LT-INF-001`로 `localtwin-aep`의 목표, 비목표, 학습 역량과 repository boundary를 고정한다.
3. 새 LocalTwin AEP 저장소를 만들고 LT-01 starting state를 격리된 fixture로 동결한다.
4. LT run metadata, retrieved context, Tool call, token, elapsed time, human intervention, patch와 evaluator result를 남기는 최소 runner를 만든다.
5. runner가 정답이나 forbidden context를 누설하지 않는지 LT-01 V0 dry run으로 확인한다.
6. LT V1A/V1B/V2를 단계적으로 구현하고 ablation을 수행한다.
7. LocalTwin 실험 설계가 안정된 뒤에만 별도 Landmark AEP를 시작한다.

첫 LT pilot 결과만으로 configuration의 우열이나 개선 퍼센트를 주장하지 않는다.

## 7. 채용 역량 목표

이 추가 프로젝트의 목적에는 다음 실무 역량을 실제 artifact로 습득·증명하는 것이 포함된다.

- Python 기반 Agent backend와 Tool/Function Calling
- LangChain/LangGraph를 이용한 planning, state, memory, retry와 Human-in-the-loop
- embedding, chunking, vector/hybrid search와 retrieval evaluation을 포함한 RAG
- 자동 evaluation dataset·harness·regression gate 설계
- tracing, latency, token, cost와 failure observability
- PyTorch 기반 ML workflow, dataset/artifact provenance와 experiment evaluation
- 최신 agentic workflow를 읽고 작은 재현 실험으로 검증하는 능력

Framework 이름을 나열하는 것이 아니라 architecture, failure evidence, metric과 재현 절차로 증명한다.

## 8. 남은 Integrity Task

- S4 validation 1위와 S3 handoff를 연결하는 Deployment Decision 작성
- 23-class split manifest와 artifact checksum 원본 복구 또는 공백 명시
- LocalTwin의 개인·팀·Agent 기여를 실제 trace와 decision 단위로 재구성
- LocalTwin docs tree 결함은 benchmark fixture를 동결하기 전 원본 저장소에서 수정하지 않기
- Landmark source의 EOL 영향 없는 portable provenance 기준 정하기

## 9. 검증 경계

이번 노트북 audit은 repository 구조, 선택 test, provenance, SQLite counts와 두 pilot 재현까지다. 다음은 아직 검증하지 않았다.

- LocalTwin 현재 `main` 전체 test/lint/typecheck/build
- Landmark 전체 training, ONNX export/parity와 mobile runtime
- Agent workflow의 성공률·비용·시간 개선
- Task Packet/commit 수 기반 개인·Agent 기여 퍼센트
