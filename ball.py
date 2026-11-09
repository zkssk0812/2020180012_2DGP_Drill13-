from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    IMAGE_FILES = {
        'small': 'ball21x21.png',
        'big': 'ball41x41.png',
    }
    images = {}  # 크기별 이미지 캐시 (한 번만 로드)

    def __init__(self, x, y, velocity, size='small'):
        if size not in Ball.images:
            Ball.images[size] = load_image(Ball.IMAGE_FILES[size])
        self.image = Ball.images[size]
        self.x, self.y = x, y
        self.velocity = velocity

    def update(self):
        self.x += self.velocity
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
