#!/usr/bin/env python
# -*- coding: utf-8 -*-

import easyvideo
import easyvideo.image
from easyvideo.screen import Screen
from easyvideo.animation import FrameSet
from easyvideo.animation import Animations
import easyvideo.animation
import easyvideo.sprites

# This import should be replaced for other like "easyevents"
# or something like that.
import pygame

import actors
import hordes

def main():
    screen = Screen()
    screen.background.draw(easyvideo.image.load(
        'data/background_test.jpg'), (0, 0))

    pelusa_frames = FrameSet('data/pelusilla_01.png',
                             'data/pelusilla_02.png',
                             'data/pelusilla_03.png',
                             'data/pelusilla_04.png',
                             'data/pelusilla_05.png',
                             'data/pelusilla_06.png',
                             'data/pelusilla_07.png',
                             'data/pelusilla_08.png')
    bullet_frames = FrameSet('data/bullet_test.png')
    
    pelusa_actions = Animations()        
    pelusa_actions.add('MOVE_LEFT',
                       pelusa_frames.animation_loop, 6)
    pelusa_actions.add('MOVE_RIGHT',
                       pelusa_frames.horizontal_flip.animation_loop, 6)
    pelusa_actions.add('DYING',
                       pelusa_frames.animation, 6)

    bullet_actions = Animations()
    bullet_actions.add('MOVE_UP',
                       bullet_frames.animation)
    # bullet_actions.add('MOVE_DOWN',
    #                    bullet_frames.vertical_flip.animation)
    bullet_actions.add('MOVE_DOWN',
                       bullet_frames.animation)
    bullet_actions.add('DYING',
                       bullet_frames.animation)


    horde = hordes.Uniform(animations=pelusa_actions,
                           factory=actors.PelusaZombie)
    horde.new_member((0, 100)).speed_x = 2
    horde.new_member((400, 300)).speed_x = 2

    singles = hordes.Alone(animations=pelusa_actions,
                           factory=actors.PelusaZombie)
    singles.new_member((600, 100)).speed_x = 2

    player_shots = hordes.Shot(animations=bullet_actions,
                               factory=actors.Bullet)
    player_shots.add_targets(singles)
    player_shots.add_targets(horde)
    
    player = hordes.Player(animations=pelusa_actions,
                           factory=actors.PelusaZombie)
    player.new_member((512, 600), pelusa_actions).speed_x = 3
    player.set_weapon(player_shots)
    
    for frame in range(500):
        # pygame should be replaced for a higher level library
        for event in pygame.event.get():
            player.handle_event(event)

        screen.playfield.clear()
        horde.draw(screen.playfield.layer)
        horde.update()
        singles.draw(screen.playfield.layer)
        singles.update()
        player.draw(screen.playfield.layer)
        player.update()
        player_shots.draw(screen.playfield.layer)
        player_shots.update()
        screen.update()
        
if __name__ == '__main__':
    main()
