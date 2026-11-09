from pico2d import *
import game_framework
import game_world
import play_mode
import pause_mode

image = None

ITEM_KEYS = {
    SDLK_0: 0,  # 공 없음
    SDLK_1: 1,  # 작은 공
    SDLK_2: 2,  # 큰 공
}


def init():
    global image
    image = load_image('item_select.png')


def finish():
    global image
    del image


def update():
    game_world.update()  # 인벤토리 중에도 애니메이션과 날아가는 공은 계속 진행


def render():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key in ITEM_KEYS:
            play_mode.boy.select_item(ITEM_KEYS[event.key])
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_mode(pause_mode)  # 일시정지 해제 시 인벤토리로 복귀
        # 그 외 키(방향키, SPACE)는 무시 → 플레이어 입력 차단


def pause():
    pass


def resume():
    pass
