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

    boton_exportar_excel = ttk.Button(ventana, text="Exportar a Excel", command=lambda: exportar_excel(datos))
    boton_exportar_excel.pack(side='left', padx=10, pady=10)

    boton_exportar_pdf = ttk.Button(ventana, text="Exportar a PDF", command=lambda: exportar_pdf(datos))
    boton_exportar_pdf.pack(side='left', padx=10, pady=10)

# --- Lista Sucursal ---
def lista_sucursales():
    try:
        response = supabase.table("sucursal").select("*").execute()
        datos = response.data
        mostrar_datos("Lista de Sucursales", datos)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Gestión de Sucursales (Añadir y Eliminar) ---
def gestion_sucursales():
    ventana = ttk.Toplevel(app)
    ventana.title("Gestión de Sucursales")
    ventana.geometry("400x300")


    def añadir_sucursal():
        try:
            nombre = simpledialog.askstring("Nombre Sucursal", "Ingrese el nombre de la sucursal:")
            if not nombre:
                raise ValueError("El nombre de la sucursal es obligatorio.")

            direccion = simpledialog.askstring("Dirección Sucursal", "Ingrese la dirección de la sucursal:")
            if not direccion:
                raise ValueError("La dirección de la sucursal es obligatoria.")

            data = {
                "nombre": nombre,
                "direccion": direccion
            }

            response = supabase.table("sucursal").insert(data).execute()
            if response.data:
                messagebox.showinfo("Éxito", "Sucursal añadida correctamente.")
            else:
                raise Exception("No se pudo añadir la sucursal.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_sucursal():
        try:
            id_sucursal = simpledialog.askinteger("Eliminar Sucursal", "Ingrese el ID de la sucursal a eliminar:")
            if id_sucursal is None:
                raise ValueError("Debe ingresar un ID válido.")

            # Verificar si la sucursal existe
            response = supabase.table("sucursal").select("*").eq("id", id_sucursal).execute()
            if not response.data:
                raise Exception("No se encontró ninguna sucursal con ese ID.")

            eliminar = supabase.table("sucursal").delete().eq("id", id_sucursal).execute()
            if eliminar.data:
                messagebox.showinfo("Éxito", "Sucursal eliminada correctamente.")
            else:
                raise Exception("No se pudo eliminar la sucursal.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(ventana, text="Añadir Sucursal", command=añadir_sucursal).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Eliminar Sucursal", command=eliminar_sucursal).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Listar Sucursales", command=lista_sucursales).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Administrar Áreas de Trabajo", command=administrar_areas_trabajo).pack(pady=5, fill=X, padx=10)



