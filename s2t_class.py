import platform
import pathlib

import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer

# from nltk import tokenize as tk
from nltk.corpus import stopwords, wordnet

# from operator import itemgetter
import sys
import vosk
import json
from vosk import SetLogLevel
import os
from time import time
from settings import Config
from datetime import datetime

SetLogLevel(-1)
# nltk.download("averaged_perceptron_tagger")
# nltk.download("punkt")
# nltk.download("wordnet")

p = platform.system()


class Speech2Text:
    def __init__(
        self, mode=None, loc=None, src=None, output=f"{int(time())}.txt", config={}
    ):
        self.mode = mode
        self.loc = loc
        self.src = src
        self.cmd = None
        self.output = output
        self.config = config
        self.file = open(self.output, "a")

    def listen(self):
        rec = sr.Recognizer()
        if self.mode == "mic":
            with sr.Microphone() as src:
                rec.adjust_for_ambient_noise(src)
                audio = rec.listen(src)
        elif self.mode == "rec":
            with sr.AudioFile(self.loc) as src:
                audio = rec.record(src)
        try:
            if self.src == "vosk":
                self.cmd = rec.recognize_vosk(audio)  # language="en-in")
            elif self.src == "google":
                self.cmd = rec.recognize_google(audio, language="en-us")
            # print(f"Command: {cmd}")
        except Exception:
            print("Sorry, couldn't hear. Mind trying typing it?")
            self.cmd = input()
        # cmd=cmd.split(" ")
        return self.cmd

    # def psphinx(self):
    #     sp = pocketsphinx.LiveSpeech()
    #     return sp

    # def pos_tagger(self, tag):
    #     if tag.startswith("J"):
    #         return wordnet.ADJ
    #     elif tag.startswith("V"):
    #         return wordnet.VERB
    #     elif tag.startswith("N"):
    #         return wordnet.NOUN
    #     elif tag.startswith("R"):
    #         return wordnet.ADV
    #     else:
    #         return None

    # def lemmatizer(self, src):
    #     w = WordNetLemmatizer()
    #     pos_tagged = nltk.pos_tag(nltk.word_tokenize(src))
    #     wn_tagged = list(map(lambda x: (x[0], self.pos_tagger(x[1])), pos_tagged))
    #     ls = []  # lemmatized sentence
    #     for word, tag in wn_tagged:
    #         if tag is None:
    #             ls.append(word)
    #         else:
    #             ls.append(w.lemmatize(word, tag))
    #     return ls

    # def make_tokens(self, lms):
    #     stop_words = set(stopwords.words("english"))
    #     src3 = []
    #     for i in lms:
    #         if i in stop_words:
    #             pass
    #         else:
    #             src3.append(str(i) + " ")
    #     print("Keywords are:", end=" ")
    #     for i in src3:
    #         print(i, end=" ")
    #     print("\n\n")

    def save(self, data):
        # f = open(self.output, "a")
        # f.write(data)
        self.file.write(data + " ")

    def exec(self):
        print(
            f"\n\nSOURCE: {self.loc}, TRANSLATOR: {self.src}, MODE={self.mode}, OUTPUT FILE: {self.output}\n\n"
        )
        if self.mode == "mic":
            try:
                while True:
                    # print("\nSay some words: ")
                    c = self.listen()
                    print("Listened value=", c)
                    if self.src == "vosk":
                        self.cmd = json.loads(c)["text"]
                    elif self.src == "google":
                        self.cmd = c
                        print("Command =", self.cmd)

                    if str(self.cmd.rstrip(" ")) in self.config["triggers"]["exit"]:
                        print("\n\nExit command triggered from command! Exiting...")
                        sys.exit()
                    # lemmatized = self.lemmatizer(self.cmd)
                    # self.make_tokens(lemmatized)
                    self.save(self.cmd)
                    if self.mode == "rec":
                        break
            except KeyboardInterrupt:
                print("\n\nExit command triggered from Keyboard! Exiting...")
        elif self.mode == "rec":
            try:
                print("\nListening to the audio you supplied...")
                c = self.listen()

                print("Listened value=", c)
                if self.src == "vosk":
                    # print(type(c))
                    d = json.loads(c)
                    self.save(d["text"])
                if self.src == "google":
                    self.save(c)
                # d = json.loads(c)
            except KeyboardInterrupt:
                print("\n\nExit command triggered from Keyboard! Exiting...")


