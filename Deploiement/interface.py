from PIL import Image
import customtkinter as ctk
from func import open_file
from pathlib import Path


upload_icon = ctk.CTkImage(light_image=Image.open("assets/light_upload.png"),dark_image=Image.open("assets/dark_upload.png"), size=(30, 30))

# customtkinter.set_appearance_mode("System")  # "Light" ou "Dark"
# customtkinter.set_default_color_theme("green") 76


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.selected_files = {}
        self.file_frame = None
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = int(screen_width * 0.7)
        height = int(screen_height * 0.7)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Musical Recommender System")
        self.configure(border_color=("black", "white"))
        
        # Main Frame 
        self.main_frame = ctk.CTkFrame(
            self,
            border_width=2,
            corner_radius=10
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = ctk.CTkLabel(
            self.main_frame,
            text="Écoutez. Likez. Découvrez.\nVotre musique, parfaitement orchestrée.",
            font=("Arial", 19, "bold"),
            justify="center",
            anchor="center"
        )
        self.label.pack(pady=100)

        self.button = ctk.CTkButton(
            self.main_frame,
            text="Importer mes musiques",
            fg_color="#FF8E25",
            hover_color="#F36C19",
            image=upload_icon,
            compound="left",
            font=("Arial", 17),
            command=self.import_files,
        )
        # self.button.pack(expand=True)
        # self.button.configure(border_width=0,hover_color="FFC125")
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def import_files(self):
        self.selected_files = open_file(self, self.selected_files)
        # Deplacement du bouton pour faire de la place à la liste
        self.button.place(relx=0.9, rely=0.1, anchor="center")
        self.button.configure(text="Importer plus!",fg_color="#FF8E25", hover_color="#F36C19", image=upload_icon, compound="left", font=("Arial", 15), command=self.import_files)  # Changer le texte du bouton après le premier import

        # Créer le frame seulement s'il n'existe pas encore
        if not self.file_frame or not self.file_frame.winfo_exists():
            self.file_frame = ctk.CTkScrollableFrame(
                self.main_frame,
                label_text="Vos fichiers",
                border_width=2,
                corner_radius=10
            )
            self.file_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Mettre à jour l'affichage
        self.refresh_file_list()

        print(self.selected_files)

    def get_selected_files(self):
        return self.selected_files
    
    def clear_selected_files(self):
        self.selected_files = {}

    def refresh_file_list(self):
        if not self.file_frame:
            return

        # Si aucun fichier → ne rien afficher ici
        if not self.selected_files:
            self.refresh_label()
            return

        # Vider le contenu
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        # Afficher les fichiers
        for file in self.selected_files:
            item_frame = ctk.CTkFrame(self.file_frame)
            item_frame.pack(fill="x", padx=10, pady=5)

            nom = Path(file).name

            label = ctk.CTkLabel(item_frame, text=nom)
            label.pack(side="left", padx=10)

            delete_btn = ctk.CTkButton(
                item_frame,
                text="❌",
                width=30,
                command=lambda f=file: self.remove_file(f)
            )
            delete_btn.pack(side="right", padx=10)

        self.refresh_label()

    def remove_file(self, file):
        if file in self.selected_files:
            del self.selected_files[file]
            self.refresh_file_list()
    
    # def reset(self):
    #     self.clear_selected_files()
    #     self.refresh_file_list()    

    def refresh_label(self):
        count = len(self.selected_files)

        if count == 0:
            if self.file_frame:
                self.file_frame.pack_forget()
                self.file_frame.destroy()
                self.file_frame = None
            
            self.update_idletasks()

            self.label.configure(
                text="Écoutez. Likez. Découvrez.\nVotre musique, parfaitement orchestrée."
            )
            self.button.place(relx=0.5, rely=0.5, anchor="center")
            self.button.configure(text="Importer mes musiques", font=("Arial", 17))

        else:
            self.label.configure(text=f"{count} fichier(s) importé(s)")



        