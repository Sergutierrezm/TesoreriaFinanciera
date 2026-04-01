from app.models.tesoreria import RegistroTesoreria
from app.repositories.tesoreria_repo import TesoreriaRepository


def ejecutar_prueba():
    print("--- Tesoreria Financiera APP AI ---")

    datos = RegistroTesoreria(
        anio=2026,
        mes="abril",
        capital_liquido=1000.0,
        inversion=500.0
    )

    print(f"Calculando total: {datos.total}$")

    repo = TesoreriaRepository()
    repo.guardar(datos)

    print ("Registro guardado en la base de datos")


if __name__ == "__main__":
    ejecutar_prueba()