# Public Evidence Policy

## 목적

이 저장소가 보여줘야 하는 것은 “AI가 무슨 생각을 했는가”가 아니라 “무엇을 요구받았고, 어떤 근거로 결정했으며, 무엇이 바뀌었고, 어떻게 검증했는가”다.

## 공개 가능한 evidence

- 공개하기로 승인된 요구사항과 acceptance criteria
- GitHub Issue, Project 상태, commit, PR과 review
- 공개 repository의 source, test와 command 결과
- 실험 configuration, trace schema, aggregate metric과 limitation
- 선택한 대안, 기각한 대안과 결정 이유
- 외부 AI review 원문과 사람의 finding triage
- 알려진 공백, 실패, 중단과 복구 기록

모든 artifact는 가능한 경우 Issue ID, commit SHA, 실행 환경과 검증 명령을 연결한다.

## 공개하지 않는 자료

- API key, token, credential, private key와 `.env`
- 개인 식별 정보와 로컬 사용자 경로
- 저작권·계약상 공개할 수 없는 제3자 source/data
- 비공개 model artifact 또는 원본 dataset
- system/developer prompt와 서비스 내부 설정
- private chain-of-thought 또는 숨겨진 evaluator answer
- 공개 동의를 받지 않은 대화 원문

제외 사실 자체가 평가에 영향을 주면 무엇을 왜 제외했는지는 공개한다. 비공개 값이나 원문은 기록하지 않는다.

## 대화 기록 원칙

대화 전체를 그대로 export하지 않는다. 대신 다음을 durable artifact로 남긴다.

1. 사용자의 요구사항과 변경 요청
2. 결정된 범위와 성공 기준
3. 고려한 선택지와 최종 결정 이유
4. 실제 변경 file과 commit
5. 실행한 검증과 실패 결과
6. 남은 불확실성과 다음 작업

이 요약은 작성자에게 유리한 정보만 남기지 않도록 관련 Issue, diff, test 또는 packet source에 연결한다.

## 외부 AI review 원칙

- 외부 reviewer는 권위자가 아니라 추가 evaluator다.
- finding은 packet 내부 evidence를 인용해야 한다.
- evidence가 없는 주장은 `Unknown` 또는 `Needs evidence`로 남긴다.
- 외부 AI의 응답만으로 코드, Issue 상태나 연구 결론을 자동 변경하지 않는다.
- 사람의 triage와 실제 수정·재검증이 끝나야 finding을 해결한 것으로 본다.

## 공개 전 gate

- source가 명시적 allowlist인가?
- 고정 commit과 checksum이 있는가?
- local path, credential과 개인정보를 검사했는가?
- 알려진 공백과 제외 사유를 적었는가?
- 숫자 개선 주장은 동일 조건 baseline과 실제 측정값이 있는가?
- human review가 완료됐는가?

자동 검사는 실수를 줄이는 장치일 뿐 완전한 보안 검토를 대체하지 않는다.
