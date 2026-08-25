# Agentic Engineering Portfolio — Master Backlog

기준일: 2026-08-25

이 문서는 GitHub 저장소와 Project를 만들기 전의 초기 계획 snapshot이다. 작업 방법은 [AEP 작업 관리 Workflow](../docs/project-management/TASK_WORKFLOW.md)를 따른다.

표기:

```text
[x] 완료하고 근거를 확인함
[ ] 아직 완료하지 않음
```

## M0 — Foundation과 작업 시스템

- [x] `FND-001` 원래 요구사항을 다시 읽고 비교 단위를 `LT baseline vs LT AEP`, `LA baseline vs LA AEP`로 수정
- [x] `FND-002` LocalTwin·Landmark source와 evidence gap 조사
- [x] `FND-003` 저장소 경계를 원본 2개, 프로젝트별 AEP 2개, 종합 portfolio로 결정
- [x] `FND-004` AI Agent 채용 역량 조사와 skill roadmap 작성
- [x] `FND-005` benchmark configuration, trace schema와 LT-01/LA-01 pilot 후보 정의
- [x] `FND-006` GitHub Project·Issue 기반 작업 Workflow와 Issue Form 초안 작성
- [ ] `FND-007` `agentic-engineering-portfolio` local Git 저장소 초기화와 첫 commit — 사용자 승인 필요
- [ ] `FND-008` GitHub 원격 저장소와 cross-repository Project 생성 — 사용자 승인 필요
- [ ] `FND-009` label, Project field, view와 automation 적용
- [ ] `FND-010` 현재 backlog를 GitHub Issue와 parent/sub-issue로 변환
- [ ] `FND-011` AEP 명칭의 전체 이름과 외부 설명을 Decision Record로 확정

M0 완료 기준:

- Portfolio 저장소, Project, label과 Issue template이 실제 GitHub에서 동작한다.
- 모든 다음 작업이 owner repository와 Project item을 가진다.
- 문서와 Issue 중 진행 상태의 source of truth가 중복되지 않는다.

## M1 — LocalTwin AEP MVP

### Scope와 저장소

- [ ] `LT-INF-001` `localtwin-aep` 목표, 비목표, trust boundary와 학습 역량 고정
- [ ] `LT-INF-002` `localtwin-aep` 저장소 생성과 Python project scaffold
- [ ] `LT-INF-003` LocalTwin source path·remote·commit 입력 contract 정의
- [ ] `LT-INF-004` secret, write Tool, network와 sandbox 정책 정의

### 공통 실행 기반의 첫 구현

- [ ] `LT-INF-005` `TaskSpec`, `RunRecord`, `ToolEvent`, `EvaluatorResult` schema 구현
- [ ] `LT-INF-006` 허용 명령, `cwd`, timeout, exit code와 stdout/stderr를 처리하는 safe command runner 구현
- [ ] `LT-INF-007` patch, event trace, verification과 artifact를 저장하는 run bundle 구현
- [ ] `LT-INF-008` model usage metadata 기반 token tracker 구현
- [ ] `LT-INF-009` versioned model price configuration과 cost calculation 구현
- [ ] `LT-INF-010` deterministic evaluator runner와 evaluator tampering 검사 구현
- [ ] `LT-INF-011` 실행 기반 unit test와 failure fixture 작성

### LT-01 fixture

- [ ] `LT-01-A` LocalTwin `8ac6178...` source archive builder 구현
- [ ] `LT-01-B` 기존 history·remote가 없는 isolated root commit 생성
- [ ] `LT-01-C` docs index pass와 docs HTML fail을 자동 재현
- [ ] `LT-01-D` agent-visible Task와 organizer-only provenance·evaluator 분리
- [ ] `LT-01-E` checker 약화, target 삭제와 scope 이탈을 차단하는 hidden evaluator 작성
- [ ] `LT-01-F` fixture rebuild reproducibility와 checksum 검증

### V0 Direct Agent

- [ ] `LT-V0-001` model provider interface와 structured response contract 구현
- [ ] `LT-V0-002` read/search/edit/test Tool의 최소 집합 구현
- [ ] `LT-V0-003` 일반 project instruction만 사용하는 Direct Agent 구성
- [ ] `LT-V0-004` LT-01 V0 dry run 1회와 전체 trace 보존
- [ ] `LT-V0-005` 정답 누출, Tool 우회, trace 누락과 evaluator false positive 점검
- [ ] `LT-V0-006` pilot 결과로 schema와 Task contract를 한 번 수정

M1 완료 기준:

