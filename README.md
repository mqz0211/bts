
> **License:** Apache-2.0 — see `LICENSE`  
> **Warning:** Use at your own risk. Review `DISCLAIMER.md` before using



🔎 What is AINS?
---
AINS (Advanced Integrated NILAM System) is the platform used in Malaysian schools to track student reading habits. Students must log books they’ve read, including:

- Title

- Author

- Publisher

- Book Type (Physical/Ebook)

- Category (Fiction/Non-Fiction)

- Summary (min. 10 words)

- Lesson (min. 5 words)
 
- Rating (1–5 stars)

This process is time-consuming, repetitive, and often demotivating for students who want to focus on real learning rather than bureaucratic logging.
---
🚀 What is BTS?

BTS (Beat The System) is a Python GUI program that automates AINS book entries.

It:

✅ Finds books automatically using OpenLibrary API (English + Malay titles).

✅ If publisher/IMEI data is missing, fills gaps using OpenAI API.

✅ Generates a random-length summary (10–18 words).

✅ Generates a lesson statement (5–8 words).

✅ Assigns a random star rating (3–5).

✅ Supports batch generation (up to 30 books per day).

✅ GUI button interface → user just clicks once, the program handles everything.

---
⚙️ Requirements

Python 3.10+

Installed libraries:
```bash
pip install requests openai python-dotenv
```
Tkinter (comes with Python by default, but on macOS you may need to run):
```bash
brew install python-tk
```
An OpenAI API key stored in .env:
```ini
OPENAI_API_KEY=sk-xxxxxx
```
---
**Instruction**

*Click “Find Book” → The GUI will:

  * Search for books.

  * Auto-fill metadata (title, author, publisher, type, category).

  * Generate summary, lesson, and rating.

  * Show results ready for copy-paste into AINS.

---
**⚠️ Disclaimer**

This project is not affiliated with or endorsed by AINS, NILAM, or the Ministry of Education Malaysia.

It is provided for educational and research purposes only to demonstrate automation with APIs, GUIs, and natural language processing.

By using this software, you agree that:

You are solely responsible for how you use it.

The author(s) are not liable for any misuse, academic consequences, or disciplinary action.

You should comply with all applicable school and government rules.

--- 




    
