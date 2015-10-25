#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import hordes
import easyvideo.screen
import easyvideo.sprites


class Actor(easyvideo.sprites.Sprite):
    def __init__(self, position, animations):
        easyvideo.sprites.Sprite.__init__(self)
        self.pos = position
        self.anims = animations.copy
        self.image = self.anims.current_frame
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.horde = None

    def change_state(self, state):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def notify_horde(self, state):
        if self.horde is not None:
            self.horde.notify_state_changed(state, self)

    def kill(self):
        easyvideo.sprites.Sprite.kill(self)
        self.horde.left(self)
        self.horde = None


class PelusaZombie(Actor):
    def __init__(self, position, animations):
        Actor.__init__(self, position, animations)
        self.__states = {
            'MOVE_LEFT': self.__move_left,
            'MOVE_RIGHT': self.__move_right,
            'DYING': self.__dying
        }
        self.change_state('MOVE_LEFT')
        self.speed_x = 1

        self.area = easyvideo.screen.get_area()

    def change_state(self, state):
        if state not in self.__states.keys():
            return
        self.__life = self.__states[state]
        self.anims.change_animation(state)
    
    def __move_left(self):
        self.rect.x -= self.speed_x
        if self.rect.x < self.area.left:
            self.notify_horde('MOVE_RIGHT')

    def __move_right(self):
        self.rect.x += self.speed_x
        if self.rect.right > self.area.right:
            self.notify_horde('MOVE_LEFT')

    def __dying(self):
        if not self.anims.more_frames:
            self.kill()
    
    def update(self):
        self.__life()
        self.image = self.anims.update()
        

class Bullet(Actor):
    def __init__(self, position, animations):
        Actor.__init__(self, position, animations)
        self.__states = {
            'MOVE_UP': self.__move_up,
            'MOVE_DOWN': self.__move_down,
            'DYING': self.__dying
        }
        self.change_state('MOVE_UP')
        self.speed = 10
        self.area = easyvideo.screen.get_area()

    def change_state(self, state):
        if state not in self.__states.keys():
            return
        self.__life = self.__states[state]
        self.anims.change_animation(state)
    
    def __move_up(self):
        self.rect.y -= self.speed
        if self.rect.bottom < self.area.top:
            self.notify_horde('DYING')

    def __move_down(self):
        self.rect.y += self.speed
        if self.rect.top > self.area.bottom:
            self.notify_horde('DYING')

    def __dying(self):
        self.kill()

    def update(self):
        self.__life()
        self.image = self.anims.update()
