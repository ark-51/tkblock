#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""main"""
import logging

from tkblock.block_service import BlockService, BlockFramework
from tkblock.block_util import change_frame

from ini_parser import Config
from logger import create_logger
from menu import Menu
from frame_test_template import FrameTestTemplate
from frame_test_layout import FrameTestLayout
from frame_test_reframe import FrametestReframe
from frame_test_widget import FrameTestWidget
from frame_test_mode import FrameTestMode


logger: logging.Logger = create_logger(__name__, level="debug")

WIDTH: int = 1200
HEIGHT: int = 800
SEPELATE_COLUMN_NUMBER: int = 60
SEPELATE_ROW_NUMBER: int = 40
APP_TITLE: str = "tkinter template"
DEBUG_MODE: str = "1"


class TkMain:
    def __init__(self) -> None:
        """初期化を行う"""
        self.initialize()

    def initialize(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.root: BlockFramework = BlockService.init(
            APP_TITLE, SEPELATE_COLUMN_NUMBER, SEPELATE_ROW_NUMBER, WIDTH, HEIGHT
        )

        self.menu: Menu = Menu(self.root)
        self.frame_test_template: FrameTestTemplate = FrameTestTemplate()
        self.frame_test_layout: FrameTestLayout = FrameTestLayout()
        self.frame_test_reframe: FrametestReframe = FrametestReframe()
        self.frame_test_widget: FrameTestWidget = FrameTestWidget()
        self.frame_test_mode: FrameTestMode = FrameTestMode()
        self.frame_test_template.create()
        self.frame_test_layout.create()
        self.frame_test_reframe.create()
        self.frame_test_widget.create()
        self.frame_test_mode.create()
        self.menu.create(
            [
                self.frame_test_template,
                self.frame_test_layout,
                self.frame_test_reframe,
                self.frame_test_widget,
                self.frame_test_mode,
            ]
        )
        BlockService.place_frame_widget()
        if self.config.setting.debug == DEBUG_MODE:
            BlockService.create_auxiliary_line()
        change_frame(self.frame_test_template.get_frame())

    def main(self) -> None:
        """main"""
        self.root.mainloop()
