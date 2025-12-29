import pyautogui as pg
import time
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, scrolledtext
from datetime import datetime
import openpyxl
import pyperclip


# === Safety Configuration ===
pg.FAILSAFE = True
pg.PAUSE = 0.5


# Global variables
entry_grid = []
selected_cells = []
selection_start = None
undo_stack = []
redo_stack = []
is_dirty = False
last_saved_time = None


def mark_dirty():
    """Mark data as modified"""
    global is_dirty
    is_dirty = True
    update_status_bar()


def create_cell(parent, row, col, default_text=""):
    """Create a cell Text widget with Excel-like behavior and auto-height"""
    cell = tk.Text(
        parent, 
        font=("Arial", 9), 
        relief=tk.SOLID, 
        bd=1,
        wrap=tk.WORD,
        height=1,
        width=1
    )
    
    if default_text:
        cell.insert("1.0", default_text)
        adjust_cell_height(cell)
    
    cell.grid(row=row, column=col, sticky='nsew', padx=0, pady=0)
    
    cell.bind('<KeyRelease>', lambda e: on_cell_change_text(cell, row, col))
    cell.bind('<Return>', lambda e: handle_return(cell, row, col, e))
    cell.bind('<Escape>', lambda e: cancel_edit(row, col))
    cell.bind('<Tab>', lambda e: move_cell(row, col, 0, 1))
    cell.bind('<Shift-Tab>', lambda e: move_cell(row, col, 0, -1))
    cell.bind('<Up>', lambda e: handle_up(cell, row, col, e))
    cell.bind('<Down>', lambda e: handle_down(cell, row, col, e))
    cell.bind('<Left>', lambda e: handle_left_text(cell, row, col, e))
    cell.bind('<Right>', lambda e: handle_right_text(cell, row, col, e))
    cell.bind('<Home>', lambda e: move_to_start(row, col))
    cell.bind('<End>', lambda e: move_to_end(row, col))
    cell.bind('<Button-1>', lambda e: start_selection(row, col, e))
    cell.bind('<B1-Motion>', lambda e: extend_selection(row, col, e))
    
    return cell


def adjust_cell_height(cell):
    """Auto-adjust Text widget height based on content"""
    content = cell.get("1.0", "end-1c")
    lines = content.count('\n') + 1
    lines = max(1, min(lines, 5))
    cell.config(height=lines)


def on_cell_change_text(cell, row, col):
    """Track cell changes and adjust height"""
    adjust_cell_height(cell)
    mark_dirty()


def handle_return(cell, row, col, event):
    """Handle Enter key - Allow newline with Ctrl+Enter, move down with Enter"""
    if event.state & 0x4:
        return
    else:
        move_cell(row, col, 1, 0)
        return "break"


def handle_up(cell, row, col, event):
    """Handle Up arrow"""
    cursor_pos = cell.index(tk.INSERT)
    if cursor_pos.startswith("1."):
        move_cell(row, col, -1, 0)
        return "break"


def handle_down(cell, row, col, event):
    """Handle Down arrow"""
    cursor_pos = cell.index(tk.INSERT)
    last_line = int(cell.index("end-1c").split('.')[0])
    current_line = int(cursor_pos.split('.')[0])
    
    if current_line >= last_line:
        move_cell(row, col, 1, 0)
        return "break"


def handle_left_text(cell, row, col, event):
    """Handle left arrow"""
    cursor_pos = cell.index(tk.INSERT)
    if cursor_pos == "1.0":
        move_cell(row, col, 0, -1)
        return "break"


def handle_right_text(cell, row, col, event):
    """Handle right arrow"""
    cursor_pos = cell.index(tk.INSERT)
    end_pos = cell.index("end-1c")
    
    if cursor_pos == end_pos:
        move_cell(row, col, 0, 1)
        return "break"


def cancel_edit(row, col):
    return "break"


def move_to_start(row, col):
    if col > 0:
        entry_grid[row][0].focus_set()
        entry_grid[row][0].mark_set(tk.INSERT, "1.0")
    return "break"


def move_to_end(row, col):
    if col < 3:
        entry_grid[row][3].focus_set()
        entry_grid[row][3].mark_set(tk.INSERT, tk.END)
    return "break"


def start_selection(row, col, event):
    global selected_cells, selection_start
    selection_start = (row, col)
    selected_cells = [(row, col)]
    highlight_selection()
    update_status_bar()


