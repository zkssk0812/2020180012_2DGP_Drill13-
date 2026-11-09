# PSD - Inventory Mode 추가

## 1. 목표
- 플레이 중 인벤토리 화면(`inventory_mode`)을 열어 발사할 공을 선택한다.
- 인벤토리 화면 이미지: `item_select.png`
- 선택 키
  | 키 | 효과 | 이미지 |
  |----|------|--------|
  | `0` | 공을 발사하지 않음 (Clear) | - |
  | `1` | 작은 공 발사 | `ball21x21.png` |
  | `2` | 큰 공 발사 | `ball41x41.png` |

## 2. 요구 사항
1. `play_mode`에서 `I` 키를 누르면 `inventory_mode`를 push 한다.
2. 인벤토리 모드 중에는 **플레이어 입력(좌/우 이동, SPACE 공 발사)만 막는다.**
3. 인벤토리 모드 중에도 **게임 월드 업데이트(소년 애니메이션, 날아가는 공)는 계속** 진행한다.
4. `0` / `1` / `2` 키로 아이템을 고르면 선택이 반영되고 플레이 모드로 돌아간다.
   `I` 키를 다시 누르면 선택 없이 닫는다.
5. 플레이 모드 복귀 시 실제 키보드 상태로 방향키를 다시 맞춘다(`sync_keys`).
6. 기본 아이템은 기존 동작과 같도록 작은 공(1)으로 한다.

## 3. 설계
### ball.py
- `Ball(x, y, velocity, size)` : `size`가 `'small'`/`'big'`에 따라 이미지를 선택.
- 이미지는 클래스 변수 딕셔너리에 캐싱하여 한 번만 로드.

### boy.py
- `self.ball_item` (0: 없음, 1: 작은 공, 2: 큰 공) 추가, 기본값 1.
- `select_item(item)` 메서드 추가.
- `fire_ball()` : `ball_item == 0`이면 발사하지 않음, 1/2이면 해당 크기의 공 생성.
- `release_keys()` : 눌린 방향키를 모두 해제하여 달리기를 멈추고 IDLE 애니메이션으로 전환
  (입력이 막힌 상태에서 계속 달려가지 않도록).

### inventory_mode.py (신규)
- `init` : `item_select.png` 로드
- `update` : `game_world.update()` 호출 → 애니메이션 유지
- `render` : 게임 월드를 그린 뒤 인벤토리 이미지를 위에 그림
- `handle_events` : `0`/`1`/`2` → `play_mode.boy.select_item()` 후 `pop_mode()`,
  `I` → `pop_mode()`, 그 외 키는 무시(플레이어 입력 차단)

### play_mode.py
- `I` 키 → `game_framework.push_mode(inventory_mode)`
- `pause()` → `boy.release_keys()`
- `resume()` → `boy.sync_keys()` (기존 유지)

## 4. 개발 절차 (커밋 단위)
1. `psd.md` 작성 및 커밋
2. `Ball`에 작은 공 / 큰 공 크기 지원 추가
3. `Boy`에 아이템 선택(`ball_item`, `select_item`) 및 발사 로직 반영
4. `inventory_mode.py` 추가
5. `play_mode`에 인벤토리 모드 진입(`I`) 및 pause/resume 처리 연결

## 5. 검증
- `I` → 인벤토리 이미지가 게임 화면 위에 표시되고 소년 애니메이션/날아가는 공이 계속 움직이는지
- 인벤토리 중 방향키/SPACE 무반응 확인
- `0` 선택 후 SPACE → 공 발사 안 됨
- `1` 선택 후 SPACE → 작은 공, `2` 선택 후 SPACE → 큰 공
- 방향키를 누른 채 인벤토리를 닫으면 바로 다시 달리는지
