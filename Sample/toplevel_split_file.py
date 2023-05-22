#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kyohei.araki
"""FrameMain"""
import os
import logging
import pathlib
import functools
import tkinter as tk
from tkinter import ttk

import pyperclip
from tkblock.block_service import BlockService
from tkblock.block_framebase import BlockFrame

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")

DEBUG_MODE: str = "1"


class ToplevelSplitFile:
    """"""

    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrame = None
        self.select_file_path = pathlib.Path(__file__).resolve().parent
        self.output_folder_path = pathlib.Path(__file__).resolve().parent

    def get_frame(self) -> BlockFrame:
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
        toplevel = BlockService.create_toplevel(
            frame, "split file", 500, 500, is_grab=True
        )
        # dialog.transient(self.root)  # タスクバーに表示しない
        # ダイアログが閉じられるまで待つ
        self.frame: BlockFrame = BlockService.create_frame(
            "split_file", col=20, row=20, root=toplevel
        )

        # ファイルとフォルダ選択と文字コード
        BlockService.create_label(self.frame, 0, 4, 1, 2, text="・分割ファイル")
        BlockService.create_label(self.frame, 0, 4, 2, 3, text="・格納フォルダ")
        BlockService.create_label(self.frame, 0, 4, 3, 4, text="・文字コード")

        _, var_entry_select = BlockService.create_entry(
            self.frame,
            6,
            20,
            1,
            2,
            init_value=str(pathlib.Path(__file__).resolve().parent),
        )
        _, var_entry_output = BlockService.create_entry(
            self.frame,
            6,
            20,
            2,
            3,
            init_value=str(pathlib.Path(__file__).resolve().parent),
        )
        _, var_encoding = BlockService.create_entry(
            self.frame, 4, 20, 3, 4, init_value="utf-8"
        )
        BlockService.create_button(
            self.frame,
            4,
            6,
            1,
            2,
            text="開く",
            command=functools.partial(
                self._open_select_file, var_entry_select, var_entry_output
            ),
        )
        BlockService.create_button(
            self.frame,
            4,
            6,
            2,
            3,
            text="開く",
            command=functools.partial(self._open_output_folder, var_entry_output),
        )

        # 実行モード選択
        BlockService.create_label(self.frame, 0, 4, 4, 5, text="・分割モード")
        _, var_radio_mode = BlockService.create_radiobutton(
            self.frame, 0, 9, 5, 6, text="行", value=1, init_value=0, anchor=tk.W
        )
        BlockService.create_radiobutton(
            self.frame,
            0,
            9,
            5,
            6,
            text="サイズ",
            value=2,
            var=var_radio_mode,
            anchor=tk.W,
        )
        BlockService.create_radiobutton(
            self.frame,
            0,
            9,
            7,
            8,
            text="サイズ(行差異許容)",
            value=3,
            var=var_radio_mode,
            anchor=tk.W,
        )

        BlockService.create_label(self.frame, 9, 12, 5, 6, text="行数")
        BlockService.create_label(self.frame, 9, 12, 6, 7, text="サイズ(KB)")

        _, var_row = BlockService.create_entry(
            self.frame, 12, 20, 5, 6, init_value="10000"
        )
        _, var_size = BlockService.create_entry(
            self.frame, 12, 20, 6, 7, init_value="1"
        )

        # ヘッダ設定
        BlockService.create_label(self.frame, 0, 4, 8, 9, text="・ヘッダ設定")
        BlockService.create_label(self.frame, 0, 4, 9, 10, text="ヘッダ数")
        _, var_head_num = BlockService.create_entry(
            self.frame, 4, 8, 9, 10, init_value="0"
        )
        BlockService.create_label(self.frame, 0, 4, 10, 11, text="スキップ行")
        _, var_head_skip_num = BlockService.create_entry(
            self.frame, 4, 8, 10, 11, init_value="0"
        )

        # result
        BlockService.create_label(self.frame, 10, 20, 9, 10, text="分割結果")
        text_result = BlockService.create_text(self.frame, 10, 20, 10, 20)

        BlockService.create_button(
            self.frame,
            8,
            10,
            9,
            20,
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

        BlockService.root.place_frame_widget(frame=toplevel)
        toplevel.wait_window(toplevel)
        self.frame.destroy()
        toplevel.destroy()
