'''
在sub中直接发起sql查询,场景不割裂

美菜专用 @杨卓 yzhuo@live.com

20250815 v0.1 创建
'''

import json
import time
from urllib.parse import quote
import re
import os
import webbrowser
import pyperclip # 监听剪贴板
import random
import string
import sys
import base64

from websocket import create_connection
from contextlib import closing
import requests
from prettytable import PrettyTable

# print = lambda x:None # 屏蔽打印

class local_sql:
	def __init__(self, debugger=False):
		self.debugger = False
		self.trans = lambda x:''.join([chr(ord(i)^1) for i in x])
		self.info_url = self.trans('iuuqr;..inld/xtori`oldhb`h/bnl.l`lr.`rrdu.fduTrdsHogn')
		self.linkstar_index = self.trans('iuuqr;..mhojru`s/xtori`oldhb`h/bnl.".`einb')
		self.linkstar_url = self.set_linkstar_url()
		self.token_path = os.getenv('APPDATA') + r'\sql_token'
		self.set_token() # self.token,self.email
		self.task_check_url = self.trans('iuuqr;..mhojru`s/xtori`oldhb`h/bnl.`einb.ptdsx.bidbjU`rj')

	def log(self,txt):
		'''打印日志'''
		if self.debugger:
			print(txt)

	def set_token(self):
		'''设置token'''
		# Windows系统下的默认路径
		try:
			with open(self.token_path, 'r', encoding='utf-8') as e:
				self.token, self.email = self.trans(e.read()).split(',')
				s = '读取本地token:' + self.token + self.email
				self.log(s)
		except:
			self.log('凭证异常,打开浏览器获取')
			self.get_token_from_webbrowser()

	def get_token_from_webbrowser(self):
		'''从浏览器获取token'''
		webbrowser.open(self.info_url)
		now = time.time()
		while True:
			clip_token = re.search(r'admin_user_\d+_\w+',pyperclip.paste())
			if clip_token:
				pyperclip.copy("") # 清空剪贴板
				token = 'beta_user_token=' + clip_token.group(0)
				rsp = requests.get(self.info_url,headers={'cookie':token}).text
				self.log('token验证结果:'+rsp)
				if 'admin_user' in rsp:
					rsp = json.loads(rsp)
					email = rsp['body']['email']
					with open(self.token_path, 'w', encoding='utf-8') as f:
						s = token + email
						f.write(self.trans(s))

					return self.set_token()
				else:
					self.log('无效的凭证')
			if time.time() - now >= 60:
				raise '超时'
			time.sleep(1)

	def get_sql_body(self,sql:str):
		'''将sql代码,转换为请求体'''
		c = {
			"dataSourceId":481,
			"db":"",
			"sql":sql,
			"type":0,
			"email":self.email,
			"sqlConf":""
			}
		c_str = json.dumps(c,ensure_ascii=False,separators=(',', ':'))
		c_quote = quote(c_str)
		c_len = len(re.findall(r'%..|.',c_quote))
		body = [f"SEND\nContent-Type:application/json;charset=utf-8\ndestination:/app/execute\ncontent-length:{c_len}\n\n{c_str}\u0000"]
		return body

	def set_linkstar_url(self):
		'''获取星罗查询链接'''
		head_url = self.trans('vrr;..mhojru`s/xtori`oldhb`h/bnl.runlq')# 193/3ijkcgcd/websocket
		randint = random.randint(100,9999)
		randstr = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))
		return f'{head_url}/{randint}/{randstr}/websocket'

	def get_task_id(self,sql:str):
		'''发起查询'''

		try:
			print('建立隧道',end='...')
			with closing(create_connection(self.linkstar_url,cookie=self.token)) as ws:
				
				print('连接声明',end='...')
				ws.send(json.dumps(["CONNECT\naccept-version:1.2\nheart-beat:10000,10000\n\n\u0000"]))
				rsp = ws.recv()

				print('订阅',end='...')
				ws.send(json.dumps([f'SUBSCRIBE\nContent-Type:application/json;charset=utf-8\nid:sub-{int(time.time())}-99\ndestination:/user/queue/execute\n\n\u0000']))
				rsp = ws.recv()

				print('查询',end='...')
				body = self.get_sql_body(sql)
				ws.send(json.dumps(body))
				rsp = ws.recv()
				task_id = re.search(r'\\"id\\":(\d+)',rsp)
				if task_id:
					self.task_id = int(task_id.group(1))
					print(f'[{self.task_id}]等待结果',end='...')
					return self.get_linkstar_result() # 获取查询结果
				else:
					raise ValueError('\n查询失败,请反馈@杨卓')
		except Exception as e:
			if 'TOKEN_EXPIRED' in str(e):
				print('凭证失效...请重新配置')
				self.get_token_from_webbrowser()
				return self.get_task_id(sql)
			else:
				print(e)

	def get_linkstar_result(self):
		'''查询星罗结果'''
		s = requests.session()

		s.headers = {
			'cookie':self.token,
			'content-type':'application/json;charset=UTF-8'
			}

		c = {"id":self.task_id}
		now = time.time()
		while True:
			# 超时
			if time.time() - now >= 60:
				print('查询结果超时,请去网页查看')
				webbrowser.open(self.linkstar_index)
				break
			rsp = s.post(self.task_check_url,json=c).json()
			# self.log(rsp)
			state = rsp['data']['state']
			records = rsp['data']['records']
			msg = rsp['msg']
			if state != 'R':
				print('\n')
				if msg != '查询成功':
					print(msg)
					break
				if msg == '查询成功':
					# print(records)
					# 表格输出
					table = PrettyTable(records[0].keys())
					table.add_rows([i.values() for i in records])
					print(table)
					break
			print('.',end='')
			time.sleep(1)

if __name__ == '__main__':
	s = local_sql() # 初始化

	sql_bs64 = sys.argv[-1] # 最后一位参数是sql-bs64
	sql = base64.b64decode(sql_bs64.encode('utf-8')).decode('utf-8') # 解码

	a = s.get_task_id(sql)
