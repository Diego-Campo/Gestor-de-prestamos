import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import datetime, timedelta
from src.database import Database
from src.usuario import Usuario
from src.cliente import Cliente

def generar_nombre():
    nombres = ["Juan", "María", "Pedro", "Ana", "Luis", "Carlos", "José", "Diana", "Miguel", "Sandra",
              "Antonio", "Carmen", "Fernando", "Patricia", "Roberto", "Laura", "Ricardo", "Mónica"]
    apellidos = ["García", "Rodríguez", "Martínez", "López", "Pérez", "González", "Hernández", "Díaz",
                "Torres", "Ramírez", "Sánchez", "Morales", "Castro", "Ortiz", "Rivera", "Cruz"]
    return f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"

def generar_cedula():
    return str(random.randint(10000000, 99999999))

def generar_telefono():
    return f"3{random.randint(100000000, 999999999)}"

def generar_monto():
    # Montos típicos de préstamo (entre 100,000 y 2,000,000)
    return random.choice([100000, 150000, 200000, 250000, 300000, 400000, 500000, 
                        600000, 800000, 1000000, 1500000, 2000000])

def simular_semana_cobro(cliente_manager, cliente_id, monto_prestado, cuota_minima):
    # Simular entre 1 y 7 pagos en la semana
    num_pagos = random.randint(1, 7)
    total_pagado = 0
    
    for _ in range(num_pagos):
        # El pago puede ser entre la cuota mínima y el doble
        monto_pago = random.randint(
            int(cuota_minima),
            int(min(cuota_minima * 2, monto_prestado - total_pagado))
        )
        tipo_pago = random.choice(["efectivo", "digital"])
        
        # Registrar el pago
        cliente_manager.registrar_pago(cliente_id, monto_pago, tipo_pago)
        total_pagado += monto_pago
        
        # Si ya pagó todo, terminar
        if total_pagado >= monto_prestado:
            break

def main():
    print("Iniciando simulación de operaciones...")
    
    # Inicializar la base de datos
    db = Database()
    usuario_manager = Usuario(db)
    cliente_manager = Cliente(db)

    # Crear 3 cobradores
    cobradores = [
        {"username": "cobrador1", "password": "pass1", "nombre": "Juan Pérez"},
        {"username": "cobrador2", "password": "pass2", "nombre": "María López"},
        {"username": "cobrador3", "password": "pass3", "nombre": "Carlos Rodríguez"}
    ]

    # Registrar cobradores
    for cobrador in cobradores:
        usuario_manager.crear_usuario(cobrador["username"], cobrador["password"], cobrador["nombre"])
        print(f"\nCobrador registrado: {cobrador['nombre']}")

    # Para cada cobrador
    for cobrador in cobradores:
        # Iniciar sesión
        usuario_id = usuario_manager.validar_usuario(cobrador["username"], cobrador["password"])
        
        if usuario_id:
            print(f"\nSimulando operaciones para {cobrador['nombre']}...")
            
            # Registrar base semanal
            base_semanal = random.randint(5000000, 10000000)
            usuario_manager.registrar_base_semanal(usuario_id, base_semanal)
            print(f"Base semanal registrada: ${base_semanal:,}")

            # Registrar clientes (entre 40 y 60)
            num_clientes = random.randint(40, 60)
            print(f"Registrando {num_clientes} clientes...")
            
            clientes_registrados = []
            for i in range(num_clientes):
                nombre = generar_nombre()
                cedula = generar_cedula()
                telefono = generar_telefono()
                monto = generar_monto()
                tipo_plazo = random.choice(["diario", "semanal", "quincenal", "mensual"])
                
                # Si el monto es mayor a 500,000, posibilidad de tasa personalizada
                tasa_interes = None
                if monto > 500000 and random.random() > 0.5:
                    tasa_interes = random.uniform(0.15, 0.25)  # Entre 15% y 25%

                cliente_id = cliente_manager.registrar_cliente(
                    usuario_id, nombre, cedula, telefono, monto, tipo_plazo, tasa_interes
                )
                
                # Guardar información del cliente para simular pagos
                cuota_minima = cliente_manager.calcular_cuota_minima(monto)
                clientes_registrados.append({
                    'id': cliente_id,
                    'monto': monto,
                    'cuota_minima': cuota_minima
                })
                
                if (i + 1) % 10 == 0:
                    print(f"Progreso: {i + 1}/{num_clientes} clientes registrados")

            # Simular una semana de cobros
            print("\nSimulando una semana de cobros...")
            for cliente in clientes_registrados:
                simular_semana_cobro(
                    cliente_manager,
                    cliente['id'],
                    cliente['monto'],
                    cliente['cuota_minima']
                )

            # Registrar algunos gastos de la semana
            print("Registrando gastos semanales...")
            gastos_semana = [
                ("Gasolina", random.randint(50000, 100000)),
                ("Almuerzo", random.randint(15000, 30000)),
                ("Transporte", random.randint(20000, 50000)),
                ("Papelería", random.randint(5000, 15000)),
                ("Mantenimiento moto", random.randint(30000, 80000))
            ]
            
            for concepto, monto in gastos_semana:
                usuario_manager.registrar_gasto(usuario_id, monto, concepto)

            # Mostrar resumen semanal
            print(f"\nResumen semanal para {cobrador['nombre']}:")
            resumen = usuario_manager.obtener_resumen_semanal(usuario_id)
            print(f"Base semanal: ${resumen['base']:,}")
            print(f"Total cobrado: ${resumen['cobrado']:,}")
            print(f"Total prestado: ${resumen['prestado']:,}")
            print(f"Total seguros: ${resumen['seguros']:,}")
            print(f"Total gastos: ${resumen['gastos']:,}")
            print(f"Pagos en efectivo: ${resumen['efectivo']:,}")
            print(f"Pagos digitales: ${resumen['digital']:,}")
            balance = resumen['base'] + resumen['cobrado'] + resumen['seguros'] - resumen['prestado'] - resumen['gastos']
            print(f"Balance final: ${balance:,}")
            print("-" * 50)

    print("\nSimulación completada. La aplicación está lista para usar.")
    db.close()

if __name__ == "__main__":
    main()