import time
import random
from PIL import Image
from selenium import webdriver
from pykeyboard import PyKeyboard
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

# 上传照片间隔
seconds = 2

class Suning():
	'''苏宁类'''

	def __init__(self, id):
		'''' 初始化苏宁属性 '''
		self.id = id

	def get_local_firefox_driver(self):
		'''获取本地Firefox sessionID'''
		driver = webdriver.Firefox(executable_path="geckodriver.exe")
		print("成功获取本地Firefox 驱动信息")
		print("Session ID: " + driver.session_id + "执行路径 " + driver.command_executor._url)
		return driver

	def create_driver_session(self, session_id, executor_url):
		'''复用本地Firefox sessionID'''
		# 保存原使执行路径
		org_command_execute = RemoteWebDriver.execute

		def new_command_execute(self, command, params=None):
			if command == "newSession":
				# 模拟返回值
				return {'success': 0, 'value': None, 'sessionId': session_id}
			else:
				return org_command_execute(self, command, params)
		# 调用新的执行路径
		RemoteWebDriver.execute = new_command_execute
		new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
		new_driver.session_id = session_id

		# 替换原有执行路径
		RemoteWebDriver.execute = org_command_execute
		print("成功复用火狐浏览器session")
		return new_driver

	def get_suning_product_url(self):
		""" 获取苏宁商品链接 """
		suning_url = "https://mcmp.suning.com/mcmp/cmPublish/queryCmInfo.htm?productCode=" + str(self.id)
		print("苏宁商品链接：" + suning_url)
		return suning_url

	def delay_time(self, seconds):
		""" 时间延迟函数 """
		while seconds > 0:
			print("延迟 " + str(seconds) + " 秒")
			seconds -= 1
			time.sleep(1)
		print("延迟等待结束！")

	def get_suning_product_color(self, browser):
		""" 获取苏宁商品颜色 """
		suning_colors = []
		color_level = 1
		css_selector = "tr[desc=颜色]>td.laign>div.yanse>div>div:nth-of-type(" + str(color_level) +  ")>input"
		try:
			suning_color = browser.find_element_by_css_selector(css_selector).get_attribute("value")
			suning_colors.append(suning_color)
		except:
			print("成功获取苏宁商品颜色: ")
			print(suning_colors)
			return suning_colors		
			
		while suning_color != 'NULL':
			color_level += 1
			css_selector = "tr[desc=颜色]>td.laign>div.yanse>div>div:nth-of-type(" + str(color_level) +  ")>input"
			try:
				suning_color = browser.find_element_by_css_selector(css_selector).get_attribute("value")
				suning_colors.append(suning_color)
			except:
				suning_color = "NULL"
				break

		print("成功获取苏宁商品颜色: ")
		print(suning_colors)
		return suning_colors

	def get_suning_product_size(self, browser):
		""" 获取苏宁商品尺码 """
		suning_sizes = []
		size_level = 1
		css_selector = "tr[desc=尺码]>td.laign>div.yanse>div>div:nth-of-type(" + str(size_level) +  ")>input"
		try:
			suning_size = browser.find_element_by_css_selector(css_selector).get_attribute("value")
			suning_sizes.append(suning_size)
		except:
			print("成功获取苏宁商品尺码: ")
			print(suning_sizes)
			return suning_sizes

		while suning_size != 'NULL':
			size_level += 1
			css_selector = "tr[desc=尺码]>td.laign>div.yanse>div>div:nth-of-type(" + str(size_level) +  ")>input"
			try:
				suning_size = browser.find_element_by_css_selector(css_selector).get_attribute("value")
				suning_sizes.append(suning_size)
			except:
				suning_size = "NULL"
				break

		print("成功获取苏宁商品尺码: ")
		print(suning_sizes)
		return suning_sizes

	def compare_taobao_suning_color(self, taobao_colors, suning_colors):
		''' 比较苏宁淘宝颜色 '''
		ret = {}
		flag = 1
		for key, taobao_color in taobao_colors.items():
			for suning_color in suning_colors:
				if taobao_color == suning_color:
					flag = 0
					continue

			if flag == 1:
				ret.update({taobao_color:key})
				flag = 0
			flag = 1

		print("应该添加苏宁商品的颜色: ")
		print(ret)
		return ret

	def compare_taobao_suning_size(self, taobao_sizes, suning_sizes):
		''' 比较苏宁淘宝尺码 '''
		ret = {}
		flag = 1
		for key, taobao_size in taobao_sizes.items():
			for suning_size in suning_sizes:
				if taobao_size == suning_size:
					flag = 0
					continue

			if flag == 1:
				ret.update({taobao_size:key})
				flag = 0
			flag = 1

		print("应该添加苏宁商品的尺码: ")
		print(ret)
		return ret

	def get_suning_product_price(self, browser, color, size):
		""" 获取苏宁商品价格 """
		css_selector = "tr[key='" + color + "^"+ size + "']>td.saleprice>div>input"
		price = browser.find_element_by_css_selector(css_selector).get_attribute("value")
		return price


	def add_suning_product_color(self, browser, add_color):
		''' 添加苏宁商品颜色 '''
		css_selector_add_color = "tr[desc='颜色']>td.laign>div.addysbox>div.clearfix>span>input"
		css_selector_color_click = "tr[desc='颜色']>td.laign>div.addysbox>div.clearfix>a"
		for color in add_color.keys():
			try:
				browser.find_element_by_css_selector(css_selector_add_color).send_keys(color)
				browser.find_element_by_css_selector(css_selector_color_click).click()
			except:
				return
		return

	def add_suning_product_size(self, browser, add_size):
		''' 添加苏宁商品尺码 '''
		css_selector_add_size = "tr[desc='尺码']>td.laign>div.addysbox>div.clearfix>span>input"
		css_selector_size_click = "tr[desc='尺码']>td.laign>div.addysbox>div.clearfix>a"
		for size in add_size:
			try:
				browser.find_element_by_css_selector(css_selector_add_size).send_keys(size)
				browser.find_element_by_css_selector(css_selector_size_click).click()
			except:
				return
		return

	def add_suning_product_highlight(self, browser):
		''' 添加苏宁商品亮点 '''
		highlightWord = ["时尚休闲", "靓丽气质", "大气时尚", "气质", "时尚百搭", "通勤日常", "显身材", "提高气质", "大方得体", "休闲百搭", "通勤", "居家日常", "舒适", "合身", "得体", "大方", "日常搭配", "百搭", "青春气息", "休闲"]
		browser.find_element_by_id("highlightWord1").clear()
		browser.find_element_by_id("highlightWord1").send_keys(random.choice(highlightWord))
		browser.find_element_by_id("highlightWord2").clear()
		browser.find_element_by_id("highlightWord2").send_keys(random.choice(highlightWord))
		browser.find_element_by_id("highlightWord3").clear()
		browser.find_element_by_id("highlightWord3").send_keys(random.choice(highlightWord))
		browser.find_element_by_id("promd").clear()
		promd = "全店满99-6，199-20，关注店铺优惠惊喜不断，任何疑问都请联系"
		browser.find_element_by_id("promd").send_keys(promd)
		return		
		
	def upload_suning_product_image(self, browser, add_color, size, upload_image_seconds):
		''' 上传苏宁商品照片 '''
		for color, image_path in add_color.items():
			pyk = PyKeyboard()
			css_selector = "tr[key='" + color + "^"+ size + "']>td.colortd>div.colorbox>div.lcolor>a.colorup>a"
			ele = browser.find_element_by_css_selector(css_selector)
			ele.location_once_scrolled_into_view
			ele.click()
			time.sleep(2)
			pyk.type_string(image_path)
			time.sleep(int(upload_image_seconds))
			try:
				pyk.tap_key(pyk.enter_key)
			except:
				pyk.press_key(pyk.alt_key)
				pyk.tap_key(pyk.function_keys[4])
				pyk.release_key(pyk.alt_key)
				upload_suning_product_image(self, browser, add_color, size)
				print("颜色：" + color + "照片: " + image_path + " 上传失败")
				print("重新开始上传...")
			time.sleep(seconds)
			print("颜色：" + color + "照片: " + image_path + " 上传成功")
		return

	def upload_suning_product_image_no_size(self, browser, add_color, upload_image_seconds):
		''' 上传苏宁商品照片, 没有size的情况 '''
		for color, image_path in add_color.items():
			pyk = PyKeyboard()
			css_selector = "tr[key='" + color + "']>td.colortd>div.colorbox>div.lcolor>a.colorup>a"
			ele = browser.find_element_by_css_selector(css_selector)
			ele.location_once_scrolled_into_view
			ele.click()
			time.sleep(2)
			pyk.type_string(image_path)
			time.sleep(int(upload_image_seconds))
			try:
				pyk.tap_key(pyk.enter_key)
			except:
				pyk.press_key(pyk.alt_key)
				pyk.tap_key(pyk.function_keys[4])
				pyk.release_key(pyk.alt_key)
				upload_suning_product_image(self, browser, add_color, size)
				print("颜色：" + color + "照片: " + image_path + " 上传失败")
				print("重新开始上传...")
			time.sleep(seconds)
			print("颜色：" + color + "照片: " + image_path + " 上传成功")
		return

	def process_background_img(self, background_path, img_path, current_dir):
		''' 处理背景照片信息 '''
		background = Image.open(background_path)
		background = background.convert('RGBA')
		
		img = Image.open(img_path)
		img = img.convert('RGBA')
		
		out_img = Image.blend(background, img,0.5)
		image_path = current_dir + "\img\\" + "background.png"
		out_img.save(image_path)
		return image_path
		
		
	def upload_suning_product_background_img(self, browser, img_path):
		''' 上传苏宁背景照片信息 '''

		pyk = PyKeyboard()
		css_selector = "tr>td.laign>div>div.adoptm>ul.propic>li.ywxpic>div#file_transparent_upload1>a.uploadfive-button"
		ele = browser.find_element_by_css_selector(css_selector)
		ele.location_once_scrolled_into_view
		ele.click()
		time.sleep(2)
		pyk.type_string(img_path)
		time.sleep(2)
		try:
			pyk.tap_key(pyk.enter_key)
		except:
			pyk.press_key(pyk.alt_key)
			pyk.tap_key(pyk.function_keys[4])
			pyk.release_key(pyk.alt_key)
			upload_suning_product_background_img(self, browser)
			print(" 背景图片上传失败")
			print("重新开始上传...")
		time.sleep(seconds)
		print("背景上传成功")
		return
		
	def delete_suning_product_color(self):
		return

	def add_suning_product_sku(self, browser, add_color, suning_size, add_size, suning_color,
								taobao_products, taobao_colors, taobao_sizes):
		''' 填写添加商品的颜色与尺码的SKU '''
		if len(suning_size) != 0 and len(suning_color) !=0:
			first_sku_saleprice_selector = "tr[key='" + suning_color[0] + "^"+ suning_size[0] + "']>td.saleprice>div>input"
		elif len(suning_size) !=0 :
			first_sku_saleprice_selector = "tr[key='"+ suning_size[0] + "']>td.saleprice>div>input"
		elif len(suning_color) != 0:
			first_sku_saleprice_selector = "tr[key='" + suning_color[0] + "']>td.saleprice>div>input"			
		else:
			first_sku_saleprice_selector = "tr>td.saleprice>span>input"			
		
		for color in add_color.keys():
			if color in taobao_colors.values():
				color_key = list(taobao_colors.keys())[list (taobao_colors.values()).index (color)]
			else:
				color_key = '0'
			
			if len(suning_size) != 0 and len(suning_color) != 0:
				for size, size_key in add_size.items():
					css_selector_saleprice = "tr[key='" + color + "^"+ size + "']>td.saleprice>div>input"
					css_selector_salekuc = "tr[key='" + color + "^"+ size + "']>td.salekuc>div>input"
					taobao_products_key = size_key + ";" + color_key
					if taobao_products_key in taobao_products:
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
					else:
						saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
						salekuc = 0
					browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
					browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))

				''' 填写添加商品的已有尺码的SKU '''
				for size in suning_size:
					if size in taobao_sizes.values():
						size_key = list(taobao_sizes.keys())[list (taobao_sizes.values()).index (size)]
					else:
						size_key = '0'
					css_selector_saleprice = "tr[key='" + color + "^"+ size + "']>td.saleprice>div>input"
					css_selector_salekuc = "tr[key='" + color + "^"+ size + "']>td.salekuc>div>input"
					taobao_products_key = size_key + ";" + color_key
					if taobao_products_key in taobao_products:
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
					else:
						saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
						salekuc = 0
					browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
					browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))
			elif len(suning_color) != 0:
				if taobao_sizes:
					for size_key in taobao_sizes.keys():
						css_selector_saleprice = "tr[key='" + color + "']>td.saleprice>div>input"
						css_selector_salekuc = "tr[key='" + color + "']>td.salekuc>div>input"
						taobao_products_key = size_key + ";" + color_key	
						if taobao_products_key in taobao_products:
							saleprice = taobao_products[taobao_products_key][6]
							salekuc = taobao_products[taobao_products_key][3]
						else:
							saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
							salekuc = 0
						browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
						browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))
						break
				else:
					css_selector_saleprice = "tr[key='" + color + "']>td.saleprice>div>input"
					css_selector_salekuc = "tr[key='" + color + "']>td.salekuc>div>input"
					taobao_products_key = color_key	
					if taobao_products_key in taobao_products:
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
					else:
						saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
						salekuc = 0
					browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
					browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))	
			else:
				if taobao_colors:
					css_selector_saleprice = "tr>td.saleprice>span>input"
					css_selector_salekuc = "tr>td.salekuc>span>input"
					for color_key in taobao_colors.keys():
						taobao_products_key = color_key	
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
						break;
				
			
		''' 填写已有商品的颜色与尺码的SKU '''
		for color in suning_color:
			if color in taobao_colors.values():
				color_key = list(taobao_colors.keys())[list (taobao_colors.values()).index (color)]
			else:
				color_key = '0'
			
			if len(suning_size) != 0:
				for size, size_key in add_size.items():
					css_selector_saleprice = "tr[key='" + color + "^"+ size + "']>td.saleprice>div>input"
					css_selector_salekuc = "tr[key='" + color + "^"+ size + "']>td.salekuc>div>input"
					taobao_products_key = size_key + ";" + color_key
					if taobao_products_key in taobao_products:
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
					else:
						saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
						salekuc = 0					
					browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
					browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))

				''' 更新已有商品价格与库存 '''
				for size in suning_size:
					if size in taobao_sizes.values():
						size_key = list(taobao_sizes.keys())[list (taobao_sizes.values()).index (size)]
					else:
						size_key = '0'
					css_selector_saleprice = "tr[key='" + color + "^"+ size + "']>td.saleprice>div>input"
					css_selector_salekuc = "tr[key='" + color + "^"+ size + "']>td.salekuc>div>input"
					taobao_products_key = size_key + ";" + color_key
					if taobao_products_key in taobao_products:
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
					else:
						saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
						salekuc = 0	
					# 不更新已有商品价格，避免后台告警
					#browser.find_element_by_css_selector(css_selector_saleprice).clear()
					#browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
					browser.find_element_by_css_selector(css_selector_salekuc).clear()
					browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))
			else:
				if taobao_sizes:
					for size_key in taobao_sizes.keys():
						css_selector_saleprice = "tr[key='" + color + "']>td.saleprice>div>input"
						css_selector_salekuc = "tr[key='" + color + "']>td.salekuc>div>input"
						taobao_products_key = size_key + ";" + color_key	
						if taobao_products_key in taobao_products:
							saleprice = taobao_products[taobao_products_key][6]
							salekuc = taobao_products[taobao_products_key][3]
						else:
							saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
							salekuc = 0
						#browser.find_element_by_css_selector(css_selector_saleprice).clear()
						#browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
						browser.find_element_by_css_selector(css_selector_salekuc).clear()
						browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))	
						break;
				else:
					css_selector_saleprice = "tr[key='" + color + "']>td.saleprice>div>input"
					css_selector_salekuc = "tr[key='" + color + "']>td.salekuc>div>input"
					taobao_products_key = color_key	
					if taobao_products_key in taobao_products:
						saleprice = taobao_products[taobao_products_key][6]
						salekuc = taobao_products[taobao_products_key][3]
					else:
						saleprice = browser.find_element_by_css_selector(first_sku_saleprice_selector).get_attribute("value")
						salekuc = 0
					#browser.find_element_by_css_selector(css_selector_saleprice).clear()
					#browser.find_element_by_css_selector(css_selector_saleprice).send_keys(str(saleprice))
					browser.find_element_by_css_selector(css_selector_salekuc).clear()
					browser.find_element_by_css_selector(css_selector_salekuc).send_keys(str(salekuc))				
		return


	def delete_suning_product_size(self):
		return

	def click_save_button(self, browser):
		browser.find_element_by_id("saveOrUpdateBtn").click()
