import tkinter as tk
import game as g

def iniciar_interfaz():
    def pedir_avatar():
        def guardar_avat(x):
            avatar_seleccionado = x
            print(avatar_seleccionado)
            def mostrar():
                if avatar_seleccionado == 1:
                    icono = canvas.create_image(20, 20, image=avat1image, anchor="nw")
                    canvas.avat1 = avat1image
                    canvas.tag_raise(icono)
                elif avatar_seleccionado == 2:
                    icono = canvas.create_image(20, 20, image=avat2image, anchor="nw")
                    canvas.avat2 = avat2image
                    canvas.tag_raise(icono)
                else:
                    icono = canvas.create_image(20, 20, image=avat3image, anchor="nw")
                    canvas.avat3 = avat3image
                    canvas.tag_raise(icono)
            
            popup_avat.destroy()
            mostrar()
        popup_avat = tk.Toplevel(ventana)
        popup_avat.geometry("742x266")
        popup_avat.resizable(False, False)
        popup_avat.title("select")
        popup_avat.grab_set() # pa bloquear la ventana anterior
        # popup_avat.protocol("WM_DELETE_WINDOW", lambda: None)
        canvas.popup_avat = tk.Canvas(popup_avat, width=760, height=370)
        canvas.popup_avat.pack()
        #background
        avatimage = tk. PhotoImage(file="Avatares.png")
        canvas.popup_avat.namebg = avatimage
        avat = canvas.popup_avat.create_image(0, 0, image= avatimage, anchor="nw")
        #--------------------------avatares--------------------------------#
        avat1image = tk.PhotoImage(file="Avat1.png")
        canvas.avat1 = avat1image
        avat2image = tk.PhotoImage(file="Avat2.png")
        canvas.avat2 = avat2image
        avat3image = tk.PhotoImage(file="Avat3.png")
        canvas.avat3 = avat3image
        
        avat1 = canvas.popup_avat.create_image(88, 140, image=avat1image, anchor="nw")
        canvas.popup_avat.tag_bind(avat1,"<Button-1>", lambda e: guardar_avat(1) )
        avat2 = canvas.popup_avat.create_image(288, 140,  image=avat2image, anchor="nw")
        canvas.popup_avat.tag_bind(avat2,"<Button-1>", lambda e: guardar_avat(2) )
        avat3 = canvas.popup_avat.create_image(488, 140, image=avat3image, anchor="nw")
        canvas.popup_avat.tag_bind(avat3,"<Button-1>", lambda e: guardar_avat(3) )

    def pedir_nombre():
        def save_name(event):
            name = nombre_var.get().strip()
            print(name)
            popup.destroy()
            pedir_avatar()
            
        popup = tk.Toplevel(ventana)
        popup.geometry("590x244")
        popup.resizable(False, False)
        popup.title("nombre")
        popup.grab_set() # pa bloquear la ventana anterior
        # popup.protocol("WM_DELETE_WINDOW", lambda: None)
        canvas_popup = tk.Canvas(popup, width=744, height=264)
        canvas_popup.pack()
        #background
        namebgimage = tk. PhotoImage(file="Namebg.png")
        canvas_popup.namebg = namebgimage
        namebg = canvas_popup.create_image(0, 0, image= namebgimage, anchor="nw")
        #entry
        nombre_var = tk.StringVar()
        entry = tk.Entry(canvas_popup, textvariable=nombre_var)
        entry.focus() # el cursor se pone dentro del entry
        canvas_popup.create_window(230, 100, window=entry)
        
        popup.bind("<Return>", save_name)

    def inicio():
        #limpiar pantalla inicio
        canvas.itemconfig(botonstart, image=botonstartPImage)
        ventana.after(150, lambda: canvas.delete(botonstart))  # elimina el botonStart del canvas
        ventana.after(150, lambda: canvas.delete(About))  # elimina el about del canvas
        ventana.after(160, pedir_nombre)
        ventana.after(160, lambda: canvas.itemconfig(bg, image=bg2)) # cambia a los niveles
        
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

                #---mundos
                #aparecer
                ventana.after(160, lambda: canvas.itemconfig(m4, state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m5, state="normal"))
                #esconder
                ventana.after(160, lambda: canvas.itemconfig(m1, state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(m2, state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(m3, state="hidden"))
                

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
                
                #---mundos
                #aparecer
                ventana.after(160, lambda: canvas.itemconfig(m1, state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m2, state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m3, state="normal"))
                #esconder
                ventana.after(160, lambda: canvas.itemconfig(m4, state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(m5, state="hidden"))

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
            
            #------------------------mundos----------------------------------#
            m1image = tk.PhotoImage(file="Lvl1.png")
            canvas.m1 = m1image
            m2image = tk.PhotoImage(file="Lvl2.png")
            canvas.m2 = m2image
            m3image = tk.PhotoImage(file="Lvl3.png")
            canvas.m3 = m3image
            m4image = tk.PhotoImage(file="Lvl4.png")
            canvas.m4 = m4image
            m5image = tk.PhotoImage(file="Lvl5.png")
            canvas.m5 = m5image

            
            m1 = canvas.create_image(88, 224, image=m1image, anchor="nw")
            m2 = canvas.create_image(272, 376, image=m2image, anchor="nw")
            m3 = canvas.create_image(504, 312, image=m3image, anchor="nw")
            m4 = canvas.create_image(216, 272, image=m4image, anchor="nw")
            canvas.itemconfig(m4, state="hidden")
            m5 = canvas.create_image(680, 208, image=m5image, anchor="nw")
            canvas.itemconfig(m5, state="hidden")

            #---------------panel--------------#
            panelimage = tk.PhotoImage(file="bar.png")
            canvas.panel= panelimage
            panel = canvas.create_image(0, 0, image=panelimage, anchor="nw")

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

    



