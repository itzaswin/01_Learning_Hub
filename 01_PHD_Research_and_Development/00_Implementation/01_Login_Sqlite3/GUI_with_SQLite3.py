import sqlite3
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox

# --------------------------
# Gradient Background
# --------------------------

def draw_multi_color_gradient(canvas, width, height, colors):
    steps = len(colors) - 1
    segment_height = height // steps

    for i in range(steps):
        r1, g1, b1 = canvas.winfo_rgb(colors[i])
        r2, g2, b2 = canvas.winfo_rgb(colors[i + 1])

        r_ratio = (r2-r1)/segment_height
        g_ratio = (g2-g1)/segment_height
        b_ratio = (b2-b1)/segment_height

        for j in range(segment_height):
            nr=int(r1+r_ratio*j)
            ng=int(g1+g_ratio*j)
            nb=int(b1+b_ratio*j)

            color=f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
            canvas.create_line(0,i*segment_height+j,width,i*segment_height+j,fill=color)

# ------------------------------------------------
# Main GUI
# ------------------------------------------------

class MainGUI:

    def __init__(self,root):
        self.root=root
        self.root.title("AGRICULTURAL INSECT IDENTIFICATION")
        self.root.geometry("1100x630")
        self.root.resizable(False,False)

        canvas=Canvas(root,width=1100,height=630)
        canvas.pack(fill="both",expand=True)
        draw_multi_color_gradient(
            canvas,
            1100,
            630,
            ["#659287","#88BDA4","#B1D3B9","#E6F2DD"]
        )

        title_frame=ctk.CTkFrame(root,width=1000,height=45,fg_color="white")
        title_frame.place(relx=.5,y=20,anchor="n")

        title=ctk.CTkLabel(
            title_frame,
            text="DEEP LEARNING BASED CLASSIFICATION AND IDENTIFICATION OF HARMFUL AND USEFUL INSECTS FOR AGRICULTURE",
            font=ctk.CTkFont(size=18,weight="bold"),
            text_color="red",
            wraplength=950
        )

        title.place(relx=.5,rely=.5,anchor="center")

        # Example Buttons

        ctk.CTkButton(root,text="Upload Dataset",width=180).place(x=50,y=120)

        ctk.CTkButton(root,text="Preprocessing",width=180).place(x=50,y=180)

        ctk.CTkButton(root,text="Training",width=180).place(x=50,y=240)

        ctk.CTkButton(root,text="Testing",width=180).place(x=50,y=300)

        ctk.CTkButton(root,text="Prediction",width=180).place(x=50,y=360)

# ------------------------------------------------
# Login Window
# ------------------------------------------------

class Login:

    def __init__(self,root):

        self.root=root

        self.root.geometry("450x350")

        self.root.title("Login")

        self.root.resizable(False,False)

        ctk.CTkLabel(
            root,
            text="LOGIN",
            font=ctk.CTkFont(size=28,weight="bold")
        ).pack(pady=20)

        self.user=ctk.CTkEntry(
            root,
            width=250,
            placeholder_text="Username"
        )

        self.user.pack(pady=10)

        self.password=ctk.CTkEntry(
            root,
            width=250,
            placeholder_text="Password",
            show="*"
        )

        self.password.pack(pady=10)

        ctk.CTkButton(
            root,
            text="Login",
            width=200,
            command=self.login
        ).pack(pady=25)

    def login(self):

        username=self.user.get()

        password=self.password.get()

        conn=sqlite3.connect("db\\users.db")

        cur=conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        row=cur.fetchone()

        conn.close()

        if row:

            messagebox.showinfo("Success","Login Successful")

            self.root.destroy()

            main=ctk.CTk()

            MainGUI(main)

            main.mainloop()

        else:

            messagebox.showerror("Login","Invalid Username or Password")

# ------------------------------------------------
# Start Application
# ------------------------------------------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root=ctk.CTk()

Login(root)

root.mainloop()