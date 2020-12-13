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
		re_results = re.findall("\d{0,2}(\d{6})", self._archive_basename)
		for result in re_results:
			pw = result
			self._pw.append(pw)
		# パスワード2
		pw = self._latest_create_time.strftime("%y%m%d")
		self._pw.append(pw)

	def make_pw_manual(self) -> bool:
		pw_str = input()
		if pw_str == "":
			return False
		else:
			self._pw = [pw_str]
			return True

	def make_instance(self, path: str):
		return unpacker_hoge(path)


def main():
	try:
		cli_ = cli("unpack")
		if cli_.enable():
			unpacker_ = unpacker_hoge(cli_.archive_file)
			unpacker_.exec()
		return 0
	except Exception as e:
		#print(e)
		return 0


if __name__ == "__main__":
	sys.exit(main())
