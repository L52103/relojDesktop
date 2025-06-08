import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
from supabase import create_client
import pandas as pd
from fpdf import FPDF

# --- Configura tu Supabase ---
SUPABASE_URL = "https://qubqttdztpvwuzismrpa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF1YnF0dGR6dHB2d3V6aXNtcnBhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk0MTE0OTksImV4cCI6MjA2NDk4NzQ5OX0.UKMk_TyQBWuOC561pO1xOaacakBGM0gSDhwC7gL3xNc"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Funciones exportar ---
def exportar_excel(datos, archivo="datos.xlsx"):
    df = pd.DataFrame(datos)
    df.to_excel(archivo, index=False)

def exportar_pdf(datos, archivo="datos.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Listado", ln=True, align='C')
    for item in datos:
        linea = ", ".join([f"{k}: {v}" for k, v in item.items()])
        pdf.cell(200, 10, txt=linea, ln=True, align='L')
    pdf.output(archivo)

# --- Función para mostrar datos en ventana ---
def mostrar_datos(titulo, datos):
    ventana = ttk.Toplevel(app)
    ventana.title(titulo)
    ventana.geometry("700x400")

    if not datos:
        messagebox.showinfo("Info", "No hay datos para mostrar.")
        return

    cols = list(datos[0].keys())
    tree = ttk.Treeview(ventana, columns=cols, show='headings')
    tree.pack(expand=True, fill='both')

    for c in cols:
        tree.heading(c, text=c)

    for fila in datos:
        tree.insert("", "end", values=[fila[c] for c in cols])

