import json
import time
import tkinter as tk
from tkinter import messagebox, font
import winsound

# Código para crear diccionario morse
# with open("morse-dict.json", "w") as morse_dict_file:
#     morse_code_dict = {
#         'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
#         'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
#         'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
#         'Y': '-.--', 'Z': '--..',
#         '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
#         '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
#         '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
#         '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
#         ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
#         '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
#     }
#     json.dump(morse_code_dict, morse_dict_file, indent=4)

DOT_DURATION = 100
SLASH_DURATION = 500
FREQUENCY = 700

accent_letters = "áéíóúüñ"
no_accent_letters = 'aeiouun'
no_accent_translation = str.maketrans(accent_letters, no_accent_letters)


def play_morse_code(morse_code):
    morse_code.replace("/", "")
    for symbol in morse_code:
        main_window.update()
        if symbol == ".":
            winsound.Beep(FREQUENCY, DOT_DURATION)
        elif symbol == "-":
            winsound.Beep(FREQUENCY, SLASH_DURATION)
        time.sleep(0.2)


def update_output(morse_code):
    output_text_widget.config(state="normal")
    output_text_widget.delete("1.0", tk.END)
    output_text_widget.insert(tk.END, morse_code)
    output_text_widget.config(state="disabled")
    main_window.update()


def adapt_output(morse_code, text_input):
    max_len = max(len(word) for word in text_input.split(" "))
    split_morse_code = [element.strip() for element in morse_code.split("\n")]
    output_text = "\n".join([f"{text}{" "*(max_len - len(text))}| {morse}"
                             for text, morse in zip(text_input.split(" "), split_morse_code)])
    return output_text


def convert_to_morse():
    text_input = input_entry.get()
    no_accent_text_input = text_input.translate(no_accent_translation)
    try:
        morse_code = " ".join([morse_code_dict[char.upper()] for char in no_accent_text_input])
        text_output = adapt_output(morse_code, text_input)
        update_output(text_output)
        play_morse_code(morse_code)
    except KeyError as e:
        message = f"The character {e} does not exist in Morse code. Try another word."
        messagebox.showinfo("Error", message)


with open("morse-dict.json", "r") as morse_dict_file:
    morse_code_dict = json.load(morse_dict_file)

main_window = tk.Tk()
main_window.title("Morse Code Dictionary - text2morse")
main_window.minsize(520, 600)
main_window.maxsize(520, 300)

title_font = font.Font(family="Helvetica", size=14)
title_label = tk.Label(main_window, text="Welcome to text2morse, get ready to watch and listen", font=title_font)
input_label = tk.Label(main_window, text="Text Input:")
output_label = tk.Label(main_window, text="Morse Code:")

input_entry = tk.Entry(main_window, width=66)
output_text_widget = tk.Text(main_window, height=28, width=50, state="disabled")

run_button = tk.Button(text="Convert to Morse", command=convert_to_morse)

title_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
input_label.grid(row=2, column=1, padx=5, pady=5, sticky="n")
input_entry.grid(row=2, column=2, padx=5, pady=5)

output_label.grid(row=3, column=1, padx=5, pady=5)
output_text_widget.grid(row=3, column=2, padx=5, pady=5)

run_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

main_window.mainloop()
