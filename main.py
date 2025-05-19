import tkinter as tk
from tkinter import messagebox
import pyperclip
from openai import OpenAI
import time

# 🔐 Replace this with your real OpenAI API key
client = OpenAI(api_key="your-api-key-here")

# 🪟 Set up the main window
root = tk.Tk()
root.title("Email Refiner")
root.geometry("800x500")
root.resizable(False, False)

# 🪟 Title Label
tk.Label(root, text="AI Email Refiner", font=("Helvetica", 18, "bold")).pack(pady=10)

# 🎯 Style Selection
style_var = tk.StringVar(value="Professional")
tk.Label(root, text="Choose Writing Style:", font=("Helvetica", 10)).pack()

style_options = ["Professional", "Formal", "Casual", "Persuasive"]
style_menu = tk.OptionMenu(root, style_var, *style_options)
style_menu.pack(pady=5)

# 🧪 Mock Mode Toggle
mock_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Use Mock Mode (Offline Testing)", variable=mock_var).pack(pady=5)

# 📝 Rough Draft Textbox (Left Pane)
rough_textbox = tk.Text(root, height=15, width=50, wrap="word", padx=10, pady=10)
rough_textbox.pack(side=tk.LEFT, padx=10, pady=10)

# ✅ Refined Output Textbox (Right Pane)
refined_textbox = tk.Text(root, height=15, width=50, wrap="word", padx=10, pady=10, bg="#f0f0f0")
refined_textbox.pack(side=tk.RIGHT, padx=10, pady=10)

# 🧠 Refine Button Logic
def refine_text():
    rough_text = rough_textbox.get("1.0", tk.END).strip()
    selected_style = style_var.get()
    use_mock = mock_var.get()

    if not rough_text:
        messagebox.showwarning("Warning", "Please enter some text to refine.")
        return

    refined_textbox.delete("1.0", tk.END)
    refined_textbox.insert(tk.END, "Loading... Please wait...")
    root.update_idletasks()

    if use_mock:
        time.sleep(1.2)
        mock_styles = {
            "Professional": "Here's a more professional version of your email:",
            "Formal": "This is a formal revision of your message:",
            "Casual": "Here’s a casual take on your message:",
            "Persuasive": "Here’s a more persuasive version:"
        }
        instruction = mock_styles.get(selected_style, "Refined output:")
        mock_response = f"{instruction}\n\n{rough_text.capitalize()} (Refined mock output.)"
        refined_textbox.delete("1.0", tk.END)
        refined_textbox.insert(tk.END, mock_response)
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Rewrite the following text in a {selected_style.lower()} style."},
                    {"role": "user", "content": rough_text}
                ]
            )
            refined_content = response.choices[0].message.content
            refined_textbox.delete("1.0", tk.END)
            refined_textbox.insert(tk.END, refined_content)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")

# 📋 Copy Button Logic
def copy_to_clipboard():
    text = refined_textbox.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Refined text copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "There's no text to copy.")

# ❌ Clear Both Fields
def clear_all():
    rough_textbox.delete("1.0", tk.END)
    refined_textbox.delete("1.0", tk.END)

# 🔘 Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Refine", command=refine_text, width=15).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Copy Refined Text", command=copy_to_clipboard, width=20).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear", command=clear_all, width=10).grid(row=0, column=2, padx=5)

# 🚀 Run the app
root.mainloop()
