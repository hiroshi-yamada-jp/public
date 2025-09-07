"""
概要: 日時文字列の変換・検査、時間計算ライブラリ
更新: 2025/09/05
AI Prompt:
   numpyで下記仕様を満たす関数を作れますか (doc stringを渡す)
"""
from __future__ import annotations
# 拡張関数
import numpy as np
from loguru import logger


class Array2d:
    # -------------------------------
    #  汎用関数
    # -------------------------------
    @staticmethod
    def transpose_array(array_2d: np.ndarray) -> np.ndarray:
        """2次元配列の行と列を入れ替える"""
        return array_2d.T

    # -------------------------------
    #  配列の各要素を対象に動作する関数
    # -------------------------------
    @staticmethod
    def array2bin_string(array_2d: np.ndarray, digit: int) -> np.ndarray:
        """ 2次元配列の各要素を2進数文字列に変換した結果を返す

        Args:
            array_2d: 2次元の整数配列
            digit: 出力する2進数の桁数（ゼロ埋めする桁数）
        Returns:
            np.ndarray: 同じ形状の2進数文字列の配列（dtype=object）
        """
        # np.vectorize(py_func): numpyの各要素にpy_funcで指定した関数を適用する
        formatter = np.vectorize(pyfunc=lambda x: format(x, f'0{digit}b'))
        return formatter(array_2d)

    @staticmethod
    def bitwise_not_array(array_2d: np.ndarray, digit: int) -> np.ndarray:
        """2次元配列の各要素に対してビット反転した結果を返す

        Args:
            array_2d: 整数型の2次元配列
            digit: ビット反転後に保持する最大桁数
        Returns:
            np.ndarray: 同じ形状のビット反転（指定ビット幅でマスク済み）済み配列
        """
        if not 0 <= digit <= 64:
            raise ValueError("bit_width must be between 1 and 64")
        mask = (1 << digit) - 1  # 例: bit_width=8 → mask=0b11111111=255
        return np.bitwise_not(array_2d) & mask

    @staticmethod
    def count_bit_on(array_2d: np.ndarray) -> np.ndarray:
        """各ノードの属性フラグにおいて、ONになっているビット数を返す

        Args:
           array_2d: 整数型の2次元配列（各要素がビットフラグ）  例: [ [0b00001111],[0b11110001],[0b00000000]]
        Returns:
            np.ndarray: 各要素のBIT ONの数の配列 [[4], [5], [0]]
        """
        return np.bitwise_count(array_2d)

    # ---------------------------------------------
    #  2次元配列から任意範囲の要素抽出
    # ---------------------------------------------
    @staticmethod
    def extract_ranged_array(array_2d: np.ndarray, rows: list[int] | None, cols: list[int] | None) -> np.ndarray:
        """2次元配列から指定範囲の行と列だけを抽出する

        Args:
            array_2d: 2次元のNumPy配列
            rows: 対象行のインデックス番号リスト / None: 全行を抽出
            cols: 対象列のインデックス番号リスト / None: 全列を抽出
        Returns:
            np.ndarray: 指定範囲を抽出した2次元配列
        """
        # rowsがNoneなら、全行インデックスのnp.arrayを生成し、それ以外は、指定行をnp.array に変換
        rows2 = np.arange(array_2d.shape[0]) if rows is None else np.array(rows)
        # colsがNoneなら、全列インデックスのnp.arrayを生成し、それ以外は、指定列をnp.array に変換
        cols2 = np.arange(array_2d.shape[1]) if cols is None else np.array(cols)
        # 指定範囲の行と列の交差範囲を抽出
        return array_2d[np.ix_(rows2, cols2)]

    @staticmethod
    def extract_not_ranged_array(array_2d: np.ndarray, rows: list[int], cols: list[int]) -> np.ndarray:
        """2次元配列から指定範囲の行と列を除いた範囲を抽出する

        Args:
            array_2d: 2次元のNumPy配列
            rows: 除外対象行のインデックス番号リスト
            cols: 除外対象列のインデックス番号リスト
        Returns:
            np.ndarray: 指定範囲を除いて抽出した2次元配列
        """
        # 指定範囲の行除外
        remaining_rows = np.setdiff1d(np.arange(array_2d.shape[0]), rows)
        # 指定範囲の列除外
        remaining_cols = np.setdiff1d(np.arange(array_2d.shape[1]), cols)
        # 指定範囲の列と行を除外した範囲を抽出
        return array_2d[np.ix_(remaining_rows, remaining_cols)]

    # ---------------------------------------------
    #  2次元配列の要素を列単位で演算する関数
    # ---------------------------------------------
    @staticmethod
    def get_value_count_for_column(array_2d: np.ndarray, value: int, is_same: bool = True) -> np.ndarray:
        """2次元整数配列に対して、各列の値が指定値と一致する(しない)数を行単位に集計する

        Args:
            array_2d: 2次元のNumPyの整数配列    例: [[0,3,0],[0,0,9],[0,1,3]]
            value: 一致検査する値
            is_same: True:指定数と一致する数をカウント / False:指定数と一致する数をカウント
        Returns:
            np.ndarray: 各行における指定列の個数結果の一次元配列 例:[3,1,1] or [0,2,2]
        """
        # 指定数と一致する数の結果を列単位にまとめて1次元配列に変換する
        if is_same:
            res = (array_2d == value).sum(axis=0)
        else:
            res = (array_2d != value).sum(axis=0)
        return res

    @staticmethod
    def bitwise_or_columns(array_2d: np.ndarray) -> np.ndarray:
        """2次元配列に対して、各列の値をBitwise ORで集約し、1列の配列を返す

        Args:
            array_2d: shape=(n_rows, n_cols) の整数型NumPy配列 例: [[0,3,7],[0,5,9],[0,1,3]]
        Returns:
            np.ndarray: 各行に対して列方向のBitORを適用結果の一次元配列 例: [0,7,15]
        """
        return np.bitwise_or.reduce(array_2d, axis=1)

    @staticmethod
    def bitwise_and_columns(array_2d: np.ndarray) -> np.ndarray:
        """2次元配列に対して、各列の値をBitwise ANDで集約し、1列の配列を返す

        Args:
            array_2d: shape=(n_rows, n_cols) の整数型NumPy配列 例: [[0,3,7],[0,5,9],[0,1,3]]
        Returns:
            np.ndarray: 各行に対して列方向のBitORを適用結果の一次元配列 例: [0,1,3]
        """
        return np.bitwise_and.reduce(array_2d, axis=1)


# ---------------------------------------------
#  基本関数の組み合わせ関数
# ---------------------------------------------
def get_zero_count_for_array(list_2d: list[list[int]], rows: list[int] | None = None,
                             cols: list[int] | None = None) -> list[int]:
    """2次元の整数アレイ対して、指定列を抽出し、各列の値が0と一致する数を行単位に集計して返す

    Args:
        list_2d: 2次元の整数リスト
        rows: 対象行のインデックス番号リスト / None: 全行を抽出
        cols: 対象列のインデックス番号リスト / None: 全列を抽出

    Returns:
        list: 各行における指定列の0の個数のリスト
    """
    logger.trace(F"Start: {list_2d=}\t{cols=}")
    array_2d = np.array(list_2d)
    # 指定範囲を抽出
    ranged_arr = Array2d.extract_ranged_array(array_2d, rows=rows, cols=cols)
    # 0値の数を数えた結果を、リスト形式に変換する
    res = Array2d.get_value_count_for_column(ranged_arr, value=0)
    logger.trace(F"End:{type(res)} / {res=}")
    return res.tolist()
