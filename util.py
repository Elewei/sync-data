'''
	商品数据维护清单
	第一列： 苏宁商品编码
	第二列： 商家商品编码
'''
suning_file_path = 'SuningID.txt'
taobao_file_path = 'TaobaoID.txt'


with open(suning_file_path) as suning_file:
	suningID_list = suning_file.readlines()

with open(taobao_file_path) as taobao_file:
	taobaoID_list = taobao_file.readlines()

filename = "format_data.txt"

i = 0

while i < len(suningID_list):
	data = suningID_list[i].strip() + ";" + taobaoID_list[i].strip() + "\n"
	with open(filename,'a') as file:
		file.writelines(data)
	file.close()
	i += 1

print("成功保存文件")
