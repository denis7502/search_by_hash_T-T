from TikTokApi import TikTokApi
import pandas as pd

class GetInfo():

	def __init__(self, custom_verifyFp, count, hashtag):
		# Данные куки для использования Тик-Ток Api
		# Количество постов для возвращения
		# Хэштэг для поиска
		self.hashtag = hashtag
		self.count = count
		self.frame = pd.DataFrame()
		self.api = TikTokApi.get_instance(custom_verifyFp = "%s"%(custom_verifyFp))

	def getRow(self, row:dict, new_row:dict, prefix = '') -> dict:
		# Получает словарь ответ от API Тик-Ток и трансформирует его в строку для добавления в Дата фрейм
		if prefix != '':
			prefix += '_'
		for key in row.keys():
			if isinstance(row[key], dict):
				prefix = key
				new_row = self.getRow(row[key], new_row, prefix = prefix)
			elif isinstance(row[key], list):
				for k, i in enumerate(row[key]):
					if isinstance(i, dict):
						prefix = key + str(k)
						new_row = self.getRow(row[key][k], new_row, prefix = prefix)
					else:
						if isinstance(row[key][k], int):
							new_row[prefix + key] = str(row[key][k])
						else:
							if isinstance(row[key], str):
								new_row[prefix + key] = row[key][k]
							else:
								new_row[prefix + key] = row[key][k]
						
			else:
				if isinstance(row[key], int):
					new_row[prefix + key] = str(row[key])
				else:
					if isinstance(row[key], str):
						new_row[prefix + key] = row[key]
					else:
						new_row[prefix + key] = row[key]

		return new_row

	def _clearFrame(self, row):
		# Очищает строку от переносов строки
		for k, i in enumerate(row):
			if isinstance(row.iloc[k], str):
				row.iloc[k] = row.iloc[k].replace('\n', '')
		return row


	def createFrame(self):
		# Создает запрос поиска по хэштегу и трансформирует ответ в Датафрейм
		try:
			self.ticToks = self.api.by_hashtag(count = self.count, hashtag = self.hashtag)
		except:
			print("Ошибка API перезапуститте программу")
			exit()
		if self.ticToks:
			for ind, ticTok in enumerate(self.ticToks):
				new_row = {}
				self.frame = self.frame.append(self.getRow(ticTok, new_row), ignore_index = True)
		self.frame = self.frame.apply(self._clearFrame)
			
	def saveFrame(self, nameFile):
		# Сохраняет фрейм в текстовый файл
		self.frame.to_csv('%s.csv'%(nameFile), index = False, sep = ';', encoding = 'utf-8')

sber = GetInfo("verify_kz3tsdp6_iK5iiClW_VaND_4CoK_8oXB_j6Lm3hVVZ3y2",
				30,
				'Сбер'
	)
sber.createFrame()
sber.saveFrame('hastag_sber')
