#from .util7z import unpacker_hoge
from util7z.unpacker_hoge import unpacker_hoge

try:
    unpacker = unpacker_hoge("./tests/20201213_test_dir_haspw_2.7z")
    unpacker.exec()
except:
    print("exception!")

