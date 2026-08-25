# Benchmark v1 Draft

상태: 후보 Task 정의 단계. 아직 frozen benchmark가 아니다.

## 1. 목적

각 원본 프로젝트 안에서 동일한 engineering Task를 기존 방식과 프로젝트 전용 AEP configuration으로 실행해 성공률, 비용, Context 사용과 사람 개입을 비교한다.

과거 프로젝트 기록은 작업 문제와 evaluator를 만드는 데 사용한다. 과거 작업 시간이나 token 수를 추측해서 baseline 수치로 사용하지 않는다.

```text
LT Task: LT V0 vs LT V1A/V1B/V2
LA Task: LA V0 vs LA V1A/V1B/V2
LT score vs LA score: 비교하지 않음
```

이 문서는 두 benchmark의 공통 실험 규칙과 후보 Task를 모은 상위 초안이다. 실제 runner, Context index, Tool과 evaluator는 `localtwin-aep`와 `landmark-assistant-aep`가 각각 소유한다.

## 2. 비교 Configuration

아래 이름은 두 AEP에서 같은 ablation 순서를 설명하기 위한 공통 vocabulary다. 동일한 구현이나 공통 framework를 전제하지 않는다.

### V0 — Direct Agent

```text
동일 모델
기본 repository search/read/edit/test Tool
일반적인 project instruction
```

현재 Codex를 일반적으로 사용하는 방식에 가장 가까운 재현 가능한 baseline이다.

### V1A — Retrieved-context Agent

V0에 다음을 추가한다.

```text
Task contract
Project rules
관련 문서 retrieval
명시적인 verification plan
```

전체 Tool 집합은 V0와 같게 두고 retrieval 효과만 분리해서 측정한다.

### V1B — Routed-context Agent

V1A에 request classification과 Context/Tool routing을 추가한다.

```text
request type과 project area 분류
관련 Context source만 검색
Task에 필요한 Tool schema만 제공
routing decision과 fallback 기록
```

LangChain 사용 여부 자체는 실험 변수가 아니다. 동일한 capability를 유지한 채 retrieval과 routing behavior의 효과를 비교하고, LangChain은 필요한 경우 그 behavior를 구현하는 수단으로만 사용한다.

### V2 — Stateful Workflow

V1B에서 상태 저장이나 실패 복구가 필요한 Task에 다음 흐름을 적용한다.

```text
Analyze
→ Retrieve
→ Plan
→ Execute
→ Verify
→ Pass 또는 Diagnose
→ 필요 시 Human approval
```

V1B에서 필요성이 확인되지 않으면 LangGraph를 추가하지 않는다.

## 3. 공정한 비교 규칙

- 비교는 반드시 같은 프로젝트의 같은 Task 안에서만 수행한다.
- Task마다 동일한 starting commit을 사용한다.
- 정답 commit과 미래 결과 문서는 Agent가 읽지 못하게 한다.
- model, temperature, timeout, retry, tool budget을 기록하고 가능하면 고정한다.
- 각 configuration은 같은 evaluator로 채점한다.
- 개발 중 사용하는 Task와 최종 holdout Task를 분리한다.
- 핵심 Task는 configuration별 최소 2~3회 반복한다.
- 실패하거나 중단된 run도 결과에서 삭제하지 않는다.
- LocalTwin과 Landmark 결과를 평균·합산하거나 단일 순위로 만들지 않는다.
- 공통 metric 이름을 쓰더라도 evaluator와 성공 기준은 프로젝트별로 따로 둔다.

## 4. LocalTwin 후보 Task

| ID | 후보 문제 | 주요 평가 |
| --- | --- | --- |
| LT-01 | 현재 docs tree 검사 실패 | 원인 진단, 최소 수정, 동일 검사 통과 |
| LT-02 | React 검색·선택·지도 state regression | 관련 test, UI state contract, 불필요한 diff |
| LT-03 | API response와 data provenance 변경 | contract test, source/period/unit 보존 |
| LT-04 | 3D lazy-loading과 초기 bundle boundary | build 결과, 초기 chunk, UI regression |
| LT-05 | Scene media validation과 resource limit | 보안 test, 실패 cleanup, scope 제한 |
| LT-06 | 제품과 문서 deployment artifact 경계 | artifact allowlist, route smoke, secret 노출 방지 |

## 5. On-device Landmark Assistant 후보 Task

| ID | 후보 문제 | 주요 평가 |
| --- | --- | --- |
| LA-01 | serving contract의 class/model/embedding metadata 불일치 | contract test 기반 탐지와 최소 수정 |
| LA-02 | 과거 `server_full` config 이름과 실제 partial unfreeze 범위 불일치 | config semantic validation과 잘못된 비교 차단 |
| LA-03 | dataset fingerprint/split mismatch | 실험 비교 차단, leakage 방지 |
| LA-04 | S4 validation 1위와 S3 final handoff 결정 | accuracy와 artifact/runtime evidence를 분리한 Decision |
| LA-05 | Android compressed large-asset cache invalidation | 실제 historical patch, 재현 test, app/model ownership 경계 |
| LA-06 | INT8/NPU latency와 accuracy parity 판단 | 배포 artifact gate와 실패 원인 분리 |

## 6. 측정값 정의

공통 metric은 두 프로젝트의 결과 저장 형식을 맞추기 위한 것이며, 서로 다른 Task 사이의 직접적인 수치 비교를 허용하지 않는다.

### Primary

