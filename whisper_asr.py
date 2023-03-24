#! python3.7
# 【彥杰修改的 whisper_real_time 語音輸入法】
# 檔案:transcribe_demo_2_cn_KeyWrite.py


import argparse
import io
import os
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform


def main():
    parser = argparse.ArgumentParser()
    # 原始 default="medium" ， 改 small，彥杰20230320。
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1500, # 原音量 1000 有雜音。
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)  
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()
    
    # The last time a recording was retreived from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False
    
    # Important for linux users. 
    # Prevents permanent application hang and crash by using the wrong Microphone
    if 'linux' in platform:
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")   
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    # 原始 sample_rate=16000 ，測試 8000，11025，32000
                    # 測試結果原預設最好。速度前面幾個沒有明顯區別32k會慢一點有雜訊，11k有雜訊。8k辨識度較差。
                    source = sr.Microphone(sample_rate=16000, device_index=index) 
                    break
    else:
        source = sr.Microphone(sample_rate=16000) # 原始 sample_rate=16000
        
    # Load / Download model
    model = args.model
    if args.model != "large" and not args.non_english:
        # model = model + ".en" # 原始
        model = model  # 不加【+ ".en"】變成中文。彥杰20230320。

    audio_model = whisper.load_model(model)

    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    temp_file = NamedTemporaryFile().name
    transcription = ['']
    
    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print("Model loaded.\n")
    
    # 彥杰新增之程式  Start =================================                                
    print('開始語音辨識，可按 F8 暫停 。。。。。\n')
    import keyboard   
    stop_text = False # 判斷按下暫停的情況。   
        
    # 彥杰新增之程式  End   =================================
                    
    while True:   
        # F8 暫停/開始，彥杰。
        # 彥杰新增之程式  Start =================================
        if keyboard.is_pressed('F8'): # cpu %15。   
            sleep(0.25)                       
            print('暫停中，再按 F8 繼續 。。。。。\n')             
            keyboard.wait('F8') # cpu 幾乎不占用。
            stop_text = True # 判斷按下暫停的情況。                             
            sleep(0.25)
            print('開始語音辨識，可按 F8 暫停 。。。。。\n')             
        # 彥杰新增之程式  End   ================================= 
                             
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():                
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True
                # This is the last time we received new audio data from the queue.
                phrase_time = now

                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                # Use AudioData to convert the raw data to wav data.
                audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())

                # Write wav data to the temporary file as bytes.
                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())

                # Read the transcription.
                # result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available(),initial_prompt='GPU 程式 FFmpeg', language='Chinese')
                # print(torch.cuda.is_available(), end='', flush=True) #torch.cuda.is_available() 常常是True。# fp16=False會快一點。
                result = audio_model.transcribe(temp_file, fp16=False,initial_prompt='GPU 程式 .', language='Chinese')
                text = result['text'].strip()

                # 判斷按下暫停的情況。不留暫停時的語音資料。
                # 彥杰新增之程式  Start =================================
                if stop_text == True:
                    text = ""
                    stop_text = False
                # 彥杰新增之程式  End   =================================

                # If we detected a pause between recordings, add a new item to our transcripion.
                # Otherwise edit the existing one.
                if phrase_complete:
                    # keyboard.write("\ncomplete:"+text) # 彥杰
                    # keyboard.write("\n") # 彥杰 

                    keyboard.write(text) # 彥杰
                    transcription.append(text) # 原始程式                                      
                else:                    
                    #【這裏想辦法使用倒退按鍵。】彥杰20230320 顯示字串長度，中英文。
                    # keyboard.write("負1("+str(len(transcription[-1]))+"):"+transcription[-1]) # 彥杰      
                    # keyboard.write("text:"+text) # 彥杰   
                    # keyboard.write("\n") # 彥杰  
                    back_len = len(transcription[-1]) # 倒退回去的字串長度。
                    for i in range(back_len):
                        keyboard.write(chr(8)) # 倒退按鍵 backspace
                    keyboard.write(text) # 更新内容彥杰

                    transcription[-1] = text # 原始程式


                # Clear the console to reprint the updated transcription.
                os.system('cls' if os.name=='nt' else 'clear') # 如果不重新整理它就會直接積下去
                for line in transcription:
                    print(line) # 原始辨識輸出。                  

                # Flush stdout.
                print('', end='', flush=True) #  True（原始）/False（彥杰）# True 會更新雜訊。
                    
                # 彥杰新增之程式  Start =================================                                
                # keyboard.write(text+"\n")                
                # 彥杰新增之程式  End   =================================

                # Infinite loops are bad for processors, must sleep.
                sleep(0.25) # 原始 sleep(0.25) 彥杰
        except KeyboardInterrupt:
            break
        
    print("\n\nTranscription:")
    for line in transcription:
        print(line)

if __name__ == "__main__":
    main()