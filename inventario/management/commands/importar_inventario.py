import csv
from django.core.management.base import BaseCommand
from inventario.models import Producto

class Command(BaseCommand):
    help = 'Importar datos de inventario desde un archivo CSV'

    def handle(self, *args, **kwargs):
        archivo_csv = r'C:\Users\PC\OneDrive\Aaa-PROGRAMAS\LaDoPro\inventario_lab\inventario.csv'

        try:
            with open(archivo_csv, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for fila in reader:
                    producto = Producto(
                        nombre=fila['equipo_instrumento'] if fila['equipo_instrumento'] != 'N/A' else None,
                        marca=fila['marca_fabricante'] if fila['marca_fabricante'] != 'N/A' else None,
                        modelo=fila['modelo'] if fila['modelo'] != 'N/A' else None,
                        numero_serie=fila['nro_serie'] if fila['nro_serie'] != 'N/A' else None,
                        objetivo_uso=fila['objeto_uso'] if fila['objeto_uso'] != 'N/A' else None,
                        cantidad=int(fila['cantidad']) if fila['cantidad'].isdigit() else 0,
                        estado=fila['estado'] if fila['estado'] != 'N/A' else None,
                        clasificacion_riesgo=fila['clasificacion_riesgo'] if fila['clasificacion_riesgo'] != 'N/A' else None,
                        mantenimiento_calibracion=fila['mantenimiento_calibracion'] if fila['mantenimiento_calibracion'] != 'N/A' else None,  # Asegúrate de este nombre
                        fecha_adquisicion=fila['fecha_adquisicion'] if fila['fecha_adquisicion'] else None,
                        informacion_adicional=fila['informacion_adicional'] if fila['informacion_adicional'] else None,
                    )

                    producto.save()

            self.stdout.write(self.style.SUCCESS('Datos de inventario importados correctamente.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('Error: El archivo no se encontró.'))
        except ValueError as ve:
            self.stderr.write(self.style.ERROR(f'Error de valor: {ve}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocurrió un error: {e}'))
