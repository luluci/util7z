import pathlib
import py7zr

class packer:

	def __init__(self, input_file) -> None:
		self._input_file: list[str] = input_file

	def exec(self, archive:str = "") -> None:
		# アーカイブファイル名を作成
		if archive == "":
			self.suggest_archive_name()
		else:
			path = pathlib.Path(archive)
			self._archive_name = path.stem
			self._archive_to = str(path.parent)
			self._archive_ext = path.suffix
		# 接頭辞を作成
		self.make_prefix()
		# ファイル名重複チェック
		self.check_duplicate()
		# パスワード作成
		self.make_password()
		# 圧縮フィルタ作成
		self.make_fileter()
		# アーカイブファイル作成
		self.make_archive()


	def suggest_archive_name(self) -> None:
		# ファイル情報初期化
		self._item_count: int = 0
		self._dir_count: int = 0
		self._file_count: int = 0
		self._archive_name: str = ""
		self._archive_to: str = ""
		# 一時変数
		path: pathlib.Path = None
		# ファイルチェック
		for file in self._input_file:
			self._item_count += 1
			path = pathlib.Path(file)
			# ファイル/フォルダチェック
			if path.is_dir():
				self._dir_count += 1
			else:
				self._file_count += 1
		# アーカイブネーム判定
		# フォルダが1つだけ指定されていればその名前を使用、同フォルダ内にアーカイブファイル作成
		# その他は最初に指定された引数の親フォルダ名、親フォルダ内にアーカイブファイル作成
		if (self._dir_count == 1) and (self._item_count == 1):
			self._archive_name = path.stem
			self._archive_to = str(path.parent)
			self._archive_ext = ".7"
		else:
			path = pathlib.Path(self._input_file[0])
			self._archive_name = path.parent.stem
			self._archive_to = str(path.parent)
			self._archive_ext = ".7"

	def make_prefix(self):
		# 派生クラスでprefix作成
		self._prefix = ""

	def check_duplicate(self):
		dup_checked:bool = False
		next_id: int = 1
		new_arc_name: str = self._archive_name
		while not dup_checked:
			# 設定したパスをチェック
			# 重複していたら適当にサフィックスを付ける
			path = pathlib.Path( self._archive_to + "\\" + self._prefix + new_arc_name + self._archive_ext )
			if path.exists():
				next_id += 1
				new_arc_name = self._archive_name + "_" + str(next_id)
			else:
				self._archive_name = new_arc_name
				dup_checked = True

	def make_password(self):
		# 派生クラスでパスワード作成
		self._pw:str = ""

	def make_fileter(self):
		# 派生クラスで圧縮フィルタ作成
		self._filter = [
			#{'id': py7zr.FILTER_X86},
			#{'id': py7zr.FILTER_LZMA2, 'preset': py7zr.PRESET_DEFAULT},
			{'id': py7zr.FILTER_CRYPTO_AES256_SHA256}
		]

	def make_archive(self):
		# 作成ファイルパス作成
		path = pathlib.Path( self._archive_to + "\\" + self._prefix + self._archive_name + self._archive_ext )
		# 情報通知
		print("アーカイブファイルを作成します")
		print("  ファイル：" + str(path))
		if self._pw != "":
			print("  PassWord：" + self._pw)
		# アーカイブ作成
		try:
			archive = py7zr.SevenZipFile(path, 'w', filters=self._filter, dereference=True, password=self._pw)
		except Exception as e:
			print(e)
			return 
		for file in self._input_file:
			try:
				temp_path = pathlib.Path(file)
				if temp_path.is_dir():
					archive.writeall(file, temp_path.name)
				else:
					archive.write(file, temp_path.name)
			except Exception as e:
				print(e)
		archive.close()
