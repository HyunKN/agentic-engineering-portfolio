# External AI Evaluation Packet Workflow

## 무엇을 해결하는가

외부 Web AI에게 repository 전체, 로컬 폴더 또는 대화 원문 전체를 넘기면 다음 문제가 생긴다.

- 어느 commit을 평가했는지 재현하기 어렵다.
- secret, local path, 개인정보와 비공개 자료가 섞일 수 있다.
- 작성자에게 유리한 evidence만 골랐는지 알기 어렵다.
- 외부 AI의 finding이 어떤 source에 근거했는지 추적하기 어렵다.

`agent_workflows.evaluation_packet`은 공개 가능한 source의 명시적 allowlist, 고정 commit, checksum, 알려진 공백과 제외 사유를 하나의 immutable packet으로 만든다.

## 입력 contract

`evaluation_specs/*.json`에는 다음을 적는다.

- `packet_id`: 새 평가 단위의 고유 ID
- `source_commit`: 평가 대상 Git ref 또는 40자리 commit
- `scope`: 이번 평가가 답해야 할 범위
- `sources`: repository-relative UTF-8 text allowlist
- `references`: 관련 Issue, commit, 공식 문서 URL
- `review_questions`: 외부 reviewer가 답할 구체적 질문
- `known_gaps`: 아직 근거가 없거나 구현하지 않은 부분
- `exclusions`: 공개하지 않은 항목과 그 이유

`.env`, key/certificate, credential file, absolute/local path와 parent traversal은 허용하지 않는다. allowlist에 없는 file은 packet에 자동으로 포함되지 않는다.

## 실행

먼저 read-only preview를 확인한다.

```powershell
python -m agent_workflows.evaluation_packet.cli build evaluation_specs/<spec>.json
```

검토 후 새 packet을 쓴다.

```powershell
python -m agent_workflows.evaluation_packet.cli build evaluation_specs/<spec>.json --apply
```

생성 후 또는 clone한 환경에서 manifest와 file hash를 확인한다.

```powershell
python -m agent_workflows.evaluation_packet.cli verify evaluation_packets/<packet-id>
```

기본 output은 `evaluation_packets/<packet-id>`다. 같은 ID가 이미 있으면 덮어쓰지 않는다. 평가 대상이나 질문이 바뀌면 `v2`처럼 새 ID를 사용한다.

## 외부 Web AI 사용 절차

1. 공개 GitHub의 packet URL 또는 packet file을 reviewer에게 제공한다.
2. `REVIEW_PROMPT.md`의 형식으로 비판적 검토를 요청한다.
3. reviewer 응답 원문은 `reviews/<packet-id>/<provider>-<date>.md`에 저장한다.
4. 각 finding을 `Verified`, `Rejected`, `Needs evidence`, `Deferred`로 사람이 분류한다.
5. 실제 수정이 필요한 finding만 별도 GitHub Issue로 만든다.
6. review 원문, triage 결정과 수정 commit을 서로 링크한다.

현재 module은 1단계 packet 생성·검증까지만 자동화한다. provider 호출과 review import를 자동화하기 전에는 서로 다른 Web AI의 export 형식, 개인정보 정책과 prompt injection 경계를 별도 결정해야 한다.

## “모든 작업과 대화 공개”의 의미

투명성은 무가공 대화 전체를 공개하는 것이 아니다. 재현과 판단에 필요한 공개 artifact를 연결하는 것이다.

- 포함: 사용자에게 보인 요구사항 요약, 승인된 결정과 이유, Issue, commit, diff, test 결과, benchmark, 공개 source, 외부 review와 triage
- 제외: credential, 개인정보, 로컬 절대 경로, 비공개 제3자 자료, system/developer prompt, private chain-of-thought
- 대체 기록: 숨겨진 추론 원문 대신 결정, 대안, 선택 이유, 검증 결과와 남은 불확실성을 문서화

구체적인 공개 기준은 [Public Evidence Policy](../../governance/PUBLIC_EVIDENCE_POLICY.md)를 따른다.
