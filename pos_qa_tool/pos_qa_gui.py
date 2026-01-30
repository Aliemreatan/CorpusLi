# -*- coding: utf-8 -*-
"""
POS Tag Quality Assurance (QA) GUI

A simple tool to review and correct POS tags in the corpus database.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# --- Constants ---
DB_PATH = r"D:\Downloads\ocrmeb\test_verisi.db"

# Standard Universal POS Tags for the Combobox
UPOS_TAGS = [
    "ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", 
    "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X"
]

class PosQaGui:
    def __init__(self, root):
        self.root = root
        self.root.title("POS Etiketi Düzeltme Aracı")
        self.root.geometry("800x600")

        # --- State Variables ---
        self.current_sent_id = 1
        self.max_sent_id = 1
        self.token_widgets = []  # To hold {'token_id': id, 'pos_var': StringVar}
        self.pending_changes = {} # {token_id: new_pos_tag}

        # --- UI Setup ---
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_nav_widgets()
        self.create_sentence_display()
        self.create_token_grid()
        self.create_action_widgets()
        
        # --- Initial Load ---
        self.fetch_max_sent_id()
        self.load_sentence()

    def create_nav_widgets(self):
        """Creates the top navigation bar."""
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill=tk.X, pady=5)

        ttk.Button(nav_frame, text="<< Önceki", command=self.load_prev_sentence).pack(side=tk.LEFT)
        
        self.sent_id_label = ttk.Label(nav_frame, text="Cümle ID: 1 / 1", font=("Helvetica", 10))
        self.sent_id_label.pack(side=tk.LEFT, expand=True)
        
        ttk.Button(nav_frame, text="Sonraki >>", command=self.load_next_sentence).pack(side=tk.RIGHT)

    def create_sentence_display(self):
        """Creates the label to show the full sentence text."""
        sentence_frame = ttk.LabelFrame(self.main_frame, text="Cümle Metni", padding="5")
        sentence_frame.pack(fill=tk.X, pady=5)
        
        self.sentence_text_label = ttk.Label(sentence_frame, text="", wraplength=750, justify=tk.LEFT)
        self.sentence_text_label.pack(fill=tk.X)

    def create_token_grid(self):
        """Creates the scrollable frame for token/POS tag editing."""
        grid_frame = ttk.LabelFrame(self.main_frame, text="Kelimeler ve POS Etiketleri", padding="5")
        grid_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(grid_frame)
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Grid headers
        ttk.Label(self.scrollable_frame, text="Kelime", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=2, sticky='w')
        ttk.Label(self.scrollable_frame, text="Mevcut POS", font=("Helvetica", 10, "bold")).grid(row=0, column=1, padx=5, pady=2, sticky='w')
        ttk.Label(self.scrollable_frame, text="Yeni POS", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=2, sticky='w')

    def create_action_widgets(self):
        """Creates the bottom action buttons."""
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_label = ttk.Label(action_frame, text="Hazır.", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(action_frame, text="Değişiklikleri Kaydet", command=self.save_changes).pack(side=tk.RIGHT)

    def fetch_max_sent_id(self):
        """Gets the maximum sentence ID from the database."""
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(sent_id) FROM sentences")
                result = cursor.fetchone()
                self.max_sent_id = result[0] if result and result[0] else 1
        except Exception as e:
            messagebox.showerror("Veritabanı Hatası", f"Maksimum cümle ID alınamadı: {e}")
            self.max_sent_id = 1
        self.update_sent_id_label()

    def load_sentence(self):
        """Fetches and displays the current sentence and its tokens."""
        self.clear_grid()
        self.pending_changes = {} # Clear pending changes for new sentence

        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Fetch sentence text
                cursor.execute("SELECT sent_text FROM sentences WHERE sent_id = ?", (self.current_sent_id,))
                sent_row = cursor.fetchone()
                if sent_row:
                    self.sentence_text_label.config(text=sent_row['sent_text'])
                else:
                    self.sentence_text_label.config(text="Cümle bulunamadı.")
                    return

                # Fetch tokens
                cursor.execute("SELECT token_id, form, upos FROM tokens WHERE sent_id = ? ORDER BY token_number", (self.current_sent_id,))
                tokens = cursor.fetchall()
                
                self.populate_grid(tokens)
                self.update_sent_id_label()
                self.status_label.config(text=f"{len(tokens)} kelime yüklendi.")

        except Exception as e:
            messagebox.showerror("Veritabanı Hatası", f"Cümle yüklenemedi: {e}")
            self.status_label.config(text="Hata: Cümle yüklenemedi.")
    
    def populate_grid(self, tokens):
        """Fills the scrollable grid with token widgets."""
        self.token_widgets = []
        for i, token in enumerate(tokens, start=1):
            token_id = token['token_id']
            form = token['form']
            pos = token['upos']

            # Word form (read-only)
            ttk.Label(self.scrollable_frame, text=form).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            
            # Current POS tag (read-only)
            ttk.Label(self.scrollable_frame, text=pos).grid(row=i, column=1, padx=5, pady=2, sticky='w')

            # New POS tag (editable ComboBox)
            pos_var = tk.StringVar(value=pos)
            pos_combo = ttk.Combobox(self.scrollable_frame, textvariable=pos_var, values=UPOS_TAGS, width=10)
            pos_combo.grid(row=i, column=2, padx=5, pady=2, sticky='w')
            
            # When the combobox value changes, call on_pos_change
            pos_combo.bind('<<ComboboxSelected>>', lambda event, t_id=token_id, p_var=pos_var: self.on_pos_change(t_id, p_var.get()))
            
            self.token_widgets.append({'token_id': token_id, 'pos_var': pos_var})

    def on_pos_change(self, token_id, new_pos):
        """Records a POS tag change."""
        self.pending_changes[token_id] = new_pos
        self.status_label.config(text=f"{len(self.pending_changes)} değişiklik kaydedilmeyi bekliyor.")

    def save_changes(self):
        """Saves all pending changes to the database."""
        if not self.pending_changes:
            messagebox.showinfo("Bilgi", "Kaydedilecek bir değişiklik yok.")
            return

        updates = list(self.pending_changes.items())
        # The format for executemany is (value, key), so we need to swap them
        updates_to_save = [(new_pos, token_id) for token_id, new_pos in updates]

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.executemany("UPDATE tokens SET upos = ? WHERE token_id = ?", updates_to_save)
                conn.commit()
            
            messagebox.showinfo("Başarılı", f"{len(updates_to_save)} değişiklik veritabanına kaydedildi.")
            self.pending_changes = {}
            self.status_label.config(text="Değişiklikler kaydedildi. Yeni cümleye geçebilirsiniz.")
            # Reload to show changes are persisted (optional, but good for feedback)
            self.load_sentence()

        except Exception as e:
            messagebox.showerror("Veritabanı Hatası", f"Değişiklikler kaydedilemedi: {e}")

    def load_next_sentence(self):
        if self.current_sent_id < self.max_sent_id:
            self.check_unsaved_changes_and_proceed(self.current_sent_id + 1)

    def load_prev_sentence(self):
        if self.current_sent_id > 1:
            self.check_unsaved_changes_and_proceed(self.current_sent_id - 1)

    def check_unsaved_changes_and_proceed(self, next_sent_id):
        """Asks user to save if there are pending changes before loading a new sentence."""
        if self.pending_changes:
            response = messagebox.askyesnocancel("Kaydedilmemiş Değişiklikler", 
                                                 "Mevcut cümlede kaydedilmemiş değişiklikler var. Kaydetmek ister misiniz?")
            if response is True: # Yes
                self.save_changes()
                self.current_sent_id = next_sent_id
                self.load_sentence()
            elif response is False: # No
                self.current_sent_id = next_sent_id
                self.load_sentence()
            else: # Cancel
                return
        else:
            self.current_sent_id = next_sent_id
            self.load_sentence()

    def clear_grid(self):
        """Clears all widgets from the scrollable frame."""
        for widget in self.scrollable_frame.winfo_children():
            # Keep headers
            if widget.grid_info()['row'] > 0:
                widget.destroy()

    def update_sent_id_label(self):
        """Updates the sentence ID label in the navigation bar."""
        self.sent_id_label.config(text=f"Cümle ID: {self.current_sent_id} / {self.max_sent_id}")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        messagebox.showerror("Hata", f"Veritabanı bulunamadı!\nBeklenen konum: {DB_PATH}\n\nLütfen ana uygulamayı çalıştırarak veritabanını oluşturun.")
    else:
        app_root = tk.Tk()
        gui = PosQaGui(app_root)
        app_root.mainloop()
