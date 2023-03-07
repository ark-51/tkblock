#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri
"""main"""
import sys
import logging

from config import ConfigParser
from logger import create_logger
from menu import Menu
from frame_test_template import FrameTestTemplate
from frame_test_layout import FrameTestLayout
from frame_test_reframe import FrametestReframe
from frame_test_widget import FrameTestWidget
from block_util import change_frame

sys.path.append(r"../tkblock/")
from block_service import BlockService, BlockFramework


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
        self.config: ConfigParser = ConfigParser.get_instance()
        self.root: BlockFramework = BlockService.init(
            APP_TITLE, SEPELATE_COLUMN_NUMBER, SEPELATE_ROW_NUMBER, WIDTH, HEIGHT
        )

        self.menu: Menu = Menu(self.root)
        self.frame_test_template: FrameTestTemplate = FrameTestTemplate()
        self.frame_test_layout: FrameTestLayout = FrameTestLayout()
        self.frame_test_reframe: FrametestReframe = FrametestReframe()
        self.frame_test_widget: FrameTestWidget = FrameTestWidget()
        self.frame_test_template.create()
        self.frame_test_layout.create()
        self.frame_test_reframe.create()
        self.frame_test_widget.create()
        self.menu.create(
            [
                self.frame_test_template,
                self.frame_test_layout,
                self.frame_test_reframe,
                self.frame_test_widget,
            ]
        )
        BlockService.place_frame_widget()
        if self.config.setting.debug == DEBUG_MODE:
            BlockService.create_auxiliary_line()
        change_frame(self.frame_test_template.get_frame())

    def main(self) -> None:
        """main"""
        self.root.mainloop()
