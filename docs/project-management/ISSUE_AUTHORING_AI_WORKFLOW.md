# AI Issue 작성·검증 Workflow

## 목적

AI가 자유 형식 Markdown을 바로 `gh issue create/edit`에 넘기지 않게 한다. AI의 책임은 JSON draft 작성까지이며, deterministic module이 형식과 공개 안전성을 검증하고 사람이 preview를 확인한 뒤에만 GitHub를 변경한다.

## Module interface

호출자가 알아야 하는 명령은 두 개다.

```powershell
# Validate + preview only. GitHub를 변경하지 않는다.
python -m tools.issue_authoring.cli issues/examples/work-issue.json

# 모든 draft가 먼저 검증된 경우에만 GitHub에 적용한다.
python -m tools.issue_authoring.cli path/to/draft.json --apply
```

Implementation은 다음을 숨긴다.

- CRLF를 LF로 정규화하고 trailing whitespace 제거
- title의 Phase, Order와 Task ID 검사
- 한국어 제목·본문, 필수 section과 checklist 줄바꿈 검사
- 허용 label과 `track:`, `type:`, `priority:` 축 검사
- local machine path와 대표적인 secret pattern 차단
- update/create body를 shell argument가 아닌 `--body-file -` stdin으로 전달
- 게시 후 title, body, Milestone과 label round-trip 검증

## Workflow

```text
Source docs + 사용자 우선순위
  -> AI Issue Author prompt
  -> JSON draft
  -> deterministic validation
  -> dry-run preview
  -> human review
  -> explicit --apply
  -> GitHub round-trip verification
```

1. AI는 [Issue Author prompt](./prompts/ISSUE_AUTHOR.md)를 따라 JSON draft만 만든다.
2. 사용자는 dry-run에서 title, body, label, Milestone과 parent를 확인한다.
3. validation error가 있으면 GitHub side effect 없이 종료한다.
4. 사용자가 승인한 draft에만 `--apply`를 사용한다.
5. create/update 후 GitHub에서 다시 읽은 값이 draft와 다르면 실패로 보고한다.

## Draft contract

필수 field:

| Field | 의미 |
| --- | --- |
| `version` | 현재 `1` |
| `repository` | `owner/name` |
| `kind` | `parent`, `work`, `experiment` |
| `title` | Phase·Order·Task ID와 한국어 제목 |
| `body` | GitHub Markdown |
| `labels` | 허용 label 목록 |
| `milestone` | 정확한 Milestone 제목 |

선택 field:

| Field | 의미 |
| --- | --- |
| `issue_number` | 있으면 해당 Issue update, 없으면 create |
| `parent_issue` | native parent Issue number |

example은 [work-issue.json](../../issues/examples/work-issue.json)에 있다.

## Validation failure

다음 조건에서는 `--apply`가 있어도 게시하지 않는다.

- `[M1-010][LT-INF-001]` title contract 위반
- `Order`가 `010`, `015` 같은 양의 5 단위가 아님
- work Issue의 필수 section 누락
- checklist가 줄 시작이 아니라 문장 중간에 나타남
- 한국어 review text 없음
- 허용되지 않은 label 또는 label 축 중복
- local absolute path 또는 high-risk secret pattern 발견
- batch 중 하나라도 validation 실패

## 현재 제한

- 특정 LLM provider를 직접 호출하지 않는다. Codex나 다른 AI가 같은 prompt와 JSON contract를 사용할 수 있다.
- 지정하지 않은 기존 label을 자동 제거하지 않는다.
- Issue close/reopen과 GitHub Project field 변경은 수행하지 않는다.
- GitHub Project의 `Order` field 동기화는 Project OAuth scope를 확보한 뒤 별도 Task로 추가한다.

## Verification

```powershell
python -m unittest discover -s tests -v
python -m tools.issue_authoring.cli issues/examples/work-issue.json
git diff --check
```
