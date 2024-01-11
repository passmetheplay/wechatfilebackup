from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton

class Utilities:
    @staticmethod
    def showHelpDialog(parent, language):
        dialog = QDialog(parent)
        dialog.setWindowTitle("Help")
        dialog.resize(600, 500)  # 增加对话框大小

        layout = QVBoxLayout(dialog)

        text_browser = QTextBrowser(dialog)
        text_browser.setOpenExternalLinks(True)  # 允许打开外部链接
        # 定义超链接
        hyperlink = "<a href='https://github.com/passmetheplay/wechatfilebackup'>https://github.com/passmetheplay/wechatfilebackup</a>"

        if language == "en":  # 英文
            help_text = "<h2>Instruction</h2>"
            help_text += "<p><b>1. Select search directory</b><br>"
            help_text += "   - Automatically search WeChat directory: The program tries to automatically locate the default WeChat storage directory.<br>"
            help_text += "   - Manually select directory: If the program does not find the WeChat directory, or needs to search other directories, click the 'Select Folder' button.</p>"
            help_text += "<p><b>2. Start search</b><br>"
            help_text += "   - Click the 'Start Search' button, the program will search the selected directory.<br>"
            help_text += "   - After the search is complete, the number of each file type is displayed.</p>"
            help_text += "<p><b>3. File migration</b><br>"
            help_text += "   - Select the files to be migrated from the results.<br>"
            help_text += "   - Set the migration directory, ensuring it is different from the search directory.<br>"
            help_text += "   - If you need to convert .silk audio files to .wav, check the corresponding option and set the silk-v3-decoder directory. If the conversion fails, you need to install ffmpeg and set ffmpeg as an environment variable in the path.<br>"
            help_text += "   - Optionally delete the source files.</p>"
            help_text += "<p><b>4. Start migration</b><br>"
            help_text += "   - Click 'Start Migration' to migrate the selected files.<br>"
            help_text += "   - After the migration, the number of files and the number of converted audio files will be displayed.</p>"
            help_text += "<p><b>5. Help</b><br>"
            help_text += "   - If you have questions or need further guidance, click the help button.</p>"
            help_text += "<p><b>Common issues:</b><br>"
            help_text += "   - WeChat directory not found: Manually select the WeChat directory.<br>"
            help_text += "   - Migration target and source directory are the same: Ensure that the migration target folder is different from the source folder.<br>"
            help_text += "   - Audio file conversion failed: Ensure that the silk-v3-decoder is correctly installed and the directory is specified.</p>"
            help_text += f"<p>For more help, please click this link: {hyperlink}.</p>"

        elif language == "zh":  # 中文
            help_text = "<h2>操作说明</h2>"
            help_text += "<p><b>1. 选择搜索目录</b><br>"
            help_text += "   - 自动搜索微信目录: 程序尝试自动定位到微信默认存储目录。<br>"
            help_text += "   - 手动选择目录: 若程序未找到微信目录，或需搜索其他目录，点击'选择文件夹'按钮。</p>"
            help_text += "<p><b>2. 开始搜索</b><br>"
            help_text += "   - 点击'开始搜索'按钮，程序搜索所选目录。<br>"
            help_text += "   - 搜索完成后显示每种文件数量。</p>"
            help_text += "<p><b>3. 文件迁移</b><br>"
            help_text += "   - 从结果中选择需迁移文件。<br>"
            help_text += "   - 设置迁移目录，确保与搜索目录不同。<br>"
            help_text += "   - 如需转换.silk语音文件为.wav，勾选相应选项，并设置silk-v3-decoder目录。如果转换失败需安装ffmpeg ，并将ffmpeg 设置如path的环境变量中。<br>"
            help_text += "   - 可选删除源文件。</p>"
            help_text += "<p><b>4. 开始迁移</b><br>"
            help_text += "   - 点击'开始迁移'，迁移选中文件。<br>"
            help_text += "   - 迁移后显示文件数量及转换的语音文件数。</p>"
            help_text += "<p><b>5. 帮助</b><br>"
            help_text += "   - 如有疑问或需进一步指导，点击帮助按钮。</p>"
            help_text += "<p><b>常见问题：</b><br>"
            help_text += "   - 微信目录未找到: 手动选择微信所在目录。<br>"
            help_text += "   - 迁移目标与源目录相同: 确保迁移目标文件夹与源文件夹不同。<br>"
            help_text += "   - 语音文件转换失败: 确保silk-v3-decoder正确安装并已指定目录。</p>"
            help_text += f"<p>更多帮助请点击这个链接查看：{hyperlink}。</p>"

        else:
            help_text = "<p>No help available for the selected language.</p>"

        text_browser.setHtml(help_text)
        layout.addWidget(text_browser)

        button_ok = QPushButton("OK", dialog)
        button_ok.clicked.connect(dialog.close)
        layout.addWidget(button_ok)

        dialog.setLayout(layout)
        dialog.exec_()
