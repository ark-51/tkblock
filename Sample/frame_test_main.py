#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameMain"""
import time
import logging
import functools
import subprocess
import tkinter as tk
from tkinter import ttk

import pyperclip
from tkblock.block_service import BlockService, wait_processe
from tkblock.block_framebase import BlockFrame

from ini_parser import Config
from logger import create_logger, FileKind
from toplevel_split_file import ToplevelSplitFile


logger: logging.Logger = create_logger(
    __name__, level="debug", is_file_handler=True, file_kind=FileKind.ROTATE
)


class FrameTestMain:
    """"""

    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrame = None

    def get_frame(self) -> BlockFrame:
        return self.frame

    def _create_font_clear(self, button_layout):
        def _button_config() -> None:
            pyperclip.copy(pyperclip.paste())
            BlockService.root.iconify()

        def key_handler(event):
            _button_config()

        _ = self._set_button_command("クリックボードフォントクリア", _button_config, button_layout)
        BlockService.root.bind("<Control-c>", key_handler)

    def _create_splited_file(self, button_layout):
        toplevel_split_file = ToplevelSplitFile()

        BlockService.create_button(
            self.frame,
            *button_layout,
            text="ファイル分割",
            command=functools.partial(toplevel_split_file.create, self.frame)
        )

    def _create_open_c(self, button_layout):
        def _button_execute() -> None:
            subprocess.Popen(["explorer", "C:\\"], shell=True)
            BlockService.root.iconify()

        _ = self._set_button_command("C直下を開く", _button_execute, button_layout)

    def _create_log_test(self, button_layout):
        def _button_execute() -> None:
            logger.warning("logのテストです。")

        _ = self._set_button_command("log出力", _button_execute, button_layout)

    def _create_sleep10_test(self, button_layout):
        @wait_processe()
        def _button_execute() -> None:
            logger.warning("sleep start")
            for index in range(10):
                logger.warning(index)
                time.sleep(1)
            logger.warning("sleep end")

        _ = self._set_button_command("sleep10", _button_execute, button_layout)

    def _set_button_command(self, text, command, button_layout):
        return BlockService.create_button(
            self.frame, *button_layout, text=text, command=command
        )

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
            self._create_log_test,
            self._create_sleep10_test,
        ]
        for index, f in enumerate(functions):
            f(button_layouts[index])
