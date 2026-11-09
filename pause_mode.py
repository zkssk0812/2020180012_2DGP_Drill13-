from pico2d import *
import game_framework
import game_world

image = None


def init():
    global image
    image = load_image('pause.png')


def finish():
    global image
    del image


def update():
    pass  # 일시정지 중에는 게임 월드를 업데이트하지 않음


def render():
    clear_canvas()
    game_world.render()  # 멈춘 플레이 화면을 그대로 보여줌
    image.draw(400, 300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_mode()


def pause():
    pass


def resume():
    pass
