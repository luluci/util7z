import py7zr
import re
import pathlib
import datetime

class unpacker:

	def __init__(self, archive_path: str) -> None:
		"""
		7-zipファイルであればアーカイブを開く。
		暗号化ファイルであってもパスワードはまだ設定しない。
		"""
		self._archive: py7zr.SevenZipFile = None
		if (py7zr.is_7zfile(archive_path)):
			# 7zipファイルに関する情報をセット
			self._archive_path:str = archive_path
			self._archive: py7zr.SevenZipFile = py7zr.SevenZipFile(self._archive_path, "r")
			self._archive_basename: str = pathlib.Path(self._archive.filename).stem
			self._archive_dir: str = str(pathlib.Path(self._archive.filename).absolute().parent)
			if self._archive.needs_password():
				# passwordが必要であれば未復号とする。
				# archiveが復号済みかどうかは関係ない。
				self._archive_decrypted: bool = False
			else:
				# passwordが不要であれば復号済みとする
				self._archive_decrypted: bool = True
			# データ初期化
			self.clear_archive_info()
			# アーカイブ内ファイルに関する情報をセット
			self.get_archive_info()
			self.suggest_extract_to()
			# その他情報をセット
			self._tz = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
		else:
			raise Exception("'" + archive_path + "' is not 7zip file!")

	def __del__(self) -> None:
		self.close()

	def exec(self) -> bool:
		result = False
		decrypt_finish = False
		# 通知
		print(self._archive_path + " を展開します。")
		# 暗号化されているなら復号をトライ
		if not self._archive_decrypted:
			while not decrypt_finish:
				decrypt_finish = self.decrypt()
				if not decrypt_finish:
					# 復号に失敗したら手動で指定するか聞く
					print("  パスワードの推測に失敗しました：[" + ",".join(self._pw) + "]")
					print("  手動入力？(空文字で終了)：", end="")
					# 文字列が入力されたら復号をリトライ
					result = self.make_pw_manual()
					if not result:
						return False
		# アーカイブを展開
		self.extract()
		return True

	def close(self) -> None:
		if self._archive != None:
			self._archive.close()
			self._archive = None

	def clear_archive_info(self):
		"""
		アーカイブ内ファイルに関する情報を初期化
		"""
		self._item_count: int = 0
		self._dir_count: int = 0
		self._file_count: int = 0
		self._root_item_count: int = 0
		self._root_dir_count: int = 0
		self._root_file_count: int = 0
		self._root_7zip_count: int = 0
		# datetimeはUTCで保持する
		self._latest_create_time: datetime.datetime = None
		self._is_7zip_double_compress: bool = False
		self._7zip_file: str = ""
		self._is_dir_compress: bool = False
		self._extract_to: str = ""
		self._pw : list[str] = []

	def get_archive_info(self):
		if (self._archive != None):
			# アーカイブ内をチェック
			file_log_7zip: str = ""
			for file_info in self._archive.list():
				# ファイル/フォルダチェック
				self._item_count += 1
				if (file_info.is_directory):
					self._dir_count += 1
				else:
					self._file_count += 1
				# ルート要素チェック
				if (not re.match("\w+/\w+", file_info.filename)):
					self._root_item_count += 1
					# ファイル名にスラッシュが出現しない場合はrootに存在する要素とみなす
					# rootに存在するファイル/フォルダをカウントする
					if (file_info.is_directory):
						self._root_dir_count += 1
					else:
						self._root_file_count += 1
					# 圧縮ファイルチェック
					if (re.match(".+\.7z", file_info.filename)):
						self._root_7zip_count += 1
						file_log_7zip = file_info.filename
				# 日時チェック
				if (self._latest_create_time == None) or (self._latest_create_time < file_info.creationtime):
					self._latest_create_time = file_info.creationtime
			# アーカイブ内のチェック完了後、アーカイブ情報作成
			# アーカイブ内に7zipファイルだけ存在したら、2重圧縮ファイルとみなす
			if (self._root_7zip_count == 1) and (self._root_item_count == 1):
				self._is_7zip_double_compress = True
				self._7zip_file = file_log_7zip
			# ルート要素にフォルダが1つだけであれば、フォルダにまとめたファイルを圧縮しているとみなす
			if (self._root_dir_count == 1) and (self._root_file_count == 0):
				self._is_dir_compress = True

	def suggest_extract_to(self):
		"""
		展開先パスを推測する。
		アーカイブの中身がフォルダだけであればそのまま展開する。
		ファイルが含まれていればアーカイブと同じ名前のフォルダに展開する。
		"""
		if (self._archive != None):
			if (self._root_dir_count == 1) and (self._root_file_count == 0):
				# root要素にフォルダのみ存在する場合、フォルダをそのまま展開する
				self._extract_to = self._archive_dir + "\\"
			else:
				self._extract_to = self._archive_dir + "\\" + self._archive_basename + "\\"

	def decrypt(self) -> bool:
		"""
		ファイルを復号する。
		readall()を利用してpasswordが正しいかどうか判定する。
		復号に成功していたらTrueを返す。失敗していたらFalseを返す。
		"""
		# リストが空ならパスワード作成
		if not self._pw:
			self.make_pw()
		# 情報取得用にアーカイブを開いていたら閉じる
		self.close()
		# 作成したパスワードで復号をトライする
		for pw in self._pw:
			# readall()に失敗したら例外発生
			try:
				self._archive = py7zr.SevenZipFile(self._archive_path, "r", password=pw)
				self._archive.readall()
				self._archive.reset()
				self._archive_decrypted = True
			except:
				self.close()
				self._archive_decrypted = False
			# 復号に成功したら終了
			if (self._archive_decrypted):
				return True
		# 復号失敗
		return False

	def make_pw(self) -> None:
		"""
		subクラスで実装する
		"""
		pass

	def make_pw_manual(self) -> bool:
		"""
		コンソールから手動でパスワードを設定する。
		空文字が入力されたら復号キャンセルとしてFalseを返す。
		"""
		pw_str = input()
		if pw_str == "":
			return False
		else:
			self._pw = [pw_str]
			return True

	def extract(self, path:str = "") -> bool:
		result = False
		# 展開先パスを作成
		if path == "":
			path = self._extract_to
		# 通知
		print("  " + self._extract_to + " へ展開します。")
		# アーカイブが展開可能であれば展開する
		if self._archive != None and self._archive_decrypted :
			# 指定のpathへ展開
			self._archive.extractall(path)
			# 2重圧縮ファイルであれば、そのファイルも展開する
			if self._is_7zip_double_compress:
				# ファイルパスを作成
				new_file_path = path + self._7zip_file
				# ファイルを展開用インスタンスを作成
				try:
					new_instance = self.make_instance(new_file_path)
					result = new_instance.exec()
				except:
					print("今展開したファイルへのパスが間違っている。バグでは？")
					return False
			else:
				result = True
		return result

	def make_instance(self, path:str):
		# 継承先のサブクラスのインスタンスを返すメソッドを実装すること
		return unpacker(path)
