# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 장르 제한 없음 · 편집 가능한 작업 원본 우선

현재 버전은 **0.3.0 — 제작 지식 이관·로컬 탐색 지원**입니다.
제작 스킬, 조건부 작업 지식, MIDI 생성·부분 수정 도구와 두 원본 팩의 전체 보관본을 포함합니다.
**아직 실제 Codex/Ableton 동작과 자동 작곡 품질이 검증된 완제품은 아닙니다.**

## 스킬은 하나, 지식은 필요한 것만

사용자의 요청에서 만들 것과 보호할 것을 먼저 구분합니다.
음악 지식을 모두 매번 읽는 대신, 아래 주제 중 현재 작업에 맞는 문서만 사용합니다.

| 주제 | 작업에 쓰는 내용 |
|---|---|
| 화성 | 화음 구성·보이싱·텐션·차용·전조, 멜로디를 보호하는 수정 |
| 멜로디·구조 | 흥얼거림, 동기의 반복·발전, 노래와 루프의 서로 다른 완결 조건 |
| 리듬 | 속도와 밀도의 구분, 킥·베이스, 스윙, 박자와 시간 단위 |
| 텍스처·악기 | 역할·음역·레이어 충돌, 대선율, 보유 음원 선택 |
| 작사 | 의도·구간 역할·디테일·운율, 고정 가사와 멜로디 보존 |
| 가사와 음표 연결 | 문자·발음·모라·음표 수 구분, 언어별 배치와 예외 |
| 보컬 제작 | 가이드·녹음·합성 구분, 표현·코러스·더블·교정 범위 |

전조, 비대칭, 같은 후렴의 변경, 피치 오류나 타이밍 흔들림을 모든 곡에 강제하지 않습니다.
짧은 사용 지시가 단순한 음악만 만들라는 뜻도 아닙니다.
[제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md) · [상세 이관 기록](docs/knowledge-curation.md)

## 원본 저장소 없이도 지식을 보유합니다

작곡 29개 모듈/74개 파일과 가사 18개 모듈/47개 파일, 총 **121개 파일**을 고정 커밋 그대로 보존했습니다.
상세 참고문서·예외·스키마·예제·LICENSE·NOTICE도 포함합니다. 원본 링크는 출처이지 설치나 작업의 의존성이 아닙니다.
보관본은 압축된 데이터이며 원본 47개 스킬을 추가 설치하지 않습니다.
기본 지침으로 부족하면 로컬 도구로 필요한 모듈의 파일 목록·목차·문자열 검색·줄 범위를 조회합니다.
원본 자동 업데이트, Git submodule, 설치 중 다운로드, 누락 시 원격 대체 경로는 없습니다.

**보존은 완료, 모든 문장·표의 검증과 지침화는 미완료**입니다. 일곱 작업 문서를 심화 자료 전체 이관으로 과장하지 않습니다.
[로컬 지식 안내](plugins/music-producer-kit/library/README.md) · [보존 검증 기록](docs/SOURCE_SNAPSHOT_REPORT.json)

## 실제 실행 도구

JSON 음표에서 MIDI 생성, MIDI 다시 읽기, 단일 트랙의 지정 구간 음표 교체를 지원합니다.
원본 SHA, 원본 파일, 범위 밖 이벤트를 보호합니다. 안전하게 지원하지 않는 페달·겹친 동일 음·경계를 가로지르는 음표는 명시적으로 거절합니다.
[4마디 화성 예제](plugins/music-producer-kit/skills/music-producer/examples/harmony-study.json)는 화성·베이스를 개별 트랙으로 남기는 직접 작성 테스트 자료입니다.
문서 표와 MIDI의 실제 음표를 대조하고 지정된 베이스 구간만 바꾸는 검사를 포함합니다. 완성곡이나 청취 평가 자료는 아닙니다.

## 설치

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

지원되는 Plugins 화면에서 설치한 뒤 새 대화를 시작합니다.
marketplace 등록, 실제 플러그인 활성화, Ableton 연결은 서로 다른 단계입니다.
[설치·로컬 검증](docs/local-smoke-test.md)을 따르세요. 원본 두 스킬팩을 별도로 설치할 필요가 없습니다.

## 개발·검증

Python 3.12+와 새 가상환경을 사용합니다.

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

지식 탐색은 Python 표준 라이브러리만 사용합니다. 배포물을 분리한 뒤 네트워크 없이 읽는 검사도 포함합니다.
테스트는 패키지·MIDI·원본 위치와 탐색을 확인하며, 음악 품질이나 실제 LLM의 지시 준수를 증명하지 않습니다.
실제로 관측한 CI 및 미검증 상태는 [STATUS](docs/STATUS.md)에 기록합니다.

## 작업 연속성과 경계

[요구사항](docs/requirements.md) · [원본 선별 기록](docs/source-selection.md) · [모듈별 보존 상태](docs/upstream-inventory.json)

개발 에이전트는 AGENTS.md를 먼저 읽고 매 세션 종료 전 STATUS를 실제 검증 결과로 갱신합니다.
현재 도구는 Live Set 생성기, 오디오 렌더러, Melodyne/Splice 컨트롤러, 보컬 합성기가 아닙니다.
보유 도구부터 쓰며 구매, 크레딧 사용, 외부 업로드를 자동 승인하지 않습니다.
개인 녹음, 유료 샘플, 미공개 곡, 인증정보, 실제 로컬 경로는 배포하지 않습니다.

## 출처·라이선스

[NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
원본 보관본은 원래 LICENSE/NOTICE와 기존 인용을 유지합니다. 제3자 서적·번역·가사까지 우리 라이선스로 재허가하지 않습니다.
프로젝트 자체의 공개 라이선스는 소유자가 아직 선택하지 않았습니다.
