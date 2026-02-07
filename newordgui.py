import json
import os
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

FILENAME = "dictionary.json"

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dictionary Learning App")
        self.root.geometry("500x400")
        self.dictionary = self.load_dictionary()
        
        # Title
        title = tk.Label(root, text="📚 Dictionary Learning App", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Buttons
        btn_add = tk.Button(root, text="Add Word", width=30, command=self.add_word)
        btn_add.pack(pady=5)
        
        btn_lookup = tk.Button(root, text="Lookup Word", width=30, command=self.lookup_word)
        btn_lookup.pack(pady=5)
        
        btn_edit = tk.Button(root, text="Edit Meaning", width=30, command=self.edit_word)
        btn_edit.pack(pady=5)
        
        btn_delete = tk.Button(root, text="Delete Word", width=30, command=self.delete_word)
        btn_delete.pack(pady=5)
        
        btn_show = tk.Button(root, text="Show All Words", width=30, command=self.show_all)
        btn_show.pack(pady=5)
        
        btn_quiz = tk.Button(root, text="Quiz Mode", width=30, command=self.quiz_mode)
        btn_quiz.pack(pady=5)
        
        btn_exit = tk.Button(root, text="Exit", width=30, command=root.quit, bg="#ff6b6b")
        btn_exit.pack(pady=5)
        
        # Word count
        self.count_label = tk.Label(root, text=f"Words in dictionary: {len(self.dictionary)}")
        self.count_label.pack(pady=10)
    
    def load_dictionary(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_dictionary(self):
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(self.dictionary, f, ensure_ascii=False, indent=2)
        self.count_label.config(text=f"Words in dictionary: {len(self.dictionary)}")
    
    def add_word(self):
        word = simpledialog.askstring("Add Word", "Enter word to add:").strip().lower()
        if word:
            meaning = simpledialog.askstring("Add Meaning", f"Enter meaning for '{word}':")
            if meaning:
                self.dictionary[word] = meaning.strip()
                self.save_dictionary()
                messagebox.showinfo("Success", f"Added: {word} → {meaning}")
    
    def lookup_word(self):
        word = simpledialog.askstring("Lookup", "Enter word to lookup:").strip().lower()
        if word in self.dictionary:
            messagebox.showinfo("Result", f"{word}:\n\n{self.dictionary[word]}")
        else:
            messagebox.showwarning("Not Found", f"'{word}' not in dictionary.")
    
    def edit_word(self):
        word = simpledialog.askstring("Edit", "Enter word to edit:").strip().lower()
        if word in self.dictionary:
            current = self.dictionary[word]
            new_meaning = simpledialog.askstring("Edit Meaning", 
                f"Current: {current}\n\nEnter new meaning:")
            if new_meaning:
                self.dictionary[word] = new_meaning.strip()
                self.save_dictionary()
                messagebox.showinfo("Success", f"Updated '{word}'")
        else:
            messagebox.showwarning("Not Found", f"'{word}' not in dictionary.")
    
    def delete_word(self):
        word = simpledialog.askstring("Delete", "Enter word to delete:").strip().lower()
        if word in self.dictionary:
            confirm = messagebox.askyesno("Confirm", f"Delete '{word}'?")
            if confirm:
                del self.dictionary[word]
                self.save_dictionary()
                messagebox.showinfo("Success", f"Deleted '{word}'")
        else:
            messagebox.showwarning("Not Found", f"'{word}' not in dictionary.")
    
    def show_all(self):
        if not self.dictionary:
            messagebox.showinfo("Dictionary", "Dictionary is empty.")
            return
        
        words_list = "\n".join([f"{w}: {m}" for w, m in self.dictionary.items()])
        
        # Create new window
        win = tk.Toplevel(self.root)
        win.title("All Words")
        win.geometry("400x300")
        
        text = tk.Text(win, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, words_list)
        text.config(state=tk.DISABLED)
    
    def quiz_mode(self):
        if not self.dictionary:
            messagebox.showwarning("Quiz", "Dictionary empty - add words first.")
            return
        
        n = simpledialog.askinteger("Quiz", "How many words to quiz on?", 
            minvalue=1, maxvalue=len(self.dictionary))
        
        if not n:
            return
        
        words = list(self.dictionary.keys())
        random.shuffle(words)
        selected = words[:min(n, len(words))]
        
        meanings = [self.dictionary[w] for w in selected]
        random.shuffle(meanings)
        
        # Create quiz window
        self.quiz_window(selected, meanings)
    
    def quiz_window(self, words, meanings):
        win = tk.Toplevel(self.root)
        win.title("Quiz Mode")
        win.geometry("500x400")
        
        self.quiz_score = 0
        self.quiz_index = 0
        self.quiz_words = words
        self.quiz_meanings = meanings
        
        # Show meanings
        meanings_text = "\n".join([f"{i+1}. {m}" for i, m in enumerate(meanings)])
        
        tk.Label(win, text="Match meanings to words:", font=("Arial", 12, "bold")).pack(pady=5)
        
        meanings_frame = tk.Frame(win)
        meanings_frame.pack(pady=5)
        
        text = tk.Text(meanings_frame, height=8, width=50)
        text.pack()
        text.insert(tk.END, meanings_text)
        text.config(state=tk.DISABLED)
        
        # Current word
        self.current_word_label = tk.Label(win, text=f"Word: {words[0]}", 
            font=("Arial", 14, "bold"))
        self.current_word_label.pack(pady=10)
        
        # Entry
        tk.Label(win, text="Enter meaning number:").pack()
        self.quiz_entry = tk.Entry(win, width=10)
        self.quiz_entry.pack(pady=5)
        
        # Submit button
        btn_submit = tk.Button(win, text="Submit", 
            command=lambda: self.check_answer(win))
        btn_submit.pack(pady=10)
        
        self.quiz_result_label = tk.Label(win, text="")
        self.quiz_result_label.pack()
    
    def check_answer(self, win):
        try:
            choice = int(self.quiz_entry.get())
            word = self.quiz_words[self.quiz_index]
            correct_meaning = self.dictionary[word]
            
            if 1 <= choice <= len(self.quiz_meanings):
                chosen = self.quiz_meanings[choice - 1]
                if chosen == correct_meaning:
                    self.quiz_result_label.config(text="✔ Correct!", fg="green")
                    self.quiz_score += 1
                else:
                    self.quiz_result_label.config(
                        text=f"✘ Wrong. Correct: {correct_meaning}", fg="red")
            else:
                self.quiz_result_label.config(text="Invalid number!", fg="red")
            
            self.quiz_index += 1
            
            if self.quiz_index < len(self.quiz_words):
                self.current_word_label.config(text=f"Word: {self.quiz_words[self.quiz_index]}")
                self.quiz_entry.delete(0, tk.END)
            else:
                # Quiz finished
                messagebox.showinfo("Quiz Results", 
                    f"You matched correctly {self.quiz_score}/{len(self.quiz_words)} words!")
                win.destroy()
        except ValueError:
            self.quiz_result_label.config(text="Please enter a number!", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
