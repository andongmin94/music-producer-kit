# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 장르 제한 없음 · 편집 가능한 작업 원본 우선

현재 버전은 **0.2.0 — 로컬 지식 보관·조회 지원**입니다.
제작 스킬과 MIDI 실행 도구에 더해, 원본 두 저장소의 전체 추적 파일을 설치 패키지에 보유합니다.
**아직 실제 Ableton MCP 연결과 자동 작곡 품질이 검증된 완제품은 아닙니다.**

## 원본 저장소 없이도 지식을 보유합니다

작곡 29개 모듈/74개 파일과 가사 18개 모듈/47개 파일, 총 **121개 파일**을 고정 커밋 그대로 보존했습니다.
본문뿐 아니라 상세 참고문서, 예외, 스키마, 예제, LICENSE와 NOTICE도 포함합니다.
원본 GitHub 링크는 출처 기록이며 설치·제작 시 의존성이 아닙니다. Git submodule, 원본 자동 업데이트나 누락 시 다운로드도 없습니다.

보관본은 압축된 데이터입니다. 활성화되는 제작 스킬은 하나이며, 필요한 문서의 필요한 절만 로컬 읽기 도구로 조회합니다.
원본의 47개 스킬을 함께 실행하거나 원본의 강제 규칙을 다시 적용하지 않습니다.
**원문 보존은 완료, 모든 문장의 검증·운영 지침 재작성은 미완료**입니다. 이를 혼동하지 않습니다.
[로컬 지식 안내](plugins/music-producer-kit/library/README.md) · [보존 검증 기록](docs/SOURCE_SNAPSHOT_REPORT.json)

## 실제 구현 범위

- 짧은 요청, 전체 곡, 가사만 작성, 드럼만 수정 등의 범위 구분과 보호 지침.
- 음악·편곡·가사/보컬·MIDI·Ableton 실행 확인·검토 참고자료.
- JSON 음표에서 MIDI 생성, 다시 읽기, 단일 트랙의 지정 구간 음표 교체와 보호 이벤트 검사.
- 원본 SHA 확인, 새 파일 저장, 원본 및 보호 이벤트 보존.
- 47개 모듈과 연결 파일의 로컬 목록/범위 읽기, 압축파일·파일별 해시와 권리 고지 검증.
- Windows/Linux 자동 검사와 두 보관본을 포함하는 재현 가능한 설치 ZIP.

원본이 배포하지 않은 서적 전문, 음원, 내부 측정 도구나 미공개 코퍼스를 포함한다는 뜻은 아닙니다.

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

지식 조회 자체는 Python 표준 라이브러리만 사용합니다. 네트워크 없이 배포물을 분리해 읽는 검사도 포함합니다.
파일 검사는 음악 품질이나 실제 Codex의 지시 준수를 증명하지 않습니다.
행동 시나리오는 정의되어 있으나 실제 Codex/Live 실행과 청취 평가는 아직 별도입니다.

## 작업 연속성과 경계

[현재 상태](docs/STATUS.md) · [요구사항](docs/requirements.md) · [선별 기록](docs/source-selection.md) · [모듈별 상태](docs/upstream-inventory.json)

개발 에이전트는 AGENTS.md를 먼저 읽고 매 세션 종료 전 STATUS를 실제 검증 결과로 갱신합니다.
현재 도구는 Live Set 생성기, 오디오 렌더러, Melodyne/Splice 컨트롤러, 보컬 합성기가 아닙니다.
MIDI 편집기는 안전하게 지원하지 않는 페달, 겹친 동일 음, 경계를 가로지르는 음표를 조용히 훼손하지 않고 거절합니다.
보유 도구부터 쓰며 구매, 크레딧 사용, 외부 업로드를 자동 승인하지 않습니다.
개인 녹음, 유료 샘플, 미공개 곡, 인증정보, 실제 로컬 경로는 배포하지 않습니다.

## 출처·라이선스

[NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
원본 보관본은 원래 LICENSE/NOTICE 및 기존 인용을 유지합니다. 제3자 서적·번역·가사까지 우리 라이선스로 재허가하지 않습니다.
프로젝트 자체의 공개 라이선스는 소유자가 아직 선택하지 않았습니다.
