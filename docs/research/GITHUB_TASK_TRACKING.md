# GitHub Task Tracking for the AEP Portfolio

작성일: 2026-08-25

## 결론

이 프로젝트는 GitHub를 쓰는 편이 맞다. 다만 `Issue만` 쓰는 방식보다, `Project + Milestone + Issue + checklist/sub-issue` 조합이 더 적합하다.

이유는 GitHub 공식 문서가 다음을 분리해서 설명하기 때문이다.

- `Projects`는 issues, pull requests, draft issues/ideas를 한 곳에서 추적하는 상위 작업판이다. user level 또는 organization level에서 table, board, roadmap으로 볼 수 있다.
  Source: https://docs.github.com/en/issues/planning-and-tracking-with-projects/about-projects
- `Milestones`는 repository 안에서 issues와 pull requests의 묶음을 추적한다.
  Source: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
- `Issues`는 개별 작업을 추적하고, sub-issues로 계층을 만들 수 있다. 여러 level의 sub-issues도 지원된다.
  Source: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- Issue templates/forms는 반복 입력을 구조화해서 같은 종류의 일을 같은 형식으로 받게 해준다.
  Sources: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms

## 추천 구조

### 1) Project는 전체 조종실

하나의 상위 Project를 만든다.

권장 이름:

`Agentic Engineering Portfolio`

이 Project는 모든 저장소의 작업을 한 화면에서 본다.

- `localtwin-aep`
- `landmark-assistant-aep`
- `agentic-engineering-portfolio`
- 필요하면 원본 `LocalTwin`, `Landmark Assistant`에서 끌어온 참조 이슈도 같이 본다

GitHub는 Projects가 issues, PRs, draft issues를 한 보드에서 추적하고, custom fields와 roadmap view를 붙일 수 있다고 설명한다.
Sources: https://docs.github.com/en/issues/planning-and-tracking-with-projects/about-projects
https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view
https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-roadmap-layout

권장 view:

- `Master`
- `LT`
- `LA`
- `Portfolio Writing`
- `Blocked`
- `This Week`
- `Roadmap`

권장 custom fields:

- `Stream` = `LT`, `LA`, `Portfolio`, `Infra`
- `Phase` = `baseline`, `fixture`, `retrieval`, `routing`, `stateful`, `evaluation`, `writeup`
- `Priority` = `P0`, `P1`, `P2`
- `Status` = `backlog`, `ready`, `in progress`, `blocked`, `verify`, `done`
- `Evidence` = `trace`, `commit`, `test`, `run`, `doc`
- `Target date`

### 2) Milestone은 repository 단위의 단계

Milestone은 repo 안에서만 잡는다. 즉, `localtwin-aep`와 `landmark-assistant-aep`는 각각 자기 milestone을 가진다.

GitHub 문서는 milestones를 repository 안의 issues/PR 묶음 추적으로 설명한다.
Source: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones

권장 방식:

- `localtwin-aep`
  - `LT-AEP 0 Baseline freeze`
  - `LT-AEP 1 Tooling + Trace`
  - `LT-AEP 2 Retrieval + Routing`
  - `LT-AEP 3 Stateful workflow`
  - `LT-AEP 4 Evaluation + Observability`
- `landmark-assistant-aep`
  - `LA-AEP 0 Baseline freeze`
  - `LA-AEP 1 Evidence retrieval`
  - `LA-AEP 2 Proposal gate`
  - `LA-AEP 3 Approval + run control`
  - `LA-AEP 4 Evaluation + decision trace`
- `agentic-engineering-portfolio`
  - `Portfolio 0 Setup`
  - `Portfolio 1 Case studies`
  - `Portfolio 2 Final narrative`

중요한 점은 milestone을 `LT vs LA` 비교용으로 쓰지 않는 것이다. 각 저장소의 진행 단계만 표시한다.

### 3) Issue는 하나의 검증 가능한 결과물

