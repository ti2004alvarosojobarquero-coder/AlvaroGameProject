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
            def NextF (): # animacion del boton, esconderlo 
                canvas.itemconfig(Next, image=NextBPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next, image=NextBimage)) 
                ventana.after(160, lambda: canvas.itemconfig(bg, image=bg3))
                ventana.after(160, lambda: canvas.itemconfig(Next, state="hidden"))
                ventana.after(160, lambda: canvas.tag_unbind(Next, "<button1>"))
                #aparecer next2
                canvas.itemconfig(Next2, image=Next2BPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next2, image=Next2Bimage)) 
                ventana.after(160, lambda: canvas.itemconfig(Next2, state="normal"))
                ventana.after(160, lambda: canvas.tag_bind(Next2,"<Button-1>", lambda e: Next2F()))


            def Next2F (): # animacion del boton, esconder
                canvas.itemconfig(Next2, image=Next2BPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next2, image=Next2Bimage)) 
                ventana.after(160, lambda: canvas.itemconfig(bg, image=bg2))
                ventana.after(160, lambda: canvas.itemconfig(Next2, state="hidden"))
                ventana.after(160, lambda: canvas.tag_unbind(Next2, "<button1>"))    

                #aparecer next1
                canvas.itemconfig(Next, image=NextBPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next, image=NextBimage)) 
                ventana.after(160, lambda: canvas.itemconfig(Next, state="normal"))
                ventana.after(160, lambda: canvas.tag_bind(Next,"<Button-1>", lambda e: NextF()))  
        
        
                
                
            #next1
            NextBimage = tk.PhotoImage(file="Next1.png")
            NextBPimage = tk.PhotoImage(file="Next1P.png")
            canvas.N = NextBimage
            canvas.NP = NextBPimage
            Next = canvas.create_image(890, 250, image=NextBimage, anchor="nw")
            canvas.tag_bind(Next,"<Button-1>", lambda e: NextF())
            
            #next2
            Next2Bimage = tk.PhotoImage(file="Next2.png")
            Next2BPimage = tk.PhotoImage(file="Next2P.png")
            canvas.N2 = Next2Bimage
            canvas.N2P = Next2BPimage
            Next2 = canvas.create_image(50, 250, image=Next2Bimage, anchor="nw")
            canvas.itemconfig(Next2, state="hidden")
            canvas.tag_bind(Next2,"<Button-1>", lambda e: Next2F())
            canvas.tag_unbind(Next2,"<Button-1>")

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
    bg3 = tk.PhotoImage(file="Levels2.png")
    canvas.bg1 = bg1
    canvas.bg2 = bg2
    canvas.bg3 = bg3
    bg = canvas.create_image(0, 0, image=bg1, anchor="nw")
    
    

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

    



