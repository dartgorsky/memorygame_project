# Memory Game - Proyecto Django

## Descripción

Memory Game es un juego web desarrollado con Django donde los usuarios pueden registrarse, iniciar sesión y jugar un clásico juego de memoria. El objetivo es encontrar pares de cartas iguales dentro de un tiempo y con un número limitado de intentos. El juego cuenta con diferentes niveles de dificultad y lleva un registro de las estadísticas personales y el ranking de los jugadores.



## Funcionalidades principales

- Registro y autenticación de usuarios.
- Selección de niveles: Básico, Medio y Avanzado.
- Juego con tablero de cartas que se voltean para encontrar pares.
- Control de vidas, puntajes e intentos.
- Estadísticas personales de cada jugador: partidas jugadas, victorias, derrotas, puntaje promedio, tiempo promedio por partida y nivel más jugado.
- Ranking público con los mejores puntajes por nivel.
- Perfil de usuario con historial de partidas y estadísticas.



## Tecnologías usadas

- Python 3.10+
- Django 5.2.4
- MySQL (base de datos)
- Bootstrap 5 para el frontend
- HTML, CSS, JavaScript para la interfaz de usuario



## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/memorygame.git
   cd memorygame

2. Crear y activar entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt

4. Aplicar migraciones:

   ```bash
   python manage.py migrate

5. Ejecutar el servidor:

   ```bash
   python manage.py runserver

# Insert de imagenes SQL 

1. Antes de iniciar una partida, debera ingresar al http://localhost:8080/ y en la tabla app_memorygame_card debera hacer la siguiente consulta SQL

   ```bash
   INSERT INTO app_memorygame_card (name, image_url, value) VALUES ('Estrella', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/estrella.png', 1), ('Fresa', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/fresa.png', 2), ('Gato', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/gato.png', 3), ('Luna', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/luna.png', 4), ('Oso', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/oso.png', 5), ('Panda', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/panda.png', 6), ('Perro', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/perro.png', 7), ('Pinguino', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/pinguino.png', 8), ('Rana', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/rana.png', 9), ('Zorro', 'https://raw.githubusercontent.com/dartgorsky/mis-svg/refs/heads/main/zorro.png', 10);