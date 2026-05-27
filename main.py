# ============================================================
#  Scientific Calculator — main.py
#  Built with Python + Tkinter
#  Features: Dark glassmorphism-style UI, scientific functions,
#            hover effects, rounded buttons, keyboard support
# ============================================================

import tkinter as tk
from math import *

# ── Window Setup ─────────────────────────────────────────────
root = tk.Tk()
root.title("🧮 Scientific Calculator")
root.geometry("420x720")
root.configure(bg="#0d0d1a")   # Deep dark background
root.resizable(False, False)

# ── Color Palette (Dark Glass Style) ─────────────────────────
CLR_BG       = "#0d0d1a"   # Window background
CLR_DISPLAY  = "#12122a"   # Display area
CLR_NUM      = "#1a1a35"   # Number button
CLR_NUM_HVR  = "#2a2a55"   # Number button hover
CLR_OP       = "#1a2a4a"   # Operator button
CLR_OP_HVR   = "#2a4a7a"   # Operator button hover
CLR_SCI      = "#1a2a2a"   # Scientific button
CLR_SCI_HVR  = "#2a4a4a"   # Scientific button hover
CLR_EQ       = "#3b5bdb"   # Equals button
CLR_EQ_HVR   = "#4c6ef5"   # Equals button hover
CLR_CLR      = "#c0392b"   # Clear button
CLR_CLR_HVR  = "#e74c3c"   # Clear button hover
CLR_TEXT     = "#e0e0ff"   # Main text
CLR_OP_TEXT  = "#74b9ff"   # Operator text color
CLR_SCI_TEXT = "#55efc4"   # Scientific text color

# ── State ─────────────────────────────────────────────────────
equation = ""
display_var = tk.StringVar()

# ── Display Area ──────────────────────────────────────────────
display_frame = tk.Frame(root, bg=CLR_DISPLAY, pady=10)
display_frame.pack(fill="both", padx=15, pady=(15, 5))

# Small expression label (shows what user typed)
expr_var = tk.StringVar()
expr_label = tk.Label(
    display_frame,
    textvariable=expr_var,
    font=("Courier New", 11),
    bg=CLR_DISPLAY,
    fg="#6666aa",
    anchor="e",
    padx=10
)
expr_label.pack(fill="both")

# Main result display
display = tk.Entry(
    display_frame,
    textvariable=display_var,
    font=("Courier New", 26, "bold"),
    bg=CLR_DISPLAY,
    fg=CLR_TEXT,
    bd=0,
    justify="right",
    insertbackground=CLR_TEXT,
    state="readonly",          # User can't type directly (use buttons/keyboard)
    readonlybackground=CLR_DISPLAY
)
display.pack(fill="both", ipadx=10, ipady=8, padx=10)

# ── Core Logic ────────────────────────────────────────────────

def press(value):
    """Append a value to the equation."""
    global equation
    equation += str(value)
    display_var.set(equation)
    expr_var.set("")

def clear():
    """Clear everything."""
    global equation
    equation = ""
    display_var.set("")
    expr_var.set("")

def backspace():
    """Delete last character."""
    global equation
    equation = equation[:-1]
    display_var.set(equation)

def calculate():
    """Evaluate the current equation."""
    global equation
    try:
        expr_var.set(equation + " =")
        result = str(eval(equation))
        # Remove unnecessary decimals (e.g. 4.0 → 4)
        if result.endswith(".0"):
            result = result[:-2]
        display_var.set(result)
        equation = result
    except ZeroDivisionError:
        display_var.set("÷ by Zero!")
        equation = ""
    except:
        display_var.set("Error")
        equation = ""

def sci_func(func, label):
    """Apply a scientific function to current value."""
    global equation
    try:
        val = eval(equation)
        if func == "sin":   result = sin(radians(val))
        elif func == "cos": result = cos(radians(val))
        elif func == "tan": result = tan(radians(val))
        elif func == "sqrt":result = sqrt(val)
        elif func == "sq":  result = val ** 2
        elif func == "log": result = log10(val)
        elif func == "ln":  result = log(val)
        elif func == "inv": result = 1 / val
        elif func == "exp": result = exp(val)
        elif func == "fact":result = factorial(int(val))
        else: return
        expr_var.set(f"{label}({equation}) =")
        result_str = str(round(result, 10))
        if result_str.endswith(".0"):
            result_str = result_str[:-2]
        display_var.set(result_str)
        equation = result_str
    except:
        display_var.set("Error")
        equation = ""

# ── Hover Effect ──────────────────────────────────────────────

def on_enter(btn, hover_color):
    btn.config(bg=hover_color)

def on_leave(btn, normal_color):
    btn.config(bg=normal_color)

# ── Button Factory ────────────────────────────────────────────

