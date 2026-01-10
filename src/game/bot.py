import random
import time

from game.fighters import IDLE, PUNCH, KICK, Fighter
from game.actions import Actions

class FighterAI(Fighter):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.last_action_time = time.time()
        self.last_attack_time = time.time()

    def random_movement(self):
        if time.time() - self.last_move_time > random.uniform(1, 2):
            move_direction = random.choice([-1, 1]) #`-1 for left, 1 for right
            self.rect.x += move_direction * self.speed
            self.last_move_time = time.time()

    def random_attack(self):
        if time.time() - self.last_attack_time > random.uniform(2, 3):
            attack_type = random.choice([PUNCH, KICK, IDLE])
            self.set_action(attack_type)
            self.attack_timer = random.randint(10, 20)
            self.attacking = True
            self.last_attack_time = time.time()

    def update(self, actions: Actions, target: Fighter):
        self.random_movement()
        self.random_attack()
        self.movex(actions, target)
        self.movey(actions)  # Use vertical movement logic from parent class
        self.handle_attack(actions)  # Use attack handling from parent class