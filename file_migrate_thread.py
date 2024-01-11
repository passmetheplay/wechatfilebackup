from PyQt5.QtCore import QThread, pyqtSignal
import os
import shutil
import subprocess
from datetime import datetime

class FileMigrateThread(QThread):
    migration_complete = pyqtSignal()
    update_progress = pyqtSignal(int, str, int, int)

    def __init__(self, selected_files, target_directory, delete_source, convert_silk=False, silk_decoder_directory=None, translate_function=None,
                 current_language='zh'):
        super().__init__()
        self.selected_files = selected_files
        self.target_directory = target_directory
        self.delete_source = delete_source
        self.convert_silk = convert_silk
        self.silk_decoder_directory = silk_decoder_directory
        self.migrated_files_count = {category: 0 for category in selected_files}
        self.converted_files_count = 0
        self.category_dirs = {}  # 存储每个类别的迁移目录
        self.translate_function = translate_function
        self.current_language = current_language  # Add current_language attribute

    def run(self):
        total_files = sum(len(files) for files in self.selected_files.values())
        processed_files = 0

        # 迁移文件
        for category, files in self.selected_files.items():
            if files:
                phase_description = self.translate_function('phase_description_migration')

                total_category_files = len(files)
                processed_category_files = 0
                if self.current_language == 'en':
                    category_name = self.translate_function(category)  # Translate category to Chinese
                else:
                    category_name = category  # Use category name as is for English
                category_dir = os.path.join(self.target_directory, f"{category_name}_back_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                self.category_dirs[category] = category_dir  # 存储目录路径
                print(f"为 {category} 创建目录：{category_dir}")
                os.makedirs(category_dir, exist_ok=True)

                for file_path in files:
                    try:
                        target_path = os.path.join(category_dir, os.path.basename(file_path))
                        if self.delete_source:
                            shutil.move(file_path, target_path)
                        else:
                            shutil.copy(file_path, target_path)
                        self.migrated_files_count[category] += 1
                    except Exception as e:
                        print(f"处理文件 {file_path} 时出现异常: {e}")
                    finally:
                        processed_files += 1
                        processed_category_files += 1
                        progress = min(int((processed_files / total_files) * 100), 100)
                        self.update_progress.emit(progress, phase_description, processed_category_files, total_category_files)

        # 转换语音文件
        if self.convert_silk and '语音' in self.selected_files:
            phase_description = self.translate_function('phase_description_audioconvert')
            total_voice_files = len(self.selected_files['语音'])
            processed_voice_files = 0
            voice_category_dir = self.category_dirs.get('语音')  # 获取语音类别的迁移目录

            for silk_file in self.selected_files['语音']:
                converted_successfully = False
                if self.silk_decoder_directory:
                    converter_path = os.path.join(self.silk_decoder_directory, "converter.sh")
                    decoder_path = os.path.join(self.silk_decoder_directory, "silk/decoder")
                    silk_filename = os.path.basename(silk_file)
                    pcm_file = silk_filename.replace('.silk', '.pcm')
                    mp3_file = silk_filename.replace('.silk', '.mp3')

                    if os.path.exists(converter_path):
                        try:
                            result = subprocess.run([converter_path, silk_filename, 'mp3'], cwd=voice_category_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            if result.returncode == 0 and "[OK]" in result.stdout:
                                converted_successfully = True
                                self.converted_files_count += 1
                        except Exception as e:
                            print(f"执行转换命令时出现异常：{e}")

                        if not converted_successfully:
                            try:
                                pcmresult = subprocess.run([decoder_path, silk_filename, pcm_file], cwd=voice_category_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                if pcmresult.returncode == 0:
                                    pcm2mp3 = subprocess.run(['ffmpeg', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', pcm_file, '-f', 'mp3', '-ar', '16000', '-b:a', '16', '-ac', '1', mp3_file], cwd=voice_category_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                    os.remove(os.path.join(voice_category_dir, pcm_file))  # 删除中间文件
                                    if self.delete_source:
                                        os.remove(os.path.join(voice_category_dir, silk_filename))
                                    converted_successfully = True
                                    self.converted_files_count += 1
                            except Exception as e:
                                print(f"备用转换方法执行异常：{e}")
                    else:
                        print(f"转换失败：未找到 {converter_path}")
                else:
                    print("转换失败：silk-v3-decoder目录未设置")
                processed_files += 1
                processed_voice_files += 1
                progress = min(int((processed_files / total_files) * 100), 100)
                self.update_progress.emit(progress, phase_description, processed_voice_files, total_voice_files)

        print("迁移完成")
        self.migration_complete.emit()
