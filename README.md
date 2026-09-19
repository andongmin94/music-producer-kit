# Music Producer Kit

**자연어 음악 제작·부분 수정을 위한 Codex 플러그인 개발 프로젝트.**
Ableton-first · 한국어/영어/일본어 · 편집 가능한 원본 우선

현재 **0.7.1 — 공식 우선 전환 정리**입니다. **완제품이 아닙니다.**
이전 개인 MCP의 시험 설치는 제거되었고, 공식 기반의 대체 Live 연결은 아직 구현·검증하지 않았습니다.

## 되는 것과 아직 안 되는 것

| 영역 | 현재 상태 |
|---|---|
| 단일 제작 스킬·음악/가사 지식 | 구현. 필요한 자료만 선택하며 장르를 J-pop으로 제한하지 않음 |
| MIDI 생성·조회·범위 제한 수정 | Mido 도구 유지 |
| 보유 샘플 검색·헤더/파일 확인 | SoundFile 도구 유지. 청취·BPM/권리 판정과는 다름 |
| 일반 MCP 목록 진단 | 기존 도구 유지. Ableton 연결 서버나 공식 SDK 자체는 아님 |
| 저장 .als 비교 | 읽기 전용 도구 유지. 삭제한 backend 모듈과의 의존성 제거 |
| 공식 기반 Live 직접 조작 | **미구현.** SDK 계약·호환 조건과 호출 경로부터 확인 필요 |
| 설치본 자연어 제작→부분 수정→저장·재열기 | **미검증.** 이전 PC 실험 결과로 대체 불가 |

이번 변경은 0.7.0 위에 최신 결정을 반영한 것입니다. 새 인계 ZIP의 오래된 0.6.0 코드로 되돌리지 않았습니다.
옛 MCP 전용 작성기와 절차는 제거했으며 비활성 fallback으로 보관하지 않습니다. 범용 도구·검사와 선별 지식은 유지합니다.

## 이제 할 일

[공식 경로 확인](docs/official-path-review.md)에 웹에서 확인한 조건, 미확인 API와 로컬 Codex 요청문을 정리했습니다.
현재 공식 안내의 Extensions는 Live 12 Suite Beta 대상입니다. 높은 일반 출시판 버전 번호만 보고 지원된다고 하지 않습니다.
SDK 자료 확보와 Beta 설치는 별도 단계이며 계정·설치 변경을 자동 승인하지 않습니다.
제조사의 SDK를 사용하는 우리 코드가 제조사 제공 MCP가 되는 것은 아닙니다. 확인되지 않은 API나 새 서버를 추측해서 추가하지 않습니다.

실제 API 확인 → 필요한 연결 하나 구현 → [설치된 사용자 흐름 검증](docs/installed-flow-acceptance.md)이 남아 있습니다.

## 보존한 지식과 동작

41개 모듈·89개 파일의 선별 지식, 한영일 가사·발음, 일반 화성·리듬·편곡 지식을 로컬에 보유합니다.
중국 특화 원본·우회 보관·원격 복원은 없습니다. 범용 중국어 음악이론과 일본어 한자는 유지합니다.
[제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md) · [자료 사용법](plugins/music-producer-kit/library/README.md) · [선별 기록](docs/source-selection.md)

## 패키지 검사

Python 3.12+의 프로젝트 환경에서:

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

[설치/로컬 검사](docs/local-smoke-test.md) · [현재 검증 상태](docs/STATUS.md) · [최신 인계문](docs/web-handoff.md)

테스트 통과는 이 코드와 파일의 검사이지 Live 연결·모델 행동·음악 품질의 인증이 아닙니다.
개인 오디오·유료 샘플·프로젝트·진단 로그·토큰은 배포하지 않습니다. 구매/크레딧/외부 업로드는 명시 승인이 필요합니다.
원본 LICENSE/NOTICE는 유지합니다. [권리 고지](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
