import tkinter as tk
from tkinter import messagebox
import game as g

def iniciar_interfaz():
    g.cargar_personajes()
    def pokemon_inicial_popup():
        popup_PI = tk.Toplevel(ventana, bg="green")
        popup_PI.geometry("590x550")
        popup_PI.resizable(False, False)
        popup_PI.title("amigos iniciales")
        popup_PI.grab_set() # pa bloquear la ventana anterior
        # popup.protocol("WM_DELETE_WINDOW", lambda: None)
       
        #checklist
        seleccionados = []
        vars_checks = []

        def por_check(var, nombre):
            if var.get():
                if len(seleccionados)>=3:
                    var.set(False)
                    return
                seleccionados.append(nombre)
            else:
                seleccionados.remove(nombre)
            
            for valor, checkbox in vars_checks:
                if not valor.get(): # si no esta marcado el check box
                    checkbox.config(state="disabled" if len(seleccionados) == 3 else "normal")
        
        for p in g.personajesP:
            Bvar = tk.BooleanVar()
            checkbox = tk.Checkbutton(popup_PI, text= p["nombre"], bg="lime green", variable= Bvar,
                        command=lambda valor=Bvar, checkbox=["nombre"]: por_check(valor, checkbox))
            checkbox.pack(anchor="w", padx="20", pady="2")
            vars_checks.append((Bvar, checkbox ))

        def confirmar():
            if len(seleccionados)!= 3:
                messagebox.showwarning("atencion", "debes elegir 3 amigos")
                return
            popup_PI.destroy()
            
            #funcion(seleccionados) futura para la siguiente lista
        tk.Button(popup_PI, text="confirmar", command=confirmar, bg="gold").pack(pady=10)

    def pedir_avatar():
        def guardar_avat(x):
            avatar_seleccionado = x
            pokemon_inicial_popup()
            def mostrar():
                if avatar_seleccionado == 1:
                    icono = canvas.create_image(20, 28, image=avat1image, anchor="nw")
                    canvas.avat1 = avat1image
                    canvas.tag_raise(icono)
                elif avatar_seleccionado == 2:
                    icono = canvas.create_image(20, 28, image=avat2image, anchor="nw")
                    canvas.avat2 = avat2image
                    canvas.tag_raise(icono)
                else:
                    icono = canvas.create_image(20, 28, image=avat3image, anchor="nw")
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
            label_info.destroy()#quitar la info ya obvia

            if nombre_var.get().strip() == "": # texto vacio
                label_error_nombre = tk.Label(popup, text="escribe un nombre", fg="red" )
                canvas_popup.create_window(100, 100, window= label_error_nombre)

            elif len(nombre_var.get().strip()) > 10: # maximo de caracteres
                label_error_caracter = tk.Label(popup, text="maximo 10 caracteres", fg="red" )
                canvas_popup.create_window(100, 100, window= label_error_caracter)

            else: #guardar
                name = nombre_var.get().strip()
                print(name)
                popup.destroy()
                label_nombre = tk.Label(ventana, text=name )
                canvas.create_window( 50, 14, window= label_nombre)
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
        canvas_popup.create_window(240, 100, window=entry)
        #label de informacion
        label_info = tk.Label(popup, text="presione enter para guardar")
        canvas_popup.create_window(90, 100, window= label_info)

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
            def flecha_selectora(nv):
                if nv == 1:
                    canvas.itemconfig(flecha, state="normal")
                    canvas.coords(flecha, 125, 120)
                elif nv == 2:
                    canvas.itemconfig(flecha, state="normal")
                    canvas.coords(flecha, 332, 260)
                elif nv == 3:
                    canvas.itemconfig(flecha, state="normal")
                    canvas.coords(flecha, 600, 180)
                elif nv == 4:
                    canvas.itemconfig(flecha, state="normal")
                    canvas.coords(flecha, 346, 170)
                elif nv == 5:
                    canvas.itemconfig(flecha, state="normal")
                    canvas.coords(flecha, 800, 120)        

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
                ventana.after(160, lambda: canvas.itemconfig(flecha, state="hidde"))

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
                ventana.after(160, lambda: canvas.itemconfig(flecha, state="hidde"))

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
            canvas.tag_bind(m1,"<Button-1>", lambda e: flecha_selectora(1))
            m2 = canvas.create_image(272, 376, image=m2image, anchor="nw")
            canvas.tag_bind(m2,"<Button-1>", lambda e: flecha_selectora(2))
            m3 = canvas.create_image(504, 312, image=m3image, anchor="nw")
            canvas.tag_bind(m3,"<Button-1>", lambda e: flecha_selectora(3))
            m4 = canvas.create_image(216, 272, image=m4image, anchor="nw")
            canvas.tag_bind(m4,"<Button-1>", lambda e: flecha_selectora(4))
            canvas.itemconfig(m4, state="hidden")
            m5 = canvas.create_image(680, 208, image=m5image, anchor="nw")
            canvas.tag_bind(m5,"<Button-1>", lambda e: flecha_selectora(5))
            canvas.itemconfig(m5, state="hidden")

            #---------------------flecha-----------------------------------------#
            flechaimage = tk.PhotoImage(file="selection.png")
            canvas.FS = flechaimage
            flecha = canvas.create_image(0, 0, image= flechaimage, anchor="nw")
            canvas.itemconfig(flecha, state="hidden")

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

    



