# Memory Game - Proyecto Django

## Descripción

Memory Game es un juego web desarrollado con Django donde los usuarios pueden registrarse, iniciar sesión y jugar un clásico juego de memoria. El objetivo es encontrar pares de cartas iguales dentro de un tiempo y con un número limitado de intentos. El juego cuenta con diferentes niveles de dificultad y lleva un registro de las estadísticas personales y el ranking de los jugadores.

---

## Funcionalidades principales

- Registro y autenticación de usuarios.
- Selección de niveles: Básico, Medio y Avanzado.
- Juego con tablero de cartas que se voltean para encontrar pares.
- Control de vidas, puntajes e intentos.
- Estadísticas personales de cada jugador: partidas jugadas, victorias, derrotas, puntaje promedio, tiempo promedio por partida y nivel más jugado.
- Ranking público con los mejores puntajes por nivel.
- Perfil de usuario con historial de partidas y estadísticas.

---

## Tecnologías usadas

- Python 3.10+
- Django 5.2.4
- MySQL (base de datos)
- Bootstrap 5 para el frontend
- HTML, CSS, JavaScript para la interfaz de usuario

---

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/memorygame.git
   cd memorygame

2. Crear y activar entorno virtual
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

3. Instalar dependencias:
   pip install -r requirements.txt

4. Aplicar migraciones:
   python manage.py migrate

5. Ejecutar el servidor:
   python manage.py runserver