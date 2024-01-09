from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt
import os
from file_migrate_thread import FileMigrateThread
from file_search_thread import FileSearchThread

class EventHandlers:
    def __init__(self, ui):
        self.ui = ui  # 主窗口UI的引用

    def updateDetailedProgress(self, progress, phase_description, processed, total):
        progress_text = f"进度: {progress}% ({processed}/{total}) - {phase_description}"
        print(progress_text)
        self.ui.detailed_progress_label.setText(progress_text)
        self.ui.progress_bar.setValue(progress)


    def setSilkDecoderDirectory(self):
        directory = QFileDialog.getExistingDirectory(self.ui, "选择silk-v3-decoder目录")
        if directory:
            if os.path.exists(os.path.join(directory, "converter.sh")):
                self.ui.silk_decoder_directory = directory
                self.ui.config_manager.set_config('silk_decoder_directory', self.ui.silk_decoder_directory)
                QMessageBox.information(self.ui, "设置成功", "silk-v3-decoder目录设置成功。")
            else:
                QMessageBox.warning(self.ui, "目录错误", "请选择包含converter.sh的正确silk-v3-decoder目录。")
        self.ui.checkAndUpdateSilkDecoderDirectoryLabel()

    def selectAllItems(self, category, state):
        self.ui.results_widgets[category].blockSignals(True)
        check_state = Qt.Checked if state == Qt.Checked else Qt.Unchecked
        for i in range(self.ui.results_widgets[category].count()):
            item = self.ui.results_widgets[category].item(i)
            item.setCheckState(check_state)
            file_path = item.data(Qt.UserRole)
            if check_state == Qt.Checked:
                self.ui.selected_files[category].add(file_path)
            else:
                self.ui.selected_files[category].discard(file_path)
        selected_count = len(self.ui.selected_files[category])
        self.ui.selected_counts_labels[category].setText(f"已选: {selected_count}")
        self.ui.results_widgets[category].blockSignals(False)

    def selectFolder(self):
        directory = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        if directory:
            self.ui.directory_label.setText(f"选定文件夹: {directory}")
            self.ui.selected_directory = directory

    def startSearch(self):
        print("开始搜索...")
        self.ui.btn_select_folder.setDisabled(True)
        self.ui.btn_start_search.setDisabled(True)
        self.ui.btn_select_target_folder.setDisabled(True)
        self.ui.delete_source_checkbox.setDisabled(True)
        for widget in self.ui.results_widgets.values():
            widget.clear()
        self.ui.search_thread = FileSearchThread(self.ui.selected_directory, self.ui.categories)
        self.ui.search_thread.update_category.connect(self.updateResults)
        self.ui.search_thread.update_progress.connect(self.updateDetailedProgress)
        self.ui.search_thread.search_finished.connect(self.onSearchFinished)
        self.ui.search_thread.start()

    def onSearchFinished(self):
        self.ui.btn_select_folder.setDisabled(False)
        self.ui.btn_start_search.setDisabled(False)
        self.ui.btn_select_target_folder.setDisabled(False)
        self.ui.delete_source_checkbox.setDisabled(False)
        self.ui.progress_bar.setValue(100)
        self.updateLabelColors()
        file_counts_message = "\n".join([f"{category}: {count}" for category, count in self.ui.searched_files_count.items()])
        QMessageBox.information(self.ui, "搜索完成", f"文件搜索完成。\n\n分类数量:\n{file_counts_message}")
        self.ui.searched_files_count = {category: 0 for category in self.ui.categories}
        self.resetAndCountFiles()
        self.disableResultsDisplay(False)

    def resetAndCountFiles(self):
        for category in self.ui.categories:
            self.ui.select_all_checkboxes[category].setChecked(False)
            self.ui.select_all_checkboxes[category].setEnabled(True)
            file_count = self.ui.results_widgets[category].count()
            for i in range(file_count):
                self.ui.results_widgets[category].item(i).setCheckState(Qt.Unchecked)
            self.ui.category_labels[category].setText(f"{category} ({file_count})")
            self.ui.selected_counts_labels[category].setText("已选: 0")
            self.ui.selected_files[category].clear()

    def toggleSelection(self, item, category):
        self.ui.results_widgets[category].blockSignals(True)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            self.ui.selected_files[category].discard(item.data(Qt.UserRole))
        else:
            item.setCheckState(Qt.Checked)
            self.ui.selected_files[category].add(item.data(Qt.UserRole))
        self.ui.results_widgets[category].blockSignals(False)
        selected_count = len(self.ui.selected_files[category])
        self.ui.selected_counts_labels[category].setText(f"已选: {selected_count}")

    def updateResults(self, file_batch):
        print(f"Updating results for a batch of {len(file_batch)} files.")
        for category_widget in self.ui.results_widgets.values():
            category_widget.setUpdatesEnabled(False)
        for category, file_path in file_batch:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            item.setToolTip(file_path)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            self.ui.results_widgets[category].blockSignals(False)
            self.ui.results_widgets[category].addItem(item)
            self.ui.results_widgets[category].itemChanged.connect(lambda i, c=category: self.toggleSelection(i, c))
            self.ui.searched_files_count[category] += 1
        for category, category_widget in self.ui.results_widgets.items():
            count = category_widget.count()
            self.ui.category_labels[category].setText(f"{category} ({count})")
            category_widget.setUpdatesEnabled(True)

    def selectTargetFolder(self):
        target_directory = QFileDialog.getExistingDirectory(self.ui, "选择迁移目标文件夹")
        if target_directory:
            if target_directory != self.ui.selected_directory:
                self.ui.target_directory = target_directory
                self.ui.target_directory_label.setText(f"迁移目标文件夹: {self.ui.target_directory}")
                self.ui.btn_migrate.setDisabled(False)
            else:
                QMessageBox.warning(self.ui, "错误", "迁移目标文件夹不能与搜索文件夹相同，请选择不同的文件夹。")
        else:
            self.ui.target_directory_label.setText("迁移目标文件夹：未选择")

    def openTargetFolder(self):
        if self.ui.target_directory:
            os.system(f'open "{self.ui.target_directory}"')

    def disableResultsDisplay(self, disable):
        for widget in self.ui.results_widgets.values():
            widget.setEnabled(not disable)

    def startMigration(self):
        print("开始迁移...")
        total_selected = sum(len(files) for files in self.ui.selected_files.values())
        if total_selected == 0:
            QMessageBox.information(self.ui, "无文件", "没有选中任何文件进行迁移。")
            return

        # 检查是否选择了语音文件并且勾选了转换语音选项
        convert_silk = self.ui.convert_silk_checkbox.isChecked()
        has_voice_files = bool(self.ui.selected_files['语音'])
        if convert_silk and has_voice_files and not self.ui.silk_decoder_directory:
            QMessageBox.warning(self.ui, "设置未完成", "您选择了转换语音文件，但未设置silk-v3-decoder目录。请先设置目录。")
            return

        if self.ui.delete_source_checkbox.isChecked():
            reply = QMessageBox.question(self.ui, "确认删除", "您确定要在迁移后删除源文件吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.disableResultsDisplay(True)
        self.ui.btn_migrate.setDisabled(True)
        self.ui.btn_select_target_folder.setDisabled(True)
        self.ui.btn_open_target_folder.setDisabled(True)
        convert_silk = self.ui.convert_silk_checkbox.isChecked()
        self.ui.migrate_thread = FileMigrateThread(self.ui.selected_files, self.ui.target_directory, self.ui.delete_source_checkbox.isChecked(), convert_silk, self.ui.silk_decoder_directory)
        self.ui.migrate_thread.migration_complete.connect(self.onMigrationComplete)
        self.ui.migrate_thread.update_progress.connect(self.updateDetailedProgress)
        self.ui.migrate_thread.start()

    def onMigrationComplete(self):
        migrated_files_message = "\n".join([f"{category}: {count}" for category, count in self.ui.migrate_thread.migrated_files_count.items()])

        # 创建一个QLabel用于显示带颜色的转换信息
        conversion_info_label = QLabel()
        conversion_info = ""

        if self.ui.convert_silk_checkbox.isChecked():
            total_voice_files_to_convert = len(self.ui.selected_files.get('语音', []))
            successful_conversions = self.ui.migrate_thread.migrated_files_count.get('语音', 0)
            failed_conversions = total_voice_files_to_convert - successful_conversions
            conversion_info = f"需要转换的语音文件数: {total_voice_files_to_convert}, 转换成功: <span style='color: green;'>{successful_conversions}</span>"
            if failed_conversions > 0:
                conversion_info += f", 失败: <span style='color: red;'>{failed_conversions}</span>"

        conversion_info_label.setText(conversion_info)

        # 创建自定义对话框
        dialog = QMessageBox()
        dialog.setWindowTitle("迁移完成")
        dialog.setText(f"文件迁移完成。\n\n分类迁移文件数:\n{migrated_files_message}")
        if conversion_info:
            dialog.layout().addWidget(conversion_info_label, 1, 1)  # 添加到对话框布局中
        dialog.exec_()

        self.ui.btn_migrate.setDisabled(False)
        self.ui.btn_select_target_folder.setDisabled(False)
        self.ui.btn_open_target_folder.setDisabled(False)
        self.updateLabelColors()
        self.ui.progress_bar.setValue(0)






    def updateLabelColors(self):
        for category, count_label in self.ui.selected_counts_labels.items():
            count_label.setText(f"已选: {len(self.ui.selected_files[category])}")
            count_label.setStyleSheet("color: green;" if self.ui.selected_files[category] else "color: black;")

