#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameMain"""
import logging
import functools
import subprocess
import tkinter as tk
from tkinter import ttk

import pyperclip
from tkblock.block_service import BlockService
from tkblock.block_framebase import BlockFrameBase

from ini_parser import Config
from logger import create_logger
from toplevel_split_file import ToplevelSplitFile


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestMain:
    """"""

    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def _create_font_clear(self, button_layout):
        def _button_config(event) -> None:
            pyperclip.copy(pyperclip.paste())
            BlockService.root.iconify()

        def key_handler(event):
            _button_config(event)

        button_clickborad_font_clear: ttk.Button = ttk.Button(
            self.frame, name="", text="クリックボードフォントクリア"
        )
        button_clickborad_font_clear.bind("<Button-1>", _button_config)
        button_clickborad_font_clear.layout = BlockService.layout(*button_layout)
        BlockService.root.bind("<Control-c>", key_handler)

    def _create_splited_file(self, button_layout):
        toplevel_split_file = ToplevelSplitFile()

        button_dialog1: tk.Button = tk.Button(
            self.frame,
            text="ファイル分割",
            command=functools.partial(toplevel_split_file.create, self.frame),
        )
        button_dialog1.layout = BlockService.layout(*button_layout)

    def _create_open_c(self, button_layout):
        def _button_execute() -> None:
            subprocess.Popen(["explorer", "C:\\"], shell=True)

        _ = self._set_button_command("C直下を開く", _button_execute, button_layout)

    def _set_button_command(self, text, command, button_layout):
        button: tk.Button = tk.Button(
            self.frame,
            text=text,
            command=command,
        )
        button.layout = BlockService.layout(*button_layout)
        return button

    def _create_button_layouts(self):
        row = self.frame.max_row
        col = self.frame.max_col
        row_split = int(row / 10)
        col_split = int(col / 10)
        layouts = []
        for r_index in range(0, row, row_split):
            for c_index in range(0, col, col_split):
                layouts.append(
                    (
                        c_index,
                        c_index + col_split,
                        r_index,
                        r_index + row_split,
                    )
                )
        return layouts

    def _create_sample(self, button_layout):
        def _button_execute() -> None:
            print("sample")

        _ = self._set_button_command("sample", _button_execute, button_layout)

    def create(self) -> None:
        self.frame = BlockService.create_frame("main")
        button_layouts = self._create_button_layouts()
        functions = [
            self._create_font_clear,
            self._create_splited_file,
            self._create_open_c,
        ]
        for index, f in enumerate(functions):
            f(button_layouts[index])
