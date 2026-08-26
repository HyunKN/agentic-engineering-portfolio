# Agentic Engineering Portfolio

## 현재 한 줄 목표

LocalTwin과 Landmark Assistant 각각에서 기존의 ad-hoc AI 사용 방식을 baseline으로 재현하고, 프로젝트 전용 AEP를 단계적으로 적용해 성공률·비용·사람 개입과 품질이 실제로 개선되는지 측정한다.

## 대상 프로젝트

- [LocalTwin](https://github.com/HyunKN/hub): Software Product Engineering 사례
- [On-device Landmark Assistant](https://github.com/HyunKN/ondevice-landmark-assistant): ML Engineering과 on-device model integration 사례

두 원본 프로젝트를 서로 비교하지 않는다. 이미 존재하는 코드, 문서, commit과 실험 결과를 각 프로젝트 내부의 `기존 방식 → AEP 적용 방식` 비교를 위한 재현 가능한 평가 자료로 바꾼다.

## 저장소와 실험 경계

```text
LocalTwin 원본 ───────→ localtwin-aep
                         LT baseline vs LT AEP

Landmark 원본 ───────→ landmark-assistant-aep
                         LA baseline vs LA AEP

두 결과 ─────────────→ agentic-engineering-portfolio
                         종합 문서·채용 포트폴리오
```

- `localtwin-aep`와 `landmark-assistant-aep`는 Context, Tool, Workflow, Task와 evaluator를 별도로 가진다.
- 이 `portfolio` 폴더는 두 AEP의 구현 저장소가 아니라 연구 질문, 증거, 결과와 Case Study를 연결하는 상위 포트폴리오다.
- 공통 library나 framework는 미리 만들지 않는다. 두 AEP에서 실제 중복과 안정된 interface가 확인된 뒤에만 추출한다.

## 임시 대상 직무

```text
Primary: Applied AI / AI Agent Engineer
Supporting: ML Engineer + LLMOps / Agent Evaluation
Foundation: Product Engineering + Python/PyTorch
```

구체적인 학습 목표와 증명 산출물은 [AI 역량 개발 계획](./docs/strategy/AI_SKILL_ROADMAP.md)에 정리한다. 지원 회사와 채용 공고가 정해지면 우선순위만 조정한다.

## 전체 진행 지도

| 단계 | 하는 일 | 산출물 | 상태 |
| --- | --- | --- | --- |
| 0. Foundation | 목적, 증거, 실험 규칙과 채용 역량 고정 | Thesis, Evidence Audit, Skill Roadmap | 진행 중 |
| 1. LocalTwin AEP | LT 전용 저장소·Task·baseline·evaluator 구성 | `localtwin-aep`, LT Task Set v1 | 다음 |
| 2. LocalTwin Experiment | LT 안에서 Direct → Retrieval → Routing → Workflow 비교 | LT trace, ablation, failure analysis | 대기 |
| 3. Landmark AEP | LA 전용 저장소·ML Task·artifact gate 구성 | `landmark-assistant-aep`, LA Task Set v1 | 대기 |
| 4. Landmark Experiment | LA 안에서 기존 방식과 AEP를 비교 | LA trace, experiment-quality analysis | 대기 |
| 5. Portfolio | 두 독립 Case Study와 습득 역량을 연결 | 공개 페이지, 영상, 발표자료 | 대기 |

## 중요한 원칙

- 과거 token 수나 작업 시간을 추측해서 개선률을 만들지 않는다.
- 동일한 Task, starting commit, model, tool budget으로 비교한다.
- Agent가 과거 정답 commit이나 미래 결과 문서를 읽지 못하게 한다.
- 자동 test와 명시적 acceptance criteria를 주 평가 기준으로 쓴다.
- Agent 성능과 LocalTwin 제품 성능 또는 Landmark 모델 성능을 섞지 않는다.
- LocalTwin 점수와 Landmark 점수를 합치거나 우열 비교하지 않는다.
- 동일한 configuration 이름을 사용하더라도 프로젝트별 Tool, Context와 evaluator는 독립적으로 설계한다.
- RAG, LangChain, LangGraph는 사용 자체가 목표가 아니다.

## 완료의 의미

최종적으로 다음 질문에 실제 측정값으로 답할 수 있어야 한다.

1. LocalTwin의 기존 개발 방식보다 LocalTwin AEP가 성공률·비용·사람 개입을 개선했는가?
2. Landmark의 기존 ML workflow보다 Landmark AEP가 잘못된 실험·근거 없는 주장·불필요한 iteration을 줄였는가?
3. 각 프로젝트에서 Retrieval, Routing과 LangGraph 중 실제 효과가 있었던 요소는 무엇인가?
4. 각 AEP에서 효과가 없거나 오히려 나빠진 조건은 무엇이었는가?
5. 두 독립 실험을 마친 뒤 공통화할 가치가 있다고 확인된 구성요소는 무엇인가?

## 현재 문서

- [포트폴리오 주제와 연구 질문](./PORTFOLIO_THESIS.md)
- [현재 증거와 공백](./EVIDENCE_AUDIT.md)
- [LocalTwin source·test·deploy·commit Evidence Map](./LOCALTWIN_EVIDENCE_MAP.md)
- [Benchmark v1 초안](./BENCHMARK_V1.md)
- [AI 역량 개발 계획](./docs/strategy/AI_SKILL_ROADMAP.md)
- [AI Agent 채용 역량 조사](./docs/research/AI_AGENT_JOB_SKILLS.md)
- [Master Backlog](./tasks/BACKLOG.md)
- [GitHub 작업 Issues](https://github.com/HyunKN/agentic-engineering-portfolio/issues)
- [GitHub 작업 관리 Workflow](./docs/project-management/TASK_WORKFLOW.md)
- [AI Issue 작성·검증 Workflow](./docs/project-management/ISSUE_AUTHORING_AI_WORKFLOW.md)
- [Agent Workflows 구조](./docs/project-management/AGENT_WORKFLOWS_ARCHITECTURE.md)
- [External AI Evaluation Packet Workflow](./docs/project-management/EVALUATION_PACKET_WORKFLOW.md)
- [Public Evidence Policy](./governance/PUBLIC_EVIDENCE_POLICY.md)
- [첫 공개 Evaluation Packet](./evaluation_packets/agent-workflows-v1/README.md)
- [외부 AI Review 저장·판정 규칙](./reviews/README.md)
- [GitHub task tracking 조사](./docs/research/GITHUB_TASK_TRACKING.md)

## 바로 다음 작업

두 개의 작은 pilot 후보는 2026-08-23 노트북에서 manual reproduction을 마쳤다.

1. LocalTwin의 현재 docs tree 검증 실패
2. On-device Landmark Assistant의 model contract drift fixture

바로 다음 구현은 이 폴더 안에 공통 runner를 만드는 것이 아니다. 별도 `localtwin-aep` 저장소의 scope와 학습 목표를 먼저 고정하고, LT-01 starting state를 격리된 fixture로 동결한 뒤 LT 전용 최소 runner와 evaluator를 만든다. Landmark AEP는 LocalTwin 실험 설계가 안정된 다음 별도 저장소에서 시작한다.

작업 진행은 [Master Backlog](./tasks/BACKLOG.md)의 ID와 체크리스트로 추적하고 있다. GitHub Project 권한 설정이 끝나면 하나의 user-level Project에서 여러 저장소의 Issue를 모아 보고, 각 저장소의 Milestone과 Issue를 실행 기준으로 전환한다.

첫 LT pilot은 V0/V1A/V1B/V2의 우열을 결론 내리는 실험이 아니다. starting state, allowed/forbidden context, trace schema와 evaluator 실행 방식이 제대로 동작하는지만 확인한 뒤 LT Task와 schema를 한 번 수정한다.