```text
Task Success:
필수 acceptance criteria와 hidden evaluator를 모두 통과한 비율

Regression-free Success:
Task test와 기존 관련 test를 함께 통과한 비율

Human Intervention:
사람이 제공한 추가 정보, 수정 지시, 승인 횟수와 소요 시간

Cost per Successful Task:
전체 LLM 비용을 성공한 Task 수로 나눈 값
```

### Secondary

```text
입력/출력 token
wall-clock time
LLM 호출 수
Tool 호출 수와 실패율
읽은 파일 수
retrieved context 중 실제 수정·근거에 사용된 비율
변경 파일 수와 불필요한 diff
retry/diagnose loop 수
```

### ML 전용

```text
invalid experiment proposal rate
fingerprint/leakage 위반 탐지율
검증되지 않은 claim 차단율
불필요한 GPU run 수 또는 예상 GPU 시간
model/artifact selection correctness
```

## 7. Trace 최소 Schema

각 run은 최소한 다음을 저장한다.

```text
run_id
task_id
project
starting_commit
agent_configuration
model
prompt_version
allowed_context
forbidden_context
tool_budget
retrieved_files
tool_calls
token_usage
elapsed_time
human_interventions
patch
verification_commands
verification_results
evaluator_scores
final_status
failure_reason
```

## 8. 프로젝트별 Pilot

### LocalTwin 첫 Pilot — LT-01

목표:

```text
LocalTwin docs 검사를 재현하고, 누락된 문서 tree 항목의 원인을 찾아 최소 수정으로 검사를 통과시킨다.
```

2026-08-23 manual reproduction:

```text
base commit: 8ac6178ed41c3056b4353cc2449791a335051dd5
index evaluator: python -B scripts/check_docs_index.py -> pass
HTML evaluator: python -B scripts/check_docs_html.py -> fail
observed error: docs/wiki/doc-viewer.html: document tree is missing docs/issues/industry-taxonomy-and-map-performance.md
```

Acceptance criteria:

- docs index check와 docs HTML check가 모두 통과한다.
- 누락된 실제 문서를 삭제하거나 checker를 약화하지 않는다.
- `doc-viewer.html`의 issues file count와 document tree가 실제 `docs/issues/` tracked file에 맞는다.
- 변경은 docs navigation 복구에 필요한 최소 범위로 제한한다.

Forbidden context는 base commit 이후의 정답 commit·patch와 이 Task의 해결 결과 문서다. 현재 base commit 자체에 결함이 있으므로 Git history를 숨길 필요는 없지만, future fix를 fetch하지 않도록 원격 접근을 차단한다.

### Landmark 첫 Pilot 후보 — LA-01 contract drift fixture

목표:

```text
On-device Landmark Assistant의 공개 serving contract fixture에서 model ID 또는 class count가 어긋난 상태를 만들고, contract test를 근거로 최소 수정한다.
```

이것은 현재 repository 결함을 주장하는 Task가 아니라 benchmark runner와 evaluator를 검증하기 위해 실제 contract에서 파생한 의도적 fixture다.

2026-08-23 manual reproduction:

```text
base commit: 823ccdabc56bd512cb77d8e498f172cdd0f116db
intentional drift: manifest.example.json class_count 23 -> 22
contract evaluator: python -B -m unittest discover -s code/model_integration/tests -v
regression evaluator: python -B -m unittest discover -s tests -v
observed result: contract 3개 중 1개 실패, portfolio test 13개 통과
```

Agent에게 제공할 starting state는 위 base commit에 drift를 적용한 뒤 새 root commit으로 동결한다. 기존 Git history나 pristine manifest를 함께 제공하면 `git diff`만으로 정답을 볼 수 있으므로 다음을 forbidden context로 둔다.

```text
base repository history
pristine manifest.example.json
fixture 생성 patch와 정답 patch
이 Task를 설명하는 BENCHMARK_V1.md의 현재 section
```

Acceptance criteria:

- metadata contract test 3개가 모두 통과한다.
- portfolio test 13개가 계속 통과한다.
- test 삭제·완화 없이 contract metadata의 root cause를 최소 수정한다.
- model ID, class order, class count, embedding dimension과 policy 연결이 서로 일치한다.
- 변경 파일과 diff가 Task 범위를 벗어나지 않는다.

구현 순서는 LT-01이 먼저다. `localtwin-aep`의 Task·runner·trace schema가 안정된 뒤, 그 구현을 복사하는 대신 배운 점만 사용해 별도 `landmark-assistant-aep`에서 LA-01을 설계한다.

각 첫 Pilot의 목적은 V0/V1 우열을 결론 내리는 것이 아니다. 아래 장치가 해당 프로젝트 안에서 제대로 작동하는지 확인한다.

- clean starting state 생성
- Agent가 받은 Context 기록
- patch 저장
- evaluator 자동 실행
- 실패 trace 보존
- 같은 Task 재실행 가능

## 9. Benchmark Freeze 조건

다음을 만족한 뒤 LocalTwin과 Landmark benchmark를 각각 독립적으로 `v1`로 고정한다.

- 각 Task의 starting commit이 명확하다.
- acceptance criteria가 solution implementation을 누설하지 않는다.
- evaluator가 정답 patch 없이도 성공을 판정한다.
- forbidden context가 정의되어 있다.
- 최소 한 번의 manual reproduction이 완료됐다.
- pilot 결과를 보고 trace schema를 한 번 수정했다.
- 다른 프로젝트의 결과나 정답을 성공 기준에 사용하지 않는다.
