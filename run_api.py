# Script para iniciar el servidor API FastAPI
# Ejecutar: python run_api.py

import os
import sys

def main():
    print("=" * 60)
    print("  GESTOR DE PRÉSTAMOS - Servidor API v2.0.0")
    print("=" * 60)
    print()
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Iniciar servidor
    import uvicorn
    
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '8000'))
    
    print(f"Iniciando servidor en http://{host}:{port}")
    print("Documentación API disponible en: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )

if __name__ == "__main__":
    main()
