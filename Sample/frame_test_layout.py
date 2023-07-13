#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameTestLayout

layoutについての検証を行う
"""
import logging
import tkinter as tk
from tkinter import ttk

from tkblock.block_service import *

from ini_parser import Config
from tkblock.logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestLayout:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame = None

    def get_frame(self) -> BlockFrame:
        return self.frame

    def create(self) -> None:
        self.frame = BlockService.create_frame("test_layout", row=9, col=12)
        # left
        BlockService.create_label(
            self.frame, 0, 1, 0, 1, text="left_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                0,
                1,
                text=f"left{index}",
                pad_left=0.1 * index,
            )
        # right
        BlockService.create_label(
            self.frame, 0, 1, 1, 2, text="right_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                1,
                2,
                pad_right=0.1 * index,
                text=f"right{index}",
            )
        # up
        BlockService.create_label(
            self.frame, 0, 1, 2, 3, text="up_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                2,
                3,
                pad_up=0.1 * index,
                text=f"up{index}",
            )
        # down
        BlockService.create_label(
            self.frame, 0, 1, 3, 4, text="down_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                3,
                4,
                pad_down=0.1 * index,
                text=f"down{index}",
            )
        # left_right
        BlockService.create_label(
            self.frame, 0, 1, 4, 5, text="right_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                4,
                5,
                pad_left=0.1 * index,
                pad_right=0.1 * index,
                text=f"lr{index}",
            )
        # up_down
        BlockService.create_label(
            self.frame, 0, 1, 5, 6, text="ud_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                5,
                6,
                pad_left=0.1 * index,
                pad_right=0.1 * index,
                text=f"ud{index}",
            )
        # left_right_up_down_1
        BlockService.create_label(
            self.frame, 0, 1, 6, 7, text="lrud1_pad", anchor=tk.CENTER
        )
        for index in range(10):
            BlockService.create_button(
                self.frame,
                index + 1,
                index + 2,
                6,
                7,
                pad_left=0.1 * index,
                pad_right=0.1 * index,
                text=f"lrud1_{index}",
            )
        # left_right_up_down_2
        BlockService.create_label(
            self.frame, 0, 1, 7, 9, text="lrud2_pad", anchor=tk.CENTER
        )
        for index in range(4):
            BlockService.create_button(
                self.frame,
                2 * index + 1,
                2 * index + 3,
                7,
                9,
                pad_left=0.2 * index,
                pad_right=0.2 * index,
                pad_up=0.2 * index,
                pad_down=0.2 * index,
                text=f"lrud2_{index}",
            )
