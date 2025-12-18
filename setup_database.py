# Script para inicializar PostgreSQL con Docker
# Ejecutar: python setup_database.py

import subprocess
import sys
import time

def main():
    print("=" * 60)
    print("  SETUP DE BASE DE DATOS POSTGRESQL")
    print("=" * 60)
    print()
    
    print("Este script iniciará PostgreSQL usando Docker Compose")
    print()
    
    # Verificar si Docker está instalado
    try:
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
        print("✅ Docker detectado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker no está instalado o no está en el PATH")
        print("   Instala Docker Desktop: https://www.docker.com/products/docker-desktop")
        sys.exit(1)
    
    # Verificar si Docker Compose está disponible
    try:
        subprocess.run(['docker-compose', '--version'], check=True, capture_output=True)
        print("✅ Docker Compose detectado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker Compose no está instalado")
        sys.exit(1)
    
    print()
    print("Iniciando PostgreSQL...")
    print()
    
    # Iniciar contenedores
    try:
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        print()
        print("✅ PostgreSQL iniciado correctamente")
        print()
        print("Esperando a que PostgreSQL esté listo...")
        time.sleep(5)
        
        print()
        print("=" * 60)
        print("INFORMACIÓN DE CONEXIÓN:")
        print("=" * 60)
        print("Host: localhost")
        print("Puerto: 5432")
        print("Base de datos: gestor_prestamos")
        print("Usuario: postgres")
        print("Contraseña: postgres")
        print()
        print("pgAdmin disponible en: http://localhost:5050")
        print("  Email: admin@gestorprestamos.com")
        print("  Password: admin123")
        print()
        print("Para detener PostgreSQL:")
        print("  docker-compose down")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar Docker Compose: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