def extend_selection(row, col, event):
    global selected_cells, selection_start
    if not selection_start:
        return
    
    start_row, start_col = selection_start
    
    min_row = min(start_row, row)
    max_row = max(start_row, row)
    min_col = min(start_col, col)
    max_col = max(start_col, col)
    
    selected_cells = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if r < len(entry_grid) and c < 4:
                selected_cells.append((r, c))
    
    highlight_selection()
    update_status_bar()


def highlight_selection():
    for row in entry_grid:
        for cell in row:
            cell.config(bg='white')
    
    for r, c in selected_cells:
        if r < len(entry_grid) and c < 4:
            entry_grid[r][c].config(bg='#D6EAF8')


def move_cell(row, col, row_delta, col_delta):
    new_row = row + row_delta
    new_col = col + col_delta
    
    if new_row < 0 or new_row >= len(entry_grid):
        return "break"
    if new_col < 0 or new_col >= 4:
        return "break"
    
    entry_grid[new_row][new_col].focus_set()
    entry_grid[new_row][new_col].mark_set(tk.INSERT, tk.END)
    
    return "break"


def copy_selection(event=None):
    if not selected_cells:
        return "break"
    
    sorted_cells = sorted(selected_cells, key=lambda x: (x[0], x[1]))
    
    rows_data = {}
    for r, c in sorted_cells:
        if r not in rows_data:
            rows_data[r] = {}
        rows_data[r][c] = entry_grid[r][c].get("1.0", "end-1c")
    
    lines = []
    for row_num in sorted(rows_data.keys()):
        row_cells = rows_data[row_num]
        line_parts = []
        for col in sorted(row_cells.keys()):
            line_parts.append(row_cells[col])
        lines.append('\t'.join(line_parts))
    
    clipboard_text = '\n'.join(lines)
    root.clipboard_clear()
    root.clipboard_append(clipboard_text)
    
    status_label.config(text=f"Copied {len(selected_cells)} cell(s)")
    root.after(2000, update_status_bar)
    
    return "break"


def cut_selection(event=None):
    copy_selection()
    
    for r, c in selected_cells:
        entry_grid[r][c].delete("1.0", tk.END)
    
    mark_dirty()
    status_label.config(text=f"Cut {len(selected_cells)} cell(s)")
    root.after(2000, update_status_bar)
    
    return "break"


def paste_handler(event=None):
    try:
        clipboard_content = root.clipboard_get()
        
        focused = root.focus_get()
        start_row, start_col = -1, -1
        
        if selected_cells:
            start_row, start_col = selected_cells[0]
        else:
            for i, row in enumerate(entry_grid):
                for j, cell in enumerate(row):
                    if focused == cell:
                        start_row, start_col = i, j
                        break
                if start_row != -1:
                    break
        
        if start_row == -1:
            start_row, start_col = 0, 0
        
        lines = clipboard_content.strip().split('\n')
        
        current_row = start_row
        
        for line in lines:
            if not line.strip():
                continue
            
            while current_row >= len(entry_grid):
                add_row()
            
            columns = line.split('\t')
            
            for col_idx, value in enumerate(columns):
                actual_col = start_col + col_idx
                
                if actual_col < 4:
                    entry_grid[current_row][actual_col].delete("1.0", tk.END)
                    entry_grid[current_row][actual_col].insert("1.0", value.strip())
                    adjust_cell_height(entry_grid[current_row][actual_col])
            
            current_row += 1
        
        mark_dirty()
        update_status_bar()
        status_label.config(text=f"Pasted {len(lines)} row(s)")
        root.after(2000, update_status_bar)
        
        return "break"
        
    except Exception as e:
        print(f"Paste error: {e}")
        messagebox.showerror("Paste Error", f"Failed to paste: {str(e)}")
        return "break"


def fill_down(event=None):
    if not selected_cells or len(selected_cells) < 2:
        return "break"
    
    sorted_cells = sorted(selected_cells, key=lambda x: (x[0], x[1]))
    
    columns = {}
    for r, c in sorted_cells:
        if c not in columns:
            columns[c] = []
        columns[c].append(r)
    
    for col, rows in columns.items():
        if len(rows) > 1:
            source_value = entry_grid[rows[0]][col].get("1.0", "end-1c")
            
            try:
                num_value = float(source_value)
                is_numeric = True
            except:
                is_numeric = False
            
            for idx, row in enumerate(rows[1:], start=1):
                if is_numeric:
                    new_value = str(num_value + idx)
                else:
                    new_value = source_value
                
                entry_grid[row][col].delete("1.0", tk.END)
                entry_grid[row][col].insert("1.0", new_value)
                adjust_cell_height(entry_grid[row][col])
    
    mark_dirty()
    status_label.config(text="Fill down applied")
    root.after(2000, update_status_bar)
    
    return "break"