- LT-01 fixture를 한 명령으로 다시 만들 수 있다.
- V0 run이 token·시간·Tool·patch·evaluator 결과를 남긴다.
- Agent는 원본 history, 정답 patch와 hidden evaluator에 접근하지 못한다.

## M2 — LocalTwin Retrieval·Routing·Workflow 실험

### Evaluation dataset

- [ ] `LT-EVAL-001` LocalTwin 후보 Task의 난이도·유형 taxonomy 작성
- [ ] `LT-EVAL-002` development Task와 holdout Task 분리
- [ ] `LT-EVAL-003` deterministic evaluator와 human rubric 작성
- [ ] `LT-EVAL-004` evaluator false positive/negative golden case 검증

### V1A Retrieval / RAG

- [ ] `LT-V1A-001` Context source inventory와 source-of-truth priority 정의
- [ ] `LT-V1A-002` deterministic path/keyword retrieval baseline 구현
- [ ] `LT-V1A-003` BM25 corpus·index·citation 구현
- [ ] `LT-V1A-004` embedding과 vector store 후보를 비교하고 하나 선택
- [ ] `LT-V1A-005` chunking, metadata filter와 hybrid retrieval 구현
- [ ] `LT-V1A-006` retrieval eval dataset과 Recall@K/MRR/context precision 측정
- [ ] `LT-V1A-007` 동일 Task에서 V0와 V1A 반복 실행

### V1B Context·Tool Routing

- [ ] `LT-V1B-001` request type과 project area taxonomy 정의
- [ ] `LT-V1B-002` router와 fallback 구현
- [ ] `LT-V1B-003` Task별 Context source와 Tool schema 제한
- [ ] `LT-V1B-004` routing accuracy, token, Tool failure와 fallback 측정
- [ ] `LT-V1B-005` 동일 Task에서 V1A와 V1B 반복 실행

### V2 LangGraph

- [ ] `LT-V2-001` V0/V1 failure taxonomy에서 stateful recovery 필요 사례 선정
- [ ] `LT-V2-002` state schema와 graph node/edge 설계
- [ ] `LT-V2-003` checkpoint, retry budget와 terminal state 구현
- [ ] `LT-V2-004` 위험한 write/deploy 작업의 Human-in-the-loop 구현
- [ ] `LT-V2-005` interruption/resume, Tool failure와 approval 시나리오 test
- [ ] `LT-V2-006` V1B와 V2 반복 실행 및 ablation

### Observability와 결과

- [ ] `LT-OBS-001` LangSmith 또는 Langfuse 중 하나를 선택하고 Decision Record 작성
- [ ] `LT-OBS-002` LLM·retrieval·Tool·verification trace 연결
- [ ] `LT-OBS-003` latency·token·cost·failure dashboard 구성
- [ ] `LT-OBS-004` 실패 trace를 eval dataset으로 되돌리는 feedback loop 구현
- [ ] `LT-RES-001` LT holdout 실행과 raw result 동결
- [ ] `LT-RES-002` success, regression, token, cost, time와 human intervention 분석
- [ ] `LT-RES-003` 효과 없음·악화 조건과 limitation 기록

M2 완료 기준:

- 같은 LT Task에서 V0/V1A/V1B/V2의 통제된 결과가 있다.
- RAG와 LangGraph 사용 이유를 실제 metric과 failure evidence로 설명할 수 있다.
- 결과는 Landmark 점수와 합산하지 않는다.

## M3 — Landmark Assistant Integrity와 AEP MVP

### 시작 전 evidence 복구

- [ ] `LA-INT-001` S4 validation 1위와 S3 handoff를 연결하는 Deployment Decision 작성
- [ ] `LA-INT-002` 23-class split manifest와 checksum 탐색·복구 또는 영구 gap 선언
- [ ] `LA-INT-003` ONNX/checkpoint와 artifact validation 원본 탐색·복구 또는 gap 선언
- [ ] `LA-INT-004` EOL 영향을 받지 않는 source provenance 기준 정의

### Scope와 저장소

- [ ] `LA-INF-001` `landmark-assistant-aep` 목표, 비목표, trust boundary와 학습 역량 고정
- [ ] `LA-INF-002` 별도 Python project와 저장소 생성
- [ ] `LA-INF-003` raw data·W&B·model artifact의 민감도와 공개 정책 정의
- [ ] `LA-INF-004` 학습·export Tool의 resource budget과 Human approval 정책 정의

### LA-01 fixture와 baseline

