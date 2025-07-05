#Imagen oficial ligera como base 
FROM python:3.10-slim
#Se establece el directorio de trabajo dentro del contenedor 
WORKDIR /app
#Copiamos el archivo de dependencias al contenedor 
COPY requirements.txt . 
#Instalamos las dependencias listadas sin usar caches para ahorrar espacio 
RUN pip install --no-cache-dir -r requirements.txt
#Copiamos el resto del codigo del proyecto 
COPY . . 
#Exponemos el puerto para acceder al servidor django desde fuera del contenedor 
EXPOSE 8000
#Comando para inicar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]