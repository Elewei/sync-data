import re
import requests
import shutil
import os
from bs4 import BeautifulSoup 

class Taobao():
	""" 淘宝类 """
	
	def __init__(self, id):
		""" 初始化淘宝属性 """
		self.id = id
		
	def get_taobao_product_url(self):
		""" 获取淘宝商品链接 """
		url = "http://item.taobao.com/item.htm?id=" + str(self.id)
		print("成功获取淘宝商品URL：" + url)
		return url
	
	def get_taobao_page(self, url):
		'''获取淘宝商品页面解析信息'''
		r = requests.get(url)
		soup = BeautifulSoup(r.text, "lxml")
		print("成功获取淘宝商品页面信息")
		return soup
	
	def get_taobao_product_json_data(self, soup):
		'''获取淘宝商品JSON数据'''
		script_list = soup.find_all('script')
		script_content = str(script_list[22])
		p1 = re.compile(r'[(](.*?)[)]', re.S)
		brackets_content = re.findall(p1, script_content)
		data = brackets_content[3]
		print("成功获取淘宝JSON数据")
		return data

	def get_taobao_frist_size_key(self, taobao_sizes):
		'''获取淘宝商品第一个尺码的键值'''
		for key in taobao_sizes.keys():
			first_size_key = key
			break
		return first_size_key
	
	def get_current_dir(self):
		current_dir = os.path.abspath(os.curdir)
		return current_dir
		
	def download_taobao_image(self, url, image_path):
		response = requests.get(url, stream=True) 
		with open(image_path, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)		
		del response
		return
		
	def delete_image(self, path):
		'''删除img下所有照片'''
		ls = os.listdir(path)
		for i in ls:
			c_path = os.path.join(path, i)
			if os.path.isdir(c_path):
				del_file(c_path)
			else:
				os.remove(c_path)
		return


		



