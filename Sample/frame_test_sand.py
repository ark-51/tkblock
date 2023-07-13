#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameSand

砂場
開発時に検証で触っていたコード
"""
import logging
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import subprocess

from tkblock.block_service import (
    BlockFrame,
    BlockService,
)

from ini_parser import Config
from tkblock.logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestSand:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrame = None

    def get_frame(self) -> BlockFrame:
        return self.frame

    def create(self) -> None:
        def _button_command(event) -> None:
            logger.debug(event.widget["text"])
            text_command_res.insert(tk.END, f"> {entry_command_input.get()}\n")
            command: str = entry_command_input.get()
            res: subprocess.CompletedProcess[str] = subprocess.run(
                command.split(" ") if len(command.split()) > 1 else [command],
                encoding=self.config.setting.encoding,
                shell=True,
                stdout=subprocess.PIPE,
            )
            text_command_res.insert(tk.END, res.stdout)
            text_command_res.see("end")

        self.frame = BlockService.create_frame("sand")
        BlockService.create_label(self.frame, 0, 3, 0, 1, name="label_command", text="コマンド")
        entry_command_input: BlockService.create_entry(self.frame, 3, 38, 0, 1, name="entry_command_input")
        entry_command_input.insert(tk.END, "echo aaa")
        entry_command_input.bind("<Return>", _button_command)
        text_command_res: BlockService.create_text = tk.Text(self.frame, 0, 40, 1, 40, name="text_command_res")
        scroll_command_res: tk.Scrollbar = tk.Scrollbar(
            self.frame,
            name="scroll_command_res",
            orient=tkinter.VERTICAL,
            command=text_command_res.yview,
        )
        scroll_command_res.pack(side=tkinter.RIGHT, fill="y")
        text_command_res["yscrollcommand"] = scroll_command_res.set
        BlockService.create_button(self.frame, 38, 40, 0, 1, text="実行", _button_command)
