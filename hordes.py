#!/usr/bin/env python
# -*- coding: utf-8 -*-

from easyvideo.sprites import Group

# This import should be replaced for other like "easyevents"
# or something like that.
import pygame

class Horde(object):
    def __init__(self, spr_group=None, factory=None):
        self.__group = Group() if spr_group is None else spr_group
        self.__elements = []
        self.__factory = factory

    def new_member(self, *args):
        if self.__factory is not None:
            element = self.__factory(*args)
            self.add(element)
        return element

    @property
    def elements(self):
        return self.__elements
    
    def add(self, actor):
        self.__elements.append(actor)
        self.__group.add(actor)
        actor.horde = self

    def left(self, actor):
        try:
            actor_idx = self.__elements.index(actor)
            del(self.__elements[actor_idx])
        except ValueError:
            pass
        finally:
            if self.__group.has(actor):
                self.__group.remove(actor)
            actor.horde = Alone()
        
    def notify_state_changed(self, new_state, actor=None):
        '''actor: Actor() who change the state'''
        pass

    def handle_event(self, event):
        pass

    def draw(self, layer):
        self.__group.draw(layer)

    def update(self):
        self.__group.update()
        

class Alone(Horde):
    def __init__(self, spr_group=None, factory=None):
        Horde.__init__(self, spr_group, factory)

    def notify_state_changed(self, new_state, actor):
        actor.change_state(new_state)


class Uniform(Horde):
    def __init__(self, spr_group=None, factory=None):
        Horde.__init__(self, spr_group, factory)

    def notify_state_changed(self, new_state, actor=None):
        for element in self.elements:
            element.change_state(new_state)


class Player(Uniform):
    def __init__(self, spr_group=None, factory=None):
        Uniform.__init__(self, spr_group, factory)
        
    def handle_event(self, event):
        # pygame should be replaced for a higher level library
        if event.type == pygame.KEYUP:
            self.notify_state_changed('STOP')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.notify_state_changed('MOVE_LEFT')
            elif event.key == pygame.K_RIGHT:
                self.notify_state_changed('MOVE_RIGHT')
                
