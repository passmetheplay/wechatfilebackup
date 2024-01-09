# Mac系统-微信文件搜索和迁移工具

## 简介

这个工具旨在帮助用户高效地搜索和迁移存储在Mac系统中微信应用的文件。它提供了一种简便的方式来查找、筛选和迁移微信中的视频、图片和语音文件，特别适用于需要整理大量微信聊天记录中文件的用户。
 ``` 注：目前只支持Mac系统```


## 解决的问题

- **文件搜索**：自动或手动搜索Mac上的微信文件，包括视频、图片和语音文件。
- **文件迁移**：将选定的文件批量迁移到指定的文件夹，方便文件管理和备份。
- **格式转换**：将微信的`.silk`语音文件转换为更通用的`.mp3`格式。
- **选择性删除**：在迁移文件后，提供选项删除原始文件，帮助释放存储空间。

## 使用指南

### 安装

请从GitHub页面下载最新版本的应用程序，安装python环境，然后运行`main.py`文件，后期推出MacOS的应用程序版本。

### 使用步骤

1. **选择搜索目录**：
    - 程序尝试自动定位到微信的默认存储目录。
    - 如果需要，可以通过点击“选择文件夹”按钮手动选择其他目录。
2. **开始搜索**：
    - 点击“开始搜索”按钮以在所选目录中搜索文件。
    - 搜索完成后，程序会显示每种类型文件的数量并列出所有找到的文件。
3. **文件迁移设置**：
    - 从搜索结果中选择需要迁移的文件。
    - 点击“选择迁移目标文件夹”按钮来指定文件迁移的目标位置。
    - 下载并安装[silk-v3-decoder](https://github.com/kn007/silk-v3-decoder)
    - 如需将`.silk`格式的语音文件转换为`.wav`格式，请勾选相应选项并设置silk-v3-decoder目录。
    - 如需在迁移后删除原始文件，请勾选“删除源文件”选项。
4. **开始迁移**：
    - 点击“开始迁移”按钮，选定的文件将开始迁移到您指定的目标文件夹。
    - 迁移完成后，程序会显示迁移的文件数量以及转换的语音文件数量。
5. **语音转换说明**：
   -  语音文件的转换是从silk文件转换为常用播放器可以播放的mp3格式，转换用到了silk-v3-decoder ，如果silk-v3-decoder也没能转换成功的，还使用的到了 [FFmpeg](https://ffmpeg.org/about.html), FFmpeg安装请参考下面步骤：
     1.  安装Homebrew：
      打开MacOS的终端。 输入以下命令来安装Homebrew：
     `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   2. 安装FFmpeg：
      一旦安装好Homebrew，只需要在终端中运行以下命令来安装FFmpeg：
      `brew install ffmpeg`
   3. 安装过程中可能会提示输入密码，输入你的Mac账户密码即可。 
   4. 安装完成后，你可以通过 `brew install ffmpeg` 来检查是否安装成功。



### 帮助与支持

如有任何疑问或需要技术支持，请参阅应用程序内的帮助部分或在GitHub页面提交问题。