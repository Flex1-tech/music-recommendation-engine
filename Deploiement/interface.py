from PIL import Image
import customtkinter as ctk
from func import open_file


upload_icon = ctk.CTkImage(light_image=Image.open("assets/light_upload.png"),dark_image=Image.open("assets/dark_upload.png"), size=(30, 30))

# customtkinter.set_appearance_mode("System")  # "Light" ou "Dark"
# customtkinter.set_default_color_theme("green") 76


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

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
        main_frame = ctk.CTkFrame(
            self,
            border_width=2,
            corner_radius=10
        )
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = ctk.CTkLabel(
            main_frame,
            text="Écoutez. Likez. Découvrez.\nVotre musique, parfaitement orchestrée.",
            font=("Arial", 19, "bold"),
            justify="center",
            anchor="center"
        )
        self.label.pack(pady=100)

        self.button = ctk.CTkButton(
            main_frame,
            text="Importer mes musiques",
            fg_color="#FF8E25",
            hover_color="#F36C19",
            # 

            image=upload_icon,
            compound="left",
            font=("Arial", 17),
            command=self.import_files,
        )
        # self.button.pack(expand=True)
        # self.button.configure(border_width=0,hover_color="FFC125")
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def import_files(self):
        self.selected_files = open_file(self, self.label)
        print(self.selected_files)
