# 📱 WhatsApp Bulk Message Sender (Desktop Automation)

A Python-based WhatsApp Desktop automation tool with an Excel-style GUI for sending bulk text messages and images.

This application is built for **Windows + WhatsApp Desktop**, supports **multi-line messages**, and allows importing data directly from **Excel files**.

---

## ✨ Features

- Excel-style table interface
- Multi-line message support (Ctrl + Enter)
- Import contacts from Excel (.xlsx)
- Copy / Paste / Cut / Fill Down like Excel
- Send text-only or image messages
- Random delay between messages
- Auto-adjusting row height
- PyAutoGUI failsafe enabled
- Final success/failure report

---

## 🖼️ Table Columns

| Column | Description |
|------|------------|
| Contact Name | Exact WhatsApp contact name |
| Message | Message text (multi-line supported) |
| Image Folder Path | Folder containing image (optional) |
| Image File Name | Image filename with extension (optional) |

If Image Path and File Name are empty, a text-only message is sent.

---

## 📂 Excel Import Format

| Excel Column | Description |
|-------------|------------|
| A | Contact Name |
| B | Message |
| C | Image Folder Path |
| D | Image File Name |

- First row is treated as header
- Multi-line messages are preserved
- Maximum 20 contacts per run

---

## 🛠️ Installation

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv practice
   practice\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt
