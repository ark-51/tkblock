#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri
"""ConfigParser

シングルトン設計
初回は下記のようにインスタンス化をする
config = ConfigParser("c:sample.ini")
それ以外はget_instanceでインスタンスを取得する
config = ConfigParser.get_instance()
"""
from typing import Any
import configparser


class ConfigParser:
    """INIファイルを読み込んで読み込み専用の属性を作成するクラス"""

    _instance: Any = None

    def __new__(cls, *args, **kwargs) -> Any:
        """シングルトン設計

        インスタンスが生成されている場合は再生成しない。

        Returns:
            Any: インスタンス
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> Any:
        """インスタンスを返す

        Returns:
            Any: インスタンス
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: str) -> None:
        """コンストラクタ
        Args:
            config_path (str): configファイルのパス
        """
        self.initialize(config_path)

    def initialize(self, config_path: str, encoding: str = "utf-8"):
        """初期化を行う

        configparserでconfigを読み取り、その内容を空クラスに書き込む。

        Args:
            config_path (str): configファイルのパス
            encoding (str, optional): configファイルの文字コード. Defaults to 'utf-8'.
        """
        self.config_path: str = config_path
        self.sections: dict = {}
        self.config_file: ConfigParser = configparser.ConfigParser()
        # ConfigParser の規定の振る舞いは INIファイルのキーの大文字小文字を区別しないため、
        # 以下の一文を追加し、大文字小文字を区別する。
        self.config_file.optionxform = str
        self.config_file.read(config_path, encoding=encoding)
        for section_name in self.config_file.sections():
            section: configparser.SectionProxy = self.config_file[section_name]
            define_property(
                self, self, section_name, type(section_name, (object,), dict())()
            )
            self.sections[section_name] = {}
            for key, value in section.items():
                define_property(getattr(self, section_name), self, key, value)
                self.sections[section_name][key] = value

    def write(self, section_name: str, key: str, value: Any) -> None:
        """configの変数に値を追加し、configファイルに書き込みを行う

        section_nameのセクションが存在しなければ、作成を行う。

        Args:
            section_name (str): 書き込むセクション名
            key (str): configのkey
            value (Any): configの値
        """
        if section_name not in dir(self):
            define_property(
                self, self, section_name, type(section_name, (object,), dict())()
            )
            self.config_file[section_name] = dict()
            self.sections[section_name] = dict()
        define_property(getattr(self, section_name), self, key, value)
        setattr(getattr(self, section_name), key, str(value))
        self.sections[section_name][key] = value

    def erase(self, section_name: str, key: str = None) -> None:
        """セクションやセクション内のキーを削除する

        Args:
            section_name (str): セクション名
            key (str, optional): キー名. Defaults to None.
        """
        if key is None:
            undefine_property_section(self, self, section_name)
            del self.sections[section_name]
        else:
            undefine_property(getattr(self, section_name), self, key)
            del self.sections[section_name][key]


def setattr_config(cls, config: ConfigParser, field_name: str, value: Any) -> None:
    """セッター＋config更新
    Args:
        config (ConfigParser): config object
        field_name (str): セットするフィールド名
        value (Any): セットする値
    """
    setattr(cls, field_name, str(value))
    config.config_file[cls.__class__.__name__][field_name[1:]] = str(value)
    with open(config.config_path, "w") as write_file:
        config.config_file.write(write_file)


def define_property(
    cls,
    config: ConfigParser,
    name: str,
    value: Any,
    readable: bool = True,
    writable: bool = True,
) -> None:
    """オブジェクトに属性とプロバティを追加する
    Args:
        config (object): config object
        name (str): 変数名
        value (object): 変数にセットする値
        readable (bool, optional): read許可設定. Defaults to True.
        writable (bool, optional): write許可設定. Defaults to False.
    """
    # 属性名にcls.__class__は不要
    # field_name = "_{}__{}".format(cls.__class__.__name__, name)
    field_name: str = "_{}".format(name)
    setattr(cls, field_name, value)
    getter: Any | None = (lambda cls: getattr(cls, field_name)) if readable else None
    # setter = lambda _, value: setattr(cls, field_name, value) if writable else None
    setter: Any | None = (
        lambda _, value: setattr_config(cls, config, field_name, value)
        if writable
        else None
    )
    setattr(cls.__class__, name, property(getter, setter))


def undefine_property(cls, config: ConfigParser, name: str) -> None:
    """オブジェクトに属性とプロバティを削除する
    Args:
        config (ConfigParser): config object
        name (str): 変数名
    """
    # 属性名にcls.__class__は不要
    # field_name = "_{}__{}".format(cls.__class__.__name__, name)
    field_name: str = "_{}".format(name)
    delattr(cls, field_name)
    delattr(cls.__class__, name)
    del config.config_file[cls.__class__.__name__][field_name[1:]]
    with open(config.config_path, "w") as write_file:
        config.config_file.write(write_file)


def undefine_property_section(cls, config: ConfigParser, name) -> None:
    """オブジェクトからセクションとプロバティを削除する
    Args:
        config (ConfigParser): config object
        name (str): 変数名
    """
    # 属性名にcls.__class__は不要
    # field_name = "_{}__{}".format(cls.__class__.__name__, name)
    field_name: str = "_{}".format(name)
    delattr(cls, field_name)
    delattr(cls.__class__, name)
    del config.config_file[field_name[1:]]
    with open(config.config_path, "w") as write_file:
        config.config_file.write(write_file)
