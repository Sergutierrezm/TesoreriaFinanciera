from app.models.tesoreria import RegistroTesoreria
from app.repositories.tesoreria_repo import TesoreriaRepository
from app.database.connection import obtener_conexion 

def menu():
    repo = TesoreriaRepository()
    
    while True:
        print("\n" + "="*35)
        print("   💰 TESORERÍA FINANCIERA AI 💰")
        print("="*35)
        print("1. Registrar cierre de mes")
        print("2. Ver histórico de ahorros")
        print("3. Editar registro (por ID)")
        print("4. Eliminar registro (por ID)")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ")

        if opcion == "1":
            print("\n--- 📝 Nuevo Registro ---")
            anio = int(input("Año (ej. 2026): "))
            mes = input("Mes (ej. Abril): ")
            capital = float(input("Capital Líquido (€): "))
            inversion = float(input("Inversión (€): "))

            datos = RegistroTesoreria(anio, mes, capital, inversion)
            
            # --- LÓGICA DE COMPARACIÓN (Último registro) ---
            ultimo_total = repo.obtener_ultimo_registro()
            
            print(f"\n✨ Patrimonio actual: {datos.total}€")
            
            if ultimo_total > 0:
                diferencia = datos.total - ultimo_total
                porcentaje = (diferencia / ultimo_total) * 100
                if diferencia > 0:
                    print(f"📈 ¡Genial! Has ahorrado {diferencia:,.2f}€ respecto al mes anterior (+{porcentaje:.2f}%)")
                else:
                    print(f"📉 Patrimonio bajó {abs(diferencia):,.2f}€ ({porcentaje:.2f}%)")
            
            repo.guardar(datos)
            
        elif opcion == "2":
            print("\n--- 📜 HISTORIAL DE TESORERÍA ---")
            registros = repo.listar_todo()
            if not registros:
                print("No hay registros todavía.")
            else:
                print(f"{'ID':<4} | {'AÑO':<5} | {'MES':<10} | {'TOTAL':<10}")
                print("-" * 40)
                for r in registros:
                    print(f"{r[0]:<4} | {r[1]:<5} | {r[2]:<10} | {r[5]:<10}€")

        elif opcion == "3":
            print("\n--- ✏️ Editar Registro ---")
            id_reg = int(input("Introduce el ID del registro a editar: "))
            
            # 1. Diccionario para convertir meses a números (Orden cronológico)
            meses_orden = {
                "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, 
                "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, 
                "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
            }

            conn = obtener_conexion()
            total_anterior = 0
            if conn:
                try:
                    with conn.cursor() as cursor:
                        # Primero obtenemos el mes y año del registro que quieres editar
                        cursor.execute("SELECT anio, mes FROM tesoreria WHERE id = %s", (id_reg,))
                        actual = cursor.fetchone()
                        
                        if actual:
                            anio_act, mes_act = actual
                            num_mes_act = meses_orden.get(mes_act.lower(), 0)

                            # Buscamos el registro que sea del mes anterior (mismo año) 
                            # o del último mes del año pasado.
                            cursor.execute("""
                                SELECT total, mes, anio FROM tesoreria 
                                WHERE id != %s 
                                ORDER BY anio DESC, 
                                CASE mes 
                                    WHEN 'enero' THEN 1 WHEN 'febrero' THEN 2 WHEN 'marzo' THEN 3 
                                    WHEN 'abril' THEN 4 WHEN 'mayo' THEN 5 WHEN 'junio' THEN 6 
                                    WHEN 'julio' THEN 7 WHEN 'agosto' THEN 8 WHEN 'septiembre' THEN 9 
                                    WHEN 'octubre' THEN 10 WHEN 'noviembre' THEN 11 WHEN 'diciembre' THEN 12 
                                END DESC
                            """, (id_reg,))
                            
                            # Recorremos los registros para encontrar el primero que sea cronológicamente anterior
                            todos = cursor.fetchall()
                            for r in todos:
                                r_total, r_mes, r_anio = r
                                num_mes_r = meses_orden.get(r_mes.lower(), 0)
                                
                                # Si es del mismo año y mes menor, O si es de un año anterior
                                if (r_anio == anio_act and num_mes_r < num_mes_act) or (r_anio < anio_act):
                                    total_anterior = float(r_total)
                                    mes_encontrado = r_mes
                                    break # Ya tenemos el anterior más cercano
                finally:
                    conn.close()

            # 2. Pedir nuevos datos
            nuevo_liq = float(input("Nuevo Capital Líquido (€): "))
            nueva_inv = float(input("Nueva Inversión (€): "))
            nuevo_tot = nuevo_liq + nueva_inv
            
            # 3. Mostrar comparativa
            print(f"\n✨ Nuevo patrimonio calculado: {nuevo_tot}€")
            if total_anterior > 0:
                dif = nuevo_tot - total_anterior
                perc = (dif / total_anterior) * 100
                print(f"📈 Comparado con {mes_encontrado}: {'+' if dif > 0 else ''}{dif:,.2f}€ ({perc:.2f}%)")
            else:
                print("ℹ️ No se encontró un registro cronológicamente anterior.")
            
            repo.actualizar(id_reg, nuevo_liq, nueva_inv, nuevo_tot)

        elif opcion == "4":
            print("\n--- 🗑️ Eliminar Registro ---")
            id_reg = int(input("Introduce el ID del registro a borrar: "))
            confirmar = input(f"¿Estás seguro de borrar el ID {id_reg}? (s/n): ")
            if confirmar.lower() == 's':
                repo.eliminar(id_reg)

        elif opcion == "5":
            print("\n👋 ¡Hasta el próximo mes, Sergio!")
            break

if __name__ == "__main__":
    menu()