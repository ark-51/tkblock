#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameSand

砂場
開発時に検証で触っていたコード
"""
import sys
import logging
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import subprocess

from config import ConfigParser
from logger import create_logger

sys.path.append(r"../tkblock/")
from block_service import (
    BlockFrameBase,
    BlockService,
)


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestSand:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: ConfigParser = ConfigParser.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
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
        label_command: ttk.Label = ttk.Label(
            self.frame, name="label_command", text="コマンド"
        )
        label_command.layout = BlockService.layout(0, 3, 0, 1)
        entry_command_input: tk.Entry = tk.Entry(self.frame, name="entry_command_input")
        entry_command_input.layout = BlockService.layout(3, 38, 0, 1)
        entry_command_input.insert(tk.END, "echo aaa")
        entry_command_input.bind("<Return>", _button_command)
        text_command_res: tk.Text = tk.Text(self.frame, name="text_command_res")
        text_command_res.layout = BlockService.layout(0, 40, 1, 40)
        scroll_command_res: tk.Scrollbar = tk.Scrollbar(
            self.frame,
            name="scroll_command_res",
            orient=tkinter.VERTICAL,
            command=text_command_res.yview,
        )
        scroll_command_res.pack(side=tkinter.RIGHT, fill="y")
        text_command_res["yscrollcommand"] = scroll_command_res.set
        button_command: ttk.Button = ttk.Button(self.frame, text="実行")
        button_command.bind("<Button-1>", _button_command)
        button_command.layout = BlockService.layout(38, 40, 0, 1)
