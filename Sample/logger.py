#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri
"""logger"""
import logging


loggers: list = []

LEVEL: dict[str, int] = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


class LoggerError(Exception):
    """Logのエラークラス"""

    pass


def create_logger(
    name: str,
    propagate: bool = False,
    level: str = "debug",
    is_stream_handler: bool = True,
    stream_level: str = "debug",
    stream_formatter: list[str] = "\t".join(
        [
            "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s"
        ]
    ),
    is_file_handler: bool = False,
    file_path: str = "./log.log",
    file_level: str = "debug",
    file_formatter: list[str] = "\t".join(
        [
            "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s"
        ]
    ),
) -> logging.Logger:
    """loggerのインスタンスを作成する。

    Args:
        name (str): loggerの名前
        propagate (bool, optional): 上位logger有効化設定. Defaults to False.
        level (str, optional): ログの出力レベル. Defaults to "debug".
        is_stream_handler (bool, optional): 標準出力可否設定. Defaults to True.
        stream_level (str, optional): 標準出力ログレベル設定. Defaults to "debug".
        stream_formatter (_type_, optional): 標準ログの出力フォーマット. Defaults to "\t".join( [ "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s" ] ).
        is_file_handler (bool, optional): ファイル出力可否設定. Defaults to False.
        file_path (str, optional): 出力先ファイルパス. Defaults to "./log.log".
        file_level (str, optional): ファイル出力ログレベル. Defaults to "debug".
        file_formatter (_type_, optional): ファイル出力ログフォーマット. Defaults to "\t".join( [ "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s" ] ).

    Raises:
        LoggerError: ログエラー

    Returns:
        logging.Logger: ロガーインスタンス
    """

    if _check_existence(name):
        raise LoggerError("this name already exists.")
    # loggerの作成
    logger: logging.Logger = logging.getLogger(name)
    logger.propagate = propagate
    logger.setLevel(LEVEL[level])
    # handlerの作成
    if is_stream_handler:
        add_stream_handler(logger, level=stream_level, formatter=stream_formatter)
    if is_file_handler:
        add_file_handler(logger, file_path, level=file_level, formatter=file_formatter)
    loggers.append({"name": name, "logger": logger})
    return logger


def _check_existence(name: str) -> bool:
    """同名のloggerがいているか確認する

    Args:
        name (str): loggerの名称

    Returns:
        bool: 存在有無
    """
    result: bool = False
    for log in loggers:
        if log["name"] == name:
            result = True
            break
    return result


def get_logger(name: str) -> logging.Logger:
    """loggerを取得する。

    Args:
        name (str): loggerの名前

    Raises:
        LoggerError: Loggerのエラー

    Returns:
        logging.Logger: logger
    """
    logger: logging.Logger = None
    for log in loggers:
        if log["name"] == name:
            logger = log["logger"]
            break
    else:
        raise LoggerError("target name logger was not found.")
    return logger


def add_stream_handler(
    logger: logging.Logger,
    level: str = "debug",
    formatter: list[str] = "\t".join(
        [
            "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s"
        ]
    ),
) -> None:
    """標準ハンドラーを追加する

    Args:
        logger (logging.Logger): 追加先のlogger
        level (str, optional): 出力logレベル. Defaults to "debug".
        formatter (list[str], optional): 出力フォーマット. Defaults to "\t".join( [ "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s" ] ).
    """
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(LEVEL[level])
    stream_handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(stream_handler)


def add_file_handler(
    logger: logging.Logger,
    file_path: str,
    level: str = "debug",
    formatter: list[str] = "\t".join(
        [
            "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s"
        ]
    ),
) -> None:
    """ファイルハンドラーを追加する

    Args:
        logger (logging.Logger): 追加先のlogger
        file_path (str): 出力ファイルパス
        level (str, optional): 出力logレベル. Defaults to "debug".
        formatter (list[str], optional): 出力フォーマット. Defaults to "\t".join( [ "%(asctime)s, %(name)s, %(levelname)s, %(filename)s, %(funcName)s, %(lineno)s, %(message)s" ] ).
    """
    file_handler: logging.FileHandler = logging.FileHandler(file_path)
    file_handler.setLevel(LEVEL[level])
    file_handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(file_handler)
