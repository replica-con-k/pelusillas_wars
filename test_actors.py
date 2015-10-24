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
    pelusa_actions = Animations()        
    pelusa_actions.add('MOVE_LEFT',
                       pelusa_frames.animation_loop, 6)
    pelusa_actions.add('MOVE_RIGHT',
                       pelusa_frames.horizontal_flip.animation_loop, 6)


    horde = hordes.Uniform(factory=actors.PelusaZombie)
    horde.new_member((0, 100), pelusa_actions).speed_x = 2
    horde.new_member((400, 300), pelusa_actions).speed_x = 2

    singles = hordes.Alone(factory=actors.PelusaZombie)
    singles.new_member((600, 100), pelusa_actions).speed_x = 2

    player = hordes.Player(factory=actors.PelusaZombie)
    player.new_member((512, 600), pelusa_actions).speed_x = 3
    
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
        screen.update()
        
if __name__ == '__main__':
    main()
