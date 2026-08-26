# External AI Reviews

이 폴더는 `evaluation_packets`를 읽은 외부 AI의 응답 원문과 사람의 판정을 분리해 저장한다. Packet을 만들었다고 review가 완료된 것은 아니며, 외부 AI가 말한 내용도 자동으로 사실이 되지 않는다.

## 구조

```text
reviews/
└─ <packet-id>/
   ├─ <provider>-<YYYY-MM-DD>.md
   └─ TRIAGE.md
```

- provider file: 수정하지 않은 review 응답, 사용한 model·날짜·packet commit
- `TRIAGE.md`: 각 finding의 evidence 확인 결과와 후속 Issue·commit

## Triage 상태

- `Verified`: packet source로 finding을 재현하거나 확인함
- `Rejected`: source와 맞지 않으며 반증 근거가 있음
- `Needs evidence`: 판단에 필요한 자료가 packet에 없음
- `Deferred`: finding은 타당하지만 현재 scope 밖임

## 최소 기록

```markdown
| Finding | 상태 | 확인한 evidence | 결정 | 후속 작업 |
| --- | --- | --- | --- | --- |
| F-001 | Verified | `sources/...` | 수정 필요 | #issue |
```

finding을 해결했다고 표시하려면 실제 변경 commit과 재검증 결과를 연결한다. 공개 기준은 [Public Evidence Policy](../governance/PUBLIC_EVIDENCE_POLICY.md)를 따른다.
