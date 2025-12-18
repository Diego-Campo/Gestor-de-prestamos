-- Script de inicialización de base de datos PostgreSQL
-- Gestor de Préstamos v2.0.0
-- Fecha: 18 de diciembre de 2025

-- Eliminar tablas si existen (solo para desarrollo)
DROP TABLE IF EXISTS gastos_semanales CASCADE;
DROP TABLE IF EXISTS pagos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS bases_semanales CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- Tabla de usuarios (cobradores y administradores)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    es_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de bases semanales
CREATE TABLE bases_semanales (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    monto DECIMAL(12, 2) NOT NULL,
    fecha DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    monto_prestado DECIMAL(12, 2) NOT NULL,
    fecha_prestamo DATE NOT NULL,
    tipo_plazo VARCHAR(20) NOT NULL,
    tasa_interes DECIMAL(5, 4) NOT NULL,
    seguro DECIMAL(12, 2) NOT NULL,
    cuota_minima DECIMAL(12, 2) NOT NULL,
    dias_plazo INTEGER NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de pagos
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    monto DECIMAL(12, 2) NOT NULL,
    tipo_pago VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de gastos semanales
CREATE TABLE gastos_semanales (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    monto DECIMAL(12, 2) NOT NULL,
    descripcion TEXT,
    fecha DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_clientes_usuario_id ON clientes(usuario_id);
CREATE INDEX idx_clientes_estado ON clientes(estado);
CREATE INDEX idx_pagos_cliente_id ON pagos(cliente_id);
CREATE INDEX idx_pagos_fecha ON pagos(fecha);
CREATE INDEX idx_bases_semanales_usuario_fecha ON bases_semanales(usuario_id, fecha);
CREATE INDEX idx_gastos_semanales_usuario_fecha ON gastos_semanales(usuario_id, fecha);

-- Insertar usuario administrador por defecto
-- Password: admin123 (hasheado con bcrypt)
INSERT INTO usuarios (username, password, nombre, es_admin)
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LDgPMU8aC', 'Administrador', TRUE);

-- Insertar usuarios de prueba (opcional)
INSERT INTO usuarios (username, password, nombre, es_admin)
VALUES 
    ('cobrador1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LDgPMU8aC', 'Juan Pérez', FALSE),
    ('cobrador2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LDgPMU8aC', 'María García', FALSE);

-- Comentarios de las tablas
COMMENT ON TABLE usuarios IS 'Usuarios del sistema (cobradores y administradores)';
COMMENT ON TABLE bases_semanales IS 'Base de dinero semanal de cada cobrador';
COMMENT ON TABLE clientes IS 'Clientes con sus préstamos';
COMMENT ON TABLE pagos IS 'Pagos realizados por los clientes';
COMMENT ON TABLE gastos_semanales IS 'Gastos operativos de los cobradores';

-- Mensaje de éxito
SELECT 'Base de datos inicializada correctamente' AS mensaje;
