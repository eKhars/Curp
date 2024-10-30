import tkinter as tk
from tkinter import ttk, messagebox
import random
import re
from datetime import datetime
from calendar import monthrange

class DateValidator:
    @staticmethod
    def is_leap_year(year):
        year = int(year)
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    @staticmethod
    def get_days_in_month(year, month):
        year = 2000 + int(year) if int(year) < 50 else 1900 + int(year)
        month = int(month)
        return monthrange(year, month)[1]

    @staticmethod
    def validate_date(year, month, day):
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            
            if month < 1 or month > 12:
                return False, "Mes inválido"
            
            year_full = 2000 + year if year < 50 else 1900 + year
            days_in_month = monthrange(year_full, month)[1]
            
            if day < 1 or day > days_in_month:
                if month == 2:
                    if DateValidator.is_leap_year(year_full):
                        return False, "Febrero en año bisiesto solo tiene 29 días"
                    else:
                        return False, "Febrero en año no bisiesto solo tiene 28 días"
                elif day > 30:
                    if month in [4, 6, 9, 11]:  # Meses con 30 días
                        return False, f"El mes {month} solo tiene 30 días"
                    else:
                        return False, f"El mes {month} tiene 31 días"
                else:
                    return False, "Día inválido"
                    
            return True, "Fecha válida"
            
        except ValueError:
            return False, "Fecha inválida"

class CURPGenerator:
    def __init__(self):
        self.ESTADOS = {
            'AGUASCALIENTES': 'AG', 'BAJA CALIFORNIA': 'BC', 'BAJA CALIFORNIA SUR': 'BS',
            'CAMPECHE': 'CC', 'COAHUILA': 'CL', 'COLIMA': 'CM', 'CHIAPAS': 'CS',
            'CHIHUAHUA': 'CH', 'CIUDAD DE MEXICO': 'DF', 'DURANGO': 'DG',
            'GUANAJUATO': 'GT', 'GUERRERO': 'GR', 'HIDALGO': 'HG', 'JALISCO': 'JC',
            'MEXICO': 'MC', 'MICHOACAN': 'MN', 'MORELOS': 'MS', 'NAYARIT': 'NT',
            'NUEVO LEON': 'NL', 'OAXACA': 'OC', 'PUEBLA': 'PL', 'QUERETARO': 'QT',
            'QUINTANA ROO': 'QR', 'SAN LUIS POTOSI': 'SP', 'SINALOA': 'SL',
            'SONORA': 'SR', 'TABASCO': 'TC', 'TAMAULIPAS': 'TS', 'TLAXCALA': 'TL',
            'VERACRUZ': 'VZ', 'YUCATAN': 'YN', 'ZACATECAS': 'ZS'
        }
        self.NOMBRES_COMUNES = ['JOSE', 'MARIA', 'JOSE MARIA', 'MA', 'MA.', 'J', 'J.']

    def get_vocales(self, texto):
        vocales = re.findall(r'[AEIOUÁÉÍÓÚ]', texto)
        return vocales[0] if vocales else 'X'

    def get_consonantes(self, texto):
        consonantes = re.findall(r'[BCDFGHJKLMNÑPQRSTVWXYZ]', texto)
        if len(consonantes) > 1:
            return consonantes[0]
        return 'X'

    def generar_curp(self, nombres, apellido1, apellido2, fecha_nac, sexo, estado):
        nombres = nombres.split()
        curp = ""
        
        if nombres[0] in self.NOMBRES_COMUNES and len(nombres) > 1:
            nombre_usado = nombres[1]
        else:
            nombre_usado = nombres[0]

        curp += apellido1[0]
        vocal = self.get_vocales(apellido1[1:])
        curp += vocal
        curp += apellido2[0]
        curp += nombre_usado[0]
        curp += fecha_nac
        curp += sexo
        curp += self.ESTADOS[estado]
        curp += self.get_consonantes(apellido1[1:])
        curp += self.get_consonantes(apellido2[1:])
        curp += self.get_consonantes(nombre_usado[1:])
        curp += str(random.randint(0, 9))
        curp += random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        return curp

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            relief=tk.FLAT,
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            activebackground='#1976D2',
            activeforeground='white'
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.configure(background='#1976D2')

    def on_leave(self, e):
        self.configure(background='#2196F3')

class CURPGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de CURP - Máquina de Turing")
        self.root.geometry("900x700")
        self.root.configure(bg='#F5F5F5')
        self.generator = CURPGenerator()
        self.date_validator = DateValidator()
        self.setup_ui()

    def setup_ui(self):
        self.configure_styles()
        
        main_container = tk.Frame(self.root, bg='#F5F5F5')
        main_container.pack(expand=True, fill='both', padx=40, pady=30)
        
        self.create_header(main_container)
        
        content_container = tk.Frame(main_container, bg='#F5F5F5')
        content_container.pack(fill='both', expand=True, pady=20)
        
        form_frame = tk.Frame(content_container, bg='white', bd=1, relief=tk.SOLID)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.create_form(form_frame)
        
        self.create_result_frame(main_container)

    def configure_styles(self):
        style = ttk.Style()
        style.configure('Custom.TEntry', padding=5)
        style.configure('Custom.TCombobox', padding=5)
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), background='#F5F5F5')
        style.configure('Subtitle.TLabel', font=('Arial', 12), background='#F5F5F5', foreground='#666666')
        style.configure('Field.TLabel', font=('Arial', 11), background='white', padding=5)

    def create_header(self, container):
        header_frame = tk.Frame(container, bg='#F5F5F5')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text="Generador de CURP",
            style='Title.TLabel'
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Ingrese los datos para generar la CURP",
            style='Subtitle.TLabel'
        )
        subtitle.pack()

    def create_form(self, container):
        form_padding = tk.Frame(container, bg='white')
        form_padding.pack(fill='both', expand=True, padx=30, pady=20)
        
        self.create_form_field(form_padding, "Nombre(s):", 'nombres', 0)
        self.create_form_field(form_padding, "Primer Apellido:", 'apellido1', 1)
        self.create_form_field(form_padding, "Segundo Apellido:", 'apellido2', 2)
        
        date_frame = tk.Frame(form_padding, bg='white')
        date_frame.grid(row=3, column=0, columnspan=2, sticky='w', pady=10)
        
        ttk.Label(date_frame, text="Fecha de Nacimiento:", style='Field.TLabel').pack(side='left')
        
        self.dia = ttk.Combobox(date_frame, width=5, values=[f"{i:02d}" for i in range(1, 32)])
        self.dia.pack(side='left', padx=5)
        
        self.mes = ttk.Combobox(date_frame, width=5, values=[f"{i:02d}" for i in range(1, 13)])
        self.mes.pack(side='left', padx=5)
        
        self.anio = ttk.Entry(date_frame, width=8)
        self.anio.pack(side='left', padx=5)
        
        self.create_combobox_field(form_padding, "Sexo:", 'sexo', ['HOMBRE', 'MUJER'], 4)
        self.create_combobox_field(form_padding, "Estado:", 'estado', 
                                 sorted(self.generator.ESTADOS.keys()), 5)
        
        generate_frame = tk.Frame(form_padding, bg='white')
        generate_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ModernButton(
            generate_frame,
            text="Generar CURP",
            command=self.generar_curp
        ).pack()

    def create_form_field(self, container, label_text, field_name, row):
        ttk.Label(
            container,
            text=label_text,
            style='Field.TLabel'
        ).grid(row=row, column=0, sticky='w', pady=5)
        
        entry = ttk.Entry(container, width=40, style='Custom.TEntry')
        entry.grid(row=row, column=1, sticky='w', padx=10)
        setattr(self, field_name, entry)

    def create_combobox_field(self, container, label_text, field_name, values, row):
        ttk.Label(
            container,
            text=label_text,
            style='Field.TLabel'
        ).grid(row=row, column=0, sticky='w', pady=5)
        
        combo = ttk.Combobox(container, width=38, values=values, style='Custom.TCombobox')
        combo.grid(row=row, column=1, sticky='w', padx=10)
        setattr(self, field_name, combo)

    def create_result_frame(self, container):
        result_frame = tk.Frame(container, bg='white', bd=1, relief=tk.SOLID)
        result_frame.pack(fill='x', padx=20, pady=10)
        
        result_padding = tk.Frame(result_frame, bg='white')
        result_padding.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(
            result_padding,
            text="CURP Generada:",
            style='Field.TLabel'
        ).pack(side='left')
        
        self.resultado = ttk.Entry(
            result_padding,
            width=30,
            font=('Arial', 14),
            style='Custom.TEntry'
        )
        self.resultado.pack(side='left', padx=10)

    def validate_date(self):
        try:
            year = self.anio.get()[-2:]
            month = self.mes.get()
            day = self.dia.get()
            
            if not all([year, month, day]):
                return False, "Todos los campos de fecha son requeridos"
                
            is_valid, message = DateValidator.validate_date(year, month, day)
            
            if not is_valid:
                messagebox.showerror("Error", message)
                return False, message
                
            return True, "Fecha válida"
            
        except Exception as e:
            return False, f"Error en la fecha: {str(e)}"

    def generar_curp(self):
        try:
            is_valid_date, date_message = self.validate_date()
            if not is_valid_date:
                messagebox.showerror("Error", date_message)
                return

            campos_requeridos = {
                'nombres': "Nombre(s)",
                'apellido1': "Primer Apellido",
                'apellido2': "Segundo Apellido",
                'sexo': "Sexo",
                'estado': "Estado"
            }
            
            for campo, nombre in campos_requeridos.items():
                if not getattr(self, campo).get().strip():
                    messagebox.showerror("Error", f"El campo {nombre} es obligatorio")
                    return
            
            fecha = f"{self.anio.get()[-2:]}{self.mes.get()}{self.dia.get()}"
            
            curp = self.generator.generar_curp(
                self.nombres.get().upper(),
                self.apellido1.get().upper(),
                self.apellido2.get().upper(),
                fecha,
                'H' if self.sexo.get() == 'HOMBRE' else 'M',
                self.estado.get()
            )
            
            self.resultado.delete(0, tk.END)
            self.resultado.insert(0, curp)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar CURP: {str(e)}")

def main():
    root = tk.Tk()
    app = CURPGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()