def undo_action(event=None):
    status_label.config(text="Undo (coming soon)")
    root.after(2000, update_status_bar)
    return "break"


def redo_action(event=None):
    status_label.config(text="Redo (coming soon)")
    root.after(2000, update_status_bar)
    return "break"


def add_row():
    if len(entry_grid) >= 20:
        messagebox.showwarning("Limit Reached", "Maximum 20 contacts allowed!")
        return
    
    row_num = len(entry_grid)
    
    row_label = tk.Label(
        table_frame, 
        text=str(row_num + 1), 
        font=("Arial", 9, "bold"),
        bg="#E8E8E8",
        relief=tk.SOLID,
        bd=1,
        anchor='center'
    )
    row_label.grid(row=row_num, column=0, sticky='nsew', padx=0, pady=0)
    
    contact_cell = create_cell(table_frame, row_num, 1, '')
    message_cell = create_cell(table_frame, row_num, 2, '')
    path_cell = create_cell(table_frame, row_num, 3, '')
    file_cell = create_cell(table_frame, row_num, 4, '')
    
    entry_grid.append([contact_cell, message_cell, path_cell, file_cell])
    
    mark_dirty()
    update_status_bar()
    
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)


def delete_row():
    if len(entry_grid) <= 1:
        messagebox.showwarning("Cannot Delete", "At least one contact must remain!")
        return
    
    entry_grid.pop()
    
    for widget in table_frame.grid_slaves(row=len(entry_grid)):
        widget.destroy()
    
    mark_dirty()
    update_status_bar()


def copy_all():
    data_lines = []
    
    for row in entry_grid:
        row_data = [cell.get("1.0", "end-1c") for cell in row]
        data_lines.append('\t'.join(row_data))
    
    clipboard_text = '\n'.join(data_lines)
    root.clipboard_clear()
    root.clipboard_append(clipboard_text)
    
    messagebox.showinfo("Copied", f"Copied {len(entry_grid)} rows to clipboard!")


def clear_all():
    confirm = messagebox.askyesno("Clear All", "Clear all data in the table?")
    if confirm:
        for row in entry_grid:
            for cell in row:
                cell.delete("1.0", tk.END)
                adjust_cell_height(cell)
        mark_dirty()
        update_status_bar()


def import_from_excel():
    """Import data from Excel preserving multi-line cells and formatting"""
    
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    
    if not file_path:
        return
    
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet = wb.active
        
        clear_all()
        
        imported_count = 0
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if imported_count >= 20:
                messagebox.showwarning("Limit Reached", "Imported maximum 20 contacts!")
                break
            
            contact = row[0] if len(row) > 0 else ""
            message = row[1] if len(row) > 1 else ""
            path = row[2] if len(row) > 2 else ""
            file_name = row[3] if len(row) > 3 else ""
            
            if not any([contact, message, path, file_name]):
                continue
            
            if imported_count >= len(entry_grid):
                add_row()
            
            entry_grid[imported_count][0].delete("1.0", tk.END)
            entry_grid[imported_count][0].insert("1.0", str(contact) if contact else "")
            adjust_cell_height(entry_grid[imported_count][0])
            
            entry_grid[imported_count][1].delete("1.0", tk.END)
            entry_grid[imported_count][1].insert("1.0", str(message) if message else "")
            adjust_cell_height(entry_grid[imported_count][1])
            
            entry_grid[imported_count][2].delete("1.0", tk.END)
            entry_grid[imported_count][2].insert("1.0", str(path) if path else "")
            adjust_cell_height(entry_grid[imported_count][2])
            
            entry_grid[imported_count][3].delete("1.0", tk.END)
            entry_grid[imported_count][3].insert("1.0", str(file_name) if file_name else "")
            adjust_cell_height(entry_grid[imported_count][3])
            
            imported_count += 1
        
        mark_dirty()
        update_status_bar()
        
        messagebox.showinfo(
            "Import Successful", 
            f"✅ Imported {imported_count} contacts from Excel!\n\n"
            f"Multi-line cells preserved."
        )
        
    except Exception as e:
        messagebox.showerror("Import Error", f"Failed to import Excel file:\n\n{str(e)}")


