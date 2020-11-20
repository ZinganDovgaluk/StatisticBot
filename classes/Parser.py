class Parser:
	@classmethod
	def parse(cls, file_name):
		f = open(file_name)
		groups = f.read().split('\n')
		f.close()
		data = []
		for i in groups:
			data.append(i.split(';'))
		for k in range(len(data)):
			data[k] = [[data[k][i * 6 + j] for j in range(6)] for i in range(int(len(data[k]) / 6))]
		return data



