#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""IniParser, Config

シングルトン設計
初回は下記のようにインスタンス化をする
config = Config("config.ini")
それ以外はget_instanceでインスタンスを取得する
config = Config.get_instance()
"""
from typing import Any
import configparser


class IniParser:
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

    def __init__(self, file_path: str) -> None:
        """コンストラクタ
        Args:
            file_path (str): iniファイルのパス
        """
        self.initialize(file_path)

    def initialize(self, file_path: str, encoding: str = "utf-8") -> None:
        """初期化を行う

        configparserでconfigを読み取り、その内容をクラスに書き込む。

        Args:
            file_path (str): iniファイルのパス
            encoding (str, optional): configファイルの文字コード. Defaults to 'utf-8'.
        """
        self.file_path: str = file_path
        self.sections: dict = {}
        self.config_parse: IniParser = configparser.ConfigParser()
        self.config_parse.optionxform = str
        self.config_parse.read(file_path, encoding=encoding)
        for section_name in self.config_parse.sections():
            section: configparser.SectionProxy = self.config_parse[section_name]
            # セクションで同名のキーが存在することがあるので、クラスを作成することで分離する
            define_property(
                self, self, section_name, type(section_name, (object,), dict())()
            )
            self.sections[section_name] = {}
            for key, value in section.items():
                define_property(getattr(self, section_name), self, key, value)
                self.sections[section_name][key] = value

    def write(self, section_name: str, key: str, value: Any) -> None:
        """iniの変数に値を追加し、iniファイルに書き込みを行う

        section_nameのセクションが存在しなければ、作成を行う。

        Args:
            section_name (str): 書き込むセクション名
            key (str): iniのkey
            value (Any): iniの値
        """
        if section_name not in dir(self):
            define_property(
                self, self, section_name, type(section_name, (object,), dict())()
            )
            self.config_parse[section_name] = dict()
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


def setattr_ini(cls, ini: Any, field_name: str, value: Any) -> None:
    """セッター＋ini更新
    Args:
        ini (Any): 属性付与対象の空のクラスオブジェクト
        field_name (str): セットするフィールド名
        value (Any): セットする値
    """
    setattr(cls, field_name, str(value))
    ini.config_parse[cls.__class__.__name__][field_name[1:]] = str(value)
    with open(ini.file_path, "w") as write_file:
        ini.config_parse.write(write_file)


def define_property(
    cls,
    class_object: Any,
    name: str,
    value: Any,
    readable: bool = True,
    writable: bool = True,
) -> None:
    """オブジェクトに属性とプロバティを追加する
    Args:
        class_object (Any): 属性付与対象の空のクラスオブジェクト
        name (str): 変数名
        value (object): 変数にセットする値
        readable (bool, optional): read許可設定. Defaults to True.
        writable (bool, optional): write許可設定. Defaults to False.
    """
    field_name: str = f"_{name}"
    setattr(cls, field_name, value)
    getter: Any | None = (lambda cls: getattr(cls, field_name)) if readable else None
    setter: Any | None = (
        lambda _, value: setattr_ini(cls, class_object, field_name, value)
        if writable
        else None
    )
    setattr(cls.__class__, name, property(getter, setter))


def undefine_property(cls, ini: Any, name: str) -> None:
    """オブジェクトに属性とプロバティを削除する
    Args:
        ini (Any): ini object
        name (str): 変数名
    """
    field_name: str = "_{}".format(name)
    delattr(cls, field_name)
    delattr(cls.__class__, name)
    del ini.config_parse[cls.__class__.__name__][field_name[1:]]
    with open(ini.file_path, "w") as write_file:
        ini.config_parse.write(write_file)


def undefine_property_section(cls, ini: Any, name) -> None:
    """オブジェクトからセクションとプロバティを削除する
    Args:
        ini (Any): ini object
        name (str): 変数名
    """
    field_name: str = "_{}".format(name)
    delattr(cls, field_name)
    delattr(cls.__class__, name)
    del ini.config_parse[field_name[1:]]
    with open(ini.file_path, "w") as write_file:
        ini.config_parse.write(write_file)


class Config(IniParser):
    """configファイルを読みだす"""
