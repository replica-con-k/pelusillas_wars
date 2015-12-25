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
import game

def main():
    main_game = game.Game()
    horde = main_game.new_enemy(actors.PelusaZombie)
    horde.new_member((0, 100)).speed_x = 2
    horde.new_member((400, 300)).speed_x = 2
    main_game.add_horde(horde)
    player = main_game.new_player()
    easyevents.ROOT.add_subscriptor('PLAYER', player)
    player.new_member((512, 600), main_game.player).speed_x = 3
    
    main_game.start()
        
if __name__ == '__main__':
    main()
