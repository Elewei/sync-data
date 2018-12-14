# -*- coding: utf-8 -*-
"""
作者：张启卫
时间：2018年11月12号
功能：苏宁与淘宝中商品信息(颜色与尺码)的同步。

软件环境搭建：
1. python3.7 版本
2. BeautifulSoup4
	pip install beautifulsoup4
3. lxml 解析库
	pip install lxml
4. request
	pip install requests
5. selenium
	pip install selenium
6. pywin32
	pip install pywin32
7. pyHook
8. PyUserInput
	pip install PyUserInput
9. geckodriver
10. pyInstaller
11. Pillow 图片库
	pip install Pillow
"""

import re
import json
import configparser
from PIL import Image
from taobao import Taobao
from suning import Suning


# 加载配置文件
config = configparser.ConfigParser()

# 写入配置文件
config.read('conf.ini', encoding='utf-8')

# 折扣比例
price_cent = config['config']['price_cent']
data_file_path = config['config']['data_file_path']
upload_image_seconds = config['config']['upload_image_seconds']
# cookie_str = config['config']['cookie_str']

# 读取苏宁商品ID
with open(data_file_path, encoding='utf-8') as data_file:
	data_file_list = data_file.readlines()

'''
	商品数据维护清单
	第一列： 苏宁商品编码
	第二列： 商家商品编码
	[
		{10689230727:527122606845},
		{},
		...
	]
'''
# 初始化
data = []

# 导入数据
i = 0
while i < len(data_file_list):
	product_id = {}
	data_str_list = data_file_list[i].split(';')
	key = data_str_list[0].strip()
	value = data_str_list[1].strip()
	product_id[key] = value
	data.append(product_id)
	i += 1

# Todo1： 将failed_sync_data文件清空
# Todo2: 将日志写入日志文件

