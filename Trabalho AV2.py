import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import *
import sqlite3

#__________ FRAMES - MAIN __________
root = Tk()
root.title("____ ALUNOS ____")
width = 700
height = 400
sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()
x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0,0)
root.config(bg='#0b628a')

#__________ VARIABLES __________

aluno = StringVar()
materia = StringVar()
nota = StringVar()
id = None
updateWindow = None
newWindow = None

#__________ METHODS __________


def database():
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS 'notas' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                aluno TEXT, materia TEXT, nota TEXT) """
    cursor.execute(query)
    cursor.execute("SELECT * FROM 'notas' ORDER BY aluno")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


def submitData():
    if aluno.get() == "" or materia.get() == "" or nota.get() == "":
        resultado = msb.showwarning(
            "", "Por favor, digite todos os campos.", icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("alunos.db")
        cursor = conn.cursor()
        query = """ INSERT INTO 'notas' (aluno, materia, nota) VALUES(?, ?, ?)"""
        cursor.execute(query, (str(aluno.get()), str(materia.get()), str(
            nota.get())))
        conn.commit()
        cursor.execute("SELECT * FROM 'notas' ORDER BY aluno")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        aluno.set("")
        materia.set("")
        nota.set("")
        


def updateData():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    cursor.execute(" UPDATE 'notas' SET aluno = ?, materia = ?, nota = ? WHERE id = ?",
                   (str(aluno.get()), str(materia.get()), str(nota.get())))
    conn.commit()
    cursor.execute("SELECT * FROM 'notas' ORDER BY nome")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    aluno.set("")
    materia.set("")
    nota.set("")
    updateWindow.destroy()


def onSelect(event):
    global id, updateWindow
    selectItem = tree.focus()
    conteudo = (tree.item(selectItem))
    selectedItem = conteudo['values']
    id = selectedItem[0]
    aluno.set("")
    materia.set("")
    nota.set("")
    aluno.set(selectedItem[1])
    materia.set(selectedItem[2])
    nota.set(selectedItem[3])
    #__________ FRAME - UPDATE __________
    updateWindow = Toplevel()
    updateWindow.title("____ ATUALIZAR ALUNO ____")
    formTitulo = Frame(updateWindow)
    formTitulo.pack(side=TOP)
    formContato = Frame(updateWindow)
    formContato.pack(side=TOP, pady=10)
    width = 400
    height = 300
    sc_width = updateWindow.winfo_screenwidth()
    sc_height = updateWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)

    #__________ LABEL - UPDATE __________
    lbl_title = Label(formTitulo, text="Atualizar aluno",
                      font=('arial', 18),  width=280)
    lbl_title.pack(fill=X)
    lbl_nome = Label(formContato, text='Aluno', font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_telefone = Label(formContato, text='Materia', font=('arial', 12))
    lbl_telefone.grid(row=1, sticky=W)
    lbl_idade = Label(formContato, text='Nota', font=('arial', 12))
    lbl_idade.grid(row=2, sticky=W)

    #__________ ENTRY - UPDATE __________
    nomeEntry = Entry(formContato, textvariable=aluno, font=('arial', 12))
    nomeEntry.grid(row=0, column=1)
    telefoneEntry = Entry(formContato, textvariable=materia, font=('arial', 12))
    telefoneEntry.grid(row=1, column=1)
    idadeEntry = Entry(formContato, textvariable=nota, font=('arial', 12))
    idadeEntry.grid(row=2, column=1)

    #__________ BUTTON - UPDATE __________
    bttn_updatecom = Button(formContato, text="Atualizar",
                            width=50, command=updateData)
    bttn_updatecom.grid(row=6, columnspan=2, pady=10)


#__________ METHOD - DELETE __________
def deleteData():
    if not tree.selection():
        resultado = msb.showwarning(
            '', 'Para deletar, selecione um item na lista!', icon='warning')
    else:
        resultado = msb.askquestion(
            '', 'Tem certeza que deseja deletar o aluno?')
        if resultado == 'yes':
            selectItem = tree.focus()
            conteudo = (tree.item(selectItem))
            selectedItem = conteudo['values']
            tree.delete(selectItem)
            conn = sqlite3.connect("alunos.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM 'notas' WHERE id = %d" %
                           selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()


def insertData():
    global newWindow
    aluno.set("")
    materia.set("")
    nota.set("")
    #__________ FRAME - REGISTER __________
    newWindow = Toplevel()
    newWindow.title("____ INSERIR ALUNO ____")
    formTitulo = Frame(newWindow)
    formTitulo.pack(side=TOP)
    formContato = Frame(newWindow)
    formContato.pack(side=TOP, pady=10)
    width = 400
    height = 300
    sc_width = newWindow.winfo_screenwidth()
    sc_height = newWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

    #__________ LABEL - REGISTER __________
    lbl_title = Label(formTitulo, text="Inserir aluno",
                      font=('arial', 18),  width=280)
    lbl_title.pack(fill=X)
    lbl_nome = Label(formContato, text='Aluno', font=('arial', 12))
    lbl_nome.grid(row=0, sticky=W)
    lbl_telefone = Label(formContato, text='Materia', font=('arial', 12))
    lbl_telefone.grid(row=1, sticky=W)
    lbl_idade = Label(formContato, text='Nota', font=('arial', 12))
    lbl_idade.grid(row=2, sticky=W)

    #__________ ENTRY - REGISTER __________
    nomeEntry = Entry(formContato, textvariable=aluno, font=('arial', 12))
    nomeEntry.grid(row=0, column=1)
    telefoneEntry = Entry(
        formContato, textvariable=materia, font=('arial', 12))
    telefoneEntry.grid(row=1, column=1)
    idadeEntry = Entry(formContato, textvariable=nota, font=('arial', 12))
    idadeEntry.grid(row=2, column=1)

    #__________ BUTTON - REGISTER __________
    bttn_submitcom = Button(formContato, text="Cadastrar",
                            width=50, command=submitData)
    bttn_submitcom.grid(row=6, columnspan=2, pady=10)


#__________ MAIN FRAME __________
top = Frame(root, width=500, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg='#0b628a')
mid.pack(side=TOP)
midleft = Frame(mid, width=100)
midleft.pack(side=LEFT, pady=10)
midleftPadding = Frame(mid, width=350, bg="#0b628a")
midleftPadding.pack(side=LEFT)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT, pady=10)
bottom = Frame(root, width=500)
bottom.pack(side=BOTTOM)
tableMargin = Frame(root, width=500)
tableMargin.pack(side=TOP)


#__________ MAIN BUTTONS __________
bttn_add = Button(midleft, text="Adicionar Aluno",  command=insertData)
bttn_add.pack()
bttn_delete = Button(midright, text="Deletar Aluno",
                      command=deleteData)
bttn_delete.pack(side=RIGHT)

#__________ MAIN TREEVIEW __________

ScrollbarX = Scrollbar(tableMargin, orient=HORIZONTAL)
ScrollbarY = Scrollbar(tableMargin, orient=VERTICAL)

tree = ttk.Treeview(tableMargin, columns=("ID", "Aluno", "Materia", "Nota"),
                    height=400, selectmode="extended", yscrollcommand=ScrollbarY.set, xscrollcommand = ScrollbarX.set)
ScrollbarY.config(command=tree.yview)
ScrollbarY.pack(side=RIGHT, fill=Y)
ScrollbarX.config(command=tree.xview)
ScrollbarX.pack(side=BOTTOM, fill=X)
tree.heading("ID", text="ID", anchor=W)
tree.heading("Aluno", text="Aluno", anchor=W)
tree.heading("Materia", text="Materia", anchor=W)
tree.heading("Nota", text="Nota", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('#1', stretch=NO, minwidth=0, width=20)
tree.column('#2', stretch=NO, minwidth=0, width=310)
tree.column('#3', stretch=NO, minwidth=0, width=310)
tree.column('#4', stretch=NO, minwidth=0, width=34)
tree.pack()
tree.bind('<Double-Button-1>', onSelect)

#__________ MAIN MENU __________
menu_bar = Menu(root)
root.config(menu=menu_bar)

#__________ SHORTCUTS __________
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Criar novo", command=insertData)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=root.destroy)
file_menu = Menu(menu_bar, tearoff=0)


if __name__ == '__main__':
    database()
    root.mainloop()
