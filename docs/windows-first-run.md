# Windows에서 첫 연결부터 실제 편집 검증까지

브라우저의 이 대화는 사용자 PC의 Ableton을 직접 볼 수 없다. 아래 작업은 Ableton이 설치된 같은 Windows의 로컬 Codex에서 실행한다.
새 기능을 더 붙이기 전에 실제 연결 상태를 확인하기 위한 시작점이다. 연결하지 않은 상태를 성공으로 기록하지 않는다.

## 로컬 Codex에 줄 요청

```text
이 music-producer-kit 저장소의 AGENTS.md, docs/STATUS.md와
plugins/music-producer-kit/skills/music-producer/references/mcp-connection.md를 읽고
내 Windows의 Codex–Ableton 첫 연결 검증을 진행해.

먼저 설치된 버전과 기존 MCP 연결을 확인해. 설정 전체나 토큰을 출력하지 말고,
연결이 있으면 제공된 mcp_probe.py로 실제 도구 규격을 비공개 작업 폴더에 기록해.
설치나 설정 변경이 필요하면 필요한 변경만 설명하고, 승인된 것만 적용해.
MCP가 없으면 기능 수보다 실제 Live 버전, Arrangement, MIDI 읽기/쓰기,
악기/샘플 로딩, 저장·재열기 지원을 확인해서 하나를 제안해.

기존 곡은 건드리지 마. 새 빈 테스트 Set을 쓸 수 있게 된 뒤
원본 4마디 harmony-study.json의 화성과 베이스를 편집 가능한 트랙으로 만들고,
베이스 2마디만 수정한 후 다른 부분이 그대로인지 확인해.
저장·재열기까지 실제로 확인하고, 자동으로 안 되는 단계는 따로 표시해.

샘플 추가 구매, Splice 크레딧 사용, 외부 업로드, 관리자 권한 변경은 하지 마.
내 음악 취향·장르·보컬 범위를 처음부터 다시 물어보지 마.
필요한 로컬 경로나 빈 Set 확인처럼 지금 환경에서만 알 수 있는 것만 물어봐.
검증 결과와 다음 작업은 공개 레포가 아닌 비공개 작업 폴더에 남겨.
```

## 단계별 결과를 따로 확인

| 확인한 것 | 아직 증명되지 않는 것 |
|---|---|
| 플러그인/스킬을 읽었다 | MCP 연결 또는 Live 접근 |
| 진단 도구가 도구 목록을 받았다 | 실제 Codex에서의 노출·권한, 열린 Live Set |
| Live 상태를 읽었다 | MIDI/악기 작성·저장 지원 |
| 편집 가능한 4마디를 만들었다 | 한 곡 자동 완성이나 음악 품질 |
| 저장하고 다시 열었다 | 누락된 외부 악기·샘플이 없다는 것과 부분 수정 보호 |

진단 보고서는 의도적으로 `live_verified=false`와 `save_reopen_verified=false`를 유지한다.
서버가 제공하는 도구 규격과 실제 DAW 작업의 성공은 다른 증거이기 때문이다.
실제 단계의 검증은 비공개 session.md에 호출·결과·남은 제한을 적고 저장한 프로젝트와 함께 유지한다.

의존성 설치에는 네트워크가 필요할 수 있지만 기존 음악 지식은 계속 로컬 선별본을 쓴다.
중국 특화 원본이나 이전 전체 스냅샷을 복구하는 단계는 없다.
설치·플러그인 자체 확인은 [기존 로컬 검사](local-smoke-test.md), 구체적인 연결 절차는 [MCP 연결 안내](../plugins/music-producer-kit/skills/music-producer/references/mcp-connection.md)를 따른다.
