# Music Producer Kit

**말로 음악을 만들고, 맡긴 부분만 고치는 Codex 플러그인.**
Ableton-first · 한국어/영어/일본어 · 다양한 장르 · 편집 가능한 작업 원본 우선

현재 버전은 **0.4.0 — 한·영·일 제작 범위와 언어별 가사 지침**입니다.
제작 스킬, 음악 지식, MIDI 생성·부분 수정 도구와 원본 자료의 독립 보관본을 포함합니다.
**실제 Codex/Ableton 동작과 작곡 품질이 검증된 완제품은 아닙니다.**

## 제작 범위

가사·보컬은 **한국어(ko), 영어(en), 일본어(ja)**만 지원하며 세 언어를 섞을 수 있습니다.
연주곡/BGM에는 가사 언어를 요구하지 않습니다. 대화 언어와 노래 언어도 구분합니다.
J-pop 전용이 아닙니다. 팝·록·재즈·전자음악·힙합·시네마틱·라틴 등 비배제 장르와 일반 음악이론을 활용합니다.
중국어·광둥어, 중국풍 작사/작곡, 중국 전통악기 편성은 제작 범위에서 제외했습니다. 후속 개발 대기 항목도 아닙니다.
지원하지 않는 언어를 요청받았다고 임의로 번역하거나 다른 팩을 설치하지 않습니다.

**중국어로 적힌 일반 화성학과 중국 음악 제작은 다릅니다.** 범용 이론은 유지하고, 일본어 가사의 한자를 중국어로 오인해 제거하지 않습니다.

## 스킬은 하나, 지식은 필요한 부분만

| 작업 | 참고자료 |
|---|---|
| 화음·보이싱·텐션·전조 | [화성](plugins/music-producer-kit/skills/music-producer/references/harmony.md) |
| 흥얼거림·동기 발전·노래/루프 구조 | [멜로디와 구조](plugins/music-producer-kit/skills/music-producer/references/melody-form.md) |
| 속도·밀도·킥/베이스·스윙·시간 단위 | [리듬](plugins/music-producer-kit/skills/music-producer/references/rhythm.md) |
| 역할·음역·레이어·대선율·음원 선택 | [텍스처와 악기](plugins/music-producer-kit/skills/music-producer/references/texture-instruments.md) |
| 가사 의도·구조·이미지·운율 | [작사](plugins/music-producer-kit/skills/music-producer/references/lyric-craft.md) |
| 음절·모라·음표 연결과 혼합 언어 | [공통 연결법](plugins/music-producer-kit/skills/music-producer/references/prosody.md) |
| 한국어 발음과 가창 배치 | [한국어](plugins/music-producer-kit/skills/music-producer/references/lyrics-korean.md) |
| 영어 강세와 가창 배치 | [영어](plugins/music-producer-kit/skills/music-producer/references/lyrics-english.md) |
| 일본어 읽기·모라와 가창 배치 | [일본어](plugins/music-producer-kit/skills/music-producer/references/lyrics-japanese.md) |
| 가이드·녹음·합성·표현·코러스 | [보컬 제작](plugins/music-producer-kit/skills/music-producer/references/vocal-production.md) |

전부 순서대로 읽지 않습니다. 맡긴 작업과 보호할 대상을 구분하고 필요한 자료만 선택합니다.
전조·비대칭·후렴 변경·피치 오류·타이밍 흔들림을 모든 곡에 강제하지 않습니다.
[제작 스킬](plugins/music-producer-kit/skills/music-producer/SKILL.md) · [지식 이관 기록](docs/knowledge-curation.md)

## 원본 독립성과 범위 제한

두 원본의 **47개 모듈/121개 파일**을 고정 커밋 그대로 보관했습니다. 참고문서·예외·예제·스키마·LICENSE/NOTICE도 포함합니다.
원본 링크는 출처이지 설치·작업 의존성이 아닙니다. 다운로드, 원격 대체, submodule이나 자동 업데이트도 없습니다.
기본 제작용 조회 목록은 **42개 모듈**입니다. 중국 특화 5개 모듈과 중국 민속악기 전용 파일은 기본 목록·조회·목차·검색에서 제외됩니다.
원본 백업 자체는 훼손하지 않습니다. 명시적인 유지관리용 archive audit과 전체 해시 검증은 가능하지만 제작 범위를 우회하는 용도가 아닙니다.
이것은 모듈/파일 단위 구분입니다. 범용 원문에 섞인 중국 사례까지 문장 단위로 전부 자동 제거했다는 뜻은 아닙니다.
[로컬 지식 안내](plugins/music-producer-kit/library/README.md) · [원본 검증 기록](docs/SOURCE_SNAPSHOT_REPORT.json)

## 실제 실행 도구

JSON 음표에서 MIDI 생성, 다시 읽기, 한 트랙의 지정 구간 음표 교체를 지원합니다.
원본 SHA·원본 파일·범위 밖 이벤트를 보호합니다. 미지원 페달, 동일 음의 모호한 겹침, 수정 경계를 가로지르는 음은 명시적으로 거절합니다.
[4마디 화성 예제](plugins/music-producer-kit/skills/music-producer/examples/harmony-study.json)는 독립 화성/베이스 트랙의 실행 검증 자료입니다. 완성곡이나 청취 품질 증거가 아닙니다.

## 설치와 확인

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

지원되는 Plugins 화면의 설치, 실제 스킬 활성화, Ableton 연결은 별도 단계입니다.
[로컬 설치·검증 안내](docs/local-smoke-test.md)를 따르세요. 원본 두 스킬팩을 추가 설치할 필요가 없습니다.

## 개발·검증

Python 3.12+와 새 가상환경을 사용합니다.

```text
python -m pip install -r plugins/music-producer-kit/requirements.txt
python tools/check.py
python -m unittest discover -s tests -v
python tools/check.py --package dist/music-producer-kit.zip
```

지식 탐색은 표준 라이브러리만 사용합니다. 별도 서버나 의존성을 추가하지 않았습니다.
검사는 파일·검색 경계·배포·MIDI를 검증합니다. 행동 시나리오 20개는 정의만 되었으며 실제 Codex 실행 결과가 아닙니다.
원어민 발음·가창 자연스러움·음악 품질·Live 연동은 테스트 개수로 증명하지 않습니다. 관측 결과는 [STATUS](docs/STATUS.md)에 적습니다.

## 작업 연속성과 경계

[요구사항](docs/requirements.md) · [선별 기록](docs/source-selection.md) · [전체 보존 목록](docs/upstream-inventory.json)

개발자는 AGENTS.md와 STATUS를 먼저 읽고 변경·검증·남은 일을 매 세션 기록합니다.
도구는 Live Set 생성기, 오디오 렌더러, Melodyne/Splice 컨트롤러 또는 보컬 합성기가 아닙니다.
개인 녹음, 유료 샘플, 미공개 곡, 인증정보, 실제 로컬 경로는 배포하지 않습니다. 구매·크레딧·외부 업로드를 자동 승인하지 않습니다.

## 출처·라이선스

[NOTICE](plugins/music-producer-kit/NOTICE.md)를 확인하세요.
보관본은 원래 LICENSE/NOTICE와 기존 인용을 유지합니다. 제3자 서적·번역·가사를 우리 라이선스로 재허가하지 않습니다.
프로젝트 자체의 공개 라이선스는 아직 소유자가 선택하지 않았습니다.
