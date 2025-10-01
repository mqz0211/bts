import tkinter as tk
from tkinter import ttk, messagebox
import random
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== Functions ===== #

def fetch_books_from_subject(subject, limit=5):
    url = f"https://openlibrary.org/subjects/{subject}.json?limit=50"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        works = data.get("works", [])
        if works:
            return random.sample(works, min(limit, len(works)))
    return []

def generate_summary_and_lesson(title):
    summary_len = random.randint(10, 18)
    lesson_len = random.randint(5, 8)
    prompt = (
        f"Write two outputs about the book '{title}':\n"
        f"1. A {summary_len}-word summary.\n"
        f"2. A {lesson_len}-word lesson.\n\n"
        f"Return them clearly labeled as 'Summary:' and 'Lesson:'."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120
    )
    text = response.choices[0].message.content.strip()
    # Extract clean parts
    summary, lesson = "Unknown", "Unknown"
    for line in text.splitlines():
        if line.lower().startswith("summary"):
            summary = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("lesson"):
            lesson = line.split(":", 1)[-1].strip()
    return summary, lesson

def process_book(work):
    title = work.get("title", "Unknown Title")
    author = work.get("authors", [{"name": "Unknown"}])[0]["name"]
    publisher = work.get("publishers", ["Unknown"])[0] if "publishers" in work else "Unknown"
    isbn = work.get("cover_edition_key", "Unknown")
    subjects = work.get("subject", [])

    category = "Fiction" if any(("fiction" in s.lower()) for s in (subjects or [])) else "Non-Fiction"
    book_type = "Physical"

    summary, lesson = generate_summary_and_lesson(title)
    stars = random.randint(3, 5)

    text = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Publisher: {publisher}\n"
        f"ISBN: {isbn}\n"
        f"Type: {book_type} | Category: {category}\n"
        f"Summary: {summary}\n"
        f"Lesson: {lesson}\n"
        f"Rating: {stars} ⭐\n"
        f"{'-'*40}\n"
    )
    return text

def batch_find_books():
    subject = subject_var.get()
    if not subject:
        messagebox.showwarning("Select subject", "Please choose a subject")
        return
    output_text.delete("1.0", tk.END)
    works = fetch_books_from_subject(subject, limit=5)
    if not works:
        output_text.insert(tk.END, "No books found for that subject.\n")
        return
    for w in works:
        try:
            entry = process_book(w)
        except Exception as e:
            entry = f"Error processing book: {e}\n"
        output_text.insert(tk.END, entry)
        output_text.see(tk.END)

# ===== GUI Setup ===== #

root = tk.Tk()
root.title("BTS AINS Auto Book Fetcher")
root.configure(bg="#f0f0f0")
root.geometry("700x500")
root.resizable(True, True)

style = ttk.Style(root)
try:
    style.theme_use("clam")
except:
    pass

style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TButton", font=("Arial", 11), padding=6)

mainframe = ttk.Frame(root, padding=20, style="TFrame")
mainframe.place(relx=0.5, rely=0.02, anchor="n")

ttk.Label(mainframe, text="Subject:").grid(row=0, column=0, sticky="w")
subject_var = tk.StringVar()
subject_dropdown = ttk.Combobox(mainframe, textvariable=subject_var, values=[
    "history", "science", "education", "technology", "malay"
], state="readonly", font=("Arial", 11), width=20)
subject_dropdown.grid(row=0, column=1, padx=10, pady=10)
subject_dropdown.current(0)

ttk.Button(mainframe, text="Fetch Books", command=batch_find_books).grid(row=0, column=2, padx=10, pady=10)

output_frame = ttk.Frame(root, style="TFrame")
output_frame.place(relx=0.5, rely=0.15, anchor="n", relwidth=0.95, relheight=0.80)

output_text = tk.Text(output_frame, wrap="word", font=("Courier", 10), bg="white", fg="black")
output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
output_text.configure(yscrollcommand=output_scroll.set)

output_scroll.pack(side="right", fill="y")
output_text.pack(side="left", fill="both", expand=True)

root.mainloop()
