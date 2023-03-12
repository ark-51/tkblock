#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""FrameTestTemplate

検証用のFrameを作成するためのテンプレート
"""
import logging

from tkblock.block_service import (
    BlockFrameBase,
    BlockService,
)

from ini_parser import Config
from logger import create_logger


logger: logging.Logger = create_logger(__name__, level="debug")


class FrameTestTemplate:
    def __init__(self) -> None:
        """初期化を行う"""
        self.config: Config = Config.get_instance()
        self.frame: BlockFrameBase = None

    def get_frame(self) -> BlockFrameBase:
        return self.frame

    def create(self) -> None:
        self.frame = BlockService.create_frame("test_template")
