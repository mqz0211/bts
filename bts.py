import tkinter as tk
from tkinter import ttk, messagebox
import requests
import random
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Functions ---

def fetch_books_from_subject(subject, limit=10):
    """Fetch random books from a subject on OpenLibrary"""
    url = f"https://openlibrary.org/subjects/{subject}.json?limit=50"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        works = data.get("works", [])
        if not works:
            return []
        return random.sample(works, min(limit, len(works)))
    return []

def fetch_missing_with_openai(title, author, missing):
    """Ask OpenAI for missing publisher or ISBN (IMEI)"""
    query = f"Find the official {missing} of the book '{title}' by {author}. Only return the {missing}, do not invent."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        max_tokens=50
    )
    return response.choices[0].message.content.strip()

def generate_summary_and_lesson(title):
    """Generate short summary and lesson"""
    summary_len = random.randint(10, 18)
    lesson_len = random.randint(5, 8)

    prompt = f"Write a {summary_len}-word summary of the book '{title}'."
    summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    ).choices[0].message.content.strip()

    lesson_prompt = f"Write a {lesson_len}-word lesson from the book '{title}'."
    lesson = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": lesson_prompt}],
        max_tokens=60
    ).choices[0].message.content.strip()

    return summary, lesson

def process_book(work):
    """Process one OpenLibrary work into full info"""
    title = work.get("title")
    author = work.get("authors", [{"name": "Unknown"}])[0]["name"]
    publisher = work.get("publishers", [None])[0] if "publishers" in work else None
    isbn = work.get("cover_edition_key", None)  # OpenLibrary often has edition keys instead of ISBN
    subjects = work.get("subject", [])

    # Fallbacks with OpenAI
    if not publisher:
        publisher = fetch_missing_with_openai(title, author, "publisher")
    if not isbn:
        isbn = fetch_missing_with_openai(title, author, "ISBN")

    # Book type & category
    book_type = "Physical"  # default assumption
    category = "Fiction" if any("fiction" in s.lower() for s in subjects or []) else "Non-Fiction"

    # Generate summary & lesson
    summary, lesson = generate_summary_and_lesson(title)

    # Random star rating
    stars = random.randint(3, 5)

    result = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Publisher: {publisher}\n"
        f"ISBN/IMEI: {isbn}\n"
        f"Book Type: {book_type}\n"
        f"Category: {category}\n\n"
        f"Summary: {summary}\n"
        f"Lesson: {lesson}\n"
        f"Rating: {stars}/5 ⭐\n"
        f"{'-'*50}\n\n"
    )
    return result

def batch_find_books():
    subject = subject_var.get()
    if not subject:
        messagebox.showwarning("Error", "Please select a subject")
        return

    works = fetch_books_from_subject(subject, limit=5)
    if not works:
        messagebox.showerror("Error", f"No books found for subject: {subject}")
        return

    output.delete("1.0", tk.END)
    for work in works:
        result = process_book(work)
        output.insert(tk.END, result)
        output.see(tk.END)
        root.update_idletasks()

# --- GUI ---
root = tk.Tk()
root.title("Book finder")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Select Subject:").grid(column=0, row=0, sticky="w")

subject_var = tk.StringVar()
subject_dropdown = ttk.Combobox(frm, textvariable=subject_var, values=[
    "history", "science", "education", "technology", "malay"
], state="readonly")
subject_dropdown.grid(column=1, row=0, padx=5)
subject_dropdown.current(0)

ttk.Button(frm, text="Find Books", command=batch_find_books).grid(column=2, row=0, padx=5)

output = tk.Text(frm, width=80, height=25)
output.grid(column=0, row=1, columnspan=3, pady=10)

root.mainloop()
