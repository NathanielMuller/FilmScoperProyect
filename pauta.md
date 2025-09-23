# Temáticas

- **INTRODUCCIÓN A LA SEMANA**  
- **RESULTADO DE APRENDIZAJE (RA) – INDICADOR DE LOGRO (IL)**  
- **PALABRAS CLAVES**  
- **PREGUNTAS GATILLANTES**  
- **¿CÓMO PODEMOS OPTIMIZAR NUESTRAS APLICACIONES WEB?**  
- **CIERRE DE LA SEMANA**  
- **REFERENCIAS**  
- **APUNTES**  

---

## Introducción a la semana

En esta semana deberán trabajar en equipo para realizar la actividad sumativa de la experiencia 2, la cual consta de dos partes.  
La parte I, consistirá en integrar seguridad a las aplicaciones web (autentificación, protección de URLs), e implementar los temas de esta experiencia al encargo grupal **Desarrollando el Backend de nuestra aplicación web**.  
Para cumplir con la Parte II, deberán trabajar sobre su repositorio en GitHub y compartir con el docente todos los avances y desarrollos creados.

---

## Resultado de Aprendizaje (RA) – Indicador de Logro (IL)

| Resultado de Aprendizaje (RA) | Indicador de Logro (IL) |
|-------------------------------|-------------------------|
| RA1. Construye el FrontEnd de una página web aplicando framework y lenguajes que respondan a la estructura visual y funcional requerida por el cliente. | IL5. Aplica las operaciones en un repositorio de trabajo colaborativo generado durante el desarrollo de la aplicación web. |
| RA2. Construye un modelo relacional normalizado que responda a los requerimientos del cliente. | IL6. Genera una aplicación utilizando el framework Django considerando los requerimientos establecidos por el cliente.<br>IL7. Establece la interacción entre la capa de presentación, la capa de negocios y datos para completar funcionalidades requeridas.<br>IL8. Realiza operaciones de creación, actualización, lectura y eliminación de registros en base a lo ingresado por el cliente en la capa de presentación.<br>IL9. Establece el acceso a la aplicación web mediante la autenticación y autentificación segura de los datos del cliente y restringiendo el acceso a funcionalidades propias del usuario. |

---

## Palabras claves

- Backend
- Oracle
- Modelos
- Autentificación
- Autorización
- Django
- Views
- Urls
- Patrón de Diseño
- Settings

---

## Preguntas gatillantes

- ¿Cómo podemos optimizar nuestra aplicación web?
- ¿Qué otros recursos nos ofrecen Django como Framework?
- ¿De qué maneras puedo implementar la seguridad en rutas de nuestro proyecto?

---

## ¿Cómo podemos optimizar nuestras aplicaciones web?

Django proporciona algunos elementos adicionales para optimizar los elementos visuales y de lógica en las aplicaciones web:

### 1. Envío de mensajes de una pantalla a otra mediante vistas

Para activar la mensajería en Django, define en `settings.py` la variable `MESSAGE_STORAGE`, que te permitirá enviar mensajes entre distintas ventanas.  
Agrega la etiqueta `django.contrib.messages.storage.cookie.CookieStorage` para activar la mensajería.

**Referencia:**  
Sepulveda, M. (2020). [CURSO DJANGO 2020 PARTE 11 - SWEET ALERT](https://www.youtube.com/watch?v=1NvbWhtKaHc&list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ&index=13)

---

### 2. Autorización en Django

Django proporciona un sistema de autenticación y autorización, construido sobre el framework de sesión.  
Este sistema es flexible y permite crear URLs, formularios, vistas y plantillas desde el inicio, simplemente llamando a la API provista para loguear al usuario.

---

### 3. Paginación para nuestros registros

En Django, la clase `Paginator` recibe el listado de todos los registros y el nivel de paginación.  
La paginación permite modificar la cantidad de datos en cada página y el estilo de división.

---

### 4. Protección de Rutas con Django

La protección de rutas consiste en bloquear o redirigir secciones de la aplicación, impidiendo el acceso a usuarios no autenticados.  
Para esto, utiliza el decorador `login_required` en las rutas que desees proteger.

---

### 5. Autenticación con Facebook

Para integrar autenticación con Facebook, realiza las configuraciones necesarias para que el usuario pueda loguearse con su cuenta de Facebook.

---

Django permite desarrollar y probar aplicaciones antes de desplegarlas en producción.  
El framework proporciona scripts de Python y un servidor web de desarrollo para pruebas locales con el explorador web.

---

## Cierre de la semana

Aplicando las consideraciones visualizadas en los ejemplos señalados, se puede mejorar tanto la interfaz como la lógica interna de los proyectos, asegurando rutas y manipulando las herramientas integradas que ofrece Django para optimizar el desarrollo de la aplicación web.

---

## Referencias

- Django Software Foundation (2022). [Documentación Django](https://www.djangoproject.com/)  
- Fazt. (2022). [Django CRUD con autenticación y Despliegue Gratuito (Login, Register, Rutas protegidas, y más)](https://www.youtube.com/watch?v=e6PkGDH4wWA)  
- Nuñez, R. (2020). [Como hacer un login en Django y proteger mis views](https://www.youtube.com/watch?v=ICdax61EeWM)  
- Sepulveda, M. (2020). [Autenticación con Facebook](https://www.youtube.com/watch?v=Y0lsI_vwH4E&list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ&index=19)  
- Sepulveda, M. (2020). [Paginación](https://www.youtube.com/watch?v=g-76pNgPFl8&list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ&index=13)  
- Sepulveda, M. (2020). [Sweet alert](https://www.youtube.com/watch?v=1NvbWhtKaHc&list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ&index=14)  
- Sepulveda, M. (2020). [Autorización](https://www.youtube.com/watch?v=XY9pOcGdMoo&list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ&index=19)  

---

## Apuntes

*(Espacio para apuntes adicionales de la semana)*