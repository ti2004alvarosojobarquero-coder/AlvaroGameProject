import tkinter as tk
import game as g
#llamada para iniciar el juego
def iniciar_interfaz():
    #cuando apretas start
    def inicio():
        ventana.config(bg="red")
        boton.destroy()   
    def salir(event):
        ventana.destroy()


    #ventana principal
    ventana = tk.Tk()
    ventana.attributes("-fullscreen", True)
    ventana.bind("<Escape>", salir)
    ventana.config(bg="blue")
    ventana.title("cerote war")
    
    #boton de start
    boton = tk.Button(ventana, text="start", bg="green", command= inicio)
    boton.pack()

    ventana.mainloop()

