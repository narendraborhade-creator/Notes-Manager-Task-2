# Notes Manager

A modern desktop note-taking application built with Python and Tkinter. This application provides a simple and elegant way to manage your notes with a sleek, dark-themed interface.

## Screenshots

![Notes Manager Home](https://github.com/user-attachments/assets/3efbb707-bc1d-4c26-8985-528451b50cbc)
*The main interface of the Notes Manager application.*

![Viewing a Note](https://github.com/user-attachments/assets/6c656eec-17f1-4cbe-9df4-6e2d0e92ba90)
*Viewing the content of a selected note.*

## Features

*   **Create, View, and Delete Notes**: Easily manage your notes with intuitive controls.
*   **Keyboard Shortcuts**: Boost your productivity with shortcuts for common actions:
    *   `Ctrl+N`: Create a new note.
    *   `F5`: Refresh and view all notes.
    *   `Delete`: Delete a selected note.
*   **Automatic Saving**: Notes are automatically saved to `notes.json`, so you never lose your work.
*   **Customizable Background**: Personalize the application by setting your own background image.
*   **Dark-Themed UI**: A modern, easy-on-the-eyes dark theme for a pleasant user experience.

## Tech Stack

*   **Language**: Python
*   **GUI Framework**: Tkinter
*   **Image Library**: Pillow (for custom background support)

## Getting Started

To run this application on your local machine, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/narendraborhade-creator/Notes-Manager-Task-2.git
    cd Notes-Manager-Task-2
    ```

2.  **Install the dependencies:**
    This project requires Python and the `Pillow` library.
    ```sh
    pip install Pillow
    ```

3.  **Run the application:**
    ```sh
    python main.py
    ```

## How It Works

The application uses a simple JSON file (`notes.json`) to store and manage your notes. The Tkinter library provides the graphical user interface, allowing for a lightweight and cross-platform experience. The integration with the Pillow library enables easy customization of the app's background.Here's a comprehensive GitHub description/README:

---

# Notes Manager

A modern, professional desktop note-taking application built with Python and Tkinter. Features a sleek dark-themed UI inspired by contemporary web design, with custom background support, JSON-based data persistence, and intuitive CRUD operations.

## 📸 Screenshots

<img width="1916" height="1079" alt="Screenshot 2026-05-03 183207" src="https://github.com/user-attachments/assets/6c656eec-17f1-4cbe-9df4-6e2d0e92ba90" />
<img width="1913" height="1078" alt="Screenshot 2026-05-03 183121" src="https://github.com/user-attachments/assets/3efbb707-bc1d-4c26-8985-528451b50cbc" />

## ✨ Features

### Core Functionality
- **Create Notes**: Add notes with titles and detailed content
- **View Notes**: Browse all stored notes with automatic preview (first 80 characters)
- **Delete Notes**: Remove unwanted notes with confirmation dialog
- **Persistent Storage**: All data automatically saved to `notes.json`
- **Double-Click Preview**: Quick view full note content with a double-click

### User Interface
- **Modern Dark Theme**: Professional dark blue color scheme (#0a1628 background)
- **Custom Background Support**: Optional background image (og-image.png)
- **Responsive Layout**: Resizable panes and adaptive window sizing
- **Menu Bar**: Traditional File, Edit, and Help menus
- **Toolbar**: Quick access buttons for common actions
- **Status Bar**: Real-time feedback on operations

### Keyboard Shortcuts
- `Ctrl+N` - Add new note
- `F5` - Refresh note list
- `Delete` - Remove selected note

## 🛠️ Tech Stack

- **Python 3.x** - Core programming language
- **Tkinter** - Native GUI framework
- **Pillow (PIL)** - Image processing for background support
- **JSON** - Lightweight data storage format

## 📦 Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone https://github.com/narendraborhade-creator/Notes-Manager-Task-2.git
cd notes-manager
```

2. Install dependencies:
```bash
pip install pillow
```

3. (Optional) Add custom background image:
   - Place your background image as `og-image.png` in the project directory
   - The app will automatically detect and use it

4. Run the application:
```bash
python notes_manager.py
```

## 🚀 Usage

### Adding a Note
1. Enter a title in the "Title" field
2. Type your note content in the text area
3. Click "Add Note" or press `Ctrl+N`
4. Note appears in the list below with preview

### Viewing Notes
- **Quick Preview**: Visible in the list (first 80 characters)
- **Full View**: Double-click any note or select and view

### Deleting Notes
1. Select a note from the list
2. Click "Delete" button or press `Delete` key
3. Confirm the deletion in the dialog

### Data Storage
All notes are automatically saved to `notes.json` in JSON format:
```json
[
  {
    "title": "Meeting Notes",
    "content": "Discuss project timeline and deliverables..."
  }
]
```

## 🎨 Customization

### Changing Colors
Edit the color constants in `notes_manager.py`:
- Background: `#0a1628` (dark navy)
- Frames: `#1e293b` (lighter navy)
- Input fields: `#0f172a` (darkest navy)
- Text: `#e2e8f0` (light gray)
- Accent blue: `#2563eb`
- Danger red: `#dc2626`

### Custom Background
Replace `og-image.png` with your own image. Supported formats: PNG, JPG, JPEG, BMP.

## 📂 Project Structure

```
notes-manager/
├── notes_manager.py      # Main application file
├── notes.json           # Data storage (auto-created)
├── og-image.png         # Background image (optional)
└── README.md           # This file
```

## 🔧 Troubleshooting

### Background image not showing
- Ensure `og-image.png` exists in the project directory
- Verify Pillow is installed: `pip show pillow`
- Check console for error messages

### Text not visible
- The app uses a dark theme - ensure you're using the provided color scheme
- Check that your system supports the specified fonts (Arial, Consolas)

### JSON errors
- Delete `notes.json` to start fresh
- Ensure no other program is locking the file

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by modern web design principles
- Built with Python's native Tkinter for cross-platform compatibility
- Color scheme inspired by Tailwind CSS dark theme

## 📧 Contact

Your Name - Narendra Borhadde Email: borhadenarendra35@gmail.com

Project Link: https://github.com/narendraborhade-creator/Notes-Manager-Task-2
---

### ⭐ Show your support

Give a ⭐️ if this project helped you!

---

**Short Description (for repository subtitle):**
> 📝 A modern, dark-themed desktop note-taking app with JSON storage, custom backgrounds, and intuitive GUI built in Python
