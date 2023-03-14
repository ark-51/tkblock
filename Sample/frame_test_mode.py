#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameTestMode

各実行モードのコピー元
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


class FrameTestMode:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def create(self) -> None:
        self.frame = BlockService.create_frame("test_template")


class TableDelete:
    """テーブル削除のフレームワーク"""

    def __init__(self, parent) -> None:
        """コンストラクタ

        Args:
            parent (FrameBase): 親フレーム
        """
        self.parent = parent
        self.frame = None
        self.config: Config = Config.get_instance()

    def create(self) -> BlockFrameBase:
        """作成する"""
        self.frame: BlockFrameBase = BlockService.create_frame(
            "table_delete", root=self.parent, col=20, row=20
        )
        self.frame.layout = BlockService.layout(0, 60, 1, 40)

        return self.frame


class TableCp:
    """テーブルコピーのフレームワーク"""

    def __init__(self, parent) -> None:
        """コンストラクタ

        Args:
            parent (FrameBase): 親フレーム
        """
        self.parent = parent
        self.frame: None = None

    def create(self) -> BlockFrameBase:
        """作成する"""
        self.frame = BlockService.create_frame(
            "table_cp", root=self.parent, col=20, row=20
        )
        self.frame.layout = BlockService.layout(0, 60, 1, 40)

        return self.frame


class FrameTestMode:
    """TestModeを扱うモード"""

    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        """フレームを返す"""
        return self.frame

    def _create_execute_mode(self, execute_modes, frames) -> None:
        """実行モードを作成する"""

        def _raise_frame(_) -> None:
            """選択されたモードへフレーム切り替えする"""
            target: str = stringvar_target.get()
            mode: str = stringvar_mode.get()
            frames[target][mode].tkraise()

        def _set_combobox_mode(_) -> None:
            """選択された対象からモードをcomboboxにセットする"""
            value: str = stringvar_target.get()
            combobox_mode["value"] = execute_modes[value]

        text_list_target: list = list(execute_modes.keys())
        label_target: ttk.Label = ttk.Label(self.frame, text="target")
        label_target.layout = BlockService.layout(0, 5, 0, 1)
        stringvar_target: tk.StringVar = tk.StringVar(value=text_list_target)
        combobox_target: ttk.Combobox = ttk.Combobox(
            self.frame, values=text_list_target, textvariable=stringvar_target
        )
        combobox_target.layout = BlockService.layout(5, 15, 0, 1)
        combobox_target.bind("<<ComboboxSelected>>", _set_combobox_mode)

        text_list_mode: str = ""
        stringvar_mode: tk.StringVar = tk.StringVar(value=text_list_mode)
        label_mode: ttk.Label = ttk.Label(self.frame, text="mode")
        label_mode.layout = BlockService.layout(15, 20, 0, 1)
        combobox_mode: ttk.Combobox = ttk.Combobox(
            self.frame, values=[""], textvariable=stringvar_mode
        )
        combobox_mode.layout = BlockService.layout(20, 30, 0, 1)
        combobox_mode.bind("<<ComboboxSelected>>", _raise_frame)

    def create(self) -> None:
        """実行モードのフレーム作成"""
        self.frame = BlockService.create_frame("test_mode")
        execute_modes: dict[str, list] = {"table": ["delete", "cp"], "schedule": []}
        frames: dict[str, dict] = {"table": {}, "schedule": {}}

        frames["table"]["delete"] = TableDelete(self.frame).create()
        frames["table"]["cp"] = TableCp(self.frame).create()
        self._create_execute_mode(execute_modes, frames)
        frames["table"]["delete"].tkraise()