def update_status_bar():
    total_rows = len(entry_grid)
    selected_row_count = len(set(r for r, c in selected_cells))
    
    issues = 0
    for row in entry_grid:
        if not row[0].get("1.0", "end-1c").strip() or not row[1].get("1.0", "end-1c").strip():
            issues += 1
    
    status_parts = []
    status_parts.append(f"Total Rows: {total_rows}")
    
    if selected_cells:
        status_parts.append(f"Selected: {len(selected_cells)} cell(s), {selected_row_count} row(s)")
    
    if issues > 0:
        status_parts.append(f"⚠️ {issues} incomplete row(s)")
    
    if is_dirty:
        status_parts.append("● Modified")
    
    if last_saved_time:
        status_parts.append(f"Last saved: {last_saved_time}")
    
    status_label.config(text=" | ".join(status_parts))


def start_automation():
    """Main automation function with CORRECTED WhatsApp Desktop navigation"""
    global last_saved_time, is_dirty
    
    contacts_data = []
    
    for row in entry_grid:
        contact_name = row[0].get("1.0", "end-1c").strip()
        message = row[1].get("1.0", "end-1c")
        image_path = row[2].get("1.0", "end-1c").strip()
        image_file = row[3].get("1.0", "end-1c").strip()
        
        if contact_name and message.strip():
            contacts_data.append({
                'name': contact_name,
                'message': message,
                'image_path': image_path,
                'image_file': image_file,
                'has_image': bool(image_path and image_file)
            })
    
    if not contacts_data:
        messagebox.showwarning("No Data", "Please add at least one contact with a message!")
        return
    
    with_images = sum(1 for c in contacts_data if c['has_image'])
    without_images = len(contacts_data) - with_images
    
    confirm = messagebox.askyesno(
        "Confirm Automation", 
        f"Send messages to {len(contacts_data)} contact(s)?\n\n"
        f"With images: {with_images}\n"
        f"Text only: {without_images}\n\n"
        f"Multi-line messages will be preserved.\n"
        f"This will start in 3 seconds..."
    )
    
    if not confirm:
        return
    
    root.withdraw()
    
    print("🚀 Starting in 3 seconds...")
    time.sleep(3)
    
    print("🚀 Starting WhatsApp automation...")
    pg.press('win')
    time.sleep(1)
    pg.typewrite('whatsapp', interval=0.15)
    time.sleep(1)
    pg.press('enter')
    
    print("⏳ Waiting for WhatsApp to load...")
    time.sleep(4)
    
    successful_sends = []
    failed_sends = []
    
    for index, contact_data in enumerate(contacts_data, start=1):
        contact = contact_data['name']
        message = contact_data['message']
        has_image = contact_data['has_image']
        image_path = contact_data['image_path']
        image_file = contact_data['image_file']
        
        print(f"\n📤 [{index}/{len(contacts_data)}] Processing: {contact}")
        print(f"   Message: {message[:50]}{'...' if len(message) > 50 else ''}")
        print(f"   Image: {'Yes ✓' if has_image else 'No ✗'}")
        
        try:
            # Search for contact
            pg.hotkey('ctrl', 'f')
            time.sleep(1)
            pg.typewrite(contact, interval=0.25)
            time.sleep(1)
            pg.press('down')
            time.sleep(0.5)
            pg.press('enter')
            time.sleep(1)
            
            # Copy-paste message
            print("   📋 Copying message to clipboard...")
            pyperclip.copy(message)
            time.sleep(0.5)
            pg.hotkey('ctrl', 'v')
            time.sleep(1)
            
            # CORRECTED: Attach image with exact sequence
            if has_image:
                print(f"   📎 Attaching image: {image_file}")
                
                # Step 1: Shift+Tab twice
                pg.hotkey('shift', 'tab')
                time.sleep(0.5)
                pg.hotkey('shift', 'tab')
                time.sleep(0.5)
                
                # Step 2: Enter
                pg.press('enter')
                time.sleep(1)
                
                # Step 3: Down arrow twice
                pg.press('down')
                time.sleep(0.5)
                pg.press('down')
                time.sleep(0.5)
                
                # Step 4: Enter
                pg.press('enter')
                time.sleep(2)
                
                # Step 5: F4
                pg.press('f4')
                time.sleep(0.5)
                
                # Step 6: Ctrl+A
                pg.hotkey('ctrl', 'a')
                time.sleep(0.5)
                
                # Step 7: Type path
                pg.typewrite(image_path, interval=0.05)
                time.sleep(0.5)
                
                # Step 8: Enter
                pg.press('enter')
                time.sleep(2)
                
                # Step 9: Tab 6 times
                for i in range(6):
                    pg.press('tab')
                    time.sleep(0.3)
                
                # Step 10: Type filename
                pg.typewrite(image_file, interval=0.05)
                time.sleep(0.5)
                
                # Step 11: Enter
                pg.press('enter')
                time.sleep(2)
                
                # Step 12: Enter again
                pg.press('enter')
                time.sleep(2)
            else:
                # No image - just send message
                pg.press('enter')
                time.sleep(2)
            
            print(f"✅ Successfully sent to: {contact}")
            successful_sends.append(contact)
            
            if index < len(contacts_data):
                delay = random.uniform(3, 6)
                print(f"⏱️  Waiting {delay:.1f}s before next contact...")
                time.sleep(delay)
                pg.hotkey('ctrl', 'f')
                time.sleep(1)
        
        except Exception as e:
            print(f"❌ Failed to send to {contact}: {str(e)}")
            failed_sends.append(contact)
            
            try:
                time.sleep(2)
                pg.hotkey('ctrl', 'f')
                time.sleep(1)
            except:
                print("⚠️  Recovery failed, continuing...")
            
            continue
    
    print("\n🔒 Closing WhatsApp...")
    time.sleep(1)
    pg.hotkey('alt', 'f4')
    
    print("\n" + "="*50)
    print("📊 AUTOMATION COMPLETE - FINAL REPORT")
    print("="*50)
    print(f"✅ Successfully sent: {len(successful_sends)}/{len(contacts_data)}")
    print(f"❌ Failed: {len(failed_sends)}/{len(contacts_data)}")
    
    if successful_sends:
        print("\n✅ Successful contacts:")
        for contact in successful_sends:
            print(f"   • {contact}")
    
    if failed_sends:
        print("\n❌ Failed contacts:")
        for contact in failed_sends:
            print(f"   • {contact}")
    
    print("\n🎉 Automation finished!")
    
    is_dirty = False
    last_saved_time = datetime.now().strftime("%H:%M:%S")
    
    root.deiconify()
    update_status_bar()
    
    messagebox.showinfo(
        "Automation Complete", 
        f"✅ Successfully sent: {len(successful_sends)}/{len(contacts_data)}\n"
        f"❌ Failed: {len(failed_sends)}/{len(contacts_data)}"
    )


