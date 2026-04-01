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







