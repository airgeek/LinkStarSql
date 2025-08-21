import sublime
import sublime_plugin
import os
import base64

class LinkStarSqlCommand(sublime_plugin.TextCommand):
	"""
	Sublime Text插件：根据选中文本状态，缓存sql
	"""
	def run(self, edit):

		# 获取当前视图
		view = self.view
		
		# 获取所有选中的区域
		selections = view.sel()

		s = '' # 初始化文本保存

		# 遍历所有选中区域、获取内容
		for i, region in enumerate(selections):
			# 检查区域是否非空
			if not region.empty():
				# 获取选中文本
				s += view.substr(region)

		# 有选中则保存
		if len(s): # 有则保存路径
			print('有选中的文本')
		else: # 如果没有选中内容，保存整个视口的所有文本
			entire_region = sublime.Region(0, view.size())
			s = view.substr(entire_region)
			print('没有选中的文本')

		if len(s) == 0:
			raise ValueError('sql语句不能为空')
			
		sql_bs64 = base64.b64encode(s.encode('utf-8')).decode('utf-8') # 进行base64编码

		# 运行脚本
		view.window().run_command("exec"，{
						'cmd':['python','-u','sql_client.py',sql_bs64], # 执行同目录入的脚本
						"env": {"PYTHONIOENCODING": "utf-8"}, # 打印时避免乱码
						"working_dir": os.path.dirname(os.path.abspath(__file__)) # 插件文件路径
						})
