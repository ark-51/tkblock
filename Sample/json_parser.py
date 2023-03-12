#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""JsonParser, Storage

シングルトン設計
初回は下記のようにインスタンス化をする
storage = Storage("storage.json")
それ以外はget_instanceでインスタンスを取得する
storage = Storage.get_instance()
"""
import json
from typing import Any


class JsonParser:
    """Jsonファイルを読み込んで読み込み専用の属性を作成するクラス"""

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

    def __init__(self, file_path: str, dict_recursive: bool = False) -> None:
        """コンストラクタ
        Args:
            file_path (str): jsonファイルのパス
            dict_recursive (bool, optional): 全ての辞書データを再帰的にクラス属性に書き込むか. Defaults to False.
        """
        self.initialize(file_path, dict_recursive)

    def initialize(
        self, file_path: str, dict_recursive: bool, encoding: str = "utf-8"
    ) -> None:
        """初期化を行う

        jsonでjsonファイルを読み取り、その内容をクラスに書き込む。

        Args:
            file_path (str): jsonファイルのパス
            dict_recursive (bool): 全ての辞書データを再帰的にクラス属性に書き込むか.
            encoding (str, optional): configファイルの文字コード. Defaults to 'utf-8'.
        """
        self.file_path: str = file_path
        with open(file_path, "r", encoding=encoding) as f:
            self.json_data = json.load(f)
        self._create_object(self, self.json_data, dict_recursive)

    def _create_object(
        self, class_object: type, data: dict, dict_recursive: bool
    ) -> None:
        """クラスオブジェクトに属性を作成する

        Args:
            class_object (_type_): 属性付与対象の空のクラスオブジェクト
            data (dict): 付与するデータ
            dict_recursive (bool): 全ての辞書データを再帰的にクラス属性に書き込むか.
        """
        if dict_recursive:
            for key, value in data.items():
                if type(value) is dict:
                    define_property(class_object, key, type(key, (object,), dict())())
                    self._create_object(
                        getattr(class_object, key), value, dict_recursive
                    )
                elif type(value) is list:
                    define_property(class_object, key, list())
                    self._recursive_list(
                        getattr(class_object, key), key, value, dict_recursive
                    )
                else:
                    define_property(class_object, key, value)
        else:
            for key, value in data.items():
                define_property(class_object, key, value)

    def _recursive_list(
        self, list_object: list, key: str, value: dict, dict_recursive: bool
    ) -> None:
        """listに対する再起処理を実施する。

        listの中にdictが含まれている場合、クラスオブジェクトを作成する必要があるので、再起処理を実施。

        Args:
            list_object (list): データを追加する対象のlist
            key (str): リストを格納している変数名
            value (dict): リストのデータ
            dict_recursive (bool): 全ての辞書データを再帰的にクラス属性に書き込むか.
        """
        for index, list_value in enumerate(value):
            if type(list_value) is dict:
                list_object.append(type(f"{key}_{index}", (object,), dict())())
                self._create_object(
                    list_object[index],
                    list_value,
                    dict_recursive,
                )
            elif type(list_value) is list:
                list_object.append(list())
                self._recursive_list(
                    list_object[index],
                    f"{key}_{index}",
                    list_value,
                    dict_recursive,
                )
            else:
                list_object.append(list_value)

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


def define_property(
    class_object,
    name: str,
    value: Any,
    readable: bool = True,
    writable: bool = True,
) -> None:
    """オブジェクトに属性とプロバティを追加する
    Args:
        class_object (object): config object
        name (str): 変数名
        value (object): 変数にセットする値
        readable (bool, optional): read許可設定. Defaults to True.
        writable (bool, optional): write許可設定. Defaults to False.
    """
    field_name: str = f"_{name}"
    setattr(class_object, field_name, value)
    getter: Any | None = (lambda cls: getattr(cls, field_name)) if readable else None
    setter = (
        lambda _, value: setattr(class_object, field_name, value) if writable else None
    )
    setattr(class_object.__class__, name, property(getter, setter))


def undefine_property(cls, config: JsonParser, name: str) -> None:
    """オブジェクトに属性とプロバティを削除する
    Args:
        config (JsonParser): config object
        name (str): 変数名
    """
    field_name: str = "_{}".format(name)
    delattr(cls, field_name)
    delattr(cls.__class__, name)
    del config.config_parse[cls.__class__.__name__][field_name[1:]]
    with open(config.config_path, "w") as write_file:
        config.config_parse.write(write_file)


def undefine_property_section(cls, config: JsonParser, name) -> None:
    """オブジェクトからセクションとプロバティを削除する
    Args:
        config (JsonParser): config object
        name (str): 変数名
    """
    field_name: str = "_{}".format(name)
    delattr(cls, field_name)
    delattr(cls.__class__, name)
    del config.config_parse[field_name[1:]]
    with open(config.config_path, "w") as write_file:
        config.config_parse.write(write_file)


class Storage(JsonParser):
    """Storageファイルを読みだす"""
