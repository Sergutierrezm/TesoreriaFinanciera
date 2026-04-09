import os
from tabulate import tabulate
from colorama import Fore, Back, Style, init
from app.models.tesoreria import RegistroTesoreria
from app.repositories.tesoreria_repo import TesoreriaRepository
from app.database.connection import obtener_conexion, inicializar_base_de_datos

# Inicializamos colorama para que funcione en Windows y Mac
init(autoreset=True)

# --- FUNCIONES AUXILIARES VISUALES Y DE VALIDACIÓN ---

def limpiar_pantalla():
    """Limpia la terminal para un aspecto más profesional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def solicitar_float(mensaje):
    """Solicita un número decimal y reintenta si el usuario se equivoca."""
    while True:
        entrada = input(f"{Fore.WHITE}{mensaje}")
        entrada = entrada.replace(',', '.')
        try:
            return float(entrada)
        except ValueError:
            print(f"{Fore.RED}⚠️ Error: Por favor, introduce un número válido (ej: 1200.50).")

def solicitar_int(mensaje):
    """Solicita un número entero y reintenta."""
    while True:
        try:
            return int(input(f"{Fore.WHITE}{mensaje}"))
        except ValueError:
            print(f"{Fore.RED}⚠️ Error: Por favor, introduce un número entero válido.")

def formatear_moneda(valor):
    """Añade el símbolo de Euro y separadores de miles."""
    return f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- FUNCIÓN PARA EL GRÁFICO ASCII ---

def dibujar_grafico_barras(registros):
    """Dibuja un gráfico de barras ASCII para visualizar el crecimiento."""
    if not registros:
        print(f"{Fore.YELLOW}No hay registros para graficar.")
        return

    meses_orden = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }
    
    registros_cronologicos = sorted(registros, key=lambda x: (x[1], meses_orden.get(x[2].capitalize(), 0)))
    
    max_total = max(r[5] for r in registros)
    if max_total == 0: return

    ANCHO_BARRA = 30
    
    print("\n" + Fore.CYAN + Style.BRIGHT + "--- 📊 GRÁFICO DE EVOLUCIÓN (Patrimonio Total) ---")
    print(Fore.YELLOW + "-" * 60)
    for r in registros_cronologicos:
        id_reg, anio, mes, liq, inv, total = r
        tamaño_barra = int((total / max_total) * ANCHO_BARRA)
        
        # La barra será verde para que destaque
        barra = Fore.GREEN + "█" * tamaño_barra
        etiqueta = f"{mes[:3]}. {anio}"
        
        print(f"{Fore.WHITE}{etiqueta:<10} | {barra:<{ANCHO_BARRA}} {Fore.CYAN}{formatear_moneda(total)}")
    print(Fore.YELLOW + "-" * 60)

# --- MENÚ PRINCIPAL ---

def menu():
    inicializar_base_de_datos()
    repo = TesoreriaRepository()
    limpiar_pantalla()
    
    while True:
        print("\n" + Fore.YELLOW + Style.BRIGHT + "="*45)
        print(Fore.CYAN + Style.BRIGHT + "     💰 TESORERÍA FINANCIERA AI v1.0 💰")
        print(Fore.YELLOW + Style.BRIGHT + "="*45)
        print(f"{Fore.WHITE}1. {Style.BRIGHT}Registrar cierre de mes")
        print(f"{Fore.WHITE}2. Ver histórico (Tabla)")
        print(f"{Fore.WHITE}3. Ver gráfico de barras")
        print(f"{Fore.BLUE}4. Editar registro")
        print(f"{Fore.RED}5. Eliminar registro")
        print(f"{Fore.YELLOW}6. Salir")
        
        opcion = input(f"\n{Fore.CYAN}Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            print(f"\n{Fore.CYAN}--- 📝 Nuevo Registro ---")
            anio = solicitar_int("Año: ")
            mes = input(f"{Fore.WHITE}Mes: ").strip()
            capital = solicitar_float("Capital Líquido (€): ")
            inversion = solicitar_float("Inversión (€): ")

            datos = RegistroTesoreria(anio, mes, capital, inversion)
            ultimo_total = repo.obtener_ultimo_registro()
            
            print(f"\n{Fore.CYAN}✨ Patrimonio actual: {Fore.WHITE}{formatear_moneda(datos.total)}")
            
            if ultimo_total > 0:
                diferencia = datos.total - ultimo_total
                porcentaje = (diferencia / ultimo_total) * 100
                if diferencia > 0:
                    print(f"{Fore.GREEN}📈 ¡Genial! Has ahorrado {formatear_moneda(diferencia)} (+{porcentaje:.2f}%)")
                else:
                    print(f"{Fore.RED}📉 Patrimonio bajó {formatear_moneda(abs(diferencia))} ({porcentaje:.2f}%)")
            
            repo.guardar(datos)
            print(f"{Fore.GREEN}✅ Guardado correctamente.")
            
        elif opcion == "2":
            print(f"\n{Fore.CYAN}--- 📜 HISTORIAL DE TESORERÍA ---")
            registros = repo.listar_todo()
            if not registros:
                print(f"{Fore.YELLOW}No hay registros.")
            else:
                datos_tabla = []
                for r in registros:
                    # Pintamos el total de cian para que resalte en la tabla
                    datos_tabla.append([r[0], r[1], r[2], formatear_moneda(r[3]), formatear_moneda(r[4]), f"{Fore.CYAN}{formatear_moneda(r[5])}{Fore.RESET}"])
                
                cabeceras = ["ID", "AÑO", "MES", "LÍQUIDO", "INVERSIÓN", "TOTAL"]
                print(tabulate(datos_tabla, headers=cabeceras, tablefmt="grid", stralign="center"))

        elif opcion == "3":
            registros = repo.listar_todo()
            limpiar_pantalla()
            dibujar_grafico_barras(registros)

        elif opcion == "4":
            print(f"\n{Fore.BLUE}--- ✏️ Editar Registro ---")
            id_reg = solicitar_int("ID a editar: ")
            
            # (Aquí va tu lógica de búsqueda de total_anterior que ya tenías...)
            # [Para brevedad, asumo que llamas a tu repo.actualizar al final]
            
            nuevo_liq = solicitar_float("Nuevo Líquido: ")
            nueva_inv = solicitar_float("Nueva Inversión: ")
            nuevo_tot = nuevo_liq + nueva_inv
            repo.actualizar(id_reg, nuevo_liq, nueva_inv, nuevo_tot)

        elif opcion == "5":
            print(f"\n{Fore.RED}--- 🗑️ Eliminar Registro ---")
            id_reg = solicitar_int("ID a borrar: ")
            confirmar = input(f"{Fore.YELLOW}¿Seguro que quieres borrar el ID {id_reg}? (s/n): ").strip()
            if confirmar.lower() == 's':
                repo.eliminar(id_reg)

        elif opcion == "6":
            print(f"\n{Fore.CYAN}👋 ¡Hasta el próximo mes, Sergio!")
            break

if __name__ == "__main__":
    menu()