-- Crear la base de datos
CREATE DATABASE vulnerable_app;

-- Seleccionar la base de datos
USE vulnerable_app;

-- Crear la tabla de usuarios
CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  user VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password VARCHAR(25) NOT NULL
);
