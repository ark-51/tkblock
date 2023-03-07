#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrametestReframe

Frame in Frame等のFrameに関する検証を行う
"""
import sys
import logging
import tkinter as tk
from tkinter import ttk

from config import ConfigParser
from logger import create_logger

sys.path.append(r"../tkblock/")
from block_service import BlockFrameBase, BlockService


logger: logging.Logger = create_logger(__name__, level="debug")
DEBUG_MODE: str = "1"


class FrametestReframe:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: ConfigParser = ConfigParser.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def _create_test2_frame(self) -> None:
        """root上のBlockFrameBaseの上のFrameの上にBlockFrameBaseを配置する例"""
        # BlockFrameBase → Frame
        frame_test2: ttk.Frame = ttk.Frame(
            self.frame,
            name="main-frame_test1-frame_test2",
        )
        frame_test2.layout = BlockService.layout(6, 9, 1, 9)

        # BlockFrameBase → Frame → BlockFrameBase
        frame_test2_frame_test1: BlockFrameBase = BlockService.create_frame(
            "test1", col=5, row=10, root=frame_test2
        )
        frame_test2_frame_test1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # BlockFrameBase → Frame → BlockFrameBase → Label
        frame_test2_frame_test1_label1: ttk.Label = ttk.Label(
            frame_test2_frame_test1,
            name="frame_test2_frame_test1_label1",
            text="FB→F→FB",
        )
        frame_test2_frame_test1_label1.layout = BlockService.layout(2, 3, 5, 6)

    def _create_test1_frame(self) -> None:
        """root上のBlockFrameBaseの上にBlockFrameBaseの上にFrameを配置する例"""
        # BlockFrameBase → BlockFrameBase
        frame_test1: BlockFrameBase = BlockService.create_frame(
            "test1", col=5, row=10, root=self.frame
        )
        frame_test1.layout = BlockService.layout(1, 4, 1, 9)

        # BlockFrameBase → BlockFrameBase → Frame
        frame_test1_frame_test1: ttk.Frame = ttk.Frame(
            frame_test1,
            name="main-frame_test1-frame_test2",
        )
        frame_test1_frame_test1.layout = BlockService.layout(1, 4, 1, 9)

        # BlockFrameBase → BlockFrameBase → Frame → label
        frame_test1_frame_test1_label1: ttk.Label = ttk.Label(
            frame_test1_frame_test1,
            name="frame_test1_frame_test1_label1",
            text="FB→FB→F",
        )
        frame_test1_frame_test1_label1.place(relx=0.5, rely=0.5)

    def _create_dialog(self) -> None:
        # dialog設定
        toplevel: tk.Toplevel = tk.Toplevel(self.frame)
        toplevel.title("toplevel_BlockFrameBase")
        toplevel.geometry("500x500")
        toplevel.width = 500
        toplevel.hegith = 500
        toplevel.grab_set()  # モーダルにする
        toplevel.focus_set()  # フォーカスを新しいウィンドウをへ移す
        # dialog.transient(self.root)  # タスクバーに表示しない
        # ダイアログが閉じられるまで待つ
        frame_test3: BlockFrameBase = BlockService.create_frame(
            "test3", col=10, row=10, width=500, height=500, root=toplevel
        )
        frame_test3_label1: ttk.Label = ttk.Label(
            frame_test3,
            name="frame_test3_label1",
            text="frame_test3_label1",
        )
        frame_test3_label1.layout = BlockService.layout(2, 9, 2, 9)
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

        button_dialog1: tk.Button = tk.Button(
            self.frame, text="toplevel BlockFrameBase", command=self._create_dialog
        )
        button_dialog1.layout = BlockService.layout(4, 6, 0, 1)
