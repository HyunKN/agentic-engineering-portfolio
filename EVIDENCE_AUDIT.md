# Evidence Audit

확인일: 2026-08-24

이 문서는 포트폴리오에서 무엇을 현재 사실로 말할 수 있고, 무엇을 추가 검증해야 하는지 구분한다.

이 증거는 LocalTwin과 Landmark를 서로 비교하기 위한 것이 아니다. 각 원본 프로젝트의 기존 방식과 해당 프로젝트 전용 AEP를 비교할 Task, evaluator와 제한 조건을 만들기 위한 입력이다.

## 1. 확인 방법

- 두 GitHub 저장소의 원격 `main`을 인증된 Git 접근으로 확인했다.
- README, architecture, harness, evaluation, experiment result와 operation 문서를 읽었다.
- 노트북의 `LocalTwin` checkout과 `종설_작업중` 원천 자료를 read-only로 대조했다.
- 공개 On-device Landmark Assistant는 원격 `main`과 동일한 임시 clone에서 test와 provenance를 검증했다.
- LocalTwin의 SQLite는 read-only URI로 열어 table count와 period range만 조회했다. `.env`와 credential 값은 읽지 않았다.
- 전체 학습과 전체 product test suite를 다시 실행하지는 않았다.
- 실행 비용이 낮은 문서·Task Packet 검사와 공개 endpoint 상태를 확인했다.

## 2. LocalTwin

Repository: <https://github.com/HyunKN/hub>

### 현재 확인된 증거

- `product/apps/web`에는 React 19/Vite/TypeScript, MapLibre 기반 frontend가 있고 `product/apps/api`에는 FastAPI/SQLAlchemy backend가 있다.
- production product operation은 PostgreSQL을 요구하고, canonical SQLite는 import/verification source로 사용하는 경계가 source와 architecture 문서에 함께 남아 있다.
- MapLibre, 3D Scene, public data, security와 deployment 관련 구현·문서가 있다.
- 노트북의 `LocalTwin` checkout은 `main`, HEAD `8ac6178ed41c3056b4353cc2449791a335051dd5`, clean 상태였고 531개 tracked file과 751개 commit이 있었다. 이 checkout의 `origin`은 `HyunKN/hub-fork`, `upstream`은 팀 저장소다.
- `.harness/tasks`에 Task Packet 73개, `.harness/runs`에 Run Report 75개가 있었다.
- web test file 48개와 API test file 26개가 있지만 이번 audit에서 전체 suite를 다시 실행하지는 않았다.
- 노트북에서 `python -B scripts/check_docs_index.py`는 통과했고 `python -B scripts/check_docs_html.py`는 기존 docs tree 누락을 재현했다.
- 처리 DB에는 `store_points` 537,489행과 `store_market_links` 4,548행이 있고, `store_metrics`·`sales_metrics`·`flow_metrics`는 모두 `20251`부터 `20254`까지 4개 분기를 담는다.
- 현재 web용 `market-analysis.json`은 같은 DB에서 생성됐지만 `20251` 한 분기와 12개 상권·업종 조합만 담는다. DB coverage와 생성 UI snapshot coverage는 같은 주장으로 합치지 않는다.
- `docs/evaluation/evaluation-log.md`에는 아직 공식 평가 결과가 없고, failure log에는 실제 실패 2건만 기록되어 있다. `.harness/evaluations`의 12-case JSON은 제품 시장분석 평가이며 Agent benchmark 결과가 아니다.
- 73개 Task Packet 중 `Owner`가 있는 것은 51개다. 표기된 값은 `N187_정현우` 37개, `HyunKN` 10개, `Codex` 3개, `Codex + project owner` 1개이고 22개는 누락되어 있다.
- 제품, API health, 문서 공개 URL은 확인 시점에 HTTP 200이었다.
- 과거 Run Report에는 web/API test와 build 결과가 기록되어 있다.

### 아직 현재 사실로 확정하지 않는 것

