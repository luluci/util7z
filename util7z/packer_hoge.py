import re
import sys
import datetime
from packer import packer
from cli import cli


class packer_hoge(packer):

	def make_prefix(self):
		# prefix作成
		dt_now = datetime.datetime.now().strftime("%Y%m%d")
		self._prefix = dt_now + "_"

	def make_password(self):
		# パスワード作成
		dt_now = datetime.datetime.now().strftime("%y%m%d")
		self._pw = "hogehoge"


def main():
	try:
		cli_ = cli("pack")
		if cli_.enable():
			packer_ = packer_hoge(cli_.input_file)
			packer_.exec()
		return 0
	except Exception as e:
		print(e)
		return 0


if __name__ == "__main__":
	sys.exit(main())
