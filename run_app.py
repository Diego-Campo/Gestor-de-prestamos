# Script para iniciar la aplicación Kivy
# Ejecutar: python run_app.py

import os
import sys

def main():
    print("=" * 60)
    print("  GESTOR DE PRÉSTAMOS - Aplicación v2.0.0")
    print("=" * 60)
    print()
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verificar que la API esté corriendo
    import requests
    api_url = os.getenv('API_URL', 'http://localhost:8000')
    
    print(f"Verificando conexión a API: {api_url}")
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Conexión a API exitosa")
        else:
            print("⚠️  Advertencia: API respondió con código", response.status_code)
    except requests.exceptions.RequestException as e:
        print("❌ No se pudo conectar a la API")
        print(f"   Error: {e}")
        print()
        print("Asegúrate de que el servidor API esté corriendo:")
        print("   python run_api.py")
        print()
        sys.exit(1)
    
    print()
    print("Iniciando aplicación...")
    print()
    
    # Iniciar aplicación
    from main import main as app_main
    app_main()

if __name__ == "__main__":
    main()
