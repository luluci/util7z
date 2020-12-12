import re
import sys
from unpacker import unpacker
from cli import cli

class unpacker_hoge(unpacker):
	
	def make_pw(self) -> None:
		"""
		復号用パスワードを設定する
		"""
		pw:str = ""
		# パスワード1
		re_results = re.findall("\d{2}(\d{6})", self._archive_basename)
		for result in re_results:
			pw = "hoge-" + result
			self._pw.append(pw)
		# パスワード2
		pw = "hoge-" + self._latest_create_time.strftime("%y%m%d")
		self._pw.append(pw)

	def make_instance(self, path: str):
		return unpacker_hoge(path)


def main():
	try:
		cli_ = cli()
		if cli_.unpack_ok():
			unpacker_ = unpacker_hoge(cli_.archive_file)
			unpacker_.exec()
		return 0
	except Exception as e:
		#print(e)
		return 0


if __name__ == "__main__":
	sys.exit(main())
