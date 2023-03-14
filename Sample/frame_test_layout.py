#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameTestLayout

layoutについての検証を行う
"""
import logging
import tkinter as tk
from tkinter import ttk

from tkblock.block_service import (
    BlockFrameBase,
    BlockService,
)

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestLayout:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def create(self) -> None:
        self.frame = BlockService.create_frame("test_layout", row=9, col=12)
        # left
        label_left: ttk.Label = ttk.Label(self.frame, text="left_pad", anchor=tk.CENTER)
        label_left.layout = BlockService.layout(0, 1, 0, 1)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"left{index}")
            button.layout = BlockService.layout(
                index + 1, index + 2, 0, 1, pad_left=0.1 * index
            )
            button.bind("<Button-1>", None)
        # right
        label_right: ttk.Label = ttk.Label(
            self.frame, text="right_pad", anchor=tk.CENTER
        )
        label_right.layout = BlockService.layout(0, 1, 1, 2)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"right{index}")
            button.layout = BlockService.layout(
                index + 1, index + 2, 1, 2, pad_right=0.1 * index
            )
            button.bind("<Button-1>", None)
        # up
        label_up: ttk.Label = ttk.Label(self.frame, text="up_pad", anchor=tk.CENTER)
        label_up.layout = BlockService.layout(0, 1, 2, 3)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"up{index}")
            button.layout = BlockService.layout(
                index + 1, index + 2, 2, 3, pad_up=0.1 * index
            )
            button.bind("<Button-1>", None)
        # down
        label_down: ttk.Label = ttk.Label(self.frame, text="down_pad", anchor=tk.CENTER)
        label_down.layout = BlockService.layout(0, 1, 3, 4)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"down{index}")
            button.layout = BlockService.layout(
                index + 1, index + 2, 3, 4, pad_down=0.1 * index
            )
            button.bind("<Button-1>", None)
        # left_right
        label_lr: ttk.Label = ttk.Label(self.frame, text="right_pad", anchor=tk.CENTER)
        label_lr.layout = BlockService.layout(0, 1, 4, 5)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"lr{index}")
            button.layout = BlockService.layout(
                index + 1,
                index + 2,
                4,
                5,
                pad_left=0.1 * index,
                pad_right=0.1 * index,
            )
            button.bind("<Button-1>", None)
        # up_down
        label_ud: ttk.Label = ttk.Label(self.frame, text="ud_pad", anchor=tk.CENTER)
        label_ud.layout = BlockService.layout(0, 1, 5, 6)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"ud{index}")
            button.layout = BlockService.layout(
                index + 1,
                index + 2,
                5,
                6,
                pad_up=0.1 * index,
                pad_down=0.1 * index,
            )
            button.bind("<Button-1>", None)
        # left_right_up_down_1
        label_lrud1: ttk.Label = ttk.Label(
            self.frame, text="lrud1_pad", anchor=tk.CENTER
        )
        label_lrud1.layout = BlockService.layout(0, 1, 6, 7)
        for index in range(10):
            button: ttk.Button = ttk.Button(self.frame, text=f"lrud1_{index}")
            button.layout = BlockService.layout(
                index + 1,
                index + 2,
                6,
                7,
                pad_left=0.1 * index,
                pad_right=0.1 * index,
                pad_up=0.1 * index,
                pad_down=0.1 * index,
            )
            button.bind("<Button-1>", None)
        # left_right_up_down_2
        label_lrud2: ttk.Label = ttk.Label(
            self.frame, text="lrud2_pad", anchor=tk.CENTER
        )
        label_lrud2.layout = BlockService.layout(0, 1, 7, 9)
        for index in range(4):
            button: ttk.Button = ttk.Button(self.frame, text=f"lrud2_{index}")
            button.layout = BlockService.layout(
                2 * index + 1,
                2 * index + 3,
                7,
                9,
                pad_left=0.2 * index,
                pad_right=0.2 * index,
                pad_up=0.2 * index,
                pad_down=0.2 * index,
            )
            button.bind("<Button-1>", None)
