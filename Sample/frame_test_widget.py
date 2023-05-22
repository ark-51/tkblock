#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameTestWidget

widgetの検証を行う
"""
import time
import logging
import tkinter as tk
from tkinter import ttk
import threading

from tkblock.block_service import (
    BlockFrame,
    BlockService,
)

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestWidget:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrame = None

    def get_frame(self) -> BlockFrame:
        return self.frame

    def create(self) -> None:

        self.frame = BlockService.create_frame("test_tkwidget")
        # Label--------------------------------------------------
        BlockService.create_label(self.frame, 0, 3, 0, 2, name="label1", text="config")
        # Entry--------------------------------------------------
        entry1, _ = BlockService.create_entry(
            self.frame, 4, 9, 0, 2, name="entry1", width=20
        )
        entry1.insert(tk.END, "test")
        # Button--------------------------------------------------
        def _button_config(event) -> None:
            logger.debug(event.widget["text"])

        BlockService.create_button(
            self.frame,
            10,
            13,
            0,
            2,
            name="button1",
            text="button",
            function=_button_config,
        )
        # Listbox--------------------------------------------------
        listbox1, listbox1_var = BlockService.create_listbox(
            self.frame,
            0,
            5,
            3,
            10,
            init_value=("tkinter", "os", "datetime", "math"),
            name="listbox1",
        )
        listbox1.insert(2, "hogehoge")
        # Checkbutton--------------------------------------------------
        def echo_checkbutton(_):
            print(checkbutton1_var.get())
            print(checkbutton2_var.get())

        _, checkbutton1_var = BlockService.create_checkbutton(
            self.frame,
            14,
            20,
            0,
            1,
            name="checkbutton1",
            text="checkbutton1",
            init_value=True,
        )
        _, checkbutton2_var = BlockService.create_checkbutton(
            self.frame,
            14,
            20,
            1,
            2,
            name="checkbutton2",
            text="checkbutton2",
            init_value=False,
        )
        BlockService.create_button(self.frame, 14, 20, 2, 3, function=echo_checkbutton)
        # Radiobutton--------------------------------------------------
        _, radiobutton1_var = BlockService.create_radiobutton(
            self.frame,
            6,
            15,
            5,
            7,
            init_value=0,
            name="radiobutton1_1",
            text="radiobutton1_1",
            value=10,
        )
        _, _ = BlockService.create_radiobutton(
            self.frame,
            6,
            15,
            7,
            10,
            name="radiobutton1_2",
            text="radiobutton1_2",
            value=20,
            variable=radiobutton1_var,
        )
        BlockService.create_label(
            self.frame,
            6,
            15,
            3,
            5,
            name="radiobutton1_label",
            textvariable=radiobutton1_var,
        )
        # Scale--------------------------------------------------
        _, scale1_var = BlockService.create_scale(
            self.frame, 16, 20, 5, 10, init_value="", name="scale1"
        )
        BlockService.create_label(
            self.frame, 16, 20, 3, 5, name="scale1_label", textvariable=scale1_var
        )
        # Message--------------------------------------------------
        BlockService.create_message(
            self.frame,
            21,
            24,
            0,
            10,
            name="message1",
            text="Messageの自動改行テスト",
            relief="raised",
        )
        # Combobox--------------------------------------------------
        BlockService.create_combobox(
            self.frame,
            0,
            5,
            11,
            15,
            name="combobox1",
            values=["Easy", "Normal", "Hard"],
        )
        # Treeview--------------------------------------------------
        treeview1 = BlockService.create_treeview(
            self.frame, 6, 15, 11, 20, name="treeview1"
        )
        treeview1_parent = treeview1.insert("", "end", text="parent")  # 親要素の挿入
        treeview1_child = treeview1.insert(
            treeview1_parent, "end", text="child"
        )  # 子要素の挿入
        # Progressbar--------------------------------------------------
        progressbar1 = BlockService.create_progressbar(
            self.frame, 16, 24, 11, 12, mode="indeterminate"
        )

        def timer():
            progressbar1.start(5)  # プログレスバー開始
            for i in range(6):
                time.sleep(1)  # 1秒待機
                progressbar1_button["text"] = i  # 秒数表示
            progressbar1.stop()  # プログレスバー停止

        def button_clicked():
            t = threading.Thread(target=timer)  # スレッド立ち上げ
            t.start()  # スレッド開始

        progressbar1_button = BlockService.create_button(
            self.frame, 16, 24, 13, 20, text="start", command=button_clicked
        )
        # Notebook--------------------------------------------------
        notebook1 = BlockService.create_notebook(self.frame, 0, 9, 21, 25)
        notebook1_frame1 = tk.Frame(self.frame)
        notebook1_frame2 = tk.Frame(self.frame)
        notebook1_frame3 = tk.Frame(self.frame)
        notebook1.add(notebook1_frame1, text="fram1")
        notebook1.add(notebook1_frame2, text="fram2")
        notebook1.add(notebook1_frame3, text="fram3")
        # Labelframe--------------------------------------------------
        labelframe1 = BlockService.create_labelframe(
            self.frame,
            10,
            15,
            21,
            25,
            relief="ridge",
            text="Labelframe",
            labelanchor="n",
        )
        labelframe1_label = tk.Label(
            labelframe1, relief="groove", width=15, text="frame test"
        )
        labelframe1_label.pack()
        labelframe1_entry = tk.Entry(labelframe1, width=15)
        labelframe1_entry.pack()
        # Spinbox--------------------------------------------------
        _, spinbox1_var = BlockService.create_spinbox(
            self.frame, 16, 25, 21, 23, init_value=0, from_=-10, to=10, increment=1
        )
        _ = BlockService.create_label(
            self.frame, 16, 25, 23, 25, textvariable=spinbox1_var
        )

        # scrollbar direct layout setting--------------------------------------------------
        scrollbar1_listbox, _ = BlockService.create_listbox(
            self.frame,
            30,
            40,
            0,
            10,
            init_value=tuple([str(x) for x in range(0, 100)]),
            name="scrollbar1_listbox",
        )
        layout = BlockService.layout(40, 41, 0, 10)
        scrollbar1 = BlockService.create_scrollbar(
            self.frame, layout=layout, orient=tk.VERTICAL
        )
        scrollbar1.config(command=scrollbar1_listbox.yview)
        scrollbar1_listbox.config(yscrollcommand=scrollbar1.set)
        # scrollbar auto layout setting--------------------------------------------------
        sc2_temp = tuple(
            [str(x) for x in range(0, 100)] + ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
        )
        scrollbar2_listbox, _ = BlockService.create_listbox(
            self.frame, 42, 49, 0, 10, init_value=sc2_temp, name="scrollbar2_listbox"
        )
        scrollbar2_listbox.scrollbar = BlockService.scrollbar(
            self.frame, x_enable=True, y_enable=True, size=15
        )

        # text--------------------------------------------------
        def echo_text(_):
            print(text1.get("1.0", "end - 1c"))

        text1 = BlockService.create_text(self.frame, 30, 40, 15, 20, name="text1")
        text1.insert(tk.END, "hoge\nfuga")
        BlockService.create_button(self.frame, 30, 40, 20, 21, function=echo_text)

        # canvas--------------------------------------------------
        cavas1 = BlockService.create_canvas(self.frame, 42, 49, 15, 20)
        cavas1.create_line(0, 0, 430, 300)