# === Create GUI ===
root = tk.Tk()
root.title("WhatsApp Automation - Excel-Style")
root.geometry("1400x750")
root.resizable(True, True)

# Header
header_frame = tk.Frame(root, bg="#25D366", height=60)
header_frame.pack(fill=tk.X)
header_frame.pack_propagate(False)

header_label = tk.Label(
    header_frame, 
    text="📱 WhatsApp Bulk Message Sender", 
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#25D366"
)
header_label.pack(pady=15)

# Info frame
info_frame = tk.Frame(root, bg="#F5F5F5", height=35)
info_frame.pack(fill=tk.X)
info_frame.pack_propagate(False)

info_label = tk.Label(
    info_frame,
    text="💡 Ctrl+Enter: New line | Multi-line preserved | Updated for new WhatsApp Desktop | Import: A=Contact, B=Message, C=Path, D=File",
    font=("Arial", 9),
    fg="#666666",
    bg="#F5F5F5"
)
info_label.pack(side=tk.LEFT, padx=20, pady=8)

# Container
container = tk.Frame(root)
container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(container, bg="white", highlightthickness=1, highlightbackground="#CCCCCC")
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

table_container = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=table_container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Header row
header_frame_table = tk.Frame(table_container, bg="white")
header_frame_table.grid(row=0, column=0, sticky='ew')

header_frame_table.grid_columnconfigure(0, minsize=50, weight=0)
header_frame_table.grid_columnconfigure(1, minsize=220, weight=0)
header_frame_table.grid_columnconfigure(2, minsize=450, weight=0)
header_frame_table.grid_columnconfigure(3, minsize=320, weight=0)
header_frame_table.grid_columnconfigure(4, minsize=220, weight=0)

