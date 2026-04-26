# import customtkinter as ctk

# mes_donnees = [
#     "Pommes", "Bananes", "Oranges", "Cerises", "Ananas", "Kiwi",
#     "Mangues", "Poires", "Pêches", "Prunes", "Raisins", "Fraises"
# ]


# app = ctk.CTk()
# app.geometry("350x500")

# # Stockage des likes
# likes = {}

# def selectionner(item):
#     print(f"Vous avez choisi : {item}")
#     # label = True ou False
# def liker(item, label):
#     likes[item] = likes.get(item, 0)+1
    

# frame_liste = ctk.CTkScrollableFrame(app, label_text="Mon Panier")
# frame_liste.pack(padx=20, pady=20, fill="both", expand=True)

# for fruit in mes_donnees:
#     likes[fruit] = 0

#     ligne = ctk.CTkFrame(frame_liste)
#     ligne.pack(fill="x", pady=2, padx=5)

#     # Bouton principal
#     btn = ctk.CTkButton(
#         ligne,
#         text=fruit,
#         command=lambda f=fruit: selectionner(f),
#         anchor="w",
#         width=150
#     )
#     btn.pack(side="left", fill="x", expand=True)

#     # Label compteur likes
#     label_like = ctk.CTkLabel(ligne, text="👍 0", width=50)
#     label_like.pack(side="left", padx=5)

#     # Bouton like
#     btn_like = ctk.CTkButton(
#         ligne,
#         text="Like",
#         width=60,
#         command=lambda f=fruit, l=label_like: liker(f, l)
#     )
#     btn_like.pack(side="left")

# app.mainloop()


import customtkinter as ctk
from PIL import Image

app = ctk.CTk()
app.geometry("300x200")

# Images
img_off = ctk.CTkImage(Image.open("assets/coeur_gris.png"), size=(30, 30))
img_on = ctk.CTkImage(Image.open("assets/coeur_rouge.png"), size=(30, 30))

# Etat
liked = False

# Animation "pop"
def animation_pop(bouton, step=0):
    sizes = [30, 36, 30]  # effet zoom

    if step < len(sizes):
        size = sizes[step]

        # recrée image avec nouvelle taille
        img = ctk.CTkImage(
            Image.open("assets/coeur_rouge.png" if liked else "assets/coeur_gris.png"),
            size=(size, size)
        )
        bouton.configure(image=img)
        bouton.image = img  # éviter suppression mémoire

        app.after(30, lambda: animation_pop(bouton, step + 1))

# Fonction like
def toggle_like(bouton):
    global liked
    liked = not liked

    # changer image de base
    if liked:
        bouton.configure(image=img_on)
    else:
        bouton.configure(image=img_off)

    # lancer animation
    animation_pop(bouton)

# Bouton cœur
btn = ctk.CTkButton(
    app,
    text="",
    image=img_off,
    width=50,
    height=50,
    fg_color="transparent",
    hover=False,
    command=lambda: toggle_like(btn)
)
btn.pack(pady=50)

app.mainloop()