import py7zr
import pathlib
import datetime

# タイムゾーンの生成
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

latest_date:datetime.datetime = None
#with py7zr.SevenZipFile("./tests/20201209_test.7z", "r", password="hoge-201209") as archive:
with py7zr.SevenZipFile("./tests/20201211_test_dir_double_haspw_11112233.7z", "r", password="hoge-201211") as archive:
	#extract_nofile_filter = [None if True for f in allfiles]
	#archive.extractall(".\\tests\\tmp")
	archive.readall()
	archive.extractall("D:\\home\\Python\\util7z\\tests\\tmp")

	print(archive.filename)
	print(pathlib.Path(archive.filename).stem)
	#print(pathlib.Path(archive.filename).absolute().stem)
	#print(pathlib.Path(archive.filename).parent)
	#print(pathlib.Path(archive.filename).absolute().parent)
	print(str(pathlib.Path(archive.filename).parent))
	print(archive.getnames())
	print(archive.needs_password())
	#print( archive.archiveinfo() )
	#print( archive.list() )
	for file_info in archive.list():
		print(file_info.filename)
		print(file_info.is_directory)
		print(file_info.creationtime)
		print(file_info.compressed)
		print(file_info.uncompressed)
		if (latest_date == None) or (latest_date < file_info.creationtime):
			latest_date = file_info.creationtime

print("")
print("TZ conv to:")
print(latest_date)
latest_date = latest_date.astimezone(JST)
print(latest_date)
print(latest_date.strftime("%y%m%d"))
