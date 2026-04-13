import tkinter as tk
import game as g

def iniciar_interfaz():
    def inicio():
        #limpiar pantalla inicio
        canvas.itemconfig(botonstart, image=botonstartPImage)
        ventana.after(150, lambda: canvas.delete(botonstart))  # elimina el botonStart del canvas
        ventana.after(150, lambda: canvas.delete(About))  # elimina el about del canvas
        ventana.after(150, lambda: canvas.itemconfig(bg, image=bg2)) # cambia a los niveles
        
        #cargar botones y paneles
        def cargar ():
            def NextF (): # animacion del boton
                canvas.itemconfig(Next, image=NextBPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next, image=NextBimage))  
                
            #nextboton
            NextBimage = tk.PhotoImage(file="Next1.png")
            NextBPimage = tk.PhotoImage(file="Next1P.png")
            canvas.N = NextBimage
            canvas.NP = NextBPimage
            Next = canvas.create_image(875, 250, image=NextBimage, anchor="nw")
            canvas.tag_bind(Next,"<Button-1>", lambda e: NextF())
        ventana.after(150, cargar)#esperar a limpiar la pantalla para crear el boton
    #boton about
    def aboutf():
        canvas.itemconfig(About, image=AboutPImage)
        ventana.after(150, lambda: canvas.itemconfig(About, image=AboutImage))  # cambia al boton normal

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
    bg2 = tk.PhotoImage(file="Levels1.png")
    canvas.bg1 = bg1
    canvas.bg2 = bg2
    bg = canvas.create_image(0, 0, image=bg1, anchor="nw")
    
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
    canvas.bsP = botonstartPImage
    botonstart = canvas.create_image(380, 300, image=botonstartImage, anchor="nw")
    canvas.tag_bind(botonstart, "<Button-1>", lambda e: inicio())
    
    #about
    AboutImage = tk.PhotoImage(file="About.png")
    AboutPImage = tk.PhotoImage(file="AboutP.png")
    canvas.Ab = AboutImage
    canvas.AbP = AboutPImage
    About = canvas.create_image(380, 450, image=AboutImage, anchor="nw")
    canvas.tag_bind(About, "<Button-1>", lambda e: aboutf())

    
    

    ventana.mainloop()

    



