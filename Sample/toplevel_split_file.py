#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""ToplvelFileSplit"""
import os
import logging
import pathlib
import functools
import tkinter as tk
from tkinter import ttk

from tkblock.block_service import BlockService
from tkblock.block_framebase import BlockFrameBase

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")

DEBUG_MODE: str = "1"


class ToplevelSplitFile:
    """"""

    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None
        self.select_file_path = pathlib.Path(__file__).resolve().parent
        self.output_folder_path = pathlib.Path(__file__).resolve().parent

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def _open_select_file(self, var_entry_select, var_entry_output) -> None:
        """分割対象ファイルを開く"""
        select_file_path = tk.filedialog.askopenfilename(
            title="分割対象ファイルを開く",
            initialdir=str(pathlib.Path(__file__).resolve().parent),
        )
        self.select_file_path = pathlib.Path(select_file_path)
        self.output_folder_path = self.select_file_path.parent
        var_entry_select.set(str(self.select_file_path))
        var_entry_output.set(str(self.output_folder_path))

    def _open_output_folder(self, var_entry_output) -> None:
        """configファイルを開き直す。"""
        output_folder_path = tk.filedialog.askdirectory(
            title="格納フォルダを開く",
            initialdir=str(pathlib.Path(__file__).resolve().parent),
        )
        self.output_folder_path = pathlib.Path(output_folder_path)
        var_entry_output.set(str(self.output_folder_path))

    def _split_file_row(
        self,
        target_file_path,
        output_dir_path,
        row,
        encoding,
        head_num,
        head_skip_num,
    ):
        max_line = row
        split_index = 1
        line_index = 1
        heads = []

        with open(target_file_path, encoding=encoding) as in_file:
            for _ in range(head_skip_num):
                in_file.readline()
            for _ in range(head_num):
                heads.append(in_file.readline())
            line = in_file.readline()
            out_file = open(
                f"{str(output_dir_path)}/{split_index}",
                "w",
                encoding=encoding,
            )
            for head in heads:
                out_file.write(head)
            while line:
                if line_index > max_line:
                    out_file.close()
                    logger.debug("write file index: %s", split_index)
                    split_index += 1
                    line_index = 1
                    out_file = open(
                        f"{output_dir_path}/{split_index}",
                        "w",
                        encoding=encoding,
                    )
                    for head in heads:
                        out_file.write(head)
                out_file.write(line)
                line_index = line_index + 1
                line = in_file.readline()
            out_file.close()
        return split_index

    def _split_file_size(self, target_file_path, output_dir_path, size):
        file_size = os.path.getsize(target_file_path)
        split_index = 1

        # チャンクサイズをバイト単位に変換
        chunk_size = int(size * 1024)
        num_chunks = file_size // chunk_size + (1 if file_size % chunk_size != 0 else 0)

        # ファイルを開く
        with open(target_file_path, "rb") as f:
            for index in range(num_chunks):
                output_file_path = f"{output_dir_path}/{index+1}"
                with open(output_file_path, "wb") as out:
                    chunk = f.read(chunk_size)
                    out.write(chunk)
                    logger.debug("write file index: %s", index + 1)
                    split_index = index + 1
        return split_index

    def _split_file_size_row(
        self,
        target_file_path,
        output_dir_path,
        size,
        encoding,
        head_num,
        head_skip_num,
    ):
        # チャンクサイズをバイト単位に変換
        chunk_size = int(size * 1024)
        split_index = 1
        write_size = 0
        heads = []
        with open(target_file_path, "r", encoding=encoding) as in_file:
            for _ in range(head_skip_num):
                in_file.readline()
            for _ in range(head_num):
                heads.append(in_file.readline())
            line = in_file.readline()
            write_size += len(line.encode(encoding))
            out_file = open(
                f"{str(output_dir_path)}/{split_index}",
                "w",
                encoding=encoding,
            )
            for head in heads:
                out_file.write(head)
            while line:
                if chunk_size < write_size:
                    out_file.close()
                    logger.debug("write file index: %s", split_index)
                    split_index += 1
                    write_size = 0
                    out_file = open(
                        f"{output_dir_path}/{split_index}",
                        "w",
                        encoding=encoding,
                    )
                    for head in heads:
                        out_file.write(head)
                out_file.write(line)
                line = in_file.readline()
                write_size += len(line.encode(encoding))
            out_file.close()
        return split_index

    def _split_file(
        self,
        text_result,
        target_file_path,
        output_file_path,
        mode,
        row,
        size,
        encoding,
        head_num,
        head_skip_num,
    ):
        text_result.delete("1.0", "end")
        target_file_path = target_file_path.get()
        output_file_path = output_file_path.get()
        mode = int(mode.get())
        row = int(row.get())
        size = float(size.get())
        encoding = encoding.get()
        head_num = int(head_num.get())
        head_skip_num = int(head_skip_num.get())
        logger.info(
            "%s,%s,%s,%s,%s", target_file_path, output_file_path, mode, row, size
        )
        if mode == 1:
            split_num = self._split_file_row(
                target_file_path,
                output_file_path,
                row,
                encoding,
                head_num,
                head_skip_num,
            )
            text_result.insert(tk.END, "実行モード：行数で分割\n")
            text_result.insert(tk.END, f"分割されたファイル数：{split_num}\n")
            text_result.insert(tk.END, f"出力先：{str(output_file_path)}\n")
            text_result.insert(tk.END, f"ヘッダスキップ数：{head_skip_num}\n")
            text_result.insert(tk.END, f"ヘッダ：{head_num}\n")
        elif mode == 2:
            split_num = self._split_file_size(target_file_path, output_file_path, size)
            text_result.insert(tk.END, "実行モード：サイズ数で分割\n")
            text_result.insert(tk.END, f"分割されたファイル数：{split_num}\n")
            text_result.insert(tk.END, f"出力先：{str(output_file_path)}\n")
        elif mode == 3:
            split_num = self._split_file_size_row(
                target_file_path,
                output_file_path,
                size,
                encoding,
                head_num,
                head_skip_num,
            )
            text_result.insert(tk.END, "実行モード：サイズ数で分割(最終行は出し切る)\n")
            text_result.insert(tk.END, f"分割されたファイル数：{split_num}\n")
            text_result.insert(tk.END, f"出力先：{str(output_file_path)}\n")
            text_result.insert(tk.END, f"ヘッダスキップ数：{head_skip_num}\n")
            text_result.insert(tk.END, f"ヘッダ：{head_num}\n")
        else:
            logger.warning("選択されていません")
            return
        text_result.see("end")

    def create(self, frame) -> None:
        width = 500
        height = 500
        toplevel: tk.Toplevel = tk.Toplevel(frame)
        toplevel.title("split file")
        toplevel.geometry(f"{width}x{height}")
        toplevel.width = width
        toplevel.hegith = height
        toplevel.grab_set()  # モーダルにする
        toplevel.focus_set()  # フォーカスを新しいウィンドウをへ移す
        # dialog.transient(self.root)  # タスクバーに表示しない
        # ダイアログが閉じられるまで待つ
        self.frame: BlockFrameBase = BlockService.create_frame(
            "split_file", col=20, row=20, width=width, height=height, root=toplevel
        )

        # ファイルとフォルダ選択と文字コード
        label_select: ttk.Label = ttk.Label(self.frame, text="・分割ファイル")
        label_select.layout = BlockService.layout(0, 4, 1, 2)
        label_output: ttk.Label = ttk.Label(self.frame, text="・格納フォルダ")
        label_output.layout = BlockService.layout(0, 4, 2, 3)
        label_encoding: ttk.Label = ttk.Label(self.frame, text="・文字コード")
        label_encoding.layout = BlockService.layout(0, 4, 3, 4)

        var_entry_select = tk.StringVar(
            value=str(pathlib.Path(__file__).resolve().parent)
        )
        entry_select: tk.Entry = tk.Entry(self.frame, textvariable=var_entry_select)
        entry_select.layout = BlockService.layout(6, 20, 1, 2)

        var_entry_output = tk.StringVar(
            value=str(pathlib.Path(__file__).resolve().parent)
        )
        entry_output: tk.Entry = tk.Entry(self.frame, textvariable=var_entry_output)
        entry_output.layout = BlockService.layout(6, 20, 2, 3)

        var_encoding = tk.StringVar(value="utf-8")
        entry_encoding: tk.Entry = tk.Entry(self.frame, textvariable=var_encoding)
        entry_encoding.layout = BlockService.layout(4, 20, 3, 4)

        button_select: tk.Button = tk.Button(
            self.frame,
            text="開く",
            command=functools.partial(
                self._open_select_file, var_entry_select, var_entry_output
            ),
        )
        button_select.layout = BlockService.layout(4, 6, 1, 2)
        button_output: tk.Button = tk.Button(
            self.frame,
            text="開く",
            command=functools.partial(self._open_output_folder, var_entry_output),
        )
        button_output.layout = BlockService.layout(4, 6, 2, 3)

        # 実行モード選択
        label_select: ttk.Label = ttk.Label(self.frame, text="・分割モード")
        label_select.layout = BlockService.layout(0, 4, 4, 5)
        var_radio_mode = tk.IntVar(value=0)
        radiobutton_mode_row = tk.Radiobutton(
            self.frame, text="行", value=1, var=var_radio_mode, anchor=tk.W
        )
        radiobutton_mode_size = tk.Radiobutton(
            self.frame, text="サイズ", value=2, var=var_radio_mode, anchor=tk.W
        )
        radiobutton_mode_size_row = tk.Radiobutton(
            self.frame, text="サイズ(行差異許容)", value=3, var=var_radio_mode, anchor=tk.W
        )
        radiobutton_mode_row.layout = BlockService.layout(0, 9, 5, 6)
        radiobutton_mode_size.layout = BlockService.layout(0, 9, 6, 7)
        radiobutton_mode_size_row.layout = BlockService.layout(0, 9, 7, 8)

        label_row: ttk.Label = ttk.Label(self.frame, text="行数")
        label_row.layout = BlockService.layout(9, 12, 5, 6)
        label_size: ttk.Label = ttk.Label(self.frame, text="サイズ(KB)")
        label_size.layout = BlockService.layout(9, 12, 6, 7)

        var_row = tk.StringVar(value="10000")
        entry_row: tk.Entry = tk.Entry(self.frame, textvariable=var_row)
        entry_row.layout = BlockService.layout(12, 20, 5, 6)
        var_size = tk.StringVar(value="1")
        entry_size: tk.Entry = tk.Entry(self.frame, textvariable=var_size)
        entry_size.layout = BlockService.layout(12, 20, 6, 7)

        # ヘッダ設定
        label_head: ttk.Label = ttk.Label(self.frame, text="・ヘッダ設定")
        label_head.layout = BlockService.layout(0, 4, 8, 9)
        # # var_check_head = tk.BooleanVar()
        # # checkbutton_head = tk.Checkbutton(
        # #     self.frame, text="有効", variable=var_check_head, anchor=tk.W
        # # )
        # checkbutton_head.layout = BlockService.layout(0, 8, 9, 10)
        label_head_num: ttk.Label = ttk.Label(self.frame, text="ヘッダ数")
        label_head_num.layout = BlockService.layout(0, 4, 9, 10)
        var_head_num = tk.IntVar()
        entry_head_num: tk.Entry = tk.Entry(self.frame, textvariable=var_head_num)
        entry_head_num.layout = BlockService.layout(4, 8, 9, 10)
        label_head_skip_num: ttk.Label = ttk.Label(self.frame, text="スキップ行")
        label_head_skip_num.layout = BlockService.layout(0, 4, 10, 11)
        var_head_skip_num = tk.IntVar()
        entry_head_skip_num: tk.Entry = tk.Entry(
            self.frame, textvariable=var_head_skip_num
        )
        entry_head_skip_num.layout = BlockService.layout(4, 8, 10, 11)

        # result
        label_result: ttk.Label = ttk.Label(self.frame, text="分割結果")
        label_result.layout = BlockService.layout(10, 20, 9, 10)
        text_result: tk.Text = tk.Text(self.frame)
        text_result.layout = BlockService.layout(10, 20, 10, 20)

        button_execute: tk.Button = tk.Button(
            self.frame,
            text="実行",
            command=functools.partial(
                self._split_file,
                text_result,
                var_entry_select,
                var_entry_output,
                var_radio_mode,
                var_row,
                var_size,
                var_encoding,
                var_head_num,
                var_head_skip_num,
            ),
        )
        button_execute.layout = BlockService.layout(8, 10, 9, 20)

        BlockService.root.place_frame_widget(frame=toplevel)
        if self.config.setting.debug == DEBUG_MODE:
            BlockService.root.create_auxiliary_line(frame=self.frame)
        toplevel.wait_window(toplevel)
        self.frame.destroy()
        toplevel.destroy()
