# Agent Workflows 구조

## 목적

이 저장소의 `agent_workflows`는 포트폴리오 작업을 안전하고 반복 가능하게 만드는 운영용 workflow 모음이다. LocalTwin AEP나 Landmark Assistant AEP의 agent runtime, Tool, Context, evaluator를 대신하는 공통 AEP core가 아니다.

현재 두 workflow가 해결하는 문제는 다음과 같다.

```text
Issue draft JSON
    └─ issue_authoring ──→ 검증된 GitHub Issue

공개 검토 spec + 고정 Git commit
    └─ evaluation_packet ──→ 검증 가능한 공개 evidence packet
                                  └─ 외부 Web AI 비판 검토
```

## 파일 구조

```text
agent_workflows/
├─ publication_safety.py
├─ issue_authoring/
│  ├─ workflow.py
│  └─ cli.py
└─ evaluation_packet/
   ├─ workflow.py
   └─ cli.py

issues/
├─ examples/
└─ specs/

evaluation_specs/
└─ <packet spec>.json

evaluation_packets/
└─ <immutable packet id>/
   ├─ README.md
   ├─ REVIEW_PROMPT.md
   ├─ PACKET_SPEC.json
   ├─ MANIFEST.json
   └─ sources/
```

## Module 1: `issue_authoring`

AI가 자유 형식 Markdown을 바로 GitHub에 쓰지 못하게 하고, JSON draft를 contract로 사용한다.

1. `workflow.py`가 title 순서, Task ID, 필수 heading, checklist, label 축, milestone, local path와 secret pattern을 검증한다.
2. 기본 실행은 read-only preview다.
3. `--apply`일 때만 `GithubPublisher`가 `gh` CLI로 Issue를 생성하거나 수정한다.
4. 게시 후 GitHub에서 다시 읽어 title, body, label과 milestone의 round-trip 일치를 확인한다.

`GithubPublisher`가 외부 side effect를 담당하므로 draft parsing과 policy 검증은 GitHub 없이 테스트할 수 있다.

## Module 2: `evaluation_packet`

외부 Web AI가 이 저장소 전체나 로컬 컴퓨터를 직접 읽게 하지 않는다. 대신 검토에 필요한 공개 source만 명시적으로 선택해 고정된 Git commit의 snapshot으로 만든다.

1. `evaluation_specs/*.json`이 평가 범위, source allowlist, 질문, 알려진 공백과 제외 사유를 선언한다.
2. `SourceReader` interface가 commit 해석과 file 읽기 경계를 만든다.
3. 실제 실행은 `GitSourceReader`, unit test는 in-memory reader를 사용한다.
4. build는 source를 UTF-8 text로 제한하고 local path, secret pattern과 금지 경로를 차단한다.
5. 각 file의 byte size와 SHA256을 `MANIFEST.json`에 기록한다.
6. packet은 같은 ID로 덮어쓰지 않는다. 변경된 검토 대상은 새 ID와 새 packet으로 만든다.

이 module은 외부 Web AI를 호출하거나 그 답변을 자동 채택하지 않는다. 입력 자료를 재현 가능하게 만들고, review 결과는 사람이 evidence와 대조해 triage하는 데까지만 contract를 제공한다.

## Shared policy: `publication_safety`

`publication_safety.py`는 public artifact로 나갈 text의 최소 안전 검사만 공유한다. 첫 workflow만 있을 때 미리 만든 추상화가 아니라, 두 번째 workflow에서도 동일한 local path·secret 차단이 필요해진 시점에 추출했다.

현재 이 module이 보장하는 것은 제한적이다.

- 알려진 local machine path pattern 차단
- 알려진 high-risk secret pattern 차단
- 검출된 값 자체를 error message에 다시 노출하지 않음

완전한 개인정보·비밀 탐지기를 의미하지 않는다. 최종 공개 전 human review는 계속 필요하다.

## 경계와 확장 원칙

- `agent_workflows`는 portfolio 운영 자동화다. 프로젝트 전용 AEP runtime과 분리한다.
- 두 workflow에 실제로 반복되는 안정된 policy만 공유한다.
- GitHub, Git과 향후 Web AI provider는 adapter 뒤에 둔다.
- 외부 review 결과가 들어와도 자동으로 Issue를 닫거나 코드를 변경하지 않는다.
- 새 workflow는 입력 contract, read-only preview, 명시적 apply, post-action verification을 우선한다.

따라서 현재 구조는 “하나의 거대한 Agent”가 아니라 작은 workflow module들의 집합이다. 나중에 공통 orchestration이 실제로 반복될 때만 상위 graph나 LangGraph 적용을 검토한다.
