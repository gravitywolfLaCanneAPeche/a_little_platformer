import pygame
from entities.player import Player
from maps import get_all_maps
from textures import init_textures
from blocks.stone import Stone
from blocks.wood import WoodPlatform
from blocks.can_broken_wood import CanBrokenWoodPlatform
from entities.monster import FireMonster
from random import randint


class Game:

    def __init__(self, screen, clock):

        init_textures()

        self.pressed = {}
        self.scroll = [0, 0]

        self.screen = screen
        self.surface = pygame.surface.Surface((screen.get_width() // 2, screen.get_height() // 2))

        self.entities = []

        self.player = Player(self, 200, 0, 2)
        self.entities.append(self.player)

        self.all_monsters = []
        self.entities.append(self.all_monsters)

        self.maps = get_all_maps()
        self.all_can_broken_wood_platforms = []
        self.all_blocks = []
        self.load_map(0)

        self.position_marker = pygame.rect.Rect(0, 0, 32, self.surface.get_height())

        self.scrolling_elements = [self.entities, self.all_blocks, self.position_marker]

        self.clock = clock
        for i in range(3):
            x = randint(-165, 165)
            self.all_monsters.append(FireMonster(self, x, 0, 'left'))

    def run(self, run):

        run = self.handling_events(run)
        self.update_elements()
        self.display_elements()

        self.clock.tick(60)

        return run

    def update_elements(self):

        for block in self.all_blocks:
            if isinstance(block, CanBrokenWoodPlatform):
                block.check_timer()

        for entity in self.entities:

            if not type(entity) == list:

                entity.update()

            else:

                for sub_entity in entity:
                    sub_entity.update()

        self.player.check_movements(self.pressed)
        self.player.little_jump(5, self.pressed)
        self.scroll_map()

    def display_elements(self):

        self.screen.fill((0, 150, 220))
        self.surface.fill((0, 150, 220))

        for stone in self.all_blocks:
            self.surface.blit(stone.image, (stone.rect.x - self.scroll[0], stone.rect.y - self.scroll[1]))

        self.blit_entities()

        self.player.update_health_bar(self.scroll)

        surf = self.surface

        if self.screen.get_width() >= 600:
            surf = pygame.transform.scale(self.surface, (self.surface.get_width() * 2, self.surface.get_height() * 2))

        self.screen.blit(surf, (0, 0))

        pygame.display.update()

    def handling_events(self, run):
        self.pressed = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.VIDEORESIZE:

                if self.screen.get_width() < 600:
                    self.surface = pygame.transform.scale(self.surface,
                                                          (self.surface.get_width(), self.screen.get_height()))

                else:
                    self.surface = pygame.transform.scale(self.surface,
                                                          (self.surface.get_width(), self.screen.get_height() // 2))

                pygame.display.update()

            elif event.type == pygame.VIDEOEXPOSE:

                self.screen.fill((0, 0, 0))

        return run

    def load_map(self, map_number):

        real_map = self.maps[map_number]
        real_map.reverse()

        y = 10
        for row in real_map:
            x = 0
            for tile in row:
                if tile == 1:
                    self.all_blocks.append(Stone((x * 32, y * 32)))
                if tile == 2:
                    self.all_blocks.append(WoodPlatform((x * 32, y * 32)))
                if tile == 3:
                    self.all_blocks.append(CanBrokenWoodPlatform((x * 32, y * 32)))
                x += 1

            y -= 1

    def scroll_map(self):

        self.scroll[0] += (self.player.rect.x - self.scroll[0] -
                           self.surface.get_width() // 2 - self.player.rect.width // 2) // 20
        self.scroll[1] += (self.player.rect.y - self.scroll[1] -
                           self.surface.get_height() // 2 - self.player.rect.height // 2) // 20

    def blit_entities(self):

        for entity in self.entities:

            if not type(entity) == list:

                if entity.orientation == 'right':

                    self.surface.blit(entity.image, (entity.rect.x - self.scroll[0],
                                                     entity.rect.y - 16 - self.scroll[1]))

                else:
                    self.surface.blit(pygame.transform.flip(entity.image, True, False),
                                      (entity.rect.x - self.scroll[0], entity.rect.y - 16 - self.scroll[1]))

            else:

                for sub_entity in entity:

                    if sub_entity.orientation == 'right':

                        self.surface.blit(sub_entity.image,
                                          (sub_entity.rect.x - self.scroll[0], sub_entity.rect.y - 16 - self.scroll[1]))

                    else:
                        self.surface.blit(pygame.transform.flip(sub_entity.image, True, False),
                                          (sub_entity.rect.x - self.scroll[0], sub_entity.rect.y - 16 - self.scroll[1]))