- 과거 Run Report에 기록된 전체 test가 현재 `main`에서도 모두 통과한다.
- Agent rubric이 실제 작업을 정확하게 평가한다.
- Agent workflow가 기존 방식보다 생산성이나 품질을 개선했다.

### 현재 발견한 공백

- 공식 Agent evaluation log에 아직 정식 평가 entry가 없다.
- Agent run별 prompt, retrieved context, tool call, token, human intervention을 연결한 trace가 없다.
- Task ID와 Run Report ID가 완전히 일치하지 않는다.
- lightweight docs HTML 검사가 `docs/issues/industry-taxonomy-and-map-performance.md` tree 누락으로 실패한다.
- Task Packet 22개에는 `Owner`가 없고, `N187_정현우`와 `HyunKN` 표기가 같은 개인을 뜻하는지 설명하는 identity mapping도 없다.
- `Owner: Codex` 또는 공동 표기된 4개 Task Packet은 Agent 관여의 1차 단서지만, 해당 Task의 실제 human decision·Agent patch·review 경계를 재구성하는 trace는 아니다.
- Git author metadata도 `unknown`과 `HyunKN`이 섞여 있어, commit 수나 Task Packet 수를 개인·Agent 기여 퍼센트로 바로 바꿀 수 없다.
- [LocalTwin Evidence Map](./LOCALTWIN_EVIDENCE_MAP.md)에 source → test → deploy → commit을 연결했다. 다만 개인·팀·Agent의 commit-level attribution 공백은 그대로 남는다.

## 3. On-device Landmark Assistant

Primary portfolio repository: <https://github.com/HyunKN/ondevice-landmark-assistant>

Supporting experiment/docs repository: <https://github.com/HyunKN/landmark-assistant-sprint1>

Team application repository: <https://github.com/lpcvc-2026-CNU/App>

### 현재 확인된 증거

- 이 저장소는 training, Sprint 1 Streamlit prototype, model-to-app integration source를 선별한 공개 portfolio case study다.
- 원격 `main`에는 69개 tracked file과 14개 commit이 있었다.
- 23-class image/text retrieval, 8개 configuration × 5-fold의 40-run matrix, FP16 image/text ONNX handoff를 설명한다.
- reviewed metrics에는 S4 full CE의 validation Top-1 99.05%, held-out test Top-1 98.67%, macro F1 97.11%가 기록되어 있다.
- final handoff manifest는 `mobileclip2_s3_server_full_ce_hardneg`, 23 class, 512-dimensional embedding, FP16 mixed storage를 명시한다.
- training snapshot에는 dataset/split, baseline·multi-task training, loss, hard-negative mining, ONNX export와 validation source가 포함되어 있다.
- prototype snapshot에는 image/text inference, score fusion, confidence policy와 regression test가 포함되어 있다.
- integration snapshot에는 class/preprocessing/manifest/confidence/text-search contract, validation script와 Android large-asset cache patch가 포함되어 있다.
- `code/CONTRIBUTIONS.md`가 본인의 model experiment·prototype·integration 작업과 팀의 final Flutter/Android 구현을 구분한다.
- 현재 `main`에서 portfolio asset/public snapshot test 13개와 metadata contract test 3개가 통과했다.
- INT8/NPU latency 성공과 accuracy 붕괴를 서로 다른 증거로 구분하고 closed-set, open-world 미검증, package size와 runtime 한계를 공개한다.
- 노트북의 raw W&B export는 52개 run으로 구성되어 있고, 문서의 `40 main matrix + 12 screening` 구분과 일치한다. 52개 모두 23-class, 6,469 records, dataset fingerprint `ec2ad988299869f98622e52f5ebcebb35f56553c`를 기록한다.
- 공개 `data/metrics.json`의 8개 aggregate는 노트북의 52-run summary에서 다시 계산한 반올림 값과 8/8 일치했다.
- 공개 training source 10개는 `landmark-assistant-model-ver2` commit `9e082460...`의 blob과, Sprint 1 prototype source 16개는 `landmark-demo-app` commit `cc7abb9...`의 blob과 모두 일치했다.
- 공개 integration script 2개, contract JSON 4개와 Android cache patch는 팀 앱 기준 commit `2e4349b...`의 source/diff와 일치했다.

