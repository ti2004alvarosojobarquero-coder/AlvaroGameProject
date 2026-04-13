import tkinter as tk
import game as g

def iniciar_interfaz():
    def inicio():
        canvas.itemconfig(botonstart, image=botonstartPImage)
        ventana.after(150, lambda: canvas.delete(botonstart))  # elimina el botonStart del canvas

    #escape
    def salir(event):
        ventana.destroy()

    ventana = tk.Tk()
    ventana.geometry("1024x576")
    ventana.resizable(False, False)
    ventana.bind("<Escape>", salir)

    canvas = tk.Canvas(ventana, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    # fondos
    bg1 = tk.PhotoImage(file="Bg1.png")
    canvas.bg1 = bg1
    canvas.create_image(0, 0, image=bg1, anchor="nw")
    
    #prueba sprite
    # villano = tk.PhotoImage(file="jefe villano 1.png")
    # villano = villano.zoom(12)
    # canvas.villano = villano
    # canvas.create_image(300, 0, image=villano, anchor="nw")

    # botónes
    #botonstart
    botonstartImage = tk.PhotoImage(file="BotonStart.png")
    botonstartPImage = tk.PhotoImage(file="BotonStartP.png")
    canvas.bs = botonstartImage
    botonstart = canvas.create_image(390, 290, image=botonstartImage, anchor="nw")
    canvas.tag_bind(botonstart, "<Button-1>", lambda e: inicio())

    
    ventana.update()
    print(canvas.coords(botonstart))

    ventana.mainloop()

    



