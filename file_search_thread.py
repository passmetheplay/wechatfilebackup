from PyQt5.QtCore import QThread, pyqtSignal
import os

class FileSearchThread(QThread):
    update_category = pyqtSignal(list)
    update_progress = pyqtSignal(int, str, int, int)  # 修改信号定义，加入额外的参数
    search_finished = pyqtSignal()

    def __init__(self, directory, file_types,translate_function):
        super().__init__()
        self.directory = directory
        self.file_types = file_types
        self.translate_function = translate_function

    def run(self):
        print("Search Thread Started")
        total_files = sum([len(files) for _, _, files in os.walk(self.directory)])
        print(f"Total files to process: {total_files}")
        processed_files = 0
        file_batch = []

        for root, dirs, files in os.walk(self.directory):
            for file in files:
                processed_files += 1
                for category, extensions in self.file_types.items():
                    if any(file.endswith(ext) for ext in extensions):
                        file_path = os.path.join(root, file)
                        file_batch.append((category, file_path))

                if len(file_batch) >= 1000:
                    self.update_category.emit(file_batch)
                    file_batch.clear()
                    progress = min(int((processed_files / total_files) * 100), 100)
                    phase_description = self.translate_function("phase_description_search")
                    self.translate_function("File Search")
                    self.update_progress.emit(progress, phase_description, processed_files, total_files)

        # 处理剩余的文件批次
        if file_batch:
            self.update_category.emit(file_batch)
            progress = min(int((processed_files / total_files) * 100), 100)
            phase_description = self.translate_function("phase_description_search")
            self.update_progress.emit(progress, phase_description, processed_files, total_files)

        print("Search Thread Finished")
        self.search_finished.emit()