# --- Trabajadores ---
def añadir_trabajador():
    ventana = ttk.Toplevel(app)
    ventana.title("Añadir Trabajador")
    ventana.geometry("300x250")

    labels = ["Nombre", "RUT", "Biometría Huella"]
    entries = {}

    for i, texto in enumerate(labels):
        ttk.Label(ventana, text=texto).grid(row=i, column=0, sticky='w', padx=5, pady=5)
        e = ttk.Entry(ventana)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[texto] = e

    def guardar():
        datos = {
            "nombre": entries["Nombre"].get(),
            "rut": entries["RUT"].get(),
            "biometria_huella": entries["Biometría Huella"].get(),
        }
        if not datos["nombre"] or not datos["rut"]:
            messagebox.showwarning("Aviso", "Nombre y RUT son obligatorios.")
            return

        try:
            supabase.table("trabajador").insert(datos).execute()
            messagebox.showinfo("Éxito", "Trabajador agregado.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(ventana, text="Guardar", command=guardar).grid(row=len(labels), column=0, columnspan=2, pady=10)

def quitar_trabajador():
    rut = simpledialog.askstring("Eliminar Trabajador", "Ingrese RUT del trabajador a eliminar:")
    if not rut:
        return
    confirm = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al trabajador con RUT {rut}?")
    if not confirm:
        return

    try:
        response = supabase.table("trabajador").select("id").eq("rut", rut).execute()
        data = response.data
        if not data:
            messagebox.showinfo("Info", "No se encontró trabajador con ese RUT.")
            return
        trabajador_id = data[0]['id']
        supabase.table("trabajador").delete().eq("id", trabajador_id).execute()
        messagebox.showinfo("Éxito", "Trabajador eliminado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def lista_trabajadores():
    try:
        response = supabase.table("trabajador").select("*").execute()
        datos = response.data
        mostrar_datos("Lista de Trabajadores", datos)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def lista_sucursales():
    try:
        response = supabase.table("sucursal").select("*").execute()
        datos = response.data
        mostrar_datos("Lista de Sucursales", datos)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def historial_ticket():
    try:
        response = supabase.table("asistencia").select("*").execute()
        datos = response.data
        mostrar_datos("Historial de asistencias", datos)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def gestion_turnos():
    ventana = ttk.Toplevel(app)
    ventana.title("Gestión de Turnos")
    ventana.geometry("400x400")

    def crear_turno():
        c = ttk.Toplevel(ventana)
        c.title("Crear Turno")
        c.geometry("300x250")

        labels = ["Horario Inicio (HH:MM:SS)", "Horario Fin (HH:MM:SS)", "Tipo Turno", "ID Área Trabajo"]
        entries = {}

        for i, texto in enumerate(labels):
            ttk.Label(c, text=texto).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            e = ttk.Entry(c)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries[texto] = e

        def guardar():
            datos = {
                "horario_inicio": entries[labels[0]].get(),
                "horario_fin": entries[labels[1]].get(),
                "tipo_turno": entries[labels[2]].get(),
                "area_id": int(entries[labels[3]].get()) if entries[labels[3]].get().isdigit() else None
            }
            if not all([datos["horario_inicio"], datos["horario_fin"], datos["tipo_turno"], datos["area_id"]]):
                messagebox.showwarning("Aviso", "Todos los campos son obligatorios y área debe ser número.")
                return
            try:
                supabase.table("turno").insert(datos).execute()
                messagebox.showinfo("Éxito", "Turno creado.")
                c.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(c, text="Guardar", command=guardar).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def listar_turnos():
        try:
            response = supabase.table("turno").select("*").execute()
            datos = response.data
            mostrar_datos("Lista de Turnos", datos)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_turno():
        turno_id = simpledialog.askinteger("Eliminar Turno", "Ingrese ID del turno a eliminar:")
        if turno_id is None:
            return
        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el turno con ID {turno_id}?")
        if not confirm:
            return
        try:
            supabase.table("turno").delete().eq("id", turno_id).execute()
            messagebox.showinfo("Éxito", "Turno eliminado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_turno():
        turno_id = simpledialog.askinteger("Editar Turno", "Ingrese ID del turno a editar:")
        if turno_id is None:
            return
        try:
            response = supabase.table("turno").select("*").eq("id", turno_id).execute()
            datos = response.data
            if not datos:
                messagebox.showinfo("Info", "No se encontró turno con ese ID.")
                return
            turno = datos[0]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        e = ttk.Toplevel(ventana)
        e.title("Editar Turno")
        e.geometry("300x250")

        labels = ["Horario Inicio (HH:MM:SS)", "Horario Fin (HH:MM:SS)", "Tipo Turno", "ID Área Trabajo"]
        entries = {}

        valores_iniciales = [
            turno.get("horario_inicio", ""),
            turno.get("horario_fin", ""),
            turno.get("tipo_turno", ""),
            str(turno.get("area_id", ""))
        ]

        for i, texto in enumerate(labels):
            ttk.Label(e, text=texto).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            ent = ttk.Entry(e)
            ent.grid(row=i, column=1, padx=5, pady=5)
            ent.insert(0, valores_iniciales[i])
            entries[texto] = ent

        def guardar_cambios():
            datos_editados = {
                "horario_inicio": entries[labels[0]].get(),
                "horario_fin": entries[labels[1]].get(),
                "tipo_turno": entries[labels[2]].get(),
                "area_id": int(entries[labels[3]].get()) if entries[labels[3]].get().isdigit() else None
            }
            if not all([datos_editados["horario_inicio"], datos_editados["horario_fin"], datos_editados["tipo_turno"], datos_editados["area_id"]]):
                messagebox.showwarning("Aviso", "Todos los campos son obligatorios y área debe ser número.")
                return
            try:
                supabase.table("turno").update(datos_editados).eq("id", turno_id).execute()
                messagebox.showinfo("Éxito", "Turno actualizado.")
                e.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(e, text="Guardar Cambios", command=guardar_cambios).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def asignar_turno():
        a = ttk.Toplevel(ventana)
        a.title("Asignar Turno a Trabajador")
        a.geometry("300x200")

        ttk.Label(a, text="ID Trabajador:").grid(row=0, column=0, padx=5, pady=5)
        id_trabajador = ttk.Entry(a)
        id_trabajador.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(a, text="ID Turno:").grid(row=1, column=0, padx=5, pady=5)
        id_turno = ttk.Entry(a)
        id_turno.grid(row=1, column=1, padx=5, pady=5)

        def asignar():
            try:
                tid = int(id_trabajador.get())
                tuid = int(id_turno.get())
            except:
                messagebox.showwarning("Aviso", "IDs deben ser números enteros.")
                return
            datos = {
                "trabajador_id": tid,
                "turno_id": tuid,
            }
            try:
                supabase.table("asignacion_turnos").insert(datos).execute()
                messagebox.showinfo("Éxito", "Turno asignado.")
                a.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(a, text="Asignar", command=asignar).grid(row=2, column=0, columnspan=2, pady=10)

    ttk.Button(ventana, text="Crear Turno", command=crear_turno).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Listar Turnos", command=listar_turnos).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Editar Turno", command=editar_turno).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Eliminar Turno", command=eliminar_turno).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Asignar Turno a Trabajador", command=asignar_turno).pack(pady=5, fill=X, padx=10)

def salir():
    app.destroy()

# --- Ventana principal ---
app = ttk.Window(themename="darkly")  # Tema oscuro moderno, cambia "darkly" si quieres otro
app.title("Sistema de Control")
app.geometry("600x450")

ttk.Label(app, text="Sistema de Gestión de Trabajadores", font=("Helvetica", 18)).pack(pady=15)

botones = [
    ("Añadir Trabajador", añadir_trabajador),
    ("Quitar Trabajador", quitar_trabajador),
    ("Lista Trabajadores", lista_trabajadores),
    ("Lista Sucursales", lista_sucursales),
    ("Historial Ticket", historial_ticket),
    ("Gestión Turnos", gestion_turnos),
    ("Salir", salir)
]

for texto, comando in botones:
    ttk.Button(app, text=texto, command=comando).pack(pady=5, fill=X, padx=50)

app.mainloop()