Issue는 너무 잘게 쪼개지지 않게 잡는다.

권장 기준:

- 한 issue는 보통 하나의 PR, 하나의 run, 또는 하나의 결정 문서로 닫힌다.
- issue 제목만 봐도 결과가 예상돼야 한다.
- `함수 하나`, `변수 하나`, `문장 하나` 단위로는 issue를 만들지 않는다.
- `새 evaluator`, `새 dataset`, `새 retrieval corpus`, `새 state transition`처럼 검증 단위가 바뀌면 issue로 분리한다.

GitHub 문서는 issue가 idea/bug/feature/task를 추적하는 기본 단위라고 설명하고, sub-issues로 계층을 만들 수 있다고 한다.
Sources: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues

권장 제목 규칙:

- `[LT-AEP][Baseline] Freeze LT-01 fixture`
- `[LT-AEP][V0] Add trace schema`
- `[LT-AEP][V1A] Build retrieval corpus`
- `[LT-AEP][V1B] Add tool router`
- `[LA-AEP][Baseline] Freeze LA-01 fixture`
- `[Portfolio] Write LT case-study narrative`

### 4) checklist와 sub-issue는 “세부 실행”용

세부 작업은 우선 checklist로 넣고, 독립적인 lifecycle이 필요한 것만 sub-issue로 만든다.

권장 규칙:

- checklist
  - 같은 PR 안에서 끝난다
  - 중간 검토가 필요 없다
  - owner를 따로 나눌 필요가 없다
- sub-issue
  - 별도 검증이 필요하다
  - 결과 trace나 dataset이 따로 남는다
  - 다른 사람에게 넘기거나 나중에 다시 열 가능성이 있다
  - parent issue 없이도 의미가 있다

GitHub는 여러 level의 sub-issues를 지원한다.
Source: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues

이 프로젝트에서는 보통 다음 순서를 권장한다.

1. parent issue를 만든다.
2. 안에서 checklist로 끝나는 작업은 checklist로 둔다.
3. 독립 검증이 필요한 작업만 sub-issue로 승격한다.

예시:

- parent issue: `LT-AEP 2 Retrieval + Routing`
  - checklist:
    - corpus manifest 작성
    - chunking rule 결정
    - query router spec 작성
  - sub-issues:
    - retrieval dataset freeze
    - BM25 baseline
    - embedding baseline
    - routing evaluator

## 과도한 issue 분해를 막는 기준

이 프로젝트는 AI workflow 자체를 평가하는 것이므로, 작업도 평가 단위에 맞게 묶어야 한다.

다음은 issue로 분리한다.

- evaluator가 달라진다
- dataset이 달라진다
- trace schema가 달라진다
- repo boundary가 달라진다
- human approval gate가 새로 들어간다
- failure class가 새로 정의된다

다음은 checklist로 남긴다.

- 파일 경로 한두 개 수정
- fixture 이름 정리
- README 문구 수정
- issue 하나 안에서 끝나는 작은 구현 단계

이 규칙을 지키지 않으면 GitHub board는 예뻐지지만 실제로는 관리가 어려워진다.

## 추천 운영 방식

### 단기

1. `Project` 1개를 만든다.
2. 각 repo에 milestone을 만든다.
3. issue template/form을 만든다.
4. 핵심 parent issue 5~8개만 먼저 만든다.

### 중기

1. parent issue 아래에 sub-issue를 붙인다.
2. checklist는 issue body 안에 둔다.
3. 완료된 issue는 Project에서 `done`으로 옮기고 닫는다.

### 장기

1. Project의 roadmap view로 LT/LA/Portfolio의 순서를 본다.
2. milestone progress로 각 repo의 phase를 본다.
3. case study 작성은 portfolio repo에서만 마무리한다.

GitHub 문서는 Projects의 roadmap layout과 custom fields를 이용해 backlog, iteration planning, roadmap을 볼 수 있다고 설명한다.
Sources: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects
https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects

## 로컬에서 먼저 준비할 파일

GitHub를 실제로 만들기 전에, 로컬에서 먼저 준비하면 좋은 것은 아래다.

- `docs/research/GITHUB_TASK_TRACKING.md`
  - 지금 문서
  - 전체 규칙의 source of truth
- `docs/planning/issue-seed.md` 또는 `docs/planning/issue-seed.csv`
  - 첫 번째 issue 묶음 초안
  - 나중에 GitHub issue로 옮기기 쉬운 형태
- `docs/planning/project-fields.md`
  - `Stream`, `Phase`, `Priority`, `Evidence` 정의
- `.github/ISSUE_TEMPLATE/task.yml`
  - 일반 작업용 issue form
- `.github/ISSUE_TEMPLATE/experiment.yml`
  - 실험/ablation용 issue form
- `.github/ISSUE_TEMPLATE/decision.yml`
  - 설계 결정용 issue form
- `.github/ISSUE_TEMPLATE/bug.yml`
  - regression/failure 기록용 issue form
- `.github/PULL_REQUEST_TEMPLATE.md`
  - PR에서 issue/trace/evidence를 연결하게 만드는 템플릿

GitHub 공식 문서는 issue templates와 issue forms가 `/.github/ISSUE_TEMPLATE` 아래에 들어간다고 설명한다.
Sources: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms

## 추천 태그 설계

labels는 너무 많지 않게 유지한다.

권장 세트:

- `area:lt`
- `area:la`
- `area:portfolio`
- `area:infra`
- `kind:task`
- `kind:experiment`
- `kind:decision`
- `kind:bug`
- `kind:research`
- `risk:needs-fixture`
- `risk:blocked`
- `evidence:missing`
- `evidence:ready`

labels는 검색과 필터용, Project fields는 상태/우선순위/일정용으로 나누는 것이 낫다.

## 실제로 어떻게 굴릴지

이 프로젝트의 운영 원칙은 다음 한 줄로 정리할 수 있다.

`Project`로 전체를 보고, `Milestone`으로 repo 단계를 나누고, `Issue`로 검증 가능한 결과물을 만들고, `checklist/sub-issue`로 실행 세부를 관리한다.

즉, 질문에 대한 실무 답은 이렇다.

- "GitHub를 쓸까?" → 예
- "Issue식으로?" → 예, 하지만 Issue만으로 끝내지 말고 Project와 Milestone을 같이 써야 한다
- "모든 걸 Issue로 쪼개야 하나?" → 아니요. 작은 건 checklist로, 독립 검증이 필요한 것만 issue/sub-issue로 만든다

## 첫 시작용 최소 백로그

이 문서를 읽은 직후 만들기 좋은 parent issue는 아래 정도다.

- `PF-001` Project/labels/template bootstrap
- `LT-001` LT baseline fixture freeze
- `LT-002` LT trace schema + run metadata
- `LT-003` LT retrieval corpus + baseline retrieval
- `LT-004` LT routing + tool selection
- `LT-005` LT evaluator + observability
- `LA-001` LA baseline fixture freeze
- `LA-002` LA evidence retrieval
- `LA-003` LA experiment/proposal gate
- `LA-004` LA approval + run control
- `LA-005` LA evaluator + decision trace
- `PORT-001` Portfolio case study outline

이 백로그는 시작점일 뿐이다. 실제 issue 수는 실험과 검증 단위가 정해진 뒤에 늘린다.

## 공식 문서 참고

- Issues overview: https://docs.github.com/issues
- About issues: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- Adding sub-issues: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
- Browsing sub-issues: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/browsing-sub-issues
- About projects: https://docs.github.com/en/issues/planning-and-tracking-with-projects/about-projects
- Best practices for Projects: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
- Quickstart for Projects: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects
- Milestones: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
- Issue templates: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
- Issue forms: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
