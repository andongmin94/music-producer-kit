# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 한국어/영어/일본어 · 편집 가능한 작업 원본 우선

현재 **0.7.0 — 설치된 제작 스킬과 기존 Ableton 연결의 최소 통합**입니다.
실제 PC 연결·4마디 작성·부분 수정·UI 저장·재열기는 로컬 인계에서 검증했습니다.
**설치된 플러그인이 자연어 요청부터 끝까지 수행하는 사용자 흐름은 다음 로컬 검증 대상**입니다.
서로 다른 검증을 하나의 완료 표시로 합치지 않습니다.

## 사용하는 경로

`설치된 music-producer → 기존 ableton_live 네이티브 MCP → 번들 검증 도구 → 호스트 Windows UI 저장·열기`

사용자는 음악을 일반적인 말로 요청합니다. 스킬이 작업 범위와 보호 대상을 정하고 필요한 음악 지식을 선택하며, 실제 도구 조회·작업 계획·검증 자료 작성을 맡습니다.
사용자가 내부 JSON이나 스크립트 명령을 외우도록 요구하지 않습니다.
가사만 필요한 요청은 Ableton을 열거나 프로젝트를 만들지 않습니다.

| 구성 | 실제 역할 |
|---|---|
| 단일 제작 스킬과 조건부 참고자료 | 전체 제작/부분 수정 구분, 한영일 가사·보컬과 다양한 장르의 제작 판단 |
| Mido MIDI 도구 | 편집 가능한 MIDI 생성·재조회·지정 구간 수정 |
| SoundFile 샘플 도구 | 승인된 로컬 폴더의 헤더 조회·파일명 검색·선택 파일 재확인 |
| `live_workflow.py` | 기존 음표 문서를 네이티브 MCP 입력으로 변환, 빈 대상 확인, 생성 결과·수정 전후·재열기 읽기 비교 |
| `live_set_diff.py` | 저장된 `.als` gzip/XML의 모든 변경 위치 보고. 자동화·장치·ID·커서도 무조건 제외하지 않음 |
| `mcp_probe.py` | 연결 장애나 서버 변경 시 도구 규격 조회만 수행. 음악을 작성하지 않음 |

실제 Live 조작은 이미 설치된 MCP가 맡고, 새 Set·저장·열기는 검증된 호스트 UI 경로가 맡습니다.
두 번째 MCP 서버, 비공개 SDK 작성기, 자동 설치·설정 덮어쓰기 또는 새 호환 계층을 추가하지 않았습니다.
[설치형 제작 흐름](plugins/music-producer-kit/skills/music-producer/references/live-workflow.md) · [제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md)

## 부분 수정과 증거의 범위

현재 자동 계획/검증 경로는 새로 만든 단순 MIDI 클립의 변경 기록을 사용합니다.
승인된 하나의 클립 범위만 교체하고, 삭제 직후 상태와 재생성 후 상태를 각각 읽어 보호 항목을 비교합니다.
타임아웃 뒤 쓰기를 무조건 재시도하지 않습니다. 인덱스는 다시 조회하고, 성공한 수정 뒤에는 새 상태의 기록을 남겨 다음 수정에 사용합니다.
곡 길이·박자·트랙 이름은 입력에 따르며 제품을 4마디 예제로 고정하지 않습니다.

MCP의 기본 음표 읽기는 모든 MPE·확률·release velocity·자동화를 보여주지 않습니다.
따라서 기존 복잡한 연주나 수동으로 바꾼 클립을 같은 삭제·재생성 경로에 억지로 넣지 않습니다.
전체 저장 파일 차이는 별도로 확인하고, 실제 UI 열기 기록과 재열기 읽기 결과를 함께 남깁니다.
파일 비교 성공만으로 UI 실행·청취·외부 플러그인/샘플 존재를 증명하지 않습니다.

## 지금 로컬에서 필요한 것

[설치된 플러그인 사용자 흐름 검증](docs/installed-flow-acceptance.md)을 새 로컬 Codex 세션에서 진행합니다.
이미 승인·설치한 연결과 별도 Python 환경을 유지합니다. 최초 설치·취향·언어 설문을 다시 하지 않습니다.
이번에는 개발 체크아웃의 지침을 대신 넣는 것이 아니라 **실제 설치 경로의 스킬**이 자연어 작성 → 부분 수정 → 저장·재열기를 수행하는지 확인합니다.

[로컬 인계 원문](docs/web-handoff.md) · [현재 상태와 검증 구분](docs/STATUS.md)

## 설치와 개발 검사

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

이미 등록되어 있으면 중복 등록하지 말고 지원되는 Plugins 화면에서 설치본을 갱신한 뒤 새 도구 세션을 시작합니다.
명령 지원과 실제 설치 위치는 현재 Codex에서 확인합니다. 저장소 등록만으로 설치·활성화가 증명되지는 않습니다.
Python 3.12+의 **기존 kit 환경**에서:

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

서버의 FastMCP 환경에 kit의 MCP SDK 버전을 덮어 설치하지 않습니다.
새 통합은 기존 Mido/SoundFile/공식 MCP SDK를 그대로 쓰며 추가 의존성이 없습니다.
[기존 패키지 검사](docs/local-smoke-test.md) · [샘플 사용](plugins/music-producer-kit/skills/music-producer/references/samples.md)

## 지식·권리·개인정보

로컬 지식은 **41모듈·89파일 선별본**이며 이번 통합에서 변경하지 않았습니다.
중국 특화 원본·숨긴 전체 ZIP·감사/복구 모드는 없습니다. 범용 이론이 중국어로 쓰였다는 이유나 일본어 한자 때문에 버리지는 않습니다.
원본 URL은 출처이고 작업 의존성이 아닙니다. 누락 시 원격 복구나 자동 업데이트를 제공하지 않습니다.

개인 녹음·유료 샘플·프로젝트·계정 설정·실제 호출 로그는 공개 저장소나 배포 ZIP에 넣지 않습니다.
샘플 구매·Splice 크레딧·외부 업로드·권한 변경을 자동 승인하지 않습니다.
[요구사항](docs/requirements.md) · [선별 원칙](docs/source-selection.md) · [NOTICE](plugins/music-producer-kit/NOTICE.md)
프로젝트 자체 공개 라이선스는 아직 소유자가 선택하지 않았습니다.
