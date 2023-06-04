import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from Scoreboard import Scoreboard
# from stars import Stars


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Allen Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_ufos()
        self.game_stats = GameStats(self)
        self.sb = Scoreboard(self)
       # self.stars = Stars(self)
        self.game_active = False

        self.play_button = Button(self, 'Play Alien Invasion')

    def run_game(self):
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._check_bullet_alien_collision()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_ESCAPE:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.game_stats.score += self.settings.alien_points * \
                    len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_ufos()
            self.settings.increase_speed()

            self.game_stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        self._check_ufo_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _create_ufos(self):
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height+80
        while current_y < (self.settings.screen_height -
                           6 * alien_height):
            while current_x < (self.settings.screen_width -
                               2*alien_width):
                self._create_aliens(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2*alien_height

    def _create_aliens(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_ufo_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_ufo_direction()
                break

    def _change_ufo_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.ufo_drop_speed

        self.settings.ufo_direction *= -1

    def _ship_hit(self):
        if self.game_stats.ships_left > 1:
            self.game_stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()

            self._create_ufos()
            self.ship.center_ship()

            sleep(1.0)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):

        if not self.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings()
                self.game_active = True

                self.bullets.empty()
                self.aliens.empty()

                self.game_stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()

                self._create_ufos()
                self.ship.center_ship()

                pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
