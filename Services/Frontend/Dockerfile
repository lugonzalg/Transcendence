# Usar una imagen de Node.js como base
FROM node:20.10

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Astro CLI globalmente
RUN npm install -g astro

# Exponer el puerto en el que Astro se ejecuta (por defecto es 3000)
EXPOSE 3000

# Montar el volumen
VOLUME ["/app"]

# Comando para iniciar Astro en modo de desarrollo
CMD ["astro", "dev", "--host"]
