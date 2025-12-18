"""
Servidor FastAPI principal.

Configura:
- App FastAPI con CORS
- Middleware de autenticación
- Rutas de la API
- Manejo de errores
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from contextlib import asynccontextmanager

from src.db.connection import Database
from src.config import APP_NAME, APP_VERSION

logger = logging.getLogger(__name__)

# Instancia global de base de datos
db_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación."""
    global db_instance
    
    # Startup
    logger.info(f"🚀 Iniciando {APP_NAME} API v{APP_VERSION}")
    try:
        db_instance = Database()
        db_instance.create_tables()
        db_instance.inicializar_admin()
        logger.info("✅ Base de datos inicializada")
    except Exception as e:
        logger.error(f"❌ Error inicializando base de datos: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando aplicación...")
    if db_instance:
        db_instance.close_all_connections()
    logger.info("✅ Aplicación cerrada correctamente")


# Crear aplicación FastAPI
app = FastAPI(
    title=APP_NAME + " API",
    description="API REST para gestión de préstamos y cobranza",
    version=APP_VERSION,
    lifespan=lifespan
)

# Configurar CORS para permitir acceso desde Android/Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejadores de errores globales
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de datos."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Error de validación",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales."""
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Error interno del servidor",
            "detail": str(exc)
        }
    )


# Ruta de health check
@app.get("/", tags=["Health"])
async def root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "success": True,
        "message": f"{APP_NAME} API",
        "version": APP_VERSION,
        "status": "online"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "success": True,
        "status": "healthy",
        "database": "connected" if db_instance else "disconnected"
    }


def get_db():
    """Dependency para obtener instancia de base de datos."""
    return db_instance


# Importar y registrar rutas
from src.api.routes import auth, usuarios, clientes, pagos

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(pagos.router, prefix="/api/pagos", tags=["Pagos"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
