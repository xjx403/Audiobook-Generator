# 有声书生成器

## 简介
这是一个基于EdgeTTS模型的有声书生成器的项目，主体就是一个python代码。

## 运行

自行克隆本项目，在项目根路径下，安装对应的依赖
```command
git clone https://github.com/smallnew666/edge-tts.git
cd Audiobook-Generator
pip install requests pydub edge-tts
```
依赖导入完成后，运行generator.py文件即可

## 注意事项
1. 小说文件是以章节名进行分章节音频文件生成的，所以请确保小说txt文件内容中包含章节，形式满足第**章的格式，且章节标题单独成行。
2. 代码主体内容是基于ChatGPT生成的，经过本人的调试，本人本地运行没有问题，但是本人对python并不熟悉，所以代码可能并不美观，请轻喷。
3. 本项目仅供学习和研究使用，不得用于商业用途。
## 贡献
感谢开源项目： https://github.com/xfgryujk/blivedmhttps://github.com/rany2/edge-tts

