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
    BlockFrameBase,
    BlockService,
)

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestWidget:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def create(self) -> None:

        self.frame = BlockService.create_frame("test_tkwidget")
        # Label
        label1: ttk.Label = ttk.Label(self.frame, name="label1", text="config")
        label1.layout = BlockService.layout(0, 3, 0, 2)
        # Entry
        entry1: tk.Entry = tk.Entry(self.frame, name="entry1", width=20)
        entry1.layout = BlockService.layout(4, 9, 0, 2)
        entry1.insert(tk.END, "test")
        # Button
        def _button_config(event) -> None:
            logger.debug(event.widget["text"])

        button1: ttk.Button = ttk.Button(self.frame, name="button1", text="button")
        button1.bind("<Button-1>", _button_config)
        button1.layout = BlockService.layout(10, 13, 0, 2)
        # Listbox
        listbox1_list = ("tkinter", "os", "datetime", "math")
        listbox1_var = tk.StringVar(value=listbox1_list)
        listbox1 = tk.Listbox(self.frame, listvariable=listbox1_var, name="listbox1")
        listbox1.layout = BlockService.layout(0, 5, 3, 10)
        listbox1.insert(2, "hogehoge")
        # Checkbutton
        def echo_checkbutton1():
            print(checkbutton1_var.get())

        checkbutton1_var = tk.BooleanVar()
        checkbutton1 = tk.Checkbutton(
            self.frame,
            name="checkbutton1",
            text="checkbutton1",
            variable=checkbutton1_var,
            command=echo_checkbutton1,
        )
        checkbutton1.layout = BlockService.layout(14, 20, 0, 2)
        # Radiobutton
        radiobutton1_var = tk.IntVar()
        radiobutton1_label = tk.Label(
            self.frame, name="radiobutton1_label", textvariable=radiobutton1_var
        )
        radiobutton1_1 = tk.Radiobutton(
            self.frame,
            name="radiobutton1_1",
            text="radiobutton1_1",
            value=10,
            var=radiobutton1_var,
        )
        radiobutton1_2 = tk.Radiobutton(
            self.frame,
            name="radiobutton1_2",
            text="radiobutton1_2",
            value=20,
            var=radiobutton1_var,
        )
        radiobutton1_label.layout = BlockService.layout(6, 15, 3, 5)
        radiobutton1_1.layout = BlockService.layout(6, 15, 5, 7)
        radiobutton1_2.layout = BlockService.layout(6, 15, 7, 10)
        # Scale
        scale1_var = tk.StringVar(value=listbox1_list)
        scale1_label = tk.Label(
            self.frame, name="scale1_label", textvariable=scale1_var
        )
        scale1 = tk.Scale(self.frame, name="scale1", variable=scale1_var)
        scale1_label.layout = BlockService.layout(16, 20, 3, 5)
        scale1.layout = BlockService.layout(16, 20, 5, 10)
        # Message
        message1 = tk.Message(
            self.frame, name="message1", text="Messageの自動改行テスト", relief="raised"
        )
        message1.layout = BlockService.layout(21, 24, 0, 10)
        # Combobox
        combobox1 = ttk.Combobox(
            self.frame, name="combobox1", values=["Easy", "Normal", "Hard"]
        )
        combobox1.layout = BlockService.layout(0, 5, 11, 15)
        # Treeview
        treeview1 = ttk.Treeview(self.frame, name="treeview1")
        treeview1_parent = treeview1.insert("", "end", text="parent")  # 親要素の挿入
        treeview1_child = treeview1.insert(
            treeview1_parent, "end", text="child"
        )  # 子要素の挿入
        treeview1.layout = BlockService.layout(6, 15, 11, 20)
        # Progressbar
        def timer():
            progressbar1.start(5)  # プログレスバー開始
            for i in range(6):
                time.sleep(1)  # 1秒待機
                progressbar1_button["text"] = i  # 秒数表示
            progressbar1.stop()  # プログレスバー停止

        # ボタンクリック時に実行する関数
        def button_clicked():
            t = threading.Thread(target=timer)  # スレッド立ち上げ
            t.start()  # スレッド開始

        progressbar1 = ttk.Progressbar(self.frame, mode="indeterminate")
        progressbar1_button = tk.Button(
            self.frame, text="start", command=button_clicked
        )
        progressbar1.layout = BlockService.layout(16, 24, 11, 12)
        progressbar1_button.layout = BlockService.layout(16, 24, 13, 20)
        # Notebook
        notebook1 = ttk.Notebook(self.frame)
        notebook1_entry = tk.Entry(self.frame)
        notebook1_entry.insert(tk.END, "hogehoge")
        notebook1_button = tk.Button(self.frame, text="button")
        notebook1.add(notebook1_entry, text="Entry")  # Entryを表示
        notebook1.add(notebook1_button, text="Button")  # Buttonを表示
        notebook1.layout = BlockService.layout(0, 9, 21, 25)
        # Labelframe
        labelframe1 = ttk.Labelframe(
            self.frame, relief="ridge", text="Labelframe", labelanchor="n"
        )
        labelframe1_label = tk.Label(
            labelframe1, relief="groove", width=15, text="frame test"
        )
        labelframe1_label.pack()
        labelframe1_entry = tk.Entry(labelframe1, width=15)
        labelframe1_entry.pack()
        labelframe1.layout = BlockService.layout(10, 15, 21, 25)  # Labelframeを表示
        # Spinbox
        spinbox1_var = tk.IntVar(self.frame)
        spinbox1_var.set(0)
        spinbox1 = tk.Spinbox(
            self.frame, textvariable=spinbox1_var, from_=-10, to=10, increment=1
        )
        spinbox1_label = tk.Label(self.frame, textvariable=spinbox1_var)
        spinbox1.layout = BlockService.layout(16, 25, 21, 23)
        spinbox1_label.layout = BlockService.layout(16, 25, 23, 25)

        # Scrollbar
        ## how to use 1
        scrollbar1_listbox_list = tuple([str(x) for x in range(0, 100)])
        scrollbar1_listbox_var = tk.StringVar(value=scrollbar1_listbox_list)
        scrollbar1_listbox = tk.Listbox(
            self.frame, listvariable=scrollbar1_listbox_var, name="scrollbar1_listbox"
        )
        scrollbar1_listbox.layout = BlockService.layout(30, 40, 0, 10)

        scrollbar1: Scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar1.layout = BlockService.layout(40, 41, 0, 10)
        scrollbar1.config(command=scrollbar1_listbox.yview)
        scrollbar1_listbox.config(yscrollcommand=scrollbar1.set)

        ## how to use 2
        scrollbar2_listbox_list = tuple(
            [str(x) for x in range(0, 100)]
            + ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
        )
        scrollbar2_listbox_var = tk.StringVar(value=scrollbar2_listbox_list)
        scrollbar2_listbox = tk.Listbox(
            self.frame, listvariable=scrollbar2_listbox_var, name="scrollbar2_listbox"
        )
        scrollbar2_listbox.layout = BlockService.layout(51, 60, 0, 10)
        scrollbar2_y_project = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar2_x_project = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        scrollbar2_y_project.config(command=scrollbar2_listbox.yview)
        scrollbar2_x_project.config(command=scrollbar2_listbox.xview)
        scrollbar2_listbox.config(yscrollcommand=scrollbar2_y_project.set)
        scrollbar2_listbox.config(xscrollcommand=scrollbar2_x_project.set)
        scrollbar2_listbox.scrollbar = BlockService.scrollbar(
            y=scrollbar2_y_project, x=scrollbar2_x_project
        )
