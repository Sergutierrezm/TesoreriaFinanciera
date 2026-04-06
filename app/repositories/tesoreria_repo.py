from app.database.connection import obtener_conexion

class TesoreriaRepository:
    def guardar(self, registro):
        sql = """
            INSERT INTO tesoreria (anio, mes, capital_liquido, inversion, total)
            VALUES (%s, %s, %s, %s, %s)
        """

        conn = obtener_conexion()

        if conn:
            try:
                with conn: 
                    with conn.cursor() as cursor:
                        cursor.execute(sql, (
                            registro.anio, 
                            registro.mes, 
                            registro.capital_liquido, 
                            registro.inversion, 
                            registro.total # El total viene calculado del modelo
                        ))
                    print (f"Registro de {registro.mes} {registro.anio} guardado")
            except Exception as e:
                        print(f"Error al insertar en la base de datos: {e}")
            finally:
                        conn.close()
    
    def listar_todo(self):

         sql = "SELECT id, anio, mes, capital_liquido, inversion, total FROM tesoreria ORDER BY anio DESC, id DESC"

         conn = obtener_conexion()

         registros = []
         if conn:
             try:
                 with conn.cursor() as cursor:
                     cursor.execute(sql)
                     registros = cursor.fetchall()
             finally:
                 conn.close()

                 return registros        
    def actualizar(self, id_registro, nuevo_liquido, nueva_inversion, nuevo_total):
        sql = """
            UPDATE tesoreria 
            SET capital_liquido = %s, inversion = %s, total = %s 
            WHERE id = %s
        """
        conn = obtener_conexion()
        if conn:
            try:
                with conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql, (nuevo_liquido, nueva_inversion, nuevo_total, id_registro))
                print(f"✅ Registro ID {id_registro} actualizado correctamente.")
            except Exception as e:
                print(f"❌ Error al actualizar: {e}")
            finally:
                conn.close()

    def eliminar(self, id_registro):
        sql = "DELETE FROM tesoreria WHERE id = %s"
        conn = obtener_conexion()
        if conn:
            try:
                with conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql, (id_registro,))
                print(f"🗑️ Registro ID {id_registro} eliminado de la base de datos.")
            except Exception as e:
                print(f"❌ Error al eliminar: {e}")
            finally:
                conn.close()

    def obtener_ultimo_registro(self):
        # Buscamos el registro con el ID más alto (el último insertado)
        sql = "SELECT total FROM tesoreria ORDER BY id DESC LIMIT 1"
        conn = obtener_conexion()
        ultimo_total = 0
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    resultado = cursor.fetchone()
                    if resultado:
                        ultimo_total = float(resultado[0])
            finally:
                conn.close()
        return ultimo_total




