# Whisper_ASR
#### Whisper_ASR：彥杰修改的 whisper_real_time 語音輸入法。
>參考網站：<https://github.com/davabase/whisper_real_time>

#### Python 程式碼執行需要將 [`ffmpeg`](https://ffmpeg.org/) 加入環境變數 Path 中。(Releases 發佈版也需要) <br>
>ffmpeg: <https://ffmpeg.org/>

#### 游標放的位置，就可以開始語音輸入。下圖左CMD，右記事本。
![Demo gif](demo.gif)
<br>
#### Releases 發佈版，程式使用方法：
在 [`Releases 發佈版`](https://github.com/zhanyanjie6796/whisper_asr_v1_20230323/releases/tag/v1.0.0)(右邊)，下載CPU或GPU版本。如果使用GPU版本記得先更新自己電腦顯卡的[`驅動程式`](http://www.nvidia.com/Download/index.aspx)。
<br>
將資料夾解壓縮後，執行如下指令：
```
whisper_asr.exe                （預設模型small）
whisper_asr.exe --model base   （使用模型base）
whisper_asr.exe --model medium （使用模型medium）

可以用這些模型["tiny", "base", "small", "medium", "large"]
第一次執行會自動下載。

使用中可以按F8,暫停或繼續。
```

#### 小結：
>whisper即時中文語音辨識建議用模型small。在當前電腦環境下，CPU執行簡單一句話大概8-10秒鐘，GPU執行大概2-3秒。GPU+模型small速度比較接近語音辨識可以接受的速度，且辨識結果勉强可以接受。

#### 其他參考網站：
>openai-whisper：<https://pypi.org/project/openai-whisper/><br>
>whisper：<https://github.com/openai/whisper><br>
>pytorch(官網含指令)：<https://pytorch.org/><br>
>torch(whl下載)：<https://download.pytorch.org/whl/torch/><br>

----

英文說明：

# Whisper_ASR
#### Whisper_ASR: The whisper_real_time voice input method modified by Yanjie.
> Reference website: <https://github.com/davabase/whisper_real_time>

#### Python code execution needs to add [`ffmpeg`](https://ffmpeg.org/) to the environment variable Path. (Required for Releases too) <br>
>ffmpeg: <https://ffmpeg.org/>

#### Where the cursor is placed, voice input can start. The picture below shows CMD on the left and Notepad on the right.
![Demo gif](demo.gif)
<br>
#### Releases release version, how to use the program:
In [`Releases release version`](https://github.com/zhanyanjie6796/whisper_asr_v1_20230323/releases/tag/v1.0.0) (right), download the CPU or GPU version. If you use the GPU version, remember to update the [`driver`](http://www.nvidia.com/Download/index.aspx) of your computer graphics card first.
<br>
After decompressing the folder, execute the following command:
```
whisper_asr.exe (preset model small)
whisper_asr.exe --model base (use model base)
whisper_asr.exe --model medium (use model medium)

You can use these models ["tiny", "base", "small", "medium", "large"]
The first execution will automatically download.

During use, you can press F8 to pause or continue.
```

#### Summary:
>whisper recommends using the model small for real-time Chinese speech recognition. In the current computer environment, the CPU executes a simple sentence for about 8-10 seconds, and the GPU executes for about 2-3 seconds. The speed of the GPU+ model small is relatively close to the acceptable speed of speech recognition, and the recognition results are barely acceptable.

#### Other reference sites:
> openai-whisper: <https://pypi.org/project/openai-whisper/><br>
>whisper: <https://github.com/openai/whisper><br>
>pytorch (official website with instructions): <https://pytorch.org/><br>
>torch (whl download): <https://download.pytorch.org/whl/torch/><br>