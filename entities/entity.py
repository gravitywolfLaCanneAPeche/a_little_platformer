from textures import get_a_texture


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile.rect):
            hit_list.append(tile)
    return hit_list

class Entity:

    def __init__(self, game, x, y, animation_number, attack, velocity, orientation='right', default_animation=0,
                 player=False):

        self.player = player
        self.attack = attack
        self.velocity = velocity

        self.animations = get_a_texture(animation_number)
        self.actual_animation = self.animations[default_animation]

        self.image = self.actual_animation[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(x=x, y=y)

        self.movement = [0, 0]

        self.air_timer = 0
        self.y_momentum = 0

        self.collisions = {
            'top': False,
            'bottom': False,
            'right': False,
            'left': False
        }

        self.game = game

        self.orientation = orientation
        self.animation_cool_down = 6
        self.animation_time_after_last_frame = 0
        self.animation_key = 0

    def apply_gravity(self):

        self.movement[1] += self.y_momentum
        self.y_momentum += 0.02
        if self.y_momentum > 3:
            self.y_momentum = 3

        if self.collisions['bottom']:
            self.y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

        if self.collisions['top']:
            self.movement[1] = 1

        if self.movement[1] > 5:
            self.movement[1] = 5

    def jump(self):
        if self.air_timer == 0:
            self.movement[1] = -5
            self.air_timer = 1

    def animation(self):

        if self.animation_time_after_last_frame >= self.animation_cool_down:

            self.image = self.actual_animation[self.animation_key]
            self.animation_key += 1

            if self.animation_key >= len(self.actual_animation):
                self.animation_key = 0

            self.animation_time_after_last_frame = 0

        else:

            self.animation_time_after_last_frame += 1

    def change_animation(self, animations_key):

        if not self.animations[animations_key] == self.actual_animation:
            self.actual_animation = self.animations[animations_key]
            self.animation_key = 0

    def move(self):

        tiles = self.game.all_blocks

        self.collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.move_ip(self.movement[0], 0)
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[0] > 0 and tile.stopping_sides.get('left'):
                self.rect.right = tile.rect.left
                self.collisions['right'] = True
            elif self.movement[0] < 0 and tile.stopping_sides.get('right'):
                self.rect.left = tile.rect.right
                self.collisions['left'] = True
        self.rect.move_ip(0, self.movement[1])
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[1] > 0 and tile.stopping_sides.get('top') and self.rect.bottom <= abs(tile.rect.top) + 5:
                self.rect.bottom = tile.rect.top
                self.collisions['bottom'] = True
                if str(tile.__class__) == '<class \'blocks.can_broken_wood.CanBrokenWoodPlatform\'>' and self.player:
                    tile.start_timer()
            elif self.movement[1] < 0 and tile.stopping_sides.get('bottom'):
                self.rect.top = tile.rect.bottom
                self.collisions['top'] = True

    def update(self):

        self.apply_gravity()
        self.animation()

        self.move()

    def remove(self):

        if not self.player:
            self.game.all_monsters.remove(self)

        else:
            self.game.entities.remove(self)
