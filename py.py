import os
import shutil
import requests
import zipfile
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import threading

# Default Among Us installation folder
DEFAULT_AMONG_US_PATH = os.path.join(os.path.expanduser("~"), "steamapps", "common", "Among Us")

def download_latest_release():
    url = "https://github.com/TheOtherRolesAU/TheOtherRoles/releases/latest/download/TheOtherRoles.zip"

    # Download the .zip file
    response = requests.get(url, stream=True)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return file_name

def extract_and_copy(zip_path, target_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)

def copy_entire_game(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for item in os.listdir(source_folder):
        s = os.path.join(source_folder, item)
        d = os.path.join(target_folder, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

# GUI Implementation using customtkinter
class TheOtherRolesDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TheOtherRoles Downloader")
        self.geometry("500x350")

        self.target_folder = tk.StringVar(value=DEFAULT_AMONG_US_PATH)
        self.source_folder = tk.StringVar(value=DEFAULT_AMONG_US_PATH)
        self.use_external_folder = tk.BooleanVar(value=False)

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Select target folder:")
        self.label.pack(pady=10)

        self.folder_entry = ctk.CTkEntry(self, textvariable=self.target_folder, width=400)
        self.folder_entry.pack(pady=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        self.external_checkbox = ctk.CTkCheckBox(self, text="Use external folder", variable=self.use_external_folder, command=self.toggle_external_folder)
        self.external_checkbox.pack(pady=5)

        self.source_label = ctk.CTkLabel(self, text="Select original Among Us folder:")
        self.source_label.pack(pady=10)

        self.source_entry = ctk.CTkEntry(self, textvariable=self.source_folder, width=400, state="disabled")
        self.source_entry.pack(pady=5)

        self.source_browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_source_folder, state="disabled")
        self.source_browse_button.pack(pady=5)

        self.download_button = ctk.CTkButton(self, text="Download and Install", command=self.start_download_thread)
        self.download_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="", wraplength=400)
        self.status_label.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_folder.set(folder_selected)

    def browse_source_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_folder.set(folder_selected)

    def toggle_external_folder(self):
        state = "normal" if self.use_external_folder.get() else "disabled"
        self.source_entry.configure(state=state)
        self.source_browse_button.configure(state=state)

    def start_download_thread(self):
        # Use a separate thread to prevent UI freezing
        thread = threading.Thread(target=self.download_and_install)
        thread.start()

    def download_and_install(self):
        try:
            if self.use_external_folder.get():
                self.status_label.configure(text="Copying original game files...")
                self.update()
                copy_entire_game(self.source_folder.get(), self.target_folder.get())

            self.status_label.configure(text="Downloading latest release...")
            self.update()

            zip_file = download_latest_release()
            self.status_label.configure(text="Extracting and installing mods...")
            self.update()

            extract_and_copy(zip_file, self.target_folder.get())
            os.remove(zip_file)  # Clean up the downloaded zip file

            self.status_label.configure(text="Installation complete!")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")

if __name__ == "__main__":
    app = TheOtherRolesDownloader()
    app.mainloop()