def driver_speech2text():
    loc = None
    source = None
    while True:
        mode = input("Enter mode: ('mic' for microphone or 'rec' for recording)\n")
        print("\n")
        if mode == "mic":
            break
        elif mode == "rec":
            while True:
                loc = input("Enter file location:\n")
                print("\n")
                if os.path.exists(loc):
                    break
                else:
                    print("\nFile doesn't exist. Try again.\n")
                    continue
            break
        else:
            print("\nInvalid mode.Try again\n")

    while True:
        source = input("Enter translator: ('vosk' for Vosk or 'google' for Google)\n")
        print("\n")
        if source == "google":
            break
        elif source == "vosk":
            break
        else:
            print("\nInvalid translator.Try again\n")

    print("\nEnter output file location:")
    output_file = input()

    print("\nEnter config file location:")
    config_file = input()

    if len(config_file) >= 6:
        config_instance = Config(loc=config_file).get_config()
    else:
        config_instance = Config().get_config()
    instance = Speech2Text(
        mode=mode, loc=loc, src=source, output=output_file, config=config_instance
    )
    instance.exec()
    instance.file.close()


def metrics(text1, text2):
    l1 = text1.split(" ")
    l2 = text2.split(" ")

    # print(l1, l2)
    metric = len(set(l2) - set(l1)) / len(set(l2))

    return 100 * (1 - metric)


def test():
    avg = 0

    BASE_DIR = os.getcwd()
    OUTPUT_DIR = f"{BASE_DIR}/tests/output"
    INPUT_DIR = f"{BASE_DIR}/tests/input"
    TEST_FILES = [str(f) for f in pathlib.Path(INPUT_DIR).iterdir() if f.is_file()]

    print(TEST_FILES, end="\n\n")
    for i in range(len(TEST_FILES)):
        tm = int(time())
        TARGET_VOSK = f"{OUTPUT_DIR}/test_run_vosk_{tm}.txt"
        TARGET_GOOGLE = f"{OUTPUT_DIR}/test_run_google_{tm}.txt"

        test_inst_vosk = Speech2Text(
            mode="rec", loc=TEST_FILES[i], src="vosk", output=TARGET_VOSK
        )
        test_inst_google = Speech2Text(
            mode="rec", loc=TEST_FILES[i], src="google", output=TARGET_GOOGLE
        )

        test_inst_google.exec()
        test_inst_vosk.exec()

        test_inst_google.file.close()
        test_inst_vosk.file.close()

        t1 = open(TARGET_VOSK).read()
        t2 = open(TARGET_GOOGLE).read()

        # print("\nTwo files' output being:\n")
        # print(t1, end="\n\n")
        # print(t2, end="\n\n")

        avg += metrics(str(t1), str(t2))
        print("Similarity in the recognition of the two voice packs:", metrics(str(t1), str(t2)))

        del test_inst_google
        del test_inst_vosk

    avg /= len(TEST_FILES)

    print(
        "\n\nTaking google speech2text as baseline, average performance of vosk = ", avg
    )

    OUTPUT_FILES = [str(f) for f in pathlib.Path(OUTPUT_DIR).iterdir() if f.is_file()]

    while(len(OUTPUT_FILES) > 0):
        os.remove(OUTPUT_FILES[-1])

if __name__ == "__main__":
    n = list(sys.argv)

    if len(n) > 1: 
        if sys.argv[1] == "--test":
            test()
    else:
        driver_speech2text()
