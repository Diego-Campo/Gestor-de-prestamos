"""
Script de setup para la aplicación Gestor de Préstamos.
Este script facilita la instalación y configuración inicial.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def print_banner():
    """Muestra el banner de bienvenida."""
    print("=" * 60)
    print("    GESTOR DE PRÉSTAMOS - SETUP DE INSTALACIÓN")
    print("    Sistema de Gestión de Préstamos v1.0.0")
    print("=" * 60)
    print()

def check_python():
    """Verifica la versión de Python."""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detectado")
    return True

def create_venv():
    """Crea el entorno virtual."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Entorno virtual ya existe")
        return True
    
    try:
        print("📦 Creando entorno virtual...")
        venv.create(venv_path, with_pip=True)
        print("✅ Entorno virtual creado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False

def install_dependencies():
    """Instala las dependencias del proyecto."""
    try:
        print("📥 Instalando dependencias...")
        
        # Determinar el ejecutable de pip según el sistema operativo
        if sys.platform == "win32":
            pip_path = Path(".venv/Scripts/pip.exe")
            python_path = Path(".venv/Scripts/python.exe")
        else:
            pip_path = Path(".venv/bin/pip")
            python_path = Path(".venv/bin/python")
        
        # Actualizar pip primero
        subprocess.run([
            str(python_path), "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        
        # Instalar dependencias
        subprocess.run([
            str(pip_path), "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print("💡 Intenta ejecutar manualmente:")
        print(r"   .\.venv\Scripts\pip.exe install -r requirements.txt")
        return False

def create_desktop_shortcut():
    """Crea un acceso directo en el escritorio (solo Windows)."""
    if sys.platform != "win32":
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Gestor de Préstamos.lnk")
        target = os.path.join(os.getcwd(), "ejecutar.bat")
        wDir = os.getcwd()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = target
        shortcut.save()
        
        print("✅ Acceso directo creado en el escritorio")
    except ImportError:
        print("ℹ️  Para crear acceso directo, instala: pip install winshell pywin32")
    except Exception as e:
        print(f"⚠️  No se pudo crear acceso directo: {e}")

def test_installation():
    """Prueba que la instalación funcione."""
    try:
        print("🧪 Probando instalación...")
        
        if sys.platform == "win32":
            python_path = Path(".venv/Scripts/python.exe")
        else:
            python_path = Path(".venv/bin/python")
        
        # Probar importaciones críticas
        result = subprocess.run([
            str(python_path), "-c", 
            "import PyQt6.QtWidgets; import bcrypt; import sqlite3; print('OK')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Prueba de instalación exitosa")
            return True
        else:
            print(f"❌ Error en prueba: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error probando instalación: {e}")
        return False

def show_usage_instructions():
    """Muestra las instrucciones de uso."""
    print("\n" + "=" * 60)
    print("🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\n📋 INSTRUCCIONES DE USO:")
    print("\n1. Para ejecutar la aplicación:")
    print("   • Opción 1: Hacer doble clic en 'ejecutar.bat'")
    print(r"   • Opción 2: Desde terminal: .\.venv\Scripts\python.exe app.py")
    
    print("\n2. Credenciales iniciales:")
    print("   • Administrador: admin / admin123")
    print("   • Cobradores: cobrador1/pass1, cobrador2/pass2, cobrador3/pass3")
    
    print("\n3. Documentación:")
    print("   • Manual de Usuario: MANUAL_USUARIO.md")
    print("   • Preguntas Frecuentes: FAQ.md")
    print("   • Instalación: INSTALL.md")
    
    print("\n⚠️  IMPORTANTE:")
    print("   • Cambiar contraseñas por defecto al primer uso")
    print("   • Hacer respaldos regulares del archivo 'gestor_prestamos.db'")
    
    print("\n🆘 Soporte:")
    print("   • Si tienes problemas, consulta FAQ.md")
    print("   • Para desarrollo: DEVELOPER_GUIDE.md")
    
    print("\n" + "=" * 60)

def main():
    """Función principal del setup."""
    print_banner()
    
    # Verificaciones previas
    if not check_python():
        sys.exit(1)
    
    # Proceso de instalación
    steps = [
        ("Crear entorno virtual", create_venv),
        ("Instalar dependencias", install_dependencies),
        ("Probar instalación", test_installation),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"\n❌ Error en: {step_name}")
            print("💡 Revisa los mensajes anteriores para más información")
            sys.exit(1)
    
    # Extras opcionales
    create_desktop_shortcut()
    
    # Instrucciones finales
    show_usage_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Para ayuda, consulta INSTALL.md o contacta soporte técnico")
        sys.exit(1)