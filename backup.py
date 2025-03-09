# This code is for v1 of the openai package: pypi.org/project/openai
from openai import OpenAI
import os
import pyautogui
import time
import speech_recognition as sr
import sys
# Assuming this script is in the mainFiles folder
current_script_path = os.path.abspath(__file__)

# Add the path to the parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(current_script_path), ".."))

# Now you can import WhisperMic using a relative import
from stt.whisper_mic1 import WhisperMic



import subprocess
from ctypes import Structure, windll, c_uint, sizeof, byref
from ctypes.wintypes import DWORD
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


api_key = "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"  # Replace this with your actual API key

class FileManager:
    def __init__(self):
        self.root_dir = 'C:\\Users\\priya\\OneDrive\\Desktop'

    def search_file(self, file_name):
        for foldername, subfolders, filenames in os.walk(self.root_dir):
            if file_name in filenames or file_name in subfolders:
                return os.path.join(foldername, file_name)
        return None

    def open_target_with_run(self, target_path):
        pyautogui.hotkey('winleft', 'r')  # Opens the Run dialog
        pyautogui.write(f'"{target_path}"')  # Enclose the target path in quotes
        pyautogui.press('enter')

    def open_target(self, target_name):
        target_path = self.search_file(target_name)
        if target_path:
            self.open_target_with_run(target_path)
        else:
            print(f"Target '{target_name}' not found.")


    def launch_application(self, app_name):
        # try:
        #     os.system(f"start {app_name}")
        # except Exception as e:
        #     print(f"Error launching application '{app_name}': {e}")
        try:
                pyautogui.press('winleft')
                time.sleep(1)
                pyautogui.write(app_name)
                pyautogui.press('enter')
        except Exception as e:
            print(f"Error launching application '{app_name}': {e}")


    def execute_command(self, command):
        if "open" in command:
            target_name = self.extract_target_name(command)
            if target_name:
                self.open_target(target_name)
            else:
                print("No target specified in the command.")
        elif "launch" in command:
            app_name = self.extract_app_name(command)
            if app_name:
                self.launch_application(app_name)
            else:
                print("No application specified in the command.")
        elif "rename" in command:
            old_name, new_name = self.extract_rename_info(command)
            if old_name and new_name:
                self.rename_file(old_name, new_name)
        elif "brightness" in command:
            brightness_value = self.extract_brightness_value(command)
            if brightness_value is not None:
                self.set_brightness(brightness_value)
        elif "volume" in command:
            volume_value = self.extract_volume_value(command)
            if volume_value is not None:
                self.set_volume(volume_value)
            else:
                print("Invalid rename command.")
        elif "size" in command:
            file_name = self.extract_target_name(command)
            if file_name:
                self.show_file_size(file_name)
            else:
                print("No file specified for size command.")
        elif "delete" in command:
            file_name = self.extract_target_name(command)
            if file_name:
                self.delete_file(file_name)
            else:
                print("No file specified for delete command.")
        elif "exit" in command:
            print("Exiting the script.")
            exit()
        else:
            print("Command not recognized.")

    def extract_rename_info(self, command):
        start_index = command.find("rename") + len("rename")
        names = command[start_index:].split(" to ")
        return names[0].strip(), names[1].strip() if len(names) == 2 else (None, None)

    def show_file_size(self, file_name):
        file_path = self.search_file(file_name)
        try:
            if file_path:
                size = os.path.getsize(file_path)
                print(f"Size of '{file_name}': {size} bytes")
            else:
                print(f"File '{file_name}' not found.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    def delete_file(self, file_name):
        file_path = self.search_file(file_name)
        try:
            if file_path:
                os.remove(file_path)
                print(f"File '{file_name}' deleted successfully.")
            else:
                print(f"File '{file_name}' not found.")
        except PermissionError:
            print(f"Permission denied to delete '{file_name}'.")

    def rename_file(self, old_name, new_name):
        old_path = self.search_file(old_name)
        if old_path:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                print(f"File '{old_name}' renamed to '{new_name}' successfully.")
            except PermissionError:
                print(f"Permission denied to rename '{old_name}'.")
        else:
            print(f"File '{old_name}' not found.")

    def extract_target_name(self, command):
        start_index = command.find(" ") + 1
        return command[start_index:].strip()

    def extract_app_name(self, command):
        start_index = command.find("launch") + len("launch")
        return command[start_index:].strip()

    def set_volume(self,value):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(value, None)

    def set_brightness(self,value):
        SC_MONITORPOWER = 0xF170
        HWND_BROADCAST = 0xFFFF
        windll.user32.SendMessageW(HWND_BROADCAST, SC_MONITORPOWER, value, 0)
    def extract_brightness_value(self, command):
        try:
            brightness_value = int(command.split()[-1])
            return brightness_value
        except ValueError:
            print("Invalid brightness command format.")
            return None

    def extract_volume_value(self, command):    
        try:
            volume_value = int(command.split()[-1])
            return volume_value
        except ValueError:
            print("Invalid volume command format.")
            return None

def interpret_and_execute(user_command):
    instruction = '''
Hi, you are an api integrated in my project. My python based project is like a voice assistant which helps in doing some laptop tasks using user’s voice commands only like opening a file, launching an application, renaming or deleting a file, playing, pausing or skipping media in media player etc. I’m using you so that you can take my general english commands , interpret what i want to do and than give me the list of commands i need to execute for completing the task. 
You can use prebuilt functions which are there in the FileManager class or you can use pyautogui command to mimic keyboard inputs. But remember you only need to give me the commands i should execute, nothing else. No words, no explanation and even no comment, just commands or functions in text form because later i will run your response which is gonna be code/functions and obviously if it will contain words than it can’t be run. If you didn’t find any possible function to be run then return ‘42’ in the output.  

Here is a example: Like suppose i tell you

Hey chatgpt, today is a nice day right? Please launch chrome and search for top food restaurant in jaipur. 
Then you should return 

file_manager.execute_command("launch chrome")
time.sleep(3)
pyautogui.write("top food restaurant in Jaipur")
pyautogui.press('enter')

The time gap is given so that there is sufficient time to chrome to open before we write anything on the type bar. 

Here is a code for file related tasks: 

import os
import pyautogui

class FileManager:
    def __init__(self):
        self.root_dir = 'C:\\'

    def search_file(self, file_name):
        for foldername, subfolders, filenames in os.walk(self.root_dir):
            if file_name in filenames or file_name in subfolders:
                return os.path.join(foldername, file_name)
        return None

    def open_target_with_run(self, target_path):
        pyautogui.hotkey('winleft', 'r')  # Opens the Run dialog
        pyautogui.write(f'"{target_path}"')  # Enclose the target path in quotes
        pyautogui.press('enter')

    def open_target(self, target_name):
        target_path = self.search_file(target_name)
        if target_path:
            self.open_target_with_run(target_path)
        else:
            print(f"Target '{target_name}' not found.")


    def launch_application(self, app_name):
        # try:
        #     os.system(f"start {app_name}")
        # except Exception as e:
        #     print(f"Error launching application '{app_name}': {e}")
        try:
                pyautogui.press('winleft')
                time.sleep(1)
                pyautogui.write(app_name)
                pyautogui.press('enter')
        except Exception as e:
            print(f"Error launching application '{app_name}': {e}")


    def execute_command(self, command):
        if "open" in command:
            target_name = self.extract_target_name(command)
            if target_name:
                self.open_target(target_name)
            else:
                print("No target specified in the command.")
        elif "launch" in command:
            app_name = self.extract_app_name(command)
            if app_name:
                self.launch_application(app_name)
            else:
                print("No application specified in the command.")
        elif "rename" in command:
            old_name, new_name = self.extract_rename_info(command)
            if old_name and new_name:
                self.rename_file(old_name, new_name)
        elif "brightness" in command:
            brightness_value = self.extract_brightness_value(command)
            if brightness_value is not None:
                self.set_brightness(brightness_value)
        elif "volume" in command:
            volume_value = self.extract_volume_value(command)
            if volume_value is not None:
                self.set_volume(volume_value)
            else:
                print("Invalid rename command.")
        elif "size" in command:
            file_name = self.extract_target_name(command)
            if file_name:
                self.show_file_size(file_name)
            else:
                print("No file specified for size command.")
        elif "delete" in command:
            file_name = self.extract_target_name(command)
            if file_name:
                self.delete_file(file_name)
            else:
                print("No file specified for delete command.")
        elif "exit" in command:
            print("Exiting the script.")
            exit()
        else:
            print("Command not recognized.")

    def extract_rename_info(self, command):
        start_index = command.find("rename") + len("rename")
        names = command[start_index:].split(" to ")
        return names[0].strip(), names[1].strip() if len(names) == 2 else (None, None)

    def show_file_size(self, file_name):
        file_path = self.search_file(file_name)
        try:
            if file_path:
                size = os.path.getsize(file_path)
                print(f"Size of '{file_name}': {size} bytes")
            else:
                print(f"File '{file_name}' not found.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    def delete_file(self, file_name):
        file_path = self.search_file(file_name)
        try:
            if file_path:
                os.remove(file_path)
                print(f"File '{file_name}' deleted successfully.")
            else:
                print(f"File '{file_name}' not found.")
        except PermissionError:
            print(f"Permission denied to delete '{file_name}'.")

    def rename_file(self, old_name, new_name):
        old_path = self.search_file(old_name)
        if old_path:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                print(f"File '{old_name}' renamed to '{new_name}' successfully.")
            except PermissionError:
                print(f"Permission denied to rename '{old_name}'.")
        else:
            print(f"File '{old_name}' not found.")

    def extract_target_name(self, command):
        start_index = command.find(" ") + 1
        return command[start_index:].strip()

    def extract_app_name(self, command):
        start_index = command.find("launch") + len("launch")
        return command[start_index:].strip()

    def set_volume(value):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(value, None)

    def set_brightness(value):
        SC_MONITORPOWER = 0xF170
        HWND_BROADCAST = 0xFFFF
        windll.user32.SendMessageW(HWND_BROADCAST, SC_MONITORPOWER, value, 0)
    def extract_brightness_value(self, command):
        try:
            brightness_value = int(command.split()[-1])
            return brightness_value
        except ValueError:
            print("Invalid brightness command format.")
            return None

    def extract_volume_value(self, command):    
        try:
            volume_value = int(command.split()[-1])
            return volume_value
        except ValueError:
            print("Invalid volume command format.")
            return None

# Example usage:
file_manager = FileManager()
while True:
    user_input = input("Enter a command (or 'exit' to quit): ").lower()
    file_manager.execute_command(user_input)



More examples: 
open mono.txt . after opening close it and rename it to dono.txt then delete it. after that open vlc media player and play the media

Output: 
file_manager.execute_command("open mono.txt")
time.sleep(5)
pyautogui.hotkey('alt', 'f4') time.sleep(1)
file_manager.execute_command("rename mono.txt to dono.txt")
file_manager.execute_command("delete dono.txt")
file_manager.execute_command("launch vlc media player")
time.sleep(2)
pyautogui.press('space')  

Noticed how this code recognised that there is a already built function to open files thus used it in first line. After that it realised that opening documents can take time thus it gave buffer using time.sleep(5). For opening ppts you can take longer gap like 7 seconds to execute next command as powerpoint opens a little late . Also it realised that there is no already built function available to close a open file thus it used keyboard hotkeys

Next example: 

hey gpt. i just made a great ppt. it's named demo.ppt. open it and go to the next slide 3 times with sufficient wait.

Output: 
file_manager.execute_command("open demo.ppt")
time.sleep(3)
pyautogui.press('right')
time.sleep(5)
pyautogui.press('right')
time.sleep(5)
pyautogui.press('right')

Do like this. also remember for powerpoint file extension is pptx not ppt.  
Be ready The next line is my command.
    '''

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": instruction},
            {"role": "user", "content": user_command}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response.choices[0].message.content)
    commands = response.choices[0].message.content.split('\n')
    
    file_manager = FileManager()
    for command in commands:
        if command.strip():
            print(command)
            exec(command)

# Example usage:
# user_command = "hey gpt. open record_000001.asf and then pause it for 5 seconds. after 5 seconds play it and then skip it 30 seconds ahead" 
# user_command = "open study.pptx and go to the next slide"
# while True:
#     user_command = input("Enter a command (or 'exit' to quit): ").lower()
#     if user_command == "exit":
#         print("Exiting the script.")
#         exit()
#     interpret_and_execute(user_command)
def listen_and_execute():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        try:
            audio = recognizer.listen(source, timeout=0.7)
        except sr.WaitTimeoutError:
            print("Timeout, no speech detected.")
            return

    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)
        interpret_and_execute(text)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    # mic = WhisperMic(model="tiny", english=True)
    # text = mic.listen()
    # print("You said:", text)
    # interpret_and_execute(text)

if __name__ == "__main__":
    while True:
        listen_and_execute()
# user_command = "open study.pptx and wait for 5 seconds after that move to the next slide"
# interpret_and_execute(user_command)
# import speech_recognition as sr



