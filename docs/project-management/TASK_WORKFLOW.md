# AEP 작업 관리 Workflow

작성일: 2026-08-25

## 1. 결정

전체 작업은 다음 세 층으로 관리한다.

```text
GitHub Project
└─ 전체 roadmap와 cross-repository 상태
   └─ Issue / parent Issue
      └─ 실제로 완료 가능한 작업 단위
         └─ Issue checklist
            └─ 구현·검증·문서화 세부 항목
```

- GitHub Project는 `localtwin-aep`, `landmark-assistant-aep`, `agentic-engineering-portfolio` Issue를 한 화면에서 본다.
- 실제 Issue는 변경 결과를 소유하는 저장소에 생성한다.
- 하나의 Issue는 하나의 검증 가능한 결과만 가진다.
- 구현 전에 Issue의 goal, scope, acceptance criteria와 verification을 먼저 고정한다.
- 모든 세부 행동을 별도 Issue로 만들지 않는다. 같은 결과를 위한 구현·test·문서 갱신은 Issue checklist로 둔다.

현재 `portfolio` 폴더는 아직 Git 저장소가 아니므로, 외부 GitHub를 만들기 전까지 [Master Backlog](../../tasks/BACKLOG.md)를 임시 source of truth로 사용한다. GitHub 전환 후에는 Issue와 Project가 진행 상태의 source of truth가 되고, 이 backlog는 초기 계획 snapshot 역할만 한다.

## 2. Repository별 Issue 소유권

| 저장소 | 소유할 Issue |
| --- | --- |
| `localtwin-aep` | LT fixture, Tool, retrieval, routing, LangGraph, evaluator, LT experiment |
| `landmark-assistant-aep` | LA evidence retrieval, experiment gate, ML Tool, evaluator, LA experiment |
| `agentic-engineering-portfolio` | 연구 질문, 채용 역량, Case Study, 결과 종합, 공개 사이트 |
| LocalTwin 원본 | 실제 제품 결함을 원본 제품에서도 수정하기로 결정한 경우만 |
| Landmark 원본 | 실제 ML source/artifact를 원본에서도 복구하기로 결정한 경우만 |

AEP 실험용 fixture와 evaluator Issue를 원본 제품 저장소에 만들지 않는다. 원본 저장소는 실험 대상이고 AEP 저장소는 실험 시스템이다.

## 3. Project board

권장 Project 이름:

```text
Agentic Engineering Portfolio
```

### Status

```text
Inbox
Backlog
Ready
In Progress
Blocked
Review
Done
```

상태 정의:

| 상태 | 진입 조건 | 종료 조건 |
| --- | --- | --- |
| Inbox | 아직 분류하지 않은 아이디어 | Track, Phase와 owner 결정 |
| Backlog | 해야 하지만 바로 시작하지 않음 | dependency와 우선순위 정리 |
| Ready | goal·acceptance·verification이 명확함 | 실제 작업 시작 |
| In Progress | 현재 구현 또는 조사 중 | 검증 완료 또는 blocker 확인 |
| Blocked | 외부 결정·자료·권한이 필요함 | blocker 해소 |
| Review | 구현 완료, 근거 검토 중 | acceptance와 검증 승인 |
| Done | acceptance를 만족하고 결과가 보존됨 | 다시 열 필요 없음 |

### Custom fields

| Field | 값 |
| --- | --- |
| Track | Foundation, LocalTwin AEP, Landmark AEP, Portfolio |
| Phase | Foundation, MVP, Baseline, Retrieval, Routing, Workflow, Evaluation, Release |
| Priority | P0, P1, P2 |
| Size | S, M, L |
| Evidence | None, Partial, Verified |
| Target | LT, LA, Portfolio |

`Status`는 Project field로만 관리하고 `status:*` label을 중복 생성하지 않는다.

## 4. Issue 계층

### Parent Issue / Epic

여러 Issue를 묶는 결과 단위다.

예:

```text
[EPIC] LT AEP baseline을 재현 가능하게 만든다
```

Sub-issue 후보:

- LT-01 fixture builder
- safe command runner
- evaluator runner
- run trace schema
- V0 dry run

### Work Issue

독립적으로 완료·검증할 수 있는 변경 단위다. 가능하면 S 또는 M 크기로 유지한다.

