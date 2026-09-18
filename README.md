# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 한국어/영어/일본어 · 편집 가능한 원본 우선

현재 **0.5.0 — 선별 원본 정리와 로컬 샘플 조회**입니다.
실제 사용자 환경의 Codex/Ableton 연동과 음악 품질 검증은 아직 완료하지 않았습니다.

## 실제 구현한 기능

한 개의 진입 스킬이 전체 제작/부분 수정과 보호 대상을 구분하고 필요한 음악·작사·보컬 지식만 읽습니다.
Mido 도구로 MIDI 생성, 다시 읽기, 특정 트랙의 지정 구간 음표 교체와 보호 이벤트 검사를 수행합니다.
새 샘플 도구는 지정한 로컬 폴더의 오디오 길이·채널·형식을 읽고, 파일 이름으로 찾은 뒤 선택 파일을 재확인합니다.
샘플 재생·업로드·구매·Splice 계정 조작은 하지 않습니다. 이름만 보고 라이선스·BPM·조성·음질을 확정하지 않습니다.

[제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md) · [샘플 사용](plugins/music-producer-kit/skills/music-producer/references/samples.md)

## 중국 특화 자료는 원본도 제거했습니다

현재 자료는 **41개 모듈, 89개 파일의 선별본**입니다. 전체 원본 ZIP, 제외 자료의 감사/복구 모드, 중복 원본 목록을 삭제했습니다.
중국 전용 모듈·중국 곡 사례·가사 예제·민속악기 절을 제외하고, 필요한 일반 음악이론과 한영일 지식은 로컬에 유지합니다.
중국어로 쓰인 일반 이론과 일본어 한자까지 지우는 문자 필터가 아닙니다.
원본 링크는 출처이며 설치나 조회에 필요하지 않습니다. 자동 업데이트·누락 시 원격 다운로드는 없습니다.
법적 출처 고지는 유지하며, 이번 변경은 현재 트리/새 배포물의 삭제이지 과거 Git 이력 재작성이 아닙니다.

[선별 범위](docs/source-selection.md) · [로컬 지식 목록](plugins/music-producer-kit/library/catalog.json) · [자료 사용법](plugins/music-producer-kit/library/README.md)

## 설치와 사용

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

지원되는 Plugins 화면에서 설치하고 새 대화를 시작합니다. 실제 활성화/Live 연결은 별도 확인 단계입니다.
[설치·로컬 검증](docs/local-smoke-test.md)을 따라 확인하세요. 원본 스킬팩은 별도 설치하지 않습니다.
샘플·MIDI 도구는 아래 의존성을 설치한 로컬 Python 3.12+ 환경에서 실행합니다.

## 개발·검증

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

MIDI는 Mido, 오디오 헤더는 SoundFile을 사용합니다. 지식 조회는 표준 라이브러리만으로 동작합니다.
테스트는 자료/패키지/도구를 확인하며 LLM의 실제 지시 준수나 작곡 품질을 입증하지 않습니다.

[현재 상태](docs/STATUS.md) · [요구사항](docs/requirements.md) · [이관 기록](docs/knowledge-curation.md)

개발 에이전트는 AGENTS.md와 실제 상태를 읽고 세션 종료 전에 검사 결과·한계·다음 단계를 남깁니다.
개인 녹음·유료 샘플·미공개 곡·인증정보·실제 로컬 경로는 공개 저장소나 ZIP에 포함하지 않습니다.
원본 노트·샘플·장치·자동화가 있는 Live 프로젝트가 목표이며, MIDI나 WAV만 만들어 놓고 Live 작업을 완료했다고 하지 않습니다.
프로젝트 자체 공개 라이선스는 미확정입니다. [NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
