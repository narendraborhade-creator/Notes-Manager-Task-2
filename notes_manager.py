"""
Notes Manager - A modern, dark-themed desktop note-taking application.

Built with Python and Tkinter. Features JSON-based persistence,
optional custom background via Pillow, and intuitive CRUD operations.
"""

import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ---------------------------------------------------------------------------
# Color constants (dark navy theme)
# ---------------------------------------------------------------------------
BG_COLOR = "#0a1628"
FRAME_COLOR = "#1e293b"
INPUT_COLOR = "#0f172a"
TEXT_COLOR = "#e2e8f0"
ACCENT_BLUE = "#2563eb"
DANGER_RED = "#dc2626"
BORDER_COLOR = "#334155"
MUTED_COLOR = "#64748b"
HOVER_COLOR = "#3b82f6"

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
NOTES_FILE = "notes.json"


def load_notes():
    """Load notes from the JSON file, returning a list of dicts."""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_notes(notes):
    """Persist notes to the JSON file."""
    with open(NOTES_FILE, "w", encoding="utf-8") as fh:
        json.dump(notes, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class NotesManager:
    """Main application window for the Notes Manager."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.notes: list[dict] = load_notes()
        self._bg_image_ref = None  # keep Tk image reference alive

        self._configure_window()
        self._build_ui()
        self._bind_shortcuts()
        self._refresh_list()
        self._set_status("Ready – {} note(s) loaded.".format(len(self.notes)))

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _configure_window(self) -> None:
        self.root.title("Notes Manager")
        self.root.geometry("960x640")
        self.root.minsize(700, 480)
        self.root.configure(bg=BG_COLOR)
        try:
            self.root.iconbitmap("")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        self._build_menu()
        self._build_toolbar()
        self._build_main_area()
        self._build_status_bar()
        self._load_background()

    # --- Menu bar ---

    def _build_menu(self) -> None:
        menubar = tk.Menu(
            self.root,
            bg=FRAME_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT_BLUE,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT,
        )

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=FRAME_COLOR, fg=TEXT_COLOR,
                            activebackground=ACCENT_BLUE, activeforeground=TEXT_COLOR)
        file_menu.add_command(label="New Note       Ctrl+N", command=self.add_note)
        file_menu.add_separator()
        file_menu.add_command(label="Refresh        F5", command=self.refresh_notes)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg=FRAME_COLOR, fg=TEXT_COLOR,
                            activebackground=ACCENT_BLUE, activeforeground=TEXT_COLOR)
        edit_menu.add_command(label="Delete Note    Del", command=self.delete_note)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=FRAME_COLOR, fg=TEXT_COLOR,
                            activebackground=ACCENT_BLUE, activeforeground=TEXT_COLOR)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    # --- Toolbar ---

    def _build_toolbar(self) -> None:
        toolbar = tk.Frame(self.root, bg=FRAME_COLOR, pady=6)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_opts = dict(
            bg=ACCENT_BLUE, fg=TEXT_COLOR,
            relief=tk.FLAT, padx=14, pady=5,
            font=("Arial", 10, "bold"),
            cursor="hand2",
        )

        tk.Button(toolbar, text="＋  New Note", command=self.add_note,
                  **btn_opts).pack(side=tk.LEFT, padx=(10, 4))

        del_opts = dict(btn_opts)
        del_opts["bg"] = DANGER_RED
        tk.Button(toolbar, text="🗑  Delete", command=self.delete_note,
                  **del_opts).pack(side=tk.LEFT, padx=4)

        tk.Button(toolbar, text="⟳  Refresh", command=self.refresh_notes,
                  **btn_opts).pack(side=tk.LEFT, padx=4)

        tk.Label(toolbar, text="Notes Manager", bg=FRAME_COLOR, fg=MUTED_COLOR,
                 font=("Arial", 11, "italic")).pack(side=tk.RIGHT, padx=12)

    # --- Main content area ---

    def _build_main_area(self) -> None:
        # Canvas for optional background image
        self.canvas = tk.Canvas(self.root, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Paned window overlaid on canvas
        paned = tk.PanedWindow(
            self.canvas,
            orient=tk.HORIZONTAL,
            bg=BG_COLOR,
            sashwidth=6,
            sashrelief=tk.FLAT,
        )
        paned.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ---- Left panel: input form ----
        left = tk.Frame(paned, bg=FRAME_COLOR, padx=16, pady=16)
        paned.add(left, minsize=280, width=320)

        tk.Label(left, text="New Note", bg=FRAME_COLOR, fg=TEXT_COLOR,
                 font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 12))

        tk.Label(left, text="Title", bg=FRAME_COLOR, fg=MUTED_COLOR,
                 font=("Arial", 9)).pack(anchor=tk.W)
        self.title_var = tk.StringVar()
        title_entry = tk.Entry(
            left, textvariable=self.title_var,
            bg=INPUT_COLOR, fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief=tk.FLAT, font=("Arial", 11),
            highlightthickness=1, highlightcolor=ACCENT_BLUE,
            highlightbackground=BORDER_COLOR,
        )
        title_entry.pack(fill=tk.X, pady=(2, 10))

        tk.Label(left, text="Content", bg=FRAME_COLOR, fg=MUTED_COLOR,
                 font=("Arial", 9)).pack(anchor=tk.W)
        self.content_text = tk.Text(
            left,
            bg=INPUT_COLOR, fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief=tk.FLAT, font=("Consolas", 11),
            wrap=tk.WORD,
            highlightthickness=1, highlightcolor=ACCENT_BLUE,
            highlightbackground=BORDER_COLOR,
            height=12,
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(2, 12))

        tk.Button(
            left, text="Add Note",
            command=self.add_note,
            bg=ACCENT_BLUE, fg=TEXT_COLOR,
            relief=tk.FLAT, padx=16, pady=7,
            font=("Arial", 11, "bold"), cursor="hand2",
        ).pack(fill=tk.X)

        # ---- Right panel: notes list ----
        right = tk.Frame(paned, bg=FRAME_COLOR, padx=16, pady=16)
        paned.add(right, minsize=300)

        header = tk.Frame(right, bg=FRAME_COLOR)
        header.pack(fill=tk.X, pady=(0, 8))
        tk.Label(header, text="All Notes", bg=FRAME_COLOR, fg=TEXT_COLOR,
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        self.count_label = tk.Label(header, text="", bg=FRAME_COLOR,
                                    fg=MUTED_COLOR, font=("Arial", 9))
        self.count_label.pack(side=tk.RIGHT, padx=4)

        list_frame = tk.Frame(right, bg=FRAME_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, bg=FRAME_COLOR, troughcolor=INPUT_COLOR)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            bg=INPUT_COLOR, fg=TEXT_COLOR,
            selectbackground=ACCENT_BLUE,
            selectforeground=TEXT_COLOR,
            relief=tk.FLAT, font=("Arial", 11),
            activestyle="none",
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Double-Button-1>", self._on_double_click)
        self.listbox.bind("<Delete>", lambda _: self.delete_note())

        # Bind canvas resize to re-draw background
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    # --- Status bar ---

    def _build_status_bar(self) -> None:
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=FRAME_COLOR, fg=MUTED_COLOR,
            anchor=tk.W, padx=10, pady=4,
            font=("Arial", 9),
            relief=tk.FLAT,
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Optional background image ---

    def _load_background(self) -> None:
        """Try to load og-image.png as background; silently skip if unavailable."""
        if not PIL_AVAILABLE:
            return
        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")
        if not os.path.exists(bg_path):
            return
        try:
            self._raw_bg = Image.open(bg_path)
            self._resize_background()
        except Exception:
            self._raw_bg = None

    def _resize_background(self) -> None:
        if not PIL_AVAILABLE or not hasattr(self, "_raw_bg") or self._raw_bg is None:
            return
        w = self.canvas.winfo_width() or 960
        h = self.canvas.winfo_height() or 640
        resized = self._raw_bg.resize((w, h), Image.LANCZOS)
        self._bg_image_ref = ImageTk.PhotoImage(resized)
        self.canvas.delete("bg")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self._bg_image_ref, tags="bg")
        self.canvas.lower("bg")

    def _on_canvas_resize(self, event) -> None:
        self._resize_background()

    # ------------------------------------------------------------------
    # Keyboard shortcuts
    # ------------------------------------------------------------------

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-n>", lambda _: self.add_note())
        self.root.bind("<F5>", lambda _: self.refresh_notes())

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------

    def add_note(self) -> None:
        """Read inputs and add a new note."""
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showwarning("Missing Title", "Please enter a title for the note.")
            return
        if not content:
            messagebox.showwarning("Missing Content", "Please enter some content for the note.")
            return

        note = {"title": title, "content": content}
        self.notes.append(note)
        save_notes(self.notes)
        self._refresh_list()
        self._clear_inputs()
        self._set_status("Note '{}' added successfully.".format(title))

    def delete_note(self) -> None:
        """Delete the currently selected note after confirmation."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a note to delete.")
            return

        index = selection[0]
        note = self.notes[index]
        confirmed = messagebox.askyesno(
            "Delete Note",
            "Are you sure you want to delete '{}'?".format(note["title"]),
        )
        if confirmed:
            removed_title = self.notes.pop(index)["title"]
            save_notes(self.notes)
            self._refresh_list()
            self._set_status("Note '{}' deleted.".format(removed_title))

    def refresh_notes(self) -> None:
        """Re-load notes from disk and refresh the list."""
        self.notes = load_notes()
        self._refresh_list()
        self._set_status("Notes refreshed – {} note(s).".format(len(self.notes)))

    # ------------------------------------------------------------------
    # List helpers
    # ------------------------------------------------------------------

    def _refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            preview = note.get("content", "").replace("\n", " ")[:80]
            if len(note.get("content", "")) > 80:
                preview += "…"
            self.listbox.insert(tk.END, "  {}  –  {}".format(note["title"], preview))
        total = len(self.notes)
        self.count_label.config(text="{} note{}".format(total, "s" if total != 1 else ""))

    def _on_double_click(self, _event) -> None:
        """Show the full content of the double-clicked note."""
        selection = self.listbox.curselection()
        if not selection:
            return
        note = self.notes[selection[0]]
        self._show_note_window(note)

    def _show_note_window(self, note: dict) -> None:
        """Open a read-only popup window showing the full note."""
        win = tk.Toplevel(self.root)
        win.title(note["title"])
        win.geometry("600x400")
        win.configure(bg=FRAME_COLOR)
        win.grab_set()

        tk.Label(win, text=note["title"], bg=FRAME_COLOR, fg=TEXT_COLOR,
                 font=("Arial", 14, "bold"), anchor=tk.W,
                 padx=16, pady=12).pack(fill=tk.X)

        sep = tk.Frame(win, bg=BORDER_COLOR, height=1)
        sep.pack(fill=tk.X, padx=16)

        text_frame = tk.Frame(win, bg=FRAME_COLOR, padx=16, pady=12)
        text_frame.pack(fill=tk.BOTH, expand=True)

        sb = tk.Scrollbar(text_frame)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        txt = tk.Text(
            text_frame,
            bg=INPUT_COLOR, fg=TEXT_COLOR,
            relief=tk.FLAT, font=("Consolas", 11),
            wrap=tk.WORD, highlightthickness=0,
            yscrollcommand=sb.set,
        )
        txt.insert("1.0", note.get("content", ""))
        txt.config(state=tk.DISABLED)
        txt.pack(fill=tk.BOTH, expand=True)
        sb.config(command=txt.yview)

        tk.Button(win, text="Close", command=win.destroy,
                  bg=ACCENT_BLUE, fg=TEXT_COLOR,
                  relief=tk.FLAT, padx=20, pady=6,
                  font=("Arial", 10, "bold"), cursor="hand2").pack(pady=(0, 12))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _clear_inputs(self) -> None:
        self.title_var.set("")
        self.content_text.delete("1.0", tk.END)

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)

    def _show_about(self) -> None:
        messagebox.showinfo(
            "About Notes Manager",
            "Notes Manager\n\n"
            "A modern, dark-themed desktop note-taking application.\n\n"
            "Built with Python & Tkinter.\n"
            "Author: Narendra Borhade\n"
            "Email: borhadenarendra35@gmail.com",
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    root = tk.Tk()
    NotesManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
