import sys

class cli:
	"""
	CommandLine Interface
	"""

	def __init__(self):
		self.py_file = sys.argv[0]
		if len(sys.argv) >= 2:
			# 最初の引数をアーカイブファイルの指定とする
			self.archive_file: str = sys.argv[1]
			self.__unpack_ok: bool = True
			# 2番目以降の引数は、ファイル圧縮であれば圧縮対象ファイルとする
			self.append_file: list[str] = []
			for arg in sys.argv[2:]:
				self.append_file.append(arg)
				self.__pack_ok: bool = True
		else:
			print("too few argument.")
			print("Usage:")
			print("  unpack: " + self.py_file + " <archive_file>")
			print("    pack: " + self.py_file + " <archive_file> <pack_file1> [<pack_file2> ...]")
			raise Exception("too few argument.")

	def unpack_ok(self) -> bool:
		return self.__unpack_ok

	def pack_ok(self) -> bool:
		return self.__pack_ok
