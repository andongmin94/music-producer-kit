# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 장르 제한 없음 · 편집 가능한 작업 원본 우선

현재 버전은 **0.1.0 초기 패키지**입니다. 음악 제작 스킬, 조건부 참고자료, 실제 MIDI 생성·부분 수정 도구를 포함합니다.
**아직 Ableton MCP 서버가 연결된 자동 작곡 완제품은 아닙니다.** Codex 설치·행동과 Live 저장/재열기·청취 검증은 별도입니다.

## 무엇을 지향하나

“오리지널 곡 하나 만들어”, “이 흥얼거림에 반주를 붙여”, “후렴 드럼만 바꿔”, “이 멜로디에 가사만 써”를 요청별로 구분합니다.
음악이론은 도구로 쓰되 비대칭, 전조, 악기 추가, 피치 흔들림을 모든 곡에 강제하지 않습니다.
전체 WAV나 stems만 남기지 않고 MIDI·개별 소스·Live 프로젝트를 보존하는 것이 제품 목표입니다.

## 이번 버전에서 실제로 구현한 것

- 루트 `plugin.json`과 Codex 저장소 marketplace, `music-producer` 진입 스킬.
- 음악·편곡·가사·Ableton 실행 확인·MIDI·검토를 필요할 때 읽는 참고문서.
- JSON 음표에서 type-1 MIDI 생성, 음표/트랙 다시 읽기, 단일 트랙의 지정 구간 음표 교체.
- 원본 SHA 확인, 새 파일로 저장, 다른 트랙과 보호 이벤트의 무결성 검사.
- 원본 두 팩 47개 모듈의 고정 커밋 목록과 선별 기록. 전문지식 전체 이관은 미완료.
- 패키지 정적 검사, Python 테스트, Windows/Linux용 단일 CI 워크플로, 재현 가능한 ZIP 생성.

## 설치 경로

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

지원되는 데스크톱 Plugins 화면에서 Music Producer Kit을 설치한 뒤 새 대화를 시작합니다.
**marketplace 등록만으로 설치·스킬 로딩·Ableton 연결이 모두 완료되는 것은 아닙니다.**
정확한 Windows 명령과 테스트 순서는 [설치·로컬 검증](docs/local-smoke-test.md)을 보세요.
원본 두 팩이나 같은 스킬의 다른 복사본을 함께 활성화하지 않습니다.

공식 패키징 형식: https://developers.openai.com/plugins/build/plugins
공식 스킬 동작: https://learn.chatgpt.com/docs/build-skills

## 개발·검증

Python 3.12+를 사용합니다. 새 가상환경을 만든 뒤 아래 의존성을 설치하세요.

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

검사는 음악의 좋고 나쁨이나 LLM의 실제 지시 준수를 평가하지 않습니다.
`evals/scenarios.json`의 행동 시나리오는 정의만 되어 있고 실제 Codex 실행 결과는 아직 없습니다.
ZIP은 marketplace·플러그인·안내문을 담는 설치용 묶음입니다. 개발 도구와 테스트는 Git 저장소에서 실행하세요.

## 읽을 문서

[현재 진행 상태](docs/STATUS.md) · [요구사항](docs/requirements.md) · [원본 선별 기록](docs/source-selection.md) · [전체 모듈 목록](docs/upstream-inventory.json)

개발 에이전트는 루트 AGENTS.md를 먼저 읽고, 매 세션 종료 전에 STATUS를 실제 검사 결과로 갱신합니다.
개인 보컬·유료 샘플·미공개 음악·인증정보·로컬 경로는 이 공개 저장소나 배포 ZIP에 넣지 않습니다.

## 알려진 경계

MIDI 도구는 음원, 오디오 렌더러, Melodyne 컨트롤러, 보컬 합성기 또는 Live Set 생성기가 아닙니다.
단일 채널, 경계 안에서 끝나는 음표를 다룹니다. 페달·겹친 동일 음·경계 걸침은 조용히 훼손하지 않고 거절합니다.
실제 MIDI -> Live 악기 배치, 저장·재열기와 범위 제한 편집은 다음 로컬 검증 대상입니다.
현재 있는 음원과 샘플부터 사용하며 구매·크레딧 소비·외부 업로드를 자동 승인하지 않습니다.

## 출처·라이선스

원본 두 저장소의 아이디어와 선별 근거는 [출처 기록](docs/source-selection.md)에 남깁니다.
책·가사·샘플 원본은 배포하지 않습니다. [NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
프로젝트 자체의 공개 라이선스는 소유자가 아직 선택하지 않았습니다. Public 저장소와 오픈소스 라이선스 부여를 혼동하지 않습니다.