headers = ['#', 'Contact Name', 'Message', 'Image Folder Path', 'Image File Name']

for col, header in enumerate(headers):
    label = tk.Label(
        header_frame_table, 
        text=header, 
        bg="#25D366", 
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.SOLID,
        bd=1,
        anchor='w',
        padx=8,
        height=2
    )
    label.grid(row=0, column=col, sticky='ew', padx=0, pady=0)

# Table frame
table_frame = tk.Frame(table_container, bg="white")
table_frame.grid(row=1, column=0, sticky='nsew')

table_frame.grid_columnconfigure(0, minsize=50, weight=0)
table_frame.grid_columnconfigure(1, minsize=220, weight=0)
table_frame.grid_columnconfigure(2, minsize=450, weight=0)
table_frame.grid_columnconfigure(3, minsize=320, weight=0)
table_frame.grid_columnconfigure(4, minsize=220, weight=0)

# Keyboard shortcuts
root.bind_all('<Control-c>', copy_selection)
root.bind_all('<Control-v>', paste_handler)
root.bind_all('<Control-x>', cut_selection)
root.bind_all('<Control-d>', fill_down)
root.bind_all('<Control-z>', undo_action)
root.bind_all('<Control-y>', redo_action)

def on_configure(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

table_container.bind("<Configure>", on_configure)

# Button frame
button_frame = tk.Frame(root, bg="#F0F0F0", height=70)
button_frame.pack(fill=tk.X, side=tk.BOTTOM)
button_frame.pack_propagate(False)

button_center = tk.Frame(button_frame, bg="#F0F0F0")
button_center.pack(expand=True)

# Import Excel button
import_button = tk.Button(
    button_center,
    text="📥 Import Excel",
    command=import_from_excel,
    font=("Arial", 10, "bold"),
    bg="#0084FF",
    fg="white",
    cursor="hand2",
    relief=tk.RAISED,
    bd=2,
    padx=18,
    pady=10
)
import_button.pack(side=tk.LEFT, padx=8)

add_button = tk.Button(
    button_center,
    text="➕ Add Row",
    command=add_row,
    font=("Arial", 10, "bold"),
    bg="#128C7E",
    fg="white",
    cursor="hand2",
    relief=tk.RAISED,
    bd=2,
    padx=18,
    pady=10
)
add_button.pack(side=tk.LEFT, padx=8)

delete_button = tk.Button(
    button_center,
    text="❌ Delete Last",
    command=delete_row,
    font=("Arial", 10, "bold"),
    bg="#FF5555",
    fg="white",
    cursor="hand2",
    relief=tk.RAISED,
    bd=2,
    padx=18,
    pady=10
)
delete_button.pack(side=tk.LEFT, padx=8)

copy_button = tk.Button(
    button_center,
    text="📋 Copy All",
    command=copy_all,
    font=("Arial", 10, "bold"),
    bg="#6C757D",
    fg="white",
    cursor="hand2",
    relief=tk.RAISED,
    bd=2,
    padx=18,
    pady=10
)
copy_button.pack(side=tk.LEFT, padx=8)

clear_button = tk.Button(
    button_center,
    text="🗑️ Clear All",
    command=clear_all,
    font=("Arial", 10, "bold"),
    bg="#FF9500",
    fg="white",
    cursor="hand2",
    relief=tk.RAISED,
    bd=2,
    padx=18,
    pady=10
)
clear_button.pack(side=tk.LEFT, padx=8)

start_button = tk.Button(
    button_center,
    text="🚀 START AUTOMATION",
    command=start_automation,
    font=("Arial", 13, "bold"),
    bg="#25D366",
    fg="white",
    cursor="hand2",
    relief=tk.RAISED,
    bd=4,
    padx=35,
    pady=12
)
start_button.pack(side=tk.LEFT, padx=15)

# Status bar
status_bar = tk.Frame(root, bg="#E8E8E8", height=25, relief=tk.SUNKEN, bd=1)
status_bar.pack(fill=tk.X, side=tk.BOTTOM)
status_bar.pack_propagate(False)

status_label = tk.Label(
    status_bar,
    text="Ready",
    font=("Arial", 9),
    bg="#E8E8E8",
    anchor='w',
    padx=10
)
status_label.pack(fill=tk.BOTH, expand=True)

# Add initial empty row
add_row()

is_dirty = False
update_status_bar()

root.mainloop()
