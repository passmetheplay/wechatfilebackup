import os
import json
import sys
from pathlib import Path
from config_manager import ConfigManager

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QProgressBar, QGroupBox, QCheckBox, \
    QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout, QShortcut, QApplication, QToolBar, QAction, QComboBox, \
    QSizePolicy, QWidgetAction
from PyQt5.QtCore import QSize, Qt, QLocale
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
import base64

from event_handlers import EventHandlers
from file_search_thread import FileSearchThread
from utilities import Utilities
from icons import HELP_ICON_BASE64  # 导入图标


class MainWindowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = {'视频': set(), '图片': set(), '语音': set()}
        self.searched_files_count = {'视频': 0, '图片': 0, '语音': 0}
        self.target_directory = None
        self.event_handlers = EventHandlers(self)
        self.config_manager = ConfigManager("app_config.json")
        self.silk_decoder_directory = self.config_manager.get_config('silk_decoder_directory')  # 从配置文件中读取silk decoder的目录
        print(f"读取silk decoder目录：{self.silk_decoder_directory}")
        locale = QLocale.system().name()
        self.current_language = locale.split('_')[0]
        self.translations = self.load_translations(locale)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle(self.translate('window_title'))


        # 创建一个垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 10, 10)

        # 创建工具栏
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.layout().setSpacing(0)

        # 添加语言选择下拉框到工具栏
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("中文", "zh")
        self.language_combo.currentIndexChanged.connect(self.changeLanguage)
        self.toolbar.addWidget(self.language_combo)

        # 添加伸缩空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacerAction = QWidgetAction(self)
        spacerAction.setDefaultWidget(spacer)
        self.toolbar.addAction(spacerAction)

        # 添加帮助按钮到工具栏
        help_icon_path = resource_path('help.png')
        help_action = QAction(QIcon(help_icon_path), 'Help', self)
        help_action.triggered.connect(lambda: Utilities.showHelpDialog(self, self.current_language))
        self.toolbar.addAction(help_action)

        # 在布局中添加工具栏

        main_layout.addWidget(self.toolbar)

        top_layout = QGridLayout()  # 使用网格布局

        # 搜索相关控件的布局
        self.search_group_box = QGroupBox("①文件搜索")
        search_layout = QVBoxLayout(self.search_group_box)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.btn_select_folder = QPushButton('选择文件夹', self)
        self.btn_select_folder.clicked.connect(self.event_handlers.selectFolder)
        button_layout.addWidget(self.btn_select_folder)

        self.btn_start_search = QPushButton('开始搜索', self)
        self.btn_start_search.clicked.connect(self.event_handlers.startSearch)
        button_layout.addWidget(self.btn_start_search)

        search_layout.addLayout(button_layout)
        self.directory_label = QLabel(self)
        self.directory_label.setWordWrap(True)  # 启用文本换行
        search_layout.addWidget(self.directory_label)

        # 迁移相关控件的布局
        self.migrate_group_box = QGroupBox("②文件迁移")
        migrate_layout = QVBoxLayout(self.migrate_group_box)  # 使用垂直布局

        # 第一行布局
        migrate_row1_layout = QHBoxLayout()
        self.btn_migrate = QPushButton('开始迁移', self)
        self.btn_migrate.clicked.connect(self.event_handlers.startMigration)
        self.btn_migrate.setDisabled(True)
        migrate_row1_layout.addWidget(self.btn_migrate)

        self.convert_silk_checkbox = QCheckBox('语音转换为wav格式', self)
        migrate_row1_layout.addWidget(self.convert_silk_checkbox)




        self.delete_source_checkbox = QCheckBox("删除源文件", self)
        migrate_row1_layout.addWidget(self.delete_source_checkbox)


        migrate_layout.addLayout(migrate_row1_layout)  # 添加第一行布局到迁移布局



        # 第二行布局
        migrate_row2_layout = QHBoxLayout()



        self.btn_select_target_folder = QPushButton('选择迁移目标文件夹', self)
        self.btn_select_target_folder.clicked.connect(self.event_handlers.selectTargetFolder)
        migrate_row2_layout.addWidget(self.btn_select_target_folder)

        self.btn_open_target_folder = QPushButton('打开迁移目标文件夹', self)
        self.btn_open_target_folder.clicked.connect(self.event_handlers.openTargetFolder)
        self.btn_open_target_folder.setDisabled(True)
        migrate_row2_layout.addWidget(self.btn_open_target_folder)
        migrate_layout.addLayout(migrate_row2_layout)  # 添加第二行布局到迁移布局


        self.btn_set_silk_decoder = QPushButton('设置silk-v3-decoder目录', self)
        self.btn_set_silk_decoder.clicked.connect(self.event_handlers.setSilkDecoderDirectory)
        migrate_row2_layout.addWidget(self.btn_set_silk_decoder)  # 新增按钮

        # 迁移目标文件夹标签
        self.target_directory_label = QLabel("迁移目标文件夹: 未选择", self)
        migrate_layout.addWidget(self.target_directory_label)
        self.silk_decoder_directory_label = QLabel(f"silk-v3-decoder目录: {self.silk_decoder_directory or '未设置'}", self)

        migrate_layout.addWidget(self.silk_decoder_directory_label)



        # 将搜索和迁移部分添加到顶部布局
        top_layout.addWidget(self.search_group_box, 0, 0)  # 第一行，第一列
        top_layout.addWidget(self.migrate_group_box, 0, 1)  # 第一行，第二列
        # 设置顶部布局的列宽比例
        top_layout.setColumnStretch(0, 1)  # 第一列
        top_layout.setColumnStretch(1, 1)  # 第二列

        self.selected_counts_labels = {}  # 存储每个类别的已选数量标签

        # 结果显示部分
        self.categories = {'视频': ['.mp4'], '图片': ['.jpg', '.png'], '语音': ['.silk']}
        self.results_widgets = {category: QListWidget(self) for category in self.categories}
        self.category_labels = {category: QLabel(f"{category} (0)") for category in self.categories}
        self.select_all_checkboxes = {}
        results_layout = QVBoxLayout()

        for category, widget in self.results_widgets.items():
            category_layout = QHBoxLayout()

            select_all_checkbox = QCheckBox()
            select_all_checkbox.stateChanged.connect(lambda state, c=category: self.event_handlers.selectAllItems(c, state))
            select_all_checkbox.setEnabled(False)
            self.select_all_checkboxes[category] = select_all_checkbox

            category_label = self.category_labels[category]
            category_layout.addWidget(select_all_checkbox)
            category_layout.addWidget(category_label)
            # 创建并添加已选数量的标签
            selected_count_label = QLabel("已选: 0")
            self.selected_counts_labels[category] = selected_count_label
            category_layout.addWidget(selected_count_label)

            widget.itemClicked.connect(lambda item, c=category: self.event_handlers.toggleSelection(item, c))


            category_layout.addWidget(widget)
            results_layout.addLayout(category_layout)

        # 设置布局
        # main_layout.addWidget(search_group_box)
        # main_layout.addWidget(migrate_group_box)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(results_layout)
        self.detailed_progress_label = QLabel("进度: 0/0", self)  # Add a label for detailed progress
        main_layout.addWidget(self.detailed_progress_label)  # Add the label to your layout
        self.progress_bar = QProgressBar(self)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)
        self.updateUIText()

        # 设置快捷键
        self.setupShortcuts()

        # 检查默认目录
        self.checkDefaultDirectory()





    def setupShortcuts(self):
        self.shortcut_minimize = QShortcut(QKeySequence("Ctrl+M"), self)
        self.shortcut_minimize.activated.connect(self.showMinimized)
        self.shortcut_close = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close.activated.connect(self.close)
        self.shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut_quit.activated.connect(QApplication.instance().quit)

    # 更新文本标签的内容使用翻译文本
    def checkDefaultDirectory(self):
        default_dir = Path.home() / "Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat"
        if default_dir.exists():
            translated_text = self.translate('default_directory_found')
            colored_text = f"{translated_text}<span style='color: green;'>{str(default_dir)}</span>"
            self.directory_label.setText(colored_text)
            self.selected_directory = str(default_dir)
        else:
            translated_text = self.translate('default_directory_not_found')
            colored_text = f"<span style='color: red;'>{translated_text}</span>"
            self.directory_label.setText(colored_text)
        self.checkAndUpdateSilkDecoderDirectoryLabel()

    def checkAndUpdateSilkDecoderDirectoryLabel(self):
        base_text = self.translate('silk_decoder_directory_label')
        if self.silk_decoder_directory:
            if os.path.exists(os.path.join(self.silk_decoder_directory, "converter.sh")):
                # 目录有效
                directory_text = f"<span style='color: green;'>{self.silk_decoder_directory}</span>"
            else:
                # 目录设置错误
                directory_text = f"<span style='color: red;'>{self.translate('silk_decoder_directory_invalid')}{ self.silk_decoder_directory}</span>"
        else:
            # 目录未设置
            directory_text = f"<span style='color: red;'>{self.translate('silk_decoder_directory_not_set')}</span>"

        self.silk_decoder_directory_label.setText(base_text + directory_text)

    def load_translations(self, locale):
        if locale == "zh":
            file_name = resource_path("translations/zh_CN.json")
        elif locale == "en":
            file_name = resource_path("translations/en_US.json")
        else:
            file_name = resource_path(f"translations/{locale}.json")
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def translate(self, text_key, **kwargs):
        translated_text = self.translations.get(text_key, text_key)
        return translated_text.format(**kwargs)






    def updateUIText(self):
        # 更新窗口标题
        self.setWindowTitle(self.translate('window_title'))

        # 更新组框标题
        self.search_group_box.setTitle(self.translate('search_group_box'))
        self.migrate_group_box.setTitle(self.translate('migrate_group_box'))

        # 更新按钮和标签文本
        self.btn_select_folder.setText(self.translate('btn_select_folder'))
        self.btn_start_search.setText(self.translate('btn_start_search'))
        self.btn_migrate.setText(self.translate('btn_migrate'))
        self.convert_silk_checkbox.setText(self.translate('convert_silk_checkbox'))
        self.delete_source_checkbox.setText(self.translate('delete_source_checkbox'))
        self.btn_select_target_folder.setText(self.translate('btn_select_target_folder'))
        self.btn_open_target_folder.setText(self.translate('btn_open_target_folder'))
        self.btn_set_silk_decoder.setText(self.translate('btn_set_silk_decoder'))

        # 更新标签文本
        if self.target_directory:
            self.target_directory_label.setText(self.translate('target_directory_label')+self.target_directory)
        else:
            self.target_directory_label.setText(self.translate('target_directory_label')+self.translate('target_directory_not_set'))

        self.silk_decoder_directory_label.setText(self.translate('silk_decoder_directory_label'))
        self.detailed_progress_label.setText(self.translate('detailed_progress_label'))

        # 更新类别标签和选择框
        for category in self.categories:
            self.select_all_checkboxes[category].setText(self.translate('select_all'))
            selected_count_text = self.translate('selected_counts_label', count=len(self.selected_files[category]))
            self.selected_counts_labels[category].setText(selected_count_text)

        for category, category_widget in self.results_widgets.items():
            count = category_widget.count()
            category_label_text = self.translate(category + "_label", count=count)
            self.category_labels[category].setText(category_label_text)


    def changeLanguage(self, index):
        language = self.language_combo.itemData(index)
        # 根据选中的语言来改变界面
        self.current_language = language
        self.translations = self.load_translations(self.current_language)
        self.updateUIText()  # 更新界面文本
        self.checkDefaultDirectory()

def resource_path(relative_path):
    """ 获取资源的绝对路径，用于打包或直接运行 """
    if getattr(sys, 'frozen', False):
        # 如果程序是打包运行的，使用这个路径
        base_path = sys._MEIPASS
    else:
        # 否则使用这个路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
