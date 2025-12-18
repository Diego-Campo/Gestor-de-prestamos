import os
import traceback

os.environ['KIVY_NO_ARGS'] = '1'

try:
    from main import GestorPrestamosApp
    app = GestorPrestamosApp()
    widget = app.build()
    print('Build exitoso:', widget)
except Exception as e:
    print("=" * 60)
    print("ERROR CAPTURADO:")
    print("=" * 60)
    traceback.print_exc()
    print("=" * 60)