def administrar_areas_trabajo():
    ventana = ttk.Toplevel(app)
    ventana.title("Administrar Áreas de Trabajo")
    ventana.geometry("400x300")


    def añadir_area():
        try:
            nombre = simpledialog.askstring("Nombre Área", "Ingrese el nombre del área:")
            if not nombre:
                raise ValueError("El nombre es obligatorio.")

            sucursal_id = simpledialog.askinteger("ID Sucursal", "Ingrese el ID de la sucursal:")
            if not sucursal_id:
                raise ValueError("El ID de sucursal es obligatorio.")

            data = {"nombre": nombre, "sucursal_id": sucursal_id}
            response = supabase.table("areatrabajo").insert(data).execute()

            if response.data:
                messagebox.showinfo("Éxito", "Área añadida correctamente.")
            else:
                raise Exception("No se pudo añadir el área.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_area():
        try:
            area_id = simpledialog.askinteger("Editar Área", "Ingrese el ID del área:")
            if not area_id:
                raise ValueError("Debe ingresar un ID válido.")

            response = supabase.table("areatrabajo").select("*").eq("id", area_id).execute()
            if not response.data:
                raise Exception("No se encontró el área.")

            actual = response.data[0]
            nuevo_nombre = simpledialog.askstring("Nuevo Nombre", f"Nombre actual: {actual['nombre']}") or actual['nombre']
            nueva_sucursal_id = simpledialog.askinteger("Nuevo ID Sucursal", f"Sucursal actual: {actual['sucursal_id']}") or actual['sucursal_id']

            data = {"nombre": nuevo_nombre, "sucursal_id": nueva_sucursal_id}
            response = supabase.table("areatrabajo").update(data).eq("id", area_id).execute()

            if response.data:
                messagebox.showinfo("Éxito", "Área actualizada correctamente.")
            else:
                raise Exception("No se pudo actualizar el área.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_area():
        try:
            area_id = simpledialog.askinteger("Eliminar Área", "Ingrese el ID del área:")
            if not area_id:
                raise ValueError("Debe ingresar un ID válido.")

            response = supabase.table("areatrabajo").delete().eq("id", area_id).execute()
            if response.data:
                messagebox.showinfo("Éxito", "Área eliminada correctamente.")
            else:
                raise Exception("No se pudo eliminar el área.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def listar_areas():
        try:
            response = supabase.table("areatrabajo").select("*").execute()
            datos = response.data

            if not datos:
                messagebox.showinfo("Sin datos", "No hay áreas registradas.")
                return

            datos_formateados = []
            for area in datos:
                datos_formateados.append({
                    "ID": area.get("id", "N/A"),
                    "Nombre": area.get("nombre", "N/A"),
                    "Sucursal ID": area.get("sucursal_id", "N/A")
                })

            mostrar_datos("Lista de Áreas de Trabajo", datos_formateados)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(ventana, text="Añadir Área", command=añadir_area).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Editar Área", command=editar_area).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Eliminar Área", command=eliminar_area).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Listar Área", command=listar_areas).pack(pady=5, fill=X, padx=10)


# --- Gestión de Turnos ---
def gestion_turnos():
    ventana = ttk.Toplevel(app)
    ventana.title("Gestión de Turnos")
    ventana.geometry("400x400")

    def crear_turno():
        try:
            horario_inicio = simpledialog.askstring("Horario Inicio", "Ingrese el horario de inicio (HH:MM):")
            horario_fin = simpledialog.askstring("Horario Fin", "Ingrese el horario de fin (HH:MM):")
            tipo_turno = simpledialog.askstring("Tipo de Turno", "Ingrese el tipo de turno:")
            area_id = simpledialog.askinteger("Área ID", "Ingrese el ID del área de trabajo:")

            if not all([horario_inicio, horario_fin, tipo_turno, area_id]):
                raise ValueError("Todos los campos son obligatorios.")

            data = {
                "horario_inicio": horario_inicio,
                "horario_fin": horario_fin,
                "tipo_turno": tipo_turno,
                "area_id": area_id
            }
            response = supabase.table("turno").insert(data).execute()

            if response.data:
                messagebox.showinfo("Éxito", "Turno añadido correctamente.")
            else:
                raise Exception("No se pudo añadir el turno.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

  
    def listar_turnos():
        try:
            response = supabase.table("turno").select("*").execute()
            datos = response.data

            if not datos:
                messagebox.showinfo("Sin datos", "No hay turnos registrados.")
                return

            datos_formateados = []
            for t in datos:
                datos_formateados.append({
                    "ID": t.get("id", "N/A"),
                    "Horario Inicio": t.get("horario_inicio", "N/A"),
                    "Horario Fin": t.get("horario_fin", "N/A"),
                    "Tipo Turno": t.get("tipo_turno", "N/A"),
                    "Área ID": t.get("area_id", "N/A")
                })

            mostrar_datos("Lista de Turnos", datos_formateados)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_turno():
        try:
            turno_id = simpledialog.askinteger("Editar Turno", "Ingrese el ID del turno a editar:")
            if not turno_id:
                raise ValueError("Debe ingresar un ID válido.")

            # Obtener turno actual
            response = supabase.table("turno").select("*").eq("id", turno_id).execute()
            if not response.data:
                raise Exception("No se encontró el turno.")

            turno_actual = response.data[0]

            # Solicitar nuevos valores (o dejar actual)
            horario_inicio = simpledialog.askstring("Horario Inicio", f"Ingrese nuevo horario inicio ({turno_actual['horario_inicio']}):") or turno_actual['horario_inicio']
            horario_fin = simpledialog.askstring("Horario Fin", f"Ingrese nuevo horario fin ({turno_actual['horario_fin']}):") or turno_actual['horario_fin']
            tipo_turno = simpledialog.askstring("Tipo Turno", f"Ingrese nuevo tipo turno ({turno_actual['tipo_turno']}):") or turno_actual['tipo_turno']
            area_id = simpledialog.askinteger("Área ID", f"Ingrese nuevo área ID ({turno_actual['area_id']}):") or turno_actual['area_id']

            data = {
                "horario_inicio": horario_inicio,
                "horario_fin": horario_fin,
                "tipo_turno": tipo_turno,
                "area_id": area_id
            }

            response = supabase.table("turno").update(data).eq("id", turno_id).execute()

            if response.data:
                messagebox.showinfo("Éxito", "Turno editado correctamente.")
            else:
                raise Exception("No se pudo editar el turno.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_turno():
        try:
            turno_id = simpledialog.askinteger("Eliminar Turno", "Ingrese el ID del turno a eliminar:")
            if not turno_id:
                raise ValueError("Debe ingresar un ID válido.")

            confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el turno con ID {turno_id}?")
            if not confirmar:
                return

            response = supabase.table("turno").delete().eq("id", turno_id).execute()

            if response.data:
                messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
            else:
                raise Exception("No se pudo eliminar el turno.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def asignar_turno():
        pass  # Aquí va el código de asignación de turno

    ttk.Button(ventana, text="Crear Turno", command=crear_turno).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Listar Turnos", command=listar_turnos).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Editar Turno", command=editar_turno).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Eliminar Turno", command=eliminar_turno).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Asignar Turno a Trabajador", command=asignar_turno).pack(pady=5, fill=X, padx=10)

# --- Gestión de Personal ---
def gestion_personal():
    ventana = ttk.Toplevel(app)
    ventana.title("Gestión de Personal")
    ventana.geometry("400x400")

    def añadir_trabajador():
        try:
            nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del trabajador:")
            if not nombre:
                raise ValueError("Nombre es obligatorio.")

            apellido = simpledialog.askstring("Apellido", "Ingrese el apellido del trabajador:")
            if not apellido:
                raise ValueError("Apellido es obligatorio.")

            rut = simpledialog.askstring("RUT", "Ingrese el RUT del trabajador:")
            if not rut:
                raise ValueError("RUT es obligatorio.")
            
            email = simpledialog.askstring("email", "Ingrese el email del trabajador:")
            if not email:
                raise ValueError("email es obligatorio.")

            password = simpledialog.askstring("password", "Ingrese la contraseña del trabajador:")
            if not password:
                raise ValueError("La contraseña es obligatorio.") 

            id_sucursal = simpledialog.askinteger("ID Sucursal", "Ingrese el ID de la sucursal:")
            if id_sucursal is None:
                raise ValueError("ID Sucursal es obligatorio.")

            data = {
                "nombre": nombre,
                "apellido": apellido,
                "rut": rut,
                "email": email,
                "password": password,
                "sucursal_id": id_sucursal 
            }
            response = supabase.table("trabajador").insert(data).execute()

            if response.data:
                messagebox.showinfo("Éxito", "Trabajador añadido correctamente.")
            else:
                raise Exception("No se pudo añadir el trabajador.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quitar_trabajador():
        try:
            rut = simpledialog.askstring("Eliminar Trabajador", "Ingrese el RUT del trabajador a eliminar:")
            if not rut:
                raise ValueError("RUT es obligatorio.")

            response = supabase.table("personal").select("*").eq("rut", rut).execute()
            if not response.data:
                raise Exception("No se encontró ningún trabajador con ese RUT.")

            eliminar = supabase.table("personal").delete().eq("rut", rut).execute()

            if eliminar.data:
                messagebox.showinfo("Éxito", "Trabajador eliminado correctamente.")
            else:
                raise Exception("No se pudo eliminar el trabajador.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def lista_trabajadores():
        try:
            response = supabase.table("trabajador").select("*").execute()
            datos = response.data
            mostrar_datos("Lista de Trabajadores", datos)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def historial_ticket():
        try:
            # Consultar todos los tickets junto con la información del trabajador
            response = supabase.table("ticket").select("fecha, personal(nombre, apellido, rut)").execute()

            datos = response.data
            if not datos:
                messagebox.showinfo("Sin datos", "No hay tickets registrados.")
                return

            # Formatear datos a mostrar
            datos_formateados = []
            for t in datos:
                trabajador = t.get("personal", {})
                nombre_completo = f"{trabajador.get('nombre', 'N/A')} {trabajador.get('apellido', 'N/A')}"
                rut = trabajador.get('rut', 'N/A')

                datos_formateados.append({
                    "Nombre": nombre_completo,
                    "RUT": rut,
                    "Fecha Entrada": t.get("fecha", "N/A")
                })

            # Mostrar en ventana
            mostrar_datos("Historial de Tickets de Todos los Trabajadores", datos_formateados)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(ventana, text="Añadir Trabajador", command=añadir_trabajador).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Quitar Trabajador", command=quitar_trabajador).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Lista Trabajadores", command=lista_trabajadores).pack(pady=5, fill=X, padx=10)
    ttk.Button(ventana, text="Historial Ticket", command=historial_ticket).pack(pady=5, fill=X, padx=10)

def salir():
    app.destroy()

app = ttk.Window(themename="darkly")
app.title("Sistema de Control")
app.geometry("600x450")

ttk.Label(app, text="Sistema de Gestión de Trabajadores", font=("Helvetica", 18)).pack(pady=15)

botones = [
    ("Gestión Sucursales", gestion_sucursales),
    ("Gestión Turnos", gestion_turnos),
    ("Gestión de Personal", gestion_personal),
    ("Salir", salir)
]

for texto, comando in botones:
    ttk.Button(app, text=texto, command=comando).pack(pady=5, fill=X, padx=50)

app.mainloop()
