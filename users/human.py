from users.base_user import User
import pygame


class Human(User):
    def __init__(self, config_path):
        class_name = type(self).__name__
        params = dict()
        params['game_display'] = True
        super(Human, self).__init__(config_path, params, class_name)
        self.running = True

    def get_target_pile(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                target_num = int(pygame.key.name(event.key))
                target_pile = self.game_controller.game_model.get_pile(target_num)
                return target_pile
            if event.type == pygame.QUIT:
                self.running = False
        return None

    def is_running(self):
        return self.running