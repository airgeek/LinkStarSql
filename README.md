## LinkStarSql

LinkStarSql 是一款 Sublime Text 插件，可以直接在编辑器中运行 SQL 查询，无需切换到外部工具。它会将选中的 SQL（如果没有选中，则使用整个文件内容）发送到内部 SQL 查询系统，并在 Sublime 的输出面板显示查询结果。

⸻

特性
- ✅ 选中即查：选中文本时，仅提交选中的 SQL。
- ✅ 全文查询：如果没有选中任何内容，则发送整个视图的内容。
- ✅ 结果输出：查询结果显示在 Sublime 的 Output Panel，无需离开编辑器。

⸻

安装

通过 Package Control（推荐）
1. 打开 Sublime Text，按 Ctrl+Shift+P（macOS：Cmd+Shift+P）。
2. 输入 Install Package 并回车。
3. 搜索 LinkStarSql 并安装。

手动安装
1. 克隆本仓库或下载 ZIP。
2. 将文件夹重命名为 LinkStarSql，放到 Sublime 的 Packages 目录下。

⸻

使用方法
- 命令面板
打开命令面板（Ctrl+Shift+P / Cmd+Shift+P），输入并执行：

LinkStar SQL: Run Query


- 快捷键（可自行配置）

- 右键菜单
在 SQL 文本上右键选择 Run Selected SQL。

逻辑：
- 如果有选中内容 → 发送选中 SQL。
- 如果未选中 → 发送整个视图内容。

⸻

查询结果
- 查询结果会显示在 Sublime 的输出面板中。

⸻

注意事项
- 该插件依赖于内部 SQL 系统，外部用户无法直接使用。
- Token会在初次运行时自动配置。

⸻

版本更新日志

请查看 messages.json。

⸻

许可证

MIT License.
