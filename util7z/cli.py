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
		self.archive_file :str = ""
		self.input_file: list[str] = []

		if type == "unpack":
			self.make_arg_parser_unpack()
		else:
			self.make_arg_parser_pack()
		# コマンドライン引数解析
		try:
			self._args = self._arg_parser.parse_args()
			if type == "unpack":
				self.init_unpack()
			else:
				self.init_pack()
			self._enable = True
		except Exception as e:
			#print(e)
			pass
		except SystemExit as e:
			#print(e)
			pass


	def make_arg_parser_unpack(self) -> None:
		# コマンドライン引数設定
		self._arg_parser = argparse.ArgumentParser(description="util7z: pack/unpack 7zip archive file.")
		self._arg_parser.add_argument("archive", help="unpack target file path.")

	def make_arg_parser_pack(self) -> None:
		# コマンドライン引数設定
		self._arg_parser = argparse.ArgumentParser(description="util7z: pack/unpack 7zip archive file.")
		self._arg_parser.add_argument("-a", "--archive", required=False, help="packed new archive file name.")
		self._arg_parser.add_argument("-i", "--input", nargs="+", required=True, help="pack target file.")

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


