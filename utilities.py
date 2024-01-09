from PyQt5.QtWidgets import QMessageBox


class Utilities:
    @staticmethod
    def showHelpDialog(self):
        help_text = "操作说明:\n\n"
        help_text += "1. 选择搜索目录\n"
        help_text += "   - 自动搜索微信目录: 程序尝试自动定位到微信默认存储目录。\n"
        help_text += "   - 手动选择目录: 若程序未找到微信目录，或需搜索其他目录，点击'选择文件夹'按钮。\n\n"
        help_text += "2. 开始搜索\n"
        help_text += "   - 点击'开始搜索'按钮，程序搜索所选目录。\n"
        help_text += "   - 搜索完成后显示每种文件数量。\n\n"
        help_text += "3. 文件迁移\n"
        help_text += "   - 从结果中选择需迁移文件。\n"
        help_text += "   - 设置迁移目录，确保与搜索目录不同。\n"
        help_text += "   - 如需转换.silk语音文件为.wav，勾选相应选项，并设置silk-v3-decoder目录。\n"
        help_text += "   - 可选删除源文件。\n\n"
        help_text += "4. 开始迁移\n"
        help_text += "   - 点击'开始迁移'，迁移选中文件。\n"
        help_text += "   - 迁移后显示文件数量及转换的语音文件数。\n\n"
        help_text += "5. 帮助\n"
        help_text += "   - 如有疑问或需进一步指导，点击帮助按钮。\n\n"
        help_text += "常见问题：\n"
        help_text += "   - 微信目录未找到: 手动选择微信所在目录。\n"
        help_text += "   - 迁移目标与源目录相同: 确保迁移目标文件夹与源文件夹不同。\n"
        help_text += "   - 语音文件转换失败: 确保silk-v3-decoder正确安装并已指定目录。\n"

        QMessageBox.information(self, "帮助", help_text)
