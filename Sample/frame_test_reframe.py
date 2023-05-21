#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrametestReframe

Frame in Frame等のFrameに関する検証を行う
"""
import logging
import tkinter as tk
from tkinter import ttk

from tkblock.block_service import BlockFrame, BlockService

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")
DEBUG_MODE: str = "1"


class FrametestReframe:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrame = None

    def get_frame(self) -> BlockFrame:
        return self.frame

    def _create_test2_frame(self) -> None:
        """root上のBlockFrameの上のFrameの上にBlockFrameを配置する例"""
        # BlockFrame → Frame
        frame_test2: ttk.Frame = ttk.Frame(
            self.frame,
            name="main-frame_test1-frame_test2",
        )
        frame_test2.layout = BlockService.layout(6, 9, 1, 9)

        # BlockFrame → Frame → BlockFrame
        frame_test2_frame_test1: BlockFrame = BlockService.create_frame(
            "test1", col=5, row=10, root=frame_test2
        )
        frame_test2_frame_test1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # BlockFrame → Frame → BlockFrame → Label
        BlockService.create_label(frame_test2_frame_test1, 2, 3, 5, 6, name="frame_test2_frame_test1_label1", text="FB→F→FB")

    def _create_test1_frame(self) -> None:
        """root上のBlockFrameの上にBlockFrameの上にFrameを配置する例"""
        # BlockFrame → BlockFrame
        frame_test1: BlockFrame = BlockService.create_frame(
            "test1", col=5, row=10, root=self.frame
        )
        frame_test1.layout = BlockService.layout(1, 4, 1, 9)

        # BlockFrame → BlockFrame → Frame
        frame_test1_frame_test1: ttk.Frame = ttk.Frame(
            frame_test1,
            name="main-frame_test1-frame_test2",
        )
        frame_test1_frame_test1.layout = BlockService.layout(1, 4, 1, 9)

        # BlockFrame → BlockFrame → Frame → label
        frame_test1_frame_test1_label1: ttk.Label = ttk.Label(
            frame_test1_frame_test1,
            name="frame_test1_frame_test1_label1",
            text="FB→FB→F",
        )
        frame_test1_frame_test1_label1.place(relx=0.5, rely=0.5)

    def _create_dialog(self) -> None:
        # dialog設定
        toplevel = BlockService.create_toplevel(self.frame, "toplevel_BlockFrame", 500, 500, is_focus=True, is_grab=True)
        frame_test3: BlockFrame = BlockService.create_frame(
            "test3", col=10, row=10, width=500, height=500, root=toplevel
        )
        BlockService.create_label(frame_test3, 2, 9, 2, 9, name="frame_test3_label1", text="frame_test3_label1")
        BlockService.root.place_frame_widget(frame=toplevel)
        if self.config.setting.debug == DEBUG_MODE:
            BlockService.root.create_auxiliary_line(frame=frame_test3)
        toplevel.wait_window(toplevel)
        frame_test3.destroy()
        toplevel.destroy()

    def create(self) -> None:
        self.frame = BlockService.create_frame("test_reframe", col=10, row=10)
        self._create_test1_frame()
        self._create_test2_frame()

        BlockService.create_button(self.frame, 4, 6, 0, 1, text="toplevel BlockFrame", command=self._create_dialog)