### 아직 현재 사실로 확정하지 않는 것

- 공개 case-study 저장소만으로 dataset부터 Android 앱까지 전체 pipeline이 한 번에 재현된다.
- 공개된 `data/metrics.json`만으로 40개 raw run의 결과가 독립적으로 재계산된다.
- model binary가 없으므로 공개 snapshot만으로 실제 ONNX inference와 parity를 다시 검증할 수 있다.
- 최종 Flutter/Android 앱 전체가 본인의 단독 구현이다.
- final FP16 artifact가 NPU accuracy, real-time latency와 shipping-size package 요구를 만족한다.

### 현재 발견한 공백

- raw W&B export와 final app commit은 추적할 수 있지만 dataset, checkpoint, ONNX binary와 원본 artifact validation JSON은 현재 노트북 범위에 없다.
- 공개 test는 portfolio snapshot과 metadata contract를 검증하지만 전체 training·export·Flutter runtime을 재실행하지 않는다.
- S4 full CE가 validation 평균 1위인 반면 실제 handoff manifest는 S3다. S3는 best single run, test/macro-F1/low-margin, 먼저 검증된 FP16 artifact라는 근거가 있지만, 어떤 배포 기준에 얼마의 가중치를 두었는지 명시한 최종 Deployment Decision Record가 없다.
- 52개 W&B run의 23-class fingerprint는 서로 일치하지만 노트북에 남은 실제 split manifest는 이전 22-class fingerprint `e33be91c8fc76fb043f759bdd8c5086450b265b4`다. 23-class split manifest와 그 checksum을 찾거나 복구해야 한다.
- ONNX export/parity 수치는 문서에 남아 있지만 해당 수치의 원본 `export_validation_report.json`, `artifact_image_validation.json`과 binary checksum을 현재 파일로 검증할 수 없다.
- later-snapshot script의 문서화된 SHA-256은 노트북 원본과 일치하지만 공개 clone의 byte hash는 줄바꿈 변환 때문에 달라진다. portable provenance에는 normalized hash 또는 Git blob ID가 필요하다.
- 상세 실험·운영 문서는 별도 Sprint 1 docs site에 의존하므로 링크와 provenance의 지속적인 검증이 필요하다.

## 4. 포트폴리오 주장 등급

### 지금 사용할 수 있는 표현

```text
구현했다
기록했다
비교 실험을 수행했다
현재 문서에는 다음 결과가 기록되어 있다
확인 시점에 endpoint가 응답했다
다음 제한 사항이 남아 있다
```

### 추가 검증 후 사용할 표현

```text
재현 가능하다
현재 전체 검증이 통과한다
Agent 적용으로 성공률이 향상됐다
비용이나 token이 감소했다
모바일 배포 요구를 만족한다
```

## 5. 먼저 해결할 Integrity Task

### LocalTwin AEP 입력

1. LocalTwin docs tree 검사 실패를 LT-01 fixture와 evaluator로 동결한다.
2. LocalTwin Evidence Map의 commit-level attribution 공백을 향후 LT trace schema로 보완한다.

### Landmark Assistant AEP 입력

1. S4 validation 1위와 S3 final handoff를 연결하는 Deployment Decision을 정리한다.
2. public metrics에서 raw experiment와 artifact까지 이어지는 Evidence Map을 만든다.
3. 23-class split과 artifact 원본이 없는 상태를 benchmark의 known evidence gap으로 고정한다.

### 최종 포트폴리오 입력

1. 두 프로젝트의 개인·Agent·팀 기여표를 각각 commit과 작업 기록에서 다시 확인한다.
2. LT 개선률과 LA 개선률을 합산하거나 프로젝트 간 우열로 해석하지 않는다.

이 작업은 포트폴리오를 꾸미기 위한 정리가 아니라, 이후 Agent benchmark가 잡아야 할 실제 품질 문제를 정의하는 단계다.
