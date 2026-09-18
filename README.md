# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 제작 도우미.**
Ableton-first · 한국어/영어/일본어 + 연주곡 · 편집 가능한 원본 우선

현재 **0.5.0 — 선별 원본 정리·로컬 샘플 탐색** 단계입니다.
스킬·음악 지식·MIDI 도구·보유 샘플 검색을 포함하지만 실제 Codex/Ableton 연결과 자동 작곡 품질이 검증된 완제품은 아닙니다.

## 현재 들어 있는 것

하나의 제작 스킬이 현재 요청에 필요한 화성, 멜로디/구조, 리듬, 악기/텍스처, 작사, 발음, 보컬 지침을 선택합니다.
한국어·영어·일본어는 곡마다 선택하거나 섞을 수 있습니다. 연주곡에 가사 언어를 요구하지 않으며 J-pop 전용으로 제한하지 않습니다.
전조·비대칭·같은 후렴 변경·피치 오류·타이밍 흔들림을 모든 곡에 강제하지 않습니다.

Mido 도구는 편집 가능한 MIDI 생성·재조회·지정 트랙/구간 음표 수정과 보호 이벤트 검사를 수행합니다.
샘플 검색 도구는 허용된 로컬 폴더에서 파일명/경로로 후보를 찾고 크기와 SHA256을 확인합니다. 구매·다운로드·업로드·청취·BPM 분석은 하지 않습니다.
[제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md) · [샘플 검색](plugins/music-producer-kit/skills/music-producer/references/samples.md)

## 불필요한 원본은 보관하지 않습니다

중국 전용 원본과 지정된 특화 절을 실제 자료에서 제거했습니다. 기존 전체 원본 ZIP과 감사용 우회 옵션도 없습니다.
현재는 **42개 선별 모듈**과 관련 참고자료·법적 고지를 패키지에 보유합니다. 중국어로 작성된 범용 음악이론과 일본어 한자는 보존합니다.
원본 URL은 출처 기록이지 설치·제작 시 의존성이 아닙니다. 자동 업데이트, submodule, 설치 중 원본 다운로드나 원격 복구는 없습니다.
현재 파일 목록·해시는 [로컬 라이브러리](plugins/music-producer-kit/library/README.md), 삭제 기록은 [선별 보고서](docs/SOURCE_SELECTION_REPORT.json)에 있습니다.
과거 Git 이력을 강제 재작성한 것은 아닙니다. 새 패키지와 현재 트리의 자료를 정리한 것입니다.

## 설치와 검증

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

지원되는 Plugins 화면의 실제 활성화와 Ableton 연결은 별도 확인이 필요합니다.
[로컬 검증 순서](docs/local-smoke-test.md)를 따르세요. 원본 두 팩을 별도로 설치하지 않습니다.

Python 3.12+의 가상환경에서:

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

코드·패키지 검사와 음악 품질 검증은 다릅니다. 실제 결과와 미검증 항목은 [STATUS](docs/STATUS.md)에 기록합니다.
[요구사항](docs/requirements.md) · [선별 원칙](docs/source-selection.md) · [지식 이관](docs/knowledge-curation.md)

## 작업과 권리 경계

개발 에이전트는 AGENTS.md와 현재 상태를 먼저 읽고 세션 종료 전에 결과·막힌 부분·다음 작업을 남깁니다.
개인 녹음, 유료 샘플, 미공개 곡, 인증정보와 실제 로컬 경로는 이 공개 저장소나 배포물에 넣지 않습니다.
이 도구는 Live Set 생성기, Splice/Melodyne 컨트롤러, 보컬 합성기 또는 오디오 품질 평가기가 아닙니다.
원본의 LICENSE/NOTICE와 제3자 인용의 권리 구분은 유지합니다. [NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
프로젝트 자체의 공개 라이선스는 소유자가 아직 선택하지 않았습니다.
