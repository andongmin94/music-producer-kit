# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 한국어/영어/일본어 · 편집 가능한 원본 우선

현재 **0.6.0 — 실제 MCP 도구 조회와 Windows 첫 연결 경로**입니다.
실제 사용자 PC의 Codex/Ableton 연동과 음악 품질 검증은 아직 완료하지 않았습니다.

## 실제 구현한 기능

하나의 진입 스킬이 전체 제작/부분 수정과 보호 대상을 구분하고 필요한 음악·작사·보컬 지식만 읽습니다.
Mido는 MIDI 생성·재조회·지정 구간 음표 수정과 보호 이벤트 검사를 담당합니다.
SoundFile 기반 샘플 도구는 지정 폴더의 길이·채널·형식을 읽고 파일명 검색과 선택 파일 재확인을 지원합니다.
새 MCP 진단 도구는 공식 Python SDK로 로컬 HTTP 또는 지정한 stdio 서버에 연결해 실제 도구 이름과 입력/출력 규격을 기록합니다.
진단 중에 작곡·편집·재생·저장 도구는 호출하지 않습니다. 서버 목록 조회를 Live 작업 성공으로 오인하지 않습니다.

[제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md) · [샘플 사용](plugins/music-producer-kit/skills/music-producer/references/samples.md) · [MCP 진단](plugins/music-producer-kit/skills/music-producer/references/mcp-connection.md)

## 다음 단계: Windows 로컬 Codex에서 시작

[첫 연결 요청문](docs/windows-first-run.md)을 같은 Windows의 Codex에 전달합니다.
현재 설치 버전과 기존 연결 확인 → 실제 도구 조회 → 승인된 새 빈 Set에서 4마디 작성 → 베이스 2마디만 수정 → 저장·재열기를 검증하는 순서입니다.
현재 곡을 자동으로 지우거나, 설정 전체를 덮거나, 관리자 권한·유료 구매·샘플 업로드를 요구하지 않습니다.
MCP가 아직 없으면 설치된 Live 버전과 필요한 작업을 먼저 대조해 하나를 정합니다. 이 패키지 자체가 Ableton MCP 서버인 것은 아닙니다.

## 중국 특화 자료는 원본도 제거했습니다

**41개 모듈, 89개 파일의 선별본**을 그대로 유지합니다. 전체 원본 ZIP과 감사/복구 모드는 없습니다.
중국 전용 모듈·곡 사례·가사 예제·민속악기 절을 제외하고 범용 음악이론과 한영일 지식은 로컬에 유지합니다.
중국어로 쓰인 일반 이론과 일본어 한자까지 지우는 문자 필터는 아닙니다.
원본 링크는 출처이며 설치나 조회에 필요하지 않습니다. 자동 업데이트·누락 시 원격 복구를 제공하지 않습니다.
법적 고지는 유지합니다. 현재 트리/새 배포물의 삭제이지 과거 Git 이력 재작성은 아닙니다.

[선별 범위](docs/source-selection.md) · [로컬 지식 목록](plugins/music-producer-kit/library/catalog.json) · [자료 사용법](plugins/music-producer-kit/library/README.md)

## 설치와 검증

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

지원되는 Plugins 화면에서 설치하고 새 대화를 시작합니다. 활성화·Live 연결은 별도 확인 단계입니다.
[플러그인 로컬 검사](docs/local-smoke-test.md)를 따르세요. 원본 스킬팩은 별도 설치하지 않습니다.
Python 3.12+ 가상환경에서:

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

MIDI는 Mido, 오디오 헤더는 SoundFile, MCP 통신은 공식 MCP SDK를 사용합니다. 지식 조회는 표준 라이브러리만 필요합니다.
진단의 stdio 명령은 신뢰하고 승인한 설치된 프로그램만 지정합니다. 프로그램 시작 자체의 부작용까지 차단하는 샌드박스는 아닙니다.
HTTP는 명시적인 loopback 주소만 지원하고 프록시 환경을 상속하지 않습니다. 토큰은 값 대신 환경변수 이름으로 전달하며 보고서는 비공개 폴더에 새로 작성합니다.
테스트용 SDK 서버는 Ableton이 아닙니다. 코드/프로토콜 검사를 실제 음악 작업이나 모델 지시 준수 검증으로 보고하지 않습니다.

[현재 상태](docs/STATUS.md) · [요구사항](docs/requirements.md) · [이관 기록](docs/knowledge-curation.md)

개인 녹음·유료 샘플·미공개 곡·인증정보·진단 보고서는 공개 저장소나 배포 ZIP에 넣지 않습니다.
구매·Splice 크레딧·외부 업로드·설정 변경은 자동 승인하지 않습니다.
프로젝트 자체 공개 라이선스는 미확정입니다. [NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