```text
[LT] LT-01 fixture builder 구현
```

### Checklist

같은 결과를 이루기 위한 세부 구현·test·docs 항목이다.

```markdown
- [ ] base commit archive
- [ ] remote/history 제거
- [ ] expected failure 재현
- [ ] fixture provenance 저장
- [ ] verification 기록
```

checklist가 서로 다른 owner, 별도 release 또는 독립 acceptance를 가지면 별도 Issue로 승격한다.

## 5. Task ID

| Prefix | 용도 |
| --- | --- |
| `FND-###` | 전체 방향, repository, task system과 공통 실험 정책 |
| `LT-###` | LocalTwin AEP Task와 experiment |
| `LA-###` | Landmark Assistant AEP Task와 experiment |
| `PF-###` | 최종 포트폴리오와 채용 artifact |

기존 benchmark의 `LT-01`, `LA-01` ID를 유지한다. 구현 infrastructure는 `LT-INF-###`, `LA-INF-###`처럼 구분할 수 있다.

## 6. Label

최소 label만 사용한다.

```text
track:foundation
track:localtwin
track:landmark
track:portfolio

type:feature
type:experiment
type:evaluation
type:research
type:docs
type:bug

priority:p0
priority:p1
priority:p2

risk:security
risk:data
risk:cost
needs:decision
```

Phase와 Status는 Project field에 있으므로 label로 다시 만들지 않는다.

## 7. Issue 시작 조건

아래 항목이 없으면 `Ready`로 이동하지 않는다.

- [ ] Goal이 결과 상태로 쓰여 있다.
- [ ] In scope와 Out of scope가 분리되어 있다.
- [ ] 입력 repository와 starting commit이 명확하다.
- [ ] acceptance criteria가 정답 구현을 누설하지 않는다.
- [ ] verification 명령 또는 human check가 정의되어 있다.
- [ ] secret, 개인정보, model/data 공개 위험을 확인했다.
- [ ] dependency와 blocker를 연결했다.

## 8. Issue 완료 조건

- [ ] acceptance criteria를 모두 충족했다.
- [ ] 관련 evaluator·test·manual check를 실행했다.
- [ ] 실제 명령과 결과를 Issue에 남겼다.
- [ ] patch, trace, metric 또는 Decision Record가 보존됐다.
- [ ] 실패와 미검증 범위를 숨기지 않았다.
- [ ] 관련 없는 변경이 없다.
- [ ] 필요한 문서를 갱신했다.

명령이 성공한 것과 목표가 해결된 것은 별도로 판단한다.

## 9. 작업 cadence

1. Inbox를 주 1회 분류한다.
2. 다음에 할 일은 `Ready`에서만 선택한다.
3. 개인 작업의 `In Progress`는 원칙적으로 1개, 최대 2개로 제한한다.
4. scope가 달라지면 Issue를 수정하거나 새 Issue로 분리한 뒤 작업한다.
5. 완료 직전 관련 검증을 한 번 통합 실행한다.
6. Review에서 evidence를 확인한 뒤 Done으로 이동한다.
7. 실패한 experiment도 Done으로 닫고 결과는 `failed` 또는 `inconclusive`로 보존한다.

## 10. GitHub 전환 순서

1. `agentic-engineering-portfolio` GitHub 저장소 생성
2. 이 폴더를 local Git 저장소로 초기화하고 첫 문서 commit 생성
3. label과 Issue Form 적용
4. 사용자 계정의 GitHub Project 생성
5. Foundation과 Portfolio Issue를 종합 저장소에 생성
6. `localtwin-aep` 생성 후 LT Issue를 해당 저장소에 생성하고 Project에 연결
7. Landmark 단계에서 `landmark-assistant-aep`와 LA Issue를 같은 방식으로 연결

외부 repository, Project와 Issue 생성은 사용자의 명시적 승인 후 실행한다.

## 11. 공식 문서

- [GitHub Projects](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [Project에 Issue와 Pull Request 추가](https://docs.github.com/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project)
- [Sub-issues](https://docs.github.com/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
- [Milestones](https://docs.github.com/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [Issue Forms](https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)
- [Task lists](https://docs.github.com/get-started/writing-on-github/working-with-advanced-formatting/about-task-lists)
