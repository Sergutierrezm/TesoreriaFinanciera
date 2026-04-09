from app.database.connection import obtener_conexion

class TesoreriaRepository:
    def guardar(self, registro):
        sql = """
            INSERT INTO tesoreria (anio, mes, capital_liquido, inversion, total)
            VALUES (?, ?, ?, ?, ?)
        """
        conn = obtener_conexion()
        if conn:
            try:
                with conn:
                    conn.execute(sql, (
                        registro.anio, 
                        registro.mes.strip().capitalize(), # Aseguramos formato (ej: Mayo)
                        registro.capital_liquido, 
                        registro.inversion, 
                        registro.total
                    ))
                # Ya no imprimimos nada aquí para que el main.py controle la salida visual
            except Exception as e:
                print(f"❌ Error al guardar en SQLite: {e}")
            finally:
                conn.close()
    
    def listar_todo(self):
        # Mantenemos el orden cronológico que definimos antes
        sql = """
            SELECT id, anio, mes, capital_liquido, inversion, total 
            FROM tesoreria 
            ORDER BY anio DESC, 
            CASE mes 
                WHEN 'enero' THEN 1 WHEN 'febrero' THEN 2 WHEN 'marzo' THEN 3 
                WHEN 'abril' THEN 4 WHEN 'mayo' THEN 5 WHEN 'junio' THEN 6 
                WHEN 'julio' THEN 7 WHEN 'agosto' THEN 8 WHEN 'septiembre' THEN 9 
                WHEN 'octubre' THEN 10 WHEN 'noviembre' THEN 11 WHEN 'diciembre' THEN 12 
            END DESC
        """
        conn = obtener_conexion()
        registros = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                registros = cursor.fetchall()
            finally:
                conn.close()
        return registros

    def actualizar(self, id_registro, nuevo_liquido, nueva_inversion, nuevo_total):
        sql = "UPDATE tesoreria SET capital_liquido = ?, inversion = ?, total = ? WHERE id = ?"
        conn = obtener_conexion()
        if conn:
            try:
                with conn:
                    conn.execute(sql, (nuevo_liquido, nueva_inversion, nuevo_total, id_registro))
                # Imprimimos confirmación visual aquí
                print(f"✅ Registro ID {id_registro} actualizado correctamente.")
            except Exception as e:
                print(f"❌ Error al actualizar: {e}")
            finally:
                conn.close()

    def eliminar(self, id_registro):
        sql = "DELETE FROM tesoreria WHERE id = ?"
        conn = obtener_conexion()
        if conn:
            try:
                with conn:
                    conn.execute(sql, (id_registro,))
                print(f"🗑️ Registro ID {id_registro} eliminado.")
            except Exception as e:
                print(f"❌ Error al eliminar: {e}")
            finally:
                conn.close()

    def obtener_ultimo_registro(self):
        sql = "SELECT total FROM tesoreria ORDER BY id DESC LIMIT 1"
        conn = obtener_conexion()
        ultimo_total = 0
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                resultado = cursor.fetchone()
                if resultado:
                    ultimo_total = float(resultado[0])
            finally:
                conn.close()
        return ultimo_total

class RegistroTesoreria:
    def __init__(self, anio, mes, capital_liquido, inversion):
        self.anio = anio
        self.mes = mes
        self.capital_liquido = capital_liquido
        self.inversion = inversion
        # El total se calcula automáticamente al instanciar el objeto
        self.total = self._calcular_total()

    def _calcular_total(self):
        """Calcula el total y redondea a 2 decimales."""
        try:
            return round(float(self.capital_liquido) + float(self.inversion), 2)
        except (ValueError, TypeError):
            print("⚠️ Error: El capital y la inversión deben ser números válidos.")
            return 0.0

    def mostrar_detalle(self):
        """Devuelve una cadena formateada con los datos del registro."""
        return (f"{self.mes} {self.anio}: Líquido={self.capital_liquido}€, "
                f"Inversión={self.inversion}€, Total={self.total}€")        




