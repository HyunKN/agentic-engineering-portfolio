# LocalTwin Evidence Map

범위: [HyunKN/hub-fork@8ac6178](https://github.com/HyunKN/hub-fork/tree/8ac6178ed41c3056b4353cc2449791a335051dd5)

현재 확인된 상태: `main`, HEAD `8ac6178ed41c3056b4353cc2449791a335051dd5`, 작업 트리는 clean 상태였다.

## 한 줄 결론

당신이 하려던 건 공공데이터 기반 상권 분석을 P0로, Gaussian Splatting 현장 탐색을 P1 보조로 붙인 LocalTwin을 문서, canonical data, validation, deploy boundary까지 묶어서 실제 시연 가능한 제품으로 만드는 일이었다.

## Claim -> evidence map

| Claim | Source | Check / verification | Deploy / artifact | Commit evidence | Status |
| --- | --- | --- | --- | --- | --- |
| LocalTwin은 웹 기반 상권 의사결정 서비스이고, 주기능은 공공데이터 기반 상권 분석이며 3D 현장 탐색은 보조 기능이다. | [README.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/README.md#L3) / [제품 기획서](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/wiki/localtwin-product-plan.md#L7) / [프로젝트 기획서](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/wiki/localtwin-project-proposal.md#L9) / [시스템 아키텍처](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/architecture.md#L6) | [검증 가이드](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/validation.md#L1), [harness](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/harness.md#L1), [check.ps1](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/scripts/check.ps1#L19), [product/package.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/package.json#L9) | [root vercel.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/vercel.json#L1), [product/vercel.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/vercel.json#L1), [showcase.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/showcase/showcase.json#L1) | `8ac6178 chore(git): merge N187 work into fork main`; 최근 연속 커밋 `7fab591`, `3cf7547`, `71cee06`, `0593998`, `ca31a9d`가 기능 개선 흐름을 보여준다. | verified |
| canonical SQLite와 Supabase PostgreSQL를 분리하고, raw snapshot -> canonical -> dev/prod DB -> API로 이어지는 데이터 경계를 유지한다. | [architecture.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/architecture.md#L13) / [data-source-mapping.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/data/data-source-mapping.md#L7) / [database-structure.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/data/database-structure.md#L7) / [pre-development-decisions.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/pre-development-decisions.md#L21) | [test_health.py](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/apps/api/tests/test_health.py#L14), [test_scene_asset_gate.py](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/apps/api/tests/test_scene_asset_gate.py#L25), [App.test.tsx](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/apps/web/src/App.test.tsx#L67) | [database-structure.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/data/database-structure.md#L63) 에 `product/data/processed/localtwin.db` 적재와 9개 core table가 기록돼 있고, [product/vercel.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/vercel.json#L2) 는 `apps/web/dist` 제품 빌드를 가리킨다. | `tasks.md`의 `DB-001`, `DATA-008`, `DATA-009`, `DATA-010`, `DATA-011`은 완료 상태로 기록돼 있다. 다만 개별 커밋-태스크 1:1 매핑은 git 메타데이터만으로 완전히 복원되지 않았다. | verified / partially inferred |
| 3D 장면은 P1 보조 기능이고, 공개 경로는 기본 차단이며 승인된 asset만 내려받도록 설계됐다. | [3d-congestion-explorer.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/features/3d-congestion-explorer.md#L5) / [pre-development-decisions.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/pre-development-decisions.md#L143) / [tasks.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/tasks.md#L179) | [test_health.py](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/apps/api/tests/test_health.py#L102), [test_scene_asset_gate.py](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/apps/api/tests/test_scene_asset_gate.py#L25), [useSceneJob.test.tsx](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/apps/web/src/features/scene/useSceneJob.test.tsx#L24) | [product/vercel.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/product/vercel.json#L11) 의 CSP는 Google Drive frame과 Render API 연결만 열고, scene는 API gate를 통해서만 접근하도록 설계돼 있다. | `tasks.md`의 `SCENE-001`~`SCENE-008`가 이 흐름을 분해해서 관리한다. | verified |
| 팀/사람/Agent 기여는 문서와 일부 task packet에는 명시돼 있지만, git history만으로는 완전한 attribution이 남아 있지 않다. | [showcase.json](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/showcase/showcase.json#L48) / [agent-rubric.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/evaluation/agent-rubric.md#L1) / [harness.md](https://github.com/HyunKN/hub-fork/blob/8ac6178ed41c3056b4353cc2449791a335051dd5/docs/development/harness.md#L1) | `git shortlog -sne --all --no-merges` 결과 author bucket은 `unknown`, `HyunKN`, `crong`이었다. `.harness/tasks` 73개 중 `Owner`가 적힌 문서는 51개였고, 22개는 owner가 비어 있었다. `docs/evaluation/evaluation-log.md`에는 아직 공식 평가 entry가 없다. | `showcase.json`은 `developmentWithAI`와 `agent` 섹션에서 Codex/GPT-5.6을 개발 파트너로 명시한다. | human/agent 기여는 서술형 증거가 있고, commit-level attribution은 부분 공백이 있다. | partially verified |

## 읽은 흔적에서 보이는 실제 의도

- `README.md`, 제품 기획서, 프로젝트 기획서는 모두 같은 방향을 말한다. 상권 점포 밀도, 경쟁 강도, 개업/폐업 흐름, 시간대별 수요를 한 화면에서 보고, 필요할 때만 3D 현장감을 보조로 붙이는 제품이다.
- `tasks.md`와 `harness.md`는 그 의도를 구현으로 바꾸는 방식을 고정한다. 작은 task packet, 검증 후 커밋, run report, 문서 갱신, 그리고 `scripts/check.ps1`를 통한 로컬 검증이 핵심이다.
- `document-management.md`와 `pre-development-decisions.md`는 문서 역할과 제품 경계를 분리한다. 그래서 README, product plan, architecture, data mapping, feature spec, validation, harness가 각각 다른 책임을 가진다.

## 현재 수치로 확인한 사실

- `product/data/processed/localtwin.db`
  - `store_points`: 537,489
  - `store_market_links`: 4,548
  - `store_metrics`: 304,775
  - `sales_metrics`: 85,732
  - `flow_metrics`: 6,595
- `product/apps/web/public/data/market-analysis.json`
  - top-level `period`: `20251`
  - top-level keys: 4
  - `generated_from`: `data/processed/localtwin.db`
  - 분석 key: 12개 상권·업종 조합
- DB 지표 period
  - `store_metrics`: `20251`~`20254`, 4개 분기
  - `sales_metrics`: `20251`~`20254`, 4개 분기
  - `flow_metrics`: `20251`~`20254`, 4개 분기
- `.harness/tasks/*.md`
  - 총 73개
  - `Owner`가 적힌 문서 51개
  - `Owner` 비어 있음 22개
  - owner bucket: `N187_정현우` 37, `HyunKN` 10, `Codex` 3, `Codex + project owner` 1

## 갭

- 이번 audit에서는 LocalTwin 전체 web/API test suite와 production build를 다시 실행하지 않았다.
- `docs/evaluation/evaluation-log.md`는 아직 공식 평가 entry가 없다.
- git history에는 최근 merge와 feature 흐름은 보이지만, agent 단위의 명시적 커밋 attribution은 없다.
- Task Packet 22개에는 `Owner`가 없고 `N187_정현우`와 `HyunKN` identity mapping도 문서화되어 있지 않다.
- 따라서 “누가 무엇을 했는가”는 commit log, task packet, showcase metadata를 함께 봐야 하며, 현재 자료만으로 개인·Agent 기여율을 계산할 수 없다.

## 최종 정리

이 저장소의 중심 목표는 “상권 분석 P0 + 3D 보조 P1 + canonical data + 검증 가능한 배포 경계”다.
즉, 당신이 하려던 건 단순한 지도 앱이 아니라, 증거가 붙은 상권 의사결정 제품을 만드는 일이었다.
