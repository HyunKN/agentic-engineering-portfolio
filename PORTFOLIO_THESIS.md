# Portfolio Thesis

## 1. 프로젝트 주제

### 작업 제목

**From Ad-hoc AI Assistance to Evaluated Engineering Workflows**

### 한 문장 설명

기존 제품 개발과 ML 개발 기록을 각각 독립된 benchmark로 변환하고, 각 프로젝트에 맞춘 Context·Retrieval·Tool Use·Guardrail·Stateful Verification이 기존 AI-assisted workflow를 실제로 개선하는지 평가한다.

이 문서에서 AEP는 원본 프로젝트에 덧붙이는 **프로젝트 전용 Agentic Engineering 실험 시스템**을 뜻한다. LocalTwin AEP와 Landmark Assistant AEP는 별도 구현·평가 단위다.

## 2. 왜 두 프로젝트를 사용하는가

두 프로젝트의 점수나 생산성을 서로 비교하기 위해서가 아니다. 서로 다른 lifecycle에서 `기존 방식 vs 해당 프로젝트 전용 AEP`를 각각 검증해, 두 개의 독립적인 채용 포트폴리오 증거를 만들기 위해서다.

### LocalTwin

제품 요구사항, frontend, backend, DB, data pipeline, security, 배포와 운영 검증이 연결된 Software Product Engineering 사례다.

여기서는 다음 질문을 다룬다.

> AI Workflow가 코드 탐색과 구현뿐 아니라 요구사항 누락, regression, 문서 동기화, 배포·보안 Gate까지 개선하는가?

### On-device Landmark Assistant

도메인 정의, dataset 구축, model candidate 비교, 5-fold 평가, error analysis, ONNX export, serving contract와 Flutter/Android 전달이 연결된 ML Engineering 사례다. 공개 저장소는 training·Sprint 1 prototype·model integration evidence를 선별한 case study이며, 최종 팀 앱 전체 source와 model binary를 포함하는 단일 실행 저장소는 아니다.

여기서는 다음 질문을 다룬다.

> AI Workflow가 잘못된 실험 비교, data leakage, 검증되지 않은 성능 주장, artifact 선택 오류와 불필요한 GPU 실행을 줄이는가?

## 3. 핵심 연구 질문

### LocalTwin AEP

1. 기존의 ad-hoc AI 개발 방식보다 구조화된 project context와 retrieval이 Task 성공률을 높이는가?
2. request classification과 Tool/Context routing이 token, 잘못된 Tool 호출과 사람 개입을 줄이는가?
3. 상태 저장, 검증과 복구 loop가 필요한 제품 개발 Task는 무엇인가?

### Landmark Assistant AEP

1. experiment history와 dataset/artifact evidence retrieval이 잘못된 실험 제안과 근거 없는 결론을 줄이는가?
2. dataset fingerprint, split, metric과 artifact contract gate가 leakage와 handoff 오류를 차단하는가?
3. Human approval을 포함한 stateful workflow가 불필요한 학습·변환 iteration을 줄이는가?

### 실험 후에만 답할 부차 질문

- 두 AEP에서 우연히 비슷해 보이는 구현이 아니라 실제로 재사용할 가치가 확인된 interface는 무엇인가?
- 공통화가 오히려 프로젝트별 판단과 evaluator를 약화시킨 부분은 무엇인가?

## 4. 지금은 주장하지 않는 것

아래 내용은 측정 전에는 포트폴리오 문구로 사용하지 않는다.

- 생산성이 몇 % 향상되었다.
- token 사용량이 몇 % 감소했다.
- LangGraph가 기본 Agent보다 우수하다.
- Agent가 Landmark 모델 정확도를 높였다.
- 하나의 범용 Agent Framework가 완성되었다.
- LocalTwin AEP가 Landmark AEP보다 우수하거나 그 반대다.
- 서로 다른 LT와 LA Task의 점수를 합산한 단일 개선률이 있다.

## 5. 채용자에게 보여줄 역량

### Engineering

- 실제 제품과 ML pipeline을 끝까지 연결하는 능력
- test, deployment, security, data contract를 포함한 검증 능력
- 실패한 결과를 숨기지 않고 다음 guardrail로 전환하는 능력

### AI Agent

- Python으로 Tool/Function Calling과 backend integration을 구현하는 능력
- embedding, chunking, vector/hybrid retrieval과 retrieval evaluation을 포함한 RAG pipeline 설계 능력
- planning, Tool selection, memory와 stateful workflow를 설계하는 능력
- Agent trajectory, latency, token, cost와 failure를 관측하고 평가하는 능력
- 자동 evaluator, regression dataset, human rubric과 production feedback loop를 구성하는 능력
- 자동화와 Human approval의 경계를 판단하는 능력
- framework 사용 여부를 실험 결과로 결정하는 능력

세부 학습 순서와 채용 증명 산출물은 [AI 역량 개발 계획](./docs/strategy/AI_SKILL_ROADMAP.md)을 따른다.

### ML

- dataset snapshot과 split을 통제하는 능력
- validation 기반 model selection과 locked test 사용
- 평균뿐 아니라 variance, macro-F1, hard case와 low-margin을 해석하는 능력
- 학습 성능과 ONNX/INT8/runtime 성능을 분리해 평가하는 능력

## 6. 개인 기여 설명 원칙

최종 Case Study마다 다음을 분리한다.

```text
내가 정의한 문제
내가 내린 결정
내가 직접 구현·검증한 범위
AI Agent가 수행한 범위
팀원이 수행한 범위
외부 서비스나 기존 모델이 제공한 범위
```

이 구분은 추후 실제 commit과 작업 기록을 기준으로 작성한다.

## 7. 성공 조건

이 포트폴리오는 다음이 모두 있을 때 완료로 본다.

- LocalTwin AEP의 재현 가능한 Task Set, raw trace, evaluator와 holdout 평가
- Landmark Assistant AEP의 재현 가능한 Task Set, raw trace, evaluator와 holdout 평가
- 각 프로젝트 안에서 baseline과 AEP configuration을 비교한 결과
- 성공 사례뿐 아니라 실패 사례와 비용
- LocalTwin과 On-device Landmark Assistant 각각의 Case Study
- 개인 기여표
- 다른 사람이 실행할 수 있는 최소 재현 절차

## 8. 저장소 원칙

```text
LocalTwin 원본                 localtwin-aep
Landmark Assistant 원본       landmark-assistant-aep
두 Case Study 종합             agentic-engineering-portfolio
```

- 원본 프로젝트 history와 AEP 실험 history를 분리한다.
- 각 AEP는 자기 프로젝트의 baseline과만 수치 비교한다.
- 이 portfolio 저장소는 결과를 연결하지만 공통 Agent 구현을 소유하지 않는다.
- 두 구현에서 안정적인 중복이 확인되기 전에는 별도 `aep-core`를 만들지 않는다.
