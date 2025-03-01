class Unit:
    def __init__(self, hp, speed, damage, sprite, *coordinates):
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.sprite = sprite
        self.x, self.y = coordinates


    def move(self, direction, step):
        d_x = 0
        d_y = 0

        if direction == "up":
            d_y = -step

        elif direction == "down":
            d_y = step

        elif direction == "left":
            d_x = -step

        elif direction == "right":
            d_x = step

        self.x += d_x
        self.y += d_y


    def update_position(self):
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y
