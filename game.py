#!/usr/bin/env python
# -*- coding: utf-8 -*-

import easyvideo
import easyvideo.image
from easyvideo.screen import Screen
from easyvideo.animation import FrameSet
from easyvideo.animation import Animations
import easyvideo.animation
import easyvideo.sprites

import easyevents

import actors
import hordes


class Game(object):
    scr = Screen()
    _shot_sprite = FrameSet('data/bullet_test.png')
    _shot_actions = Animations()
    _shot_actions.add('MOVE_UP', _shot_sprite.animation)
    _shot_actions.add('MOVE_DOWN', _shot_sprite.vertical_flip.animation)
    _shot_actions.add('DYING', _shot_sprite.animation)
    player_shots = hordes.Shot(animations=_shot_actions,
                               factory=actors.Bullet)

    _enemy_sprite = FrameSet('data/pelusilla_01.png',
                             'data/pelusilla_02.png',
                             'data/pelusilla_03.png',
                             'data/pelusilla_04.png',
                             'data/pelusilla_05.png',
                             'data/pelusilla_06.png',
                             'data/pelusilla_07.png',
                             'data/pelusilla_08.png')
    _enemy_actions = Animations()        
    _enemy_actions.add('MOVE_LEFT',
                       _enemy_sprite.animation_loop, 6)
    _enemy_actions.add('MOVE_RIGHT',
                       _enemy_sprite.horizontal_flip.animation_loop, 6)
    _enemy_actions.add('DYING',
                       _enemy_sprite.animation, 6)
    
    def __init__(self):
        self.in_game = True
        self.players = []
        self.current_hordes = []
        
    player_shots.add_targets(singles)
    player_shots.add_targets(horde)

    def set_background(self, background):
        self.scr.draw(background, (0, 0))

    def add_player(self, player):
        player.set_weapon(self.player_shots)
        self.players.append(player)

    def add_horde(self, horde):
        self.player_shots.add_targets(horde)
        self.current_hordes(horde)

    def start(self):
        while self.in_game:
            easyevents.process_events()
            self.scr.playfield.clear()
            for horde in self.current_hordes:
                horde.draw(self.scr.playfield.layer)
                horde.update()
            for player in self.players:
                player.draw(self.scr.playfield.layer)
                player.update()
            self.player_shots.draw(self.scr.playfield.layer)
            self.player_shots.update()
            self.scr.update()

    def new_enemy(self, factory):
        return hordes.Uniform(animations=self._enemy_actions,
                              factory=factory)

    def new_player(self):
        return hordes.Player(animations=self._enemy_actions,
                             factory=actors.PelusaZombie)

    @property
    def player(self):
        return self._enemy_actions
