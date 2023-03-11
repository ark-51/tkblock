#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""main"""
import sys
import logging
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from functools import partial

from ini_parser import IniParser
from logger import create_logger

sys.path.append(r"../tkblock/")
from block_util import change_frame
from block_service import BlockFramework, BlockFrameBase

logger: logging.Logger = create_logger(__name__, level="debug")


class Menu:
    def __init__(self, root: BlockFramework) -> None:
        """初期化を行う

        Args:
            root (BlockFramework): BlockFramework
        """
        self.initialize(root)

    def initialize(self, root: BlockFramework) -> None:
        """初期化を行う

        Args:
            root (BlockFramework): BlockFramework
        """
        self.config: IniParser = IniParser.get_instance()
        self.root: BlockFramework = root
        self.menu: tk.Menu = None

    def get_menu(self) -> tk.Menu:
        """menuを返す"""
        return self.menu

    def _open_config_file(self) -> None:
        """configファイルを開き直す。"""
        file_path = tkinter.filedialog.askopenfilename(
            title="設定ファイルを開く",
            filetypes=[
                ("Ini", ".ini"),
            ],
            initialdir="./",
        )
        self.config.initialize(file_path)
        logger.debug(file_path)

    def _change_config(self) -> None:
        """configのファイルを書き換える

        ダイアログを使ったGUIを作成する。
        configのファイルとconfigのオブジェクトも変更する。
        """

        def _edit_config(self) -> None:
            """configのファイルを編集する"""
            target_item: str = None
            for item in tree_view.selection():
                parent_item: str = tree_view.parent(item)
                section: str = tree_view.item(parent_item, "text")
                values: tuple = tree_view.item(item, "values")
                target_item = item
                break

            def _get_value() -> None:
                """変更値となる値を取得する"""
                chane_value: str = entry.get()
                tree_view.set(target_item, column=1, value=chane_value)
                self.config.write(section, values[0], chane_value)
                dialog_edit.destroy()

            dialog_edit: tk.Toplevel = tk.Toplevel(dialog)
            dialog_edit.title("Change Config")
            dialog_edit.geometry("300x200")
            dialog_edit.grab_set()  # モーダルにする
            dialog_edit.focus_set()  # フォーカスを新しいウィンドウをへ移す
            dialog_edit.transient(self.root)  # タスクバーに表示しない
            entry: tkinter.Entry = tkinter.Entry(dialog_edit)
            entry.pack()
            button: tkinter.Button = tkinter.Button(
                dialog_edit, command=_get_value, text="変更"
            )
            button.pack()

            # ダイアログが閉じられるまで待つ
            self.root.wait_window(dialog_edit)

        def _delete_config(self) -> None:
            """tree viewで選択されたconfigの情報を削除する"""
            for item in tree_view.selection():
                parent_item: str = tree_view.parent(item)
                section: str = tree_view.item(parent_item, "text")
                values: tuple = tree_view.item(item, "values")
                self.config.erase(section, key=values[0])
                tree_view.delete(item)

        # dialog設定
        dialog: tk.Toplevel = tk.Toplevel(self.root)
        dialog.title("Change Config")
        dialog.geometry("500x420")
        dialog.grab_set()  # モーダルにする
        dialog.focus_set()  # フォーカスを新しいウィンドウをへ移す
        dialog.transient(self.root)  # タスクバーに表示しない
        # configの情報を記載
        tree_view: ttk.Treeview = ttk.Treeview(
            dialog, columns=["key", "value"], height=19
        )
        tree_view.column("#0", width=100)
        tree_view.column("key", width=100)
        tree_view.column("value", width=100)
        tree_view.heading("#0", text="階層列")
        tree_view.heading("key", text="key")
        tree_view.heading("value", text="value")
        for section_name, value in self.config.sections.items():
            insert_id: str = tree_view.insert(
                "",
                tk.END,
                text=section_name,
                open=True,
            )
            for key, value in value.items():
                tree_view.insert(
                    insert_id,
                    tk.END,
                    open=True,
                    values=(key, value),
                )
        scroll_tree_view: ttk.Scrollbar = ttk.Scrollbar(
            dialog,
            name="scroll_tree_view",
            orient=tkinter.VERTICAL,
            command=tree_view.yview,
        )
        scroll_tree_view.pack(side=tkinter.RIGHT, fill="y")
        tree_view["yscrollcommand"] = scroll_tree_view.set
        # dialog.columnconfigure(0, weight=1)
        # dialog.grid_propagate(False)
        # scroll_tree_view.grid(row=1, column=0, sticky=tk.EW)
        scroll_tree_view.grid(row=0, column=1, rowspan=4, sticky=tk.NS)
        tree_view.grid(row=0, column=0, rowspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        button_edit: tk.Button = tk.Button(
            dialog, text="編集", width=20, height=5, command=lambda: _edit_config(self)
        )
        button_clear: tk.Button = tk.Button(
            dialog, text="削除", width=20, height=5, command=lambda: _delete_config(self)
        )
        button_edit.grid(column=3, row=1, columnspan=3, sticky=tk.E)
        button_clear.grid(column=3, row=3, columnspan=3, sticky=tk.E)

        # ダイアログが閉じられるまで待つ
        self.root.wait_window(dialog)

    def create(self, execute_modes=None) -> None:
        """メニューバーを作成する"""

        self.menu: tk.Menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        menu_file: tk.Menu = tk.Menu(self.root)
        menu_mode: tk.Menu = tk.Menu(self.root)
        self.menu.add_cascade(label="設定", menu=menu_file)
        self.menu.add_cascade(label="モード", menu=menu_mode)
        menu_file.add_command(
            label="config変更", command=lambda: self._open_config_file()
        )
        menu_file.add_command(label="config編集", command=lambda: self._change_config())
        # mode
        for execute_mode in execute_modes:
            menu_mode.add_command(
                label=execute_mode.get_frame()._name,
                command=partial(change_frame, execute_mode.get_frame()),
            )
