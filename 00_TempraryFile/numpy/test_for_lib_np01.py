"""
概要: テストスクリプト
検証結果: OK 2025/09/07
"""

from time import sleep

# テスト対象ライブラリ
from lib_numpy.lib_np01 import get_zero_count_for_array
from loguru import logger


# ===================================
#    テストコード
# ===================================
test_cases_01 = [
    {
        "array_2d": [[0, 1, 0, 3], [4, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
        "rows": None,
        "cols": [0, 1, 2, 3],
        "expected": [3, 3, 2, 1],
    },
    {
        "array_2d": [[0, 1, 0, 3], [4, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
        "rows": [0, 1, 2, 3],
        "cols": [0, 1, 3],
        "expected": [3, 3, 1],
    },
    {
        "array_2d": [[0, 1, 0, 3], [4, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
        "rows": [1],
        "cols": [0, 1, 3],
        "expected":[0, 1, 1],
    },
]


def test1():
    print(F'1. get_zero_count_for_array')
    sleep(0.5)
    for i, case in enumerate(test_cases_01):
        array_2d = case["array_2d"]
        cols = case["cols"]
        rows = case["rows"]
        ex1 = case["expected"]
        logger.info(f"==== Test Case {i + 1} ======")
        logger.info(f"Input:{rows=}\t{cols=}\t{array_2d=}")
        res1 = get_zero_count_for_array(array_2d, rows=rows, cols=cols)
        logger.info(F"get_zero_count_for_array(array_2d, rows=rows, cols=cols)={res1}")
        is_ok1 = (res1 == ex1)
        if is_ok1:
            logger.success(F"{ex1=}\t\t{is_ok1=}")
        else:
            logger.error(F"{ex1=}\t\t{is_ok1=}")
        logger.info(f"==== End of Test Case {i + 1} ======")



# -----------------------------------------------
# テストメイン
# -----------------------------------------------
def test_main(test_list):
    for test_id in test_list:
        try:
            print(F'\n######  test_id={test_id}  #########')
            exec(F"test{test_id}()")
        except NameError as e:
            print(F"\n*** Exception:{type(e)}\ttest_idエラー:{test_id}")


# -----------------------------------------------
# コマンドラインからの実行
# -----------------------------------------------
if __name__ == "__main__":
    test_id_list = [1]
    test_main(test_id_list)
