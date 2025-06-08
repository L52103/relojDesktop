import pandas as pd
from fpdf import FPDF

def exportar_excel(datos, archivo="asistencia.xlsx"):
    df = pd.DataFrame(datos)
    df.to_excel(archivo, index=False)

def exportar_pdf(datos, archivo="asistencia.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Listado de Asistencia", ln=True, align='C')
    
    for item in datos:
        linea = ", ".join([f"{k}: {v}" for k, v in item.items()])
        pdf.cell(200, 10, txt=linea, ln=True, align='L')

    pdf.output(archivo)