- [ ] `LA-01-A` public base commit에서 isolated fixture builder 구현
- [ ] `LA-01-B` `class_count 23 → 22` drift 적용 후 새 root commit 생성
- [ ] `LA-01-C` contract 1 fail·portfolio 13 pass를 자동 재현
- [ ] `LA-01-D` pristine manifest, mutation patch와 hidden evaluator 차단
- [ ] `LA-01-E` LA 전용 schema·runner·trace 구현
- [ ] `LA-V0-001` 기존 ML 의사결정 방식의 Direct Agent baseline 구성
- [ ] `LA-V0-002` LA-01 dry run과 evaluator 우회·정답 누출 점검

M3 완료 기준:

- LA-01이 실제 source contract에서 파생됐지만 현재 제품 결함으로 오해되지 않는다.
- dataset·experiment·artifact evidence boundary가 명시된다.
- 고비용 또는 외부 side effect Tool은 approval 없이 실행되지 않는다.

## M4 — Landmark Retrieval·Experiment Workflow 실험

### Evidence retrieval

- [ ] `LA-V1A-001` dataset, paper/model card, W&B run, metric와 artifact corpus 정의
- [ ] `LA-V1A-002` evidence metadata, lineage와 citation schema 구현
- [ ] `LA-V1A-003` deterministic/BM25/embedding retrieval 비교
- [ ] `LA-V1A-004` evidence retrieval dataset과 metric 구성

### Experiment Tool·Routing

- [ ] `LA-V1B-001` dataset audit, metric aggregation, proposal, export와 artifact Tool contract 구현
- [ ] `LA-V1B-002` data/model/export/deploy request routing 구현
- [ ] `LA-V1B-003` fingerprint, split, metric와 artifact gate 구현
- [ ] `LA-V1B-004` invalid proposal와 검증되지 않은 claim 차단 평가

### Stateful ML workflow

- [ ] `LA-V2-001` Evidence→Propose→Approve→Run/Simulate→Evaluate→Decide graph 설계
- [ ] `LA-V2-002` GPU 학습·export 전 Human approval와 budget gate 구현
- [ ] `LA-V2-003` W&B run, aggregate metric, artifact checksum과 decision trace 연결
- [ ] `LA-V2-004` 실패·중단·재개와 artifact parity 시나리오 검증

### 결과

- [ ] `LA-EVAL-001` development/holdout ML Task와 evaluator 구성
- [ ] `LA-RES-001` V0/V1A/V1B/V2 반복 실행
- [ ] `LA-RES-002` invalid proposal, leakage, unsupported claim와 iteration 분석
- [ ] `LA-RES-003` GPU 시간·비용은 실제 측정 또는 명시된 추정으로 분리
- [ ] `LA-RES-004` 효과 없음·악화 조건과 limitation 기록

M4 완료 기준:

- 기존 LA workflow와 LA AEP의 결과를 같은 LA Task 안에서 비교할 수 있다.
- 모델 성능 향상과 Agent workflow 품질을 섞지 않는다.
- expensive experiment 감소 주장은 실제 trace나 명시된 simulation으로만 한다.

## M5 — 종합 포트폴리오와 채용 artifact

- [ ] `PF-001` LocalTwin AEP Case Study 작성
- [ ] `PF-002` Landmark Assistant AEP Case Study 작성
- [ ] `PF-003` 각 Case Study의 문제·결정·개인·Agent·팀 기여표 작성
- [ ] `PF-004` architecture, trust boundary와 workflow diagram 작성
- [ ] `PF-005` raw result에서 공개 chart로 이어지는 provenance 구성
- [ ] `PF-006` Python·Tool Calling·RAG·LangGraph·eval·observability skill evidence 연결
- [ ] `PF-007` 실패 사례, cost와 limitation section 작성
- [ ] `PF-008` 재현 runbook과 최소 공개 fixture 작성
- [ ] `PF-009` 공개 portfolio site 또는 docs build 구현
- [ ] `PF-010` demo video와 발표자료 제작
- [ ] `PF-011` 이력서 bullet과 면접 설명 작성
- [ ] `PF-012` 공개 전 secret·license·개인정보·model/data 검토
- [ ] `PF-013` 최종 링크·재현·접근성 검증

M5 완료 기준:

- 채용자가 두 Case Study의 baseline, AEP 변화, 측정 결과와 본인 기여를 빠르게 확인할 수 있다.
- framework 이름이 아니라 source, trace, evaluator, metric과 failure evidence로 역량을 증명한다.
- 공개할 수 없는 자료와 검증하지 못한 주장을 명확히 분리한다.

## 현재 바로 시작할 Task

GitHub 외부 생성 승인 전:

- 다음 실행 항목: `LT-INF-001` — `localtwin-aep` scope와 trust boundary 작성

GitHub 외부 생성 승인 후:

- 전환 순서: `FND-007`~`FND-010` — 이 backlog를 실제 Issue/Project로 전환