# 循环查找data中所有条目
for i in range(len(data)):
	# 对单个商品信息进行处理
	for suning_productCode, taobao_id in data[i].items():
		sync_failed_data = {}
		try:	
			# 初始并实例化淘宝商品类
			taobao = Taobao(taobao_id)

			taobao_product_url = taobao.get_taobao_product_url()
			taobao_mdskip_url = taobao.get_taobao_product_mdskip_url()
			headers = taobao.get_taobao_product_headers()
			# 淘宝商品由 PVS: {颜色，尺码，价格，库存，折扣，照片}
			taobao_products = {}
			# 淘宝颜色由
			taobao_colors = {}
			taobao_sizes = {}

			# 初始并实例化苏宁商品类
			suning = Suning(suning_productCode)
			suning_product_url = suning.get_suning_product_url()
			suning_products = {}

			# 获取淘宝页面信息
			soup = taobao.get_taobao_page(taobao_product_url)

			# 获取淘宝data数据
			product_json = taobao.get_taobao_product_json_data(soup)
			print("打印淘宝商品数据：")
			print(product_json)
			print("\n\n")
			
			#获取淘宝setMdskip数据
			setMdskip_json = taobao.get_taobao_setmdskip_data(taobao_mdskip_url, headers)
			print("打印淘宝setMDskip数据：")
			print(setMdskip_json)
			print("\n\n")

			if setMdskip_json == None:
				print("Cookie 信息过期")
				break

			#处理setMdskip_json数据
			setMdskip_data = json.loads(setMdskip_json)
			priceInfo = setMdskip_data['defaultModel']['itemPriceResultDO']['priceInfo']
			skuQuantity = setMdskip_data['defaultModel']['inventoryDO']['skuQuantity']

			# 处理product_json数据
			json_data = json.loads(product_json)
			skuList = json_data['valItemInfo']['skuList']
			skuMap = json_data['valItemInfo']['skuMap']
			propertyPics = json_data['propertyPics']

			# 获取淘宝商品信息
			for list in skuList:
				# 初始化一个淘宝商品项目
				taobao_item = []
				
				str_names = list['names']
				names_list = str_names.split()
				if len(names_list) != 1:
					# 获取淘宝商品尺码
					size = names_list[0]
					# 获取淘宝商品颜色
					color = names_list[1]
				else:
					# 获取淘宝商品尺码
					size = ""
					# 获取淘宝商品颜色
					color = names_list[0]
					
				# 获取淘宝商品的key
				str_pvs = list['pvs']
				pvs_list = str_pvs.split(';')
				if len(pvs_list) != 1:
					# 获取淘宝尺码pvs
					taobao_sizes[pvs_list[0]] = size
					# 获取淘宝颜色pvs
					taobao_colors[pvs_list[1]] = color
				else:
					# 获取淘宝颜色pvs
					taobao_colors[pvs_list[0]] = color				
				
				# 获取skuMap中pvs的key
				pvs = ";" + list['pvs'] + ";"
				
				if len(pvs_list) != 1:
					# 获取淘宝照片key
					pic_key = ";" + pvs_list[1] + ";"
				else:
					# 获取淘宝照片key
					pic_key = ";" + pvs_list[0] + ";"
				
				#获取skuID
				skuId = list['skuId']
				
				try:
					# 获取淘宝照片URL
					taobao_image_url = "https:" + propertyPics[pic_key][0]
				except:
					taobao_image_url = ""
					if len(pvs_list) != 1:
						# 获取淘宝尺码pvs
						del taobao_sizes[pvs_list[0]]
						# 获取淘宝颜色pvs
						del taobao_colors[pvs_list[1]]
					else:
						# 获取淘宝颜色pvs
						del taobao_colors[pvs_list[0]]
					continue		
				
				try:
					# 输入商品折扣，计算商品rel_price, 一种情况
					rel_price = round(float(priceInfo[skuId]['promotionList'][0]['price']) * float(price_cent), 2)
				except:
					# 输入商品折扣，计算商品rel_price， 第二种情况
					rel_price = round(float(priceInfo[skuId]['price']) * float(price_cent), 2)

				# 淘宝项目中添加 颜色
				taobao_item.append(color)
				# 淘宝项目中添加 尺码
				taobao_item.append(size)
				# 淘宝项目中添加 价格
				taobao_item.append(skuMap[pvs]['price'])
				# 淘宝项目中添加 库存
				taobao_item.append(skuQuantity[skuId]['quantity'])
				# 淘宝项目中添加 折扣
				taobao_item.append(skuMap[pvs]['priceCent'])
				# 淘宝项目中添加 照片路径
				taobao_item.append(taobao_image_url)
				# 淘宝项目中添加 促销价
				taobao_item.append(rel_price)
				# 淘宝项目中添加 skuID
				taobao_item.append(skuId)
				# 最后将单个淘宝项目添加入淘宝商品项中，key为PVS
				taobao_products[str_pvs] = taobao_item


			# 打印当前淘宝商品颜色
			print("打印当前淘宝商品颜色")
			print(taobao_colors)
			print("\n\n")

			# 打印当前淘宝商品尺码
			print("打印当前淘宝商品尺码")
			print(taobao_sizes)
			print("\n\n")

			# 打印当前淘宝商品信息
			print("打印当前淘宝商品信息")
			print(taobao_products)
			print("\n\n")


			# 获取本地Firefox sessionID 且复用
			if i == 0:
				driver = suning.get_local_firefox_driver()
				suning_url = "https://sop.suning.com/sel/tradeCenter/showMainTradeCenter.action?version=newTrad"
				driver.get(suning_url)
				browser = suning.create_driver_session(driver.session_id, driver.command_executor._url)

				# 延迟80s，等待登录
				suning.delay_time( 80 )
			else:
				# 延迟2s，等待页面加载
				suning.delay_time( 2 )
			
			# 跳转到苏宁编辑商品链接
			browser.get(suning_product_url)

			# 延迟3s，等待页面加载
			suning.delay_time( 3 )

			# 获取苏宁商品颜色
			suning_products['color'] = suning.get_suning_product_color(browser)

			# 获取苏宁商品尺码
			suning_products['size'] = suning.get_suning_product_size(browser)

			# 比较苏宁淘宝商品颜色
			add_color = suning.compare_taobao_suning_color(taobao_colors, suning_products['color'])

			# 比较苏宁淘宝商品尺码
			add_size = suning.compare_taobao_suning_size(taobao_sizes, suning_products['size'])

			# 下载需要添加颜色的照片且修改照片信息
			# 照片命名格式 img\taobao_id_position.jpg
			if taobao_sizes:
				first_size_key = taobao.get_taobao_frist_size_key(taobao_sizes)
			current_dir = taobao.get_current_dir()
			add_color_remove = []
			for color, key in add_color.items():
				str_key = re.sub("[:]", "", key)
				image_name = str(taobao_id) + "_" + str_key + ".jpg"
				image_path = current_dir + "\img\\" + image_name
				if taobao_sizes:
					image_key = first_size_key + ";" + key
				else:
					image_key = key
				if image_key in taobao_products:
					taobao.download_taobao_image(taobao_products[image_key][5], image_path)
				else:
					add_color_remove.append(color)
					continue
				im = Image.open(image_path)
				rgb_im = im.convert('RGB')
				(x, y) = rgb_im.size
				if (x < 800 or y < 800):
					if (x < y):
						x_s = 1000
						y_s = y * x_s / x
						out = rgb_im.resize((x_s,int(y_s)),Image.ANTIALIAS)
						out.save(image_path)
					else:
						y_s = 1000
						x_s = x * y_s / y
						out = rgb_im.resize((int(x_s),y_s),Image.ANTIALIAS)
						out.save(image_path)
				add_color[color] = image_path

			for color in add_color_remove:
				del add_color[color]
			
			print("修改后add_color:")
			print(add_color)

			# 添加苏宁商品颜色
			suning.add_suning_product_color(browser, add_color)

			# 添加苏宁商品尺码
			suning.add_suning_product_size(browser, add_size)

			# 填写商品价格与库存
			suning.add_suning_product_sku(browser, add_color, suning_products['size'], add_size, suning_products['color'],
											taobao_products, taobao_colors, taobao_sizes)

			# 上传苏宁颜色照片
			if len(suning_products['color']) != 0 and len(suning_products['size']) != 0:
				suning.upload_suning_product_image(browser, add_color, suning_products['size'][0], upload_image_seconds)
			elif len(suning_products['color']) != 0:
				suning.upload_suning_product_image_no_size(browser, add_color, upload_image_seconds)
				
			# 延迟2s，等待登录
			suning.delay_time( 2 )

			# 点击上传保存
			browser.find_element_by_id("saveOrUpdateBtn").click()
				
			# 延迟5s，等待保存
			suning.delay_time( 5 )

			# 删除img目录下面所有照片
			image_path = current_dir + "\img\\"
			try:
				taobao.delete_image(image_path)
			except:
				continue

			# 返回首页
			#browser.get("https://sop.suning.com/sel/tradeCenter/showMainTradeCenter.action")
		
		except:
			taobao.failed_data_save("failed_sync_data.txt", suning_productCode, taobao_id)
			continue
