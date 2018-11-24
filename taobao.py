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
	
	def get_taobao_product_mdskip_url(self):
		mdskip_url = "https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=true&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId=" + str(self.id) +"&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1542978963000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1543025658589&isg=null&isg2=BDQ0b7pG05_520dZX1xQFFpNBvKs61mgF7cneM6V179COdSD9h7UhxjwvbFE2pBP&ref=https://login.tmall.com/?spm=a220o.1000855.a2226mz.2.463d4a25MREVWU&redirectURL=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm%3Da220m.1000858.1000725.5.131a5c01OHNvdP%26id%3D39304952279"
		return mdskip_url
		
	def get_taobao_product_headers(self):
		headers={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
			"Accept":"*/*",
			'Referer': "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.5.131a5c01OHNvdP&id=" +str(self.id),
			'Cookie' : "cna=b2GnE2d6skoCAXBQMDLN2Umz; isg=BFJSCe-wXRULD6HjbfiOdylSoBg-hVeqBeGBYhyrfoXwL_IpBPOmDVhOm0u2RM6V; t=b525ba036468c5314900e84257932446; uc3=vt3=F8dByR6qLv%2BUHWfgqtg%3D&id2=VAMbPgZ7IDS7&nk2=BIOAPxBE6QRNZA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; tracknick=guigui_186; lgc=guigui_186; _cc_=VT5L2FSpdA%3D%3D; tg=0; mt=np=; ucn=unsh; enc=Ebbry7iV1wsqoUxjU%2BdSxA2oZggcoo4WS9a3ggjPN6%2Fo%2BNz5%2FhmNfD3ypdV4nuGJDfZO4Ee7lsWwAxdtz7ipLA%3D%3D; cookie2=1afc11f73c70b9965ada800ed6781e4d; _tb_token_=e5e63353d05f6; v=0; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=W5iHLLyFe3xm&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTYNcubBM8XPg%3D%3D&tag=8&lng=zh_CN; skt=fade465661af7a2a; csg=7ecdca09; existShop=MTU0MzAyNTU1MQ%3D%3D; dnk=guigui_186; unb=728617752; sg=625; _l_g_=Ug%3D%3D; cookie1=AQDIDr8NyCISMo8lQgKUBhADoAUO8StxWt2T%2Buhg17c%3D; _nk_=guigui_186; cookie17=VAMbPgZ7IDS7",
		} 
		
		return headers

	def get_taobao_setmdskip_data(self, url, headers):
		rs=requests.get(url,headers=headers, verify=False)
		data = rs.text
		p1 = re.compile(r'[(](.*?)[)]', re.S)
		brackets_content = re.findall(p1, data)
		json_data = brackets_content[0]	
		return json_data
	
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
		if brackets_content == []:
			script_content = str(script_list[21])
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


		



