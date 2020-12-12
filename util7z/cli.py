import sys
import argparse

class cli:
	"""
	CommandLine Interface
	"""

	def __init__(self, type:str):
		check:bool = False
		self.py_file = sys.argv[0]
		self._enable = False

		if type == "unpack":
			check = self.make_arg_parser_unpack()
			if check:
				self.init_unpack()
				self._enable = True
		else:
			check = self.make_arg_parser_pack()
			if check:
				self.init_pack()
				self._enable = True


	def make_arg_parser_unpack(self) -> bool:
		# コマンドライン引数設定
		self._arg_parser = argparse.ArgumentParser(description="util7z: pack/unpack 7zip archive file.")
		self._arg_parser.add_argument("archive", help="unpack target file path.")
		# コマンドライン引数解析
		try:
			self._args = self._arg_parser.parse_args()
			return True
		except:
			return False

	def make_arg_parser_pack(self) -> bool:
		# コマンドライン引数設定
		self._arg_parser = argparse.ArgumentParser(description="util7z: pack/unpack 7zip archive file.")
		self._arg_parser.add_argument("-a", "--archive", required=False, help="packed new archive file name.")
		self._arg_parser.add_argument("-i", "--input", nargs="+", help="pack target file.")
		# コマンドライン引数解析
		try:
			self._args = self._arg_parser.parse_args()
			return True
		except:
			return False

	def init_unpack(self) -> None:
		self.archive_file = self._args.archive

	def init_pack(self) -> None:
		self.archive_file = self._args.archive
		self.input_file = self._args.input

	def enable(self) -> bool:
		return self._enable


if __name__ == "__main__":
	cli_ = cli("unpack")
	#cli_ = cli("pack")


