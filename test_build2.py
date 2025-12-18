import os
os.environ['KIVY_NO_ARGS'] = '1'

from main import GestorPrestamosApp

app = GestorPrestamosApp()
print("App creada")

widget = app.build()
print("Widget creado:", widget)
