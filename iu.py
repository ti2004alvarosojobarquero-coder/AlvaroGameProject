import tkinter as tk
from tkinter import messagebox
import game as g
 
delatador = 0
 
def iniciar_interfaz():
    g.cargar_personajes()
 
    #------------------------------------------------------------#
    #  INVENTARIO
    #  Lee canvas.inventario directamente pa mostrar siempre
    #  el estado actual, incluyendo pokemones ganados en batalla.
    #------------------------------------------------------------#
    def invFun(selec):
        popup_inv = tk.Toplevel(ventana, bg="green")
        popup_inv.geometry("590x550")
        popup_inv.resizable(False, False)
        popup_inv.title("INVENTARIO")
        popup_inv.grab_set()
        for p in canvas.inventario:
            labelinv = tk.Label(popup_inv,
                                text=f"{p['nombre']}, vida={p['hp']}, daño={p['ataque']}",
                                bg="lime green")
            labelinv.pack(anchor="w", padx=20, pady=2)
 
    #------------------------------------------------------------#
    #  PRE-BATALLA: elegir 3 pokemones del inventario
    #  Recibe el nivel pa pasarselo a batalla_popup.
    #  Si no hay pokemones vivos avisa y no abre la batalla.
    #------------------------------------------------------------#
    def seleccion_batalla_popup(nivel=1):
        popup_sel = tk.Toplevel(ventana, bg="purple")
        popup_sel.geometry("400x450")
        popup_sel.resizable(False, False)
        popup_sel.title("Elegir equipo de batalla")
        popup_sel.grab_set()
 
        tk.Label(popup_sel, text="Elegí 3 pokemones para batallar",
                 bg="purple", fg="white", font=("Arial", 12)).pack(pady=10)
 
        elegidos    = []
        vars_checks = []
 
        def por_check_batalla(var, pokemon):
            if var.get():
                if len(elegidos) >= 3:
                    var.set(False)
                    return
                elegidos.append(pokemon)
            else:
                if pokemon in elegidos:
                    elegidos.remove(pokemon)
            for valor, checkbox in vars_checks:
                if not valor.get():
                    checkbox.config(state="disabled" if len(elegidos) == 3 else "normal")
 
        # solo pokemones vivos del inventario permanente
        vivos = [p for p in canvas.inventario if p["hp"] > 0]
 
        # --- si no hay pokemones vivos no se puede batallar ---
        if not vivos:
            messagebox.showerror("Sin pokemones", "No tenés pokemones vivos para batallar.")
            popup_sel.destroy()
            return
 
        for p in vivos:
            Bvar     = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                popup_sel,
                text=f"{p['nombre']}  ❤{p['hp']}  ⚔{p['ataque']}",
                bg="purple", fg="white", selectcolor="black",
                variable=Bvar,
                command=lambda v=Bvar, pk=p: por_check_batalla(v, pk)
            )
            checkbox.pack(anchor="w", padx=20, pady=3)
            vars_checks.append((Bvar, checkbox))
 
        def confirmar_equipo():
            if len(elegidos) != 3:
                messagebox.showwarning("atención", "elegí exactamente 3 pokemones")
                return
            popup_sel.destroy()
            batalla_popup(list(elegidos), nivel)
 
        tk.Button(popup_sel, text="¡A BATALLAR!", bg="gold",
                  font=("Arial", 11, "bold"), command=confirmar_equipo).pack(pady=15)
 
    #------------------------------------------------------------#
    #  POPUP DE BATALLA
    #  Recibe el equipo del jugador y el nivel.
    #  El Hollow se muestra arriba como avatar enemigo pero
    #  NO pelea, igual que el avatar del jugador.
    #  El equipo enemigo son 3 pokemones que el jugador no tiene.
    #------------------------------------------------------------#
    def batalla_popup(equipo_jugador, nivel=1):
        popup_bat = tk.Toplevel(ventana, bg="purple")
        popup_bat.geometry("700x550")
        popup_bat.resizable(False, False)
        popup_bat.title("BATALLA")
        popup_bat.grab_set()
 
        canvas_bat = tk.Canvas(popup_bat, width=700, height=550,
                               bg="#2d0057", highlightthickness=0)
        canvas_bat.pack()
 
        # --- equipo enemigo: 3 pokemones + path del hollow como avatar ---
        equipo_enemigo, hollow_path = g.generar_equipo_enemigo(nivel, canvas.inventario)
 
        # ------- avatar del jugador (izquierda arriba) -------#
        if hasattr(canvas, "avat1") and canvas.avat1:
            img_avat = canvas.avat1
        elif hasattr(canvas, "avat2") and canvas.avat2:
            img_avat = canvas.avat2
        else:
            img_avat = canvas.avat3
        canvas_bat.create_image(30, 20, image=img_avat, anchor="nw")
        canvas_bat.img_avat = img_avat
 
        # ------- hollow como avatar enemigo (derecha arriba) -------#
        try:
            img_hollow = tk.PhotoImage(file=hollow_path)
        except Exception:
            img_hollow = tk.PhotoImage(width=64, height=64)
        canvas_bat.create_image(606, 20, image=img_hollow, anchor="nw")
        canvas_bat.img_hollow = img_hollow  # referencia pa no perderla
 
        # ------- títulos de columna -------#
        canvas_bat.create_text(180, 15, text="TU EQUIPO",
                               fill="white", font=("Arial", 10, "bold"))
        canvas_bat.create_text(520, 15, text="ENEMIGOS",
                               fill="red",   font=("Arial", 10, "bold"))
 
        # ------- imágenes pokemones del jugador (izquierda) -------#
        imgs_jug = []
        for i, poke in enumerate(equipo_jugador):
            img = tk.PhotoImage(file=poke["imagen"])
            imgs_jug.append(img)
            canvas_bat.create_image(50 + i * 110, 270, image=img,
                                    anchor="nw", tags=f"pjug_{i}")
        canvas_bat.imgs_jug = imgs_jug
 
        # ------- imágenes pokemones enemigos (derecha) -------#
        imgs_ene = []
        for i, poke in enumerate(equipo_enemigo):
            img = tk.PhotoImage(file=poke["imagen"])
            imgs_ene.append(img)
            canvas_bat.create_image(390 + i * 100, 270, image=img,
                                    anchor="nw", tags=f"pene_{i}")
        canvas_bat.imgs_ene = imgs_ene
 
        # ------- labels de HP jugador -------#
        hp_jug = []
        for i, poke in enumerate(equipo_jugador):
            lbl = tk.Label(popup_bat,
                           text=f"{poke['nombre']}\n❤ {poke['hp']}",
                           bg="#2d0057", fg="lime", font=("Arial", 8))
            canvas_bat.create_window(90 + i * 110, 360, window=lbl)
            hp_jug.append(lbl)
 
        # ------- labels de HP enemigo -------#
        hp_ene = []
        for i, poke in enumerate(equipo_enemigo):
            lbl = tk.Label(popup_bat,
                           text=f"{poke['nombre']}\n❤ {poke['hp']}",
                           bg="#2d0057", fg="red", font=("Arial", 8))
            canvas_bat.create_window(430 + i * 100, 360, window=lbl)
            hp_ene.append(lbl)
 
        # ------- log de batalla -------#
        log_text = tk.Text(popup_bat, width=50, height=5,
                           bg="black", fg="lime",
                           font=("Courier", 8), state="disabled")
        canvas_bat.create_window(350, 470, window=log_text)
 
        def escribir_log(msg):
            log_text.config(state="normal")
            log_text.insert("end", f"> {msg}\n")
            log_text.see("end")
            log_text.config(state="disabled")
 
        # ------- botón atacar y label de turno -------#
        btn_atacar = tk.Button(popup_bat, text="⚔  ATACAR",
                               bg="gold", font=("Arial", 13, "bold"), width=10)
        canvas_bat.create_window(180, 420, window=btn_atacar)
 
        lbl_turno = tk.Label(popup_bat, text="¡Tu turno!",
                             bg="#2d0057", fg="yellow", font=("Arial", 11, "bold"))
        canvas_bat.create_window(500, 420, window=lbl_turno)
 
        # =========================================================
        # RECURSIÓN DE COLA: procesar_turno(acciones, i)
        # ---------------------------------------------------------
        # Recibe una lista de funciones (acciones) y un índice i.
        # Ejecuta acciones[i] y se llama a sí misma con i+1
        # después de 1 segundo via after(), sin bloquear tkinter.
        # Caso base: i >= len(acciones) → reactiva botón.
        # =========================================================
        def procesar_turno(acciones, i=0):
            if i >= len(acciones):
                btn_atacar.config(state="normal")
                lbl_turno.config(text="¡Tu turno!", fg="yellow")
                return
            acciones[i]()
            popup_bat.after(1000, lambda: procesar_turno(acciones, i + 1))
 
        # ------- acción del jugador en su turno -------#
        def accion_jugador():
            atacante = next((p for p in equipo_jugador if p["hp"] > 0), None)
            defensor = next((p for p in equipo_enemigo if p["hp"] > 0), None)
            if not atacante or not defensor:
                return
 
            daño = g.calcular_daño(atacante, defensor)
 
            if daño == 0:
                escribir_log(f"{defensor['nombre']} esquivó el ataque de {atacante['nombre']}!")
                return
 
            defensor["hp"] = max(0, defensor["hp"] - daño)
            idx = equipo_enemigo.index(defensor)
            hp_ene[idx].config(text=f"{defensor['nombre']}\n❤ {defensor['hp']}")
            escribir_log(f"{atacante['nombre']} golpeó a {defensor['nombre']} (-{daño} hp)")
 
            if defensor["hp"] <= 0:
                canvas_bat.itemconfig(f"pene_{idx}", state="hidden")
                escribir_log(f"¡{defensor['nombre']} fue derrotado!")
 
                # --- chequear victoria ---
                if all(p["hp"] <= 0 for p in equipo_enemigo):
                    # buscar el hp original en personajesP pa agregar con vida completa
                    nuevos = []
                    for p in equipo_enemigo:
                        original = next((x for x in g.personajesP if x["nombre"] == p["nombre"]), None)
                        if original:
                            nuevos.append(dict(original))  # copia fresca con hp original
                    canvas.inventario.extend(nuevos)
                    escribir_log("¡¡GANASTE!! Los pokemones enemigos son tuyos.")
                    btn_atacar.config(state="disabled", text="Victoria ✓")
                    popup_bat.after(2000, popup_bat.destroy)
 
        # ------- respuesta del enemigo -------#
        def accion_enemigo():
            atacante = next((p for p in equipo_enemigo if p["hp"] > 0), None)
            defensor = next((p for p in equipo_jugador if p["hp"] > 0), None)
            if not atacante or not defensor:
                return
 
            lbl_turno.config(text="Turno enemigo...", fg="red")
            daño = g.calcular_daño(atacante, defensor)
 
            if daño == 0:
                escribir_log(f"{defensor['nombre']} esquivó el ataque de {atacante['nombre']}!")
                return
 
            defensor["hp"] = max(0, defensor["hp"] - daño)
            idx = equipo_jugador.index(defensor)
            hp_jug[idx].config(text=f"{defensor['nombre']}\n❤ {defensor['hp']}")
            escribir_log(f"{atacante['nombre']} golpeó a {defensor['nombre']} (-{daño} hp)")
 
            if defensor["hp"] <= 0:
                canvas_bat.itemconfig(f"pjug_{idx}", state="hidden")
                escribir_log(f"¡{defensor['nombre']} cayó para siempre!")
 
                # se elimina permanentemente del inventario
                if defensor in canvas.inventario:
                    canvas.inventario.remove(defensor)
 
                # --- chequear derrota ---
                if all(p["hp"] <= 0 for p in equipo_jugador):
                    escribir_log("PERDISTE... todos tus pokemones cayeron.")
                    btn_atacar.config(state="disabled", text="Derrota ✗")
 
        # ------- al presionar el botón atacar -------#
        def atacar():
            btn_atacar.config(state="disabled")
            lbl_turno.config(text="Atacando...", fg="white")
            procesar_turno([accion_jugador, accion_enemigo])
 
        btn_atacar.config(command=atacar)
 
    #------------------------------------------------------------#
    #  INVENTARIO INICIAL
    #------------------------------------------------------------#
    def pokemon_inicial_popup():
        popup_PI = tk.Toplevel(ventana, bg="green")
        popup_PI.geometry("590x550")
        popup_PI.resizable(False, False)
        popup_PI.title("amigos iniciales")
        popup_PI.grab_set()
 
        seleccionados = []
        vars_checks   = []
 
        def por_check(var, nombre):
            if var.get():
                if len(seleccionados) >= 3:
                    var.set(False)
                    return
                seleccionados.append(nombre)
            else:
                seleccionados.remove(nombre)
            for valor, checkbox in vars_checks:
                if not valor.get():
                    checkbox.config(state="disabled" if len(seleccionados) == 3 else "normal")
 
        for p in g.personajesP:
            Bvar     = tk.BooleanVar()
            checkbox = tk.Checkbutton(popup_PI, text=p["nombre"],
                                      bg="lime green", variable=Bvar,
                                      command=lambda valor=Bvar, personaje=p: por_check(valor, personaje))
            checkbox.pack(anchor="w", padx=20, pady=2)
            vars_checks.append((Bvar, checkbox))
 
        def confirmar():
            if len(seleccionados) != 3:
                messagebox.showwarning("atencion", "debes elegir 3 amigos")
                return
 
            canvas.inventario = list(seleccionados)
 
            invimage = tk.PhotoImage(file="Poke.png")
            canvas.inv = invimage
            inv = canvas.create_image(900, 20, image=invimage, anchor="nw", tags="selectorniv")
            canvas.tag_bind(inv, "<Button-1>", lambda e: invFun(seleccionados))
 
            popup_PI.destroy()
            print(seleccionados)
 
        tk.Button(popup_PI, text="confirmar", command=confirmar, bg="gold").pack(pady=10)
 
    #------------------------------------------------------------#
    #  SELECCIÓN DE AVATAR
    #------------------------------------------------------------#
    def pedir_avatar():
        def guardar_avat(x):
            avatar_seleccionado = x
            pokemon_inicial_popup()
 
            def mostrar():
                if avatar_seleccionado == 1:
                    icono = canvas.create_image(20, 28, image=avat1image, anchor="nw", tags="selectorniv")
                    canvas.avat1 = avat1image
                    canvas.tag_raise(icono)
                elif avatar_seleccionado == 2:
                    icono = canvas.create_image(20, 28, image=avat2image, anchor="nw", tags="selectorniv")
                    canvas.avat2 = avat2image
                    canvas.tag_raise(icono)
                else:
                    icono = canvas.create_image(20, 28, image=avat3image, anchor="nw", tags="selectorniv")
                    canvas.avat3 = avat3image
                    canvas.tag_raise(icono)
 
            popup_avat.destroy()
            mostrar()
 
        popup_avat = tk.Toplevel(ventana)
        popup_avat.geometry("742x266")
        popup_avat.resizable(False, False)
        popup_avat.title("select")
        popup_avat.grab_set()
 
        canvas.popup_avat = tk.Canvas(popup_avat, width=760, height=370)
        canvas.popup_avat.pack()
 
        avatimage = tk.PhotoImage(file="Avatares.png")
        canvas.popup_avat.namebg = avatimage
        canvas.popup_avat.create_image(0, 0, image=avatimage, anchor="nw")
 
        avat1image = tk.PhotoImage(file="Avat1.png")
        canvas.avat1 = avat1image
        avat2image = tk.PhotoImage(file="Avat2.png")
        canvas.avat2 = avat2image
        avat3image = tk.PhotoImage(file="Avat3.png")
        canvas.avat3 = avat3image
 
        avat1 = canvas.popup_avat.create_image(88,  140, image=avat1image, anchor="nw")
        canvas.popup_avat.tag_bind(avat1, "<Button-1>", lambda e: guardar_avat(1))
        avat2 = canvas.popup_avat.create_image(288, 140, image=avat2image, anchor="nw")
        canvas.popup_avat.tag_bind(avat2, "<Button-1>", lambda e: guardar_avat(2))
        avat3 = canvas.popup_avat.create_image(488, 140, image=avat3image, anchor="nw")
        canvas.popup_avat.tag_bind(avat3, "<Button-1>", lambda e: guardar_avat(3))
 
    #------------------------------------------------------------#
    #  PEDIR NOMBRE
    #------------------------------------------------------------#
    def pedir_nombre():
        def save_name(event):
            label_info.destroy()
 
            if nombre_var.get().strip() == "":
                label_error = tk.Label(popup, text="escribe un nombre", fg="red")
                canvas_popup.create_window(100, 100, window=label_error)
 
            elif len(nombre_var.get().strip()) > 10:
                label_error = tk.Label(popup, text="maximo 10 caracteres", fg="red")
                canvas_popup.create_window(100, 100, window=label_error)
 
            else:
                name = nombre_var.get().strip()
                print(name)
                popup.destroy()
                label_nombre = tk.Label(ventana, text=name)
                canvas.create_window(50, 14, window=label_nombre, tags="selectorniv")
                pedir_avatar()
                global delatador
                delatador = 1
 
        popup = tk.Toplevel(ventana)
        popup.geometry("590x244")
        popup.resizable(False, False)
        popup.title("nombre")
        popup.grab_set()
 
        canvas_popup = tk.Canvas(popup, width=744, height=264)
        canvas_popup.pack()
 
        namebgimage = tk.PhotoImage(file="Namebg.png")
        canvas_popup.namebg = namebgimage
        canvas_popup.create_image(0, 0, image=namebgimage, anchor="nw")
 
        nombre_var = tk.StringVar()
        entry = tk.Entry(canvas_popup, textvariable=nombre_var)
        entry.focus()
        canvas_popup.create_window(240, 100, window=entry)
 
        label_info = tk.Label(popup, text="presione enter para guardar")
        canvas_popup.create_window(90, 100, window=label_info)
 
        popup.bind("<Return>", save_name)
 
    #------------------------------------------------------------#
    #  MENU Y INICIO
    #------------------------------------------------------------#
    def menu():
        canvas.itemconfig("selectorniv",  state="hidden")
        canvas.itemconfig("selectornivE", state="hidden")
        canvas.itemconfig("selectorniv2", state="hidden")
        canvas.itemconfig("inicio",       state="normal")
        canvas.itemconfig(botonstart, image=botonstartImage)
        canvas.itemconfig(bg, image=bg1)
 
    def inicio():
        nonlocal ya_cargo
        canvas.itemconfig(botonstart, image=botonstartPImage)
        ventana.after(150, lambda: canvas.itemconfig("inicio", state="hidden"))
        if delatador == 0: ventana.after(160, pedir_nombre)
        ventana.after(160, lambda: canvas.itemconfig(bg, image=bg2))
        ventana.after(160, lambda: canvas.itemconfig("selectorniv", state="normal"))
 
        def cargar():
            def flecha_selectora(nv):
                posiciones = {1: (125,120), 2: (332,260), 3: (600,180),
                              4: (346,170), 5: (800,120)}
                if nv in posiciones:
                    canvas.itemconfig(flecha, state="normal")
                    canvas.coords(flecha, *posiciones[nv])
 
            #-----------------nextbuttons----------------------------#
            def NextF():
                canvas.itemconfig(Next, image=NextBPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next,  image=NextBimage))
                ventana.after(160, lambda: canvas.itemconfig(bg,    image=bg3))
                ventana.after(160, lambda: canvas.itemconfig(Next,  state="hidden"))
                ventana.after(160, lambda: canvas.tag_unbind(Next,  "<Button-1>"))
                canvas.itemconfig(Next2, image=Next2BPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next2, image=Next2Bimage))
                ventana.after(160, lambda: canvas.itemconfig(Next2, state="normal"))
                ventana.after(160, lambda: canvas.tag_bind(Next2, "<Button-1>", lambda e: Next2F()))
                ventana.after(160, lambda: canvas.itemconfig(m4,    state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m5,    state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m1,    state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(m2,    state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(m3,    state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(flecha, state="hidden"))
 
            def Next2F():
                canvas.itemconfig(Next2, image=Next2BPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next2, image=Next2Bimage))
                ventana.after(160, lambda: canvas.itemconfig(bg,    image=bg2))
                ventana.after(160, lambda: canvas.itemconfig(Next2, state="hidden"))
                ventana.after(160, lambda: canvas.tag_unbind(Next2, "<Button-1>"))
                canvas.itemconfig(Next, image=NextBPimage)
                ventana.after(150, lambda: canvas.itemconfig(Next,  image=NextBimage))
                ventana.after(160, lambda: canvas.itemconfig(Next,  state="normal"))
                ventana.after(160, lambda: canvas.tag_bind(Next, "<Button-1>", lambda e: NextF()))
                ventana.after(160, lambda: canvas.itemconfig(m1,    state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m2,    state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m3,    state="normal"))
                ventana.after(160, lambda: canvas.itemconfig(m4,    state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(m5,    state="hidden"))
                ventana.after(160, lambda: canvas.itemconfig(flecha, state="hidden"))
 
            NextBimage   = tk.PhotoImage(file="Next1.png")
            NextBPimage  = tk.PhotoImage(file="Next1P.png")
            canvas.N     = NextBimage
            canvas.NP    = NextBPimage
            Next = canvas.create_image(890, 250, image=NextBimage, anchor="nw", tags="selectorniv")
            canvas.tag_bind(Next, "<Button-1>", lambda e: NextF())
 
            Next2Bimage  = tk.PhotoImage(file="Next2.png")
            Next2BPimage = tk.PhotoImage(file="Next2P.png")
            canvas.N2    = Next2Bimage
            canvas.N2P   = Next2BPimage
            Next2 = canvas.create_image(50, 250, image=Next2Bimage, anchor="nw", tags="selectorniv2")
            canvas.itemconfig(Next2, state="hidden")
            canvas.tag_bind(Next2, "<Button-1>", lambda e: Next2F())
            canvas.tag_unbind(Next2, "<Button-1>")
 
            #------------------------mundos----------------------------------#
            m1image = tk.PhotoImage(file="Lvl1.png"); canvas.m1 = m1image
            m2image = tk.PhotoImage(file="Lvl2.png"); canvas.m2 = m2image
            m3image = tk.PhotoImage(file="Lvl3.png"); canvas.m3 = m3image
            m4image = tk.PhotoImage(file="Lvl4.png"); canvas.m4 = m4image
            m5image = tk.PhotoImage(file="Lvl5.png"); canvas.m5 = m5image
 
            m1 = canvas.create_image(88,  224, image=m1image, anchor="nw", tags="selectorniv")
            canvas.tag_bind(m1, "<Button-1>",        lambda e: flecha_selectora(1))
            canvas.tag_bind(m1, "<Double-Button-1>", lambda e: seleccion_batalla_popup(nivel=1))
 
            m2 = canvas.create_image(272, 376, image=m2image, anchor="nw", tags="selectorniv")
            canvas.tag_bind(m2, "<Button-1>",        lambda e: flecha_selectora(2))
            canvas.tag_bind(m2, "<Double-Button-1>", lambda e: seleccion_batalla_popup(nivel=2))
 
            m3 = canvas.create_image(504, 312, image=m3image, anchor="nw", tags="selectorniv")
            canvas.tag_bind(m3, "<Button-1>",        lambda e: flecha_selectora(3))
            canvas.tag_bind(m3, "<Double-Button-1>", lambda e: seleccion_batalla_popup(nivel=3))
 
            m4 = canvas.create_image(216, 272, image=m4image, anchor="nw", tags="selectorniv2")
            canvas.tag_bind(m4, "<Button-1>",        lambda e: flecha_selectora(4))
            canvas.tag_bind(m4, "<Double-Button-1>", lambda e: seleccion_batalla_popup(nivel=4))
            canvas.itemconfig(m4, state="hidden")
 
            m5 = canvas.create_image(680, 208, image=m5image, anchor="nw", tags="selectorniv2")
            canvas.tag_bind(m5, "<Button-1>",        lambda e: flecha_selectora(5))
            canvas.tag_bind(m5, "<Double-Button-1>", lambda e: seleccion_batalla_popup(nivel=5))
            canvas.itemconfig(m5, state="hidden")
 
            #---------------------flecha-----------------------------------------#
            flechaimage = tk.PhotoImage(file="selection.png")
            canvas.FS = flechaimage
            flecha = canvas.create_image(0, 0, image=flechaimage, anchor="nw", tags="selectornivE")
            canvas.itemconfig(flecha, state="hidden")
 
            #---------------panel--------------#
            panelimage = tk.PhotoImage(file="bar.png")
            canvas.panel = panelimage
            canvas.create_image(0, 0, image=panelimage, anchor="nw", tags="selectorniv")
 
            #-------------------menu--------------------#
            botonmenu = tk.Button(ventana, text="menu", bg="yellow", command=menu)
            canvas.create_window(800, 30, window=botonmenu, tags="selectorniv")
 
        if not ya_cargo:
            ventana.after(150, cargar)
            ya_cargo = True
 
    #------------------------------------------------------------#
    #  ABOUT
    #------------------------------------------------------------#
    def aboutf():
        canvas.itemconfig(About, image=AboutPImage)
        ventana.after(150, lambda: canvas.itemconfig(About, image=AboutImage))
 
    def salir(event):
        ventana.destroy()
 
    #------------------------------------------------------------#
    #  VENTANA PRINCIPAL
    #------------------------------------------------------------#
    ventana = tk.Tk()
    ventana.geometry("1024x576")
    ventana.resizable(False, False)
    ventana.bind("<Escape>", salir)
 
    canvas = tk.Canvas(ventana, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)
    ya_cargo = False
 
    bg1 = tk.PhotoImage(file="Bg1.png");     canvas.bg1 = bg1
    bg2 = tk.PhotoImage(file="Levels1.png"); canvas.bg2 = bg2
    bg3 = tk.PhotoImage(file="Levels2.png"); canvas.bg3 = bg3
    bg  = canvas.create_image(0, 0, image=bg1, anchor="nw")
 
    botonstartImage  = tk.PhotoImage(file="BotonStart.png");  canvas.bs  = botonstartImage
    botonstartPImage = tk.PhotoImage(file="BotonStartP.png"); canvas.bsP = botonstartPImage
    botonstart = canvas.create_image(380, 300, image=botonstartImage, anchor="nw", tags="inicio")
    canvas.tag_bind(botonstart, "<Button-1>", lambda e: inicio())
 
    AboutImage  = tk.PhotoImage(file="About.png");  canvas.Ab  = AboutImage
    AboutPImage = tk.PhotoImage(file="AboutP.png"); canvas.AbP = AboutPImage
    About = canvas.create_image(380, 450, image=AboutImage, anchor="nw", tags="inicio")
    canvas.tag_bind(About, "<Button-1>", lambda e: aboutf())
 
    ventana.mainloop()
