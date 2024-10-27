import tkinter as tk

def abrir_janela():
    root = tk.Tk()
    root.title("Teste Tkinter")
    root.geometry("300x200")
    
    label = tk.Label(root, text="Janela aberta com sucesso!")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    abrir_janela()