def make_button(parent, text, command, row, col,
                bg=CLR_NUM, fg=CLR_TEXT, hover=CLR_NUM_HVR,
                colspan=1, rowspan=1, font_size=14):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Courier New", font_size, "bold"),
        bg=bg,
        fg=fg,
        bd=0,
        relief="flat",
        activebackground=hover,
        activeforeground=fg,
        cursor="hand2"
    )
    btn.grid(
        row=row, column=col,
        columnspan=colspan, rowspan=rowspan,
        padx=5, pady=5,
        sticky="nsew",
        ipadx=5, ipady=10
    )
    # Hover effects
    btn.bind("<Enter>", lambda e: on_enter(btn, hover))
    btn.bind("<Leave>", lambda e: on_leave(btn, bg))
    return btn

# ── Button Grid ───────────────────────────────────────────────
frame = tk.Frame(root, bg=CLR_BG)
frame.pack(fill="both", expand=True, padx=15, pady=5)

# Make all columns & rows stretch evenly
for i in range(4):
    frame.columnconfigure(i, weight=1)
for i in range(9):
    frame.rowconfigure(i, weight=1)

# Row 0 — Scientific row 1
make_button(frame, "sin",  lambda: sci_func("sin","sin"),  0, 0, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "cos",  lambda: sci_func("cos","cos"),  0, 1, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "tan",  lambda: sci_func("tan","tan"),  0, 2, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "π",    lambda: press(str(pi)),         0, 3, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)

# Row 1 — Scientific row 2
make_button(frame, "ln",   lambda: sci_func("ln","ln"),    1, 0, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "log",  lambda: sci_func("log","log"),  1, 1, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "1/x",  lambda: sci_func("inv","1/x"),  1, 2, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "e",    lambda: press(str(e)),          1, 3, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)

# Row 2 — Scientific row 3
make_button(frame, "eˣ",   lambda: sci_func("exp","eˣ"),   2, 0, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "x²",   lambda: sci_func("sq","x²"),    2, 1, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "√",    lambda: sci_func("sqrt","√"),   2, 2, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)
make_button(frame, "n!",   lambda: sci_func("fact","n!"),  2, 3, bg=CLR_SCI, fg=CLR_SCI_TEXT, hover=CLR_SCI_HVR, font_size=12)

# Row 3 — Control row
make_button(frame, "C",    clear,                          3, 0, bg=CLR_CLR, fg="white", hover=CLR_CLR_HVR)
make_button(frame, "( )",  lambda: press("("),             3, 1, bg=CLR_OP,  fg=CLR_OP_TEXT, hover=CLR_OP_HVR)
make_button(frame, ")",    lambda: press(")"),             3, 2, bg=CLR_OP,  fg=CLR_OP_TEXT, hover=CLR_OP_HVR)
make_button(frame, "÷",    lambda: press("/"),             3, 3, bg=CLR_OP,  fg=CLR_OP_TEXT, hover=CLR_OP_HVR)

# Row 4
make_button(frame, "7",    lambda: press("7"),             4, 0)
make_button(frame, "8",    lambda: press("8"),             4, 1)
make_button(frame, "9",    lambda: press("9"),             4, 2)
make_button(frame, "×",    lambda: press("*"),             4, 3, bg=CLR_OP, fg=CLR_OP_TEXT, hover=CLR_OP_HVR)

# Row 5
make_button(frame, "4",    lambda: press("4"),             5, 0)
make_button(frame, "5",    lambda: press("5"),             5, 1)
make_button(frame, "6",    lambda: press("6"),             5, 2)
make_button(frame, "−",    lambda: press("-"),             5, 3, bg=CLR_OP, fg=CLR_OP_TEXT, hover=CLR_OP_HVR)

# Row 6
make_button(frame, "1",    lambda: press("1"),             6, 0)
make_button(frame, "2",    lambda: press("2"),             6, 1)
make_button(frame, "3",    lambda: press("3"),             6, 2)
make_button(frame, "+",    lambda: press("+"),             6, 3, bg=CLR_OP, fg=CLR_OP_TEXT, hover=CLR_OP_HVR)

# Row 7
make_button(frame, "%",    lambda: press("%"),             7, 0, bg=CLR_OP, fg=CLR_OP_TEXT, hover=CLR_OP_HVR)
make_button(frame, "0",    lambda: press("0"),             7, 1)
make_button(frame, ".",    lambda: press("."),             7, 2)
make_button(frame, "⌫",    backspace,                      7, 3, bg=CLR_OP, fg="#ff7675", hover=CLR_OP_HVR)

# Row 8 — Equals (full width)
make_button(frame, "=",    calculate,                      8, 0, bg=CLR_EQ, fg="white",
            hover=CLR_EQ_HVR, colspan=4, font_size=18)

# ── Keyboard Support ──────────────────────────────────────────

def on_key(event):
    key = event.keysym
    char = event.char

    if char in "0123456789.+-*/()%":
        press(char)
    elif key == "Return" or key == "equal":
        calculate()
    elif key == "BackSpace":
        backspace()
    elif key == "Escape":
        clear()

root.bind("<Key>", on_key)

# ── Run ───────────────────────────────────────────────────────
root.mainloop()
