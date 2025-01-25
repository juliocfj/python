import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

# Configuração do Banco de Dados
def init_db():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()

    # Criar tabela de agendamentos
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        date TEXT,
                        time TEXT)''')

    # Criar tabela de dentistas
    cursor.execute('''CREATE TABLE IF NOT EXISTS dentist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    # Inserir dentista padrão, caso não exista
    cursor.execute('''INSERT OR IGNORE INTO dentist (username, password) VALUES (?, ?)''', ("admin", "1234"))

    conn.commit()
    conn.close()

# Função para salvar agendamento
def save_appointment(name, date, time):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()

# Função para verificar login de dentista
def verify_login(username, password):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dentist WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Função para exibir agendamentos
def show_appointments():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    conn.close()

    appointments_window = tk.Toplevel()
    appointments_window.title("Agendamentos")

    for appointment in appointments:
        appointment_label = tk.Label(appointments_window, text=f"Nome: {appointment[1]}, Data: {appointment[2]}, Hora: {appointment[3]}")
        appointment_label.pack()

# Função para a tela inicial (home)
def show_home_page():
    root = tk.Tk()
    root.title("Consulta Dentista")

    # Definindo o fundo da tela
    bg_image = Image.open("bg.webp")
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Criando o Canvas para a imagem de fundo
    canvas = tk.Canvas(root, width=bg_photo.width(), height=bg_photo.height())
    canvas.pack(fill="both", expand=True)

    # Adicionando a imagem de fundo
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

    # Criando o frame onde vamos colocar os widgets
    frame = tk.Frame(root, bg="white", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Função para abrir a tela de agendamento
    def open_appointment_page():
        appointment_window = tk.Toplevel()
        appointment_window.title("Agendar Consulta")

        # Campos de entrada para o nome, data e hora
        tk.Label(appointment_window, text="Nome:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        name_entry = tk.Entry(appointment_window)
        name_entry.pack()

        tk.Label(appointment_window, text="Data:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        date_entry = tk.Entry(appointment_window)
        date_entry.pack()

        tk.Label(appointment_window, text="Hora:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        time_entry = tk.Entry(appointment_window)
        time_entry.pack()

        # Função para salvar o agendamento
        def submit_appointment():
            name = name_entry.get()
            date = date_entry.get()
            time = time_entry.get()

            if name and date and time:
                save_appointment(name, date, time)
                messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
                appointment_window.destroy()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

        # Botão para salvar agendamento
        tk.Button(appointment_window, text="Agendar", command=submit_appointment).pack()

    # Função para abrir tela de login de dentista
    def open_login_page():
        login_window = tk.Toplevel()
        login_window.title("Login Dentista")

        tk.Label(login_window, text="Usuário:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack()

        tk.Label(login_window, text="Senha:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack()

        # Função de login
        def login():
            username = username_entry.get()
            password = password_entry.get()
            if verify_login(username, password):
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                login_window.destroy()
                show_appointments()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")

        # Botão de login
        tk.Button(login_window, text="Login", command=login).pack()

    # Função para abrir a tela de cadastro de dentista
    def open_register_page():
        register_window = tk.Toplevel()
        register_window.title("Cadastro de Dentista")

        tk.Label(register_window, text="Nome de Usuário:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        username_entry = tk.Entry(register_window)
        username_entry.pack()

        tk.Label(register_window, text="Senha:", font=("Arial", 12, "bold"), fg="#B76E79").pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()

        # Função para registrar o dentista
        def register():
            username = username_entry.get()
            password = password_entry.get()

            conn = sqlite3.connect("appointments.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO dentist (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dentista cadastrado com sucesso!")
                register_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Nome de usuário já existe.")
            finally:
                conn.close()

        # Botão de cadastro
        tk.Button(register_window, text="Cadastrar", command=register).pack()

    # Botões para as diferentes funcionalidades
    tk.Button(frame, text="Agendar Consulta", command=open_appointment_page, font=("Arial", 12, "bold"), fg="#B76E79").pack(pady=10)
    tk.Button(frame, text="Login Dentista", command=open_login_page, font=("Arial", 12, "bold"), fg="#B76E79").pack(pady=10)
    tk.Button(frame, text="Cadastrar Dentista", command=open_register_page, font=("Arial", 12, "bold"), fg="#B76E79").pack(pady=10)

    root.mainloop()

# Inicializando o banco de dados
init_db()

# Exibindo a tela inicial
show_home_page()

