# FilmScoper 🎬

## Descripción

FilmScoper es una plataforma web moderna desarrollada con Django que permite a los usuarios descubrir, explorar y calificar películas. El proyecto integra funcionalidades avanzadas de gestión de usuarios, sistema de reseñas, categorización de películas y una interfaz de usuario elegante con Bootstrap 5.

## 🎯 Alcance y Estado del Proyecto

### ✅ Funcionalidades Completamente Implementadas
- [x] **Catálogo de Películas**: Navegación por categorías (Acción, Comedia, Documentales, Romance, Terror)
- [x] **Sistema de Usuarios**: Registro, login, logout con validaciones completas
- [x] **Perfil de Usuario**: Gestión de información personal, foto de perfil y géneros favoritos
- [x] **Base de Datos**: 29 películas distribuidas en 5 categorías
- [x] **Paginación**: Navegación optimizada en listados (12 películas por página)
- [x] **Interfaz Responsiva**: Compatible con dispositivos móviles y desktop
- [x] **Listas Personalizadas**: Sistema de favoritos y "Ver más tarde" completamente funcional
- [x] **Protección de Rutas**: Decoradores `@login_required` para vistas sensibles
- [x] **Validación de Formularios**: Django Forms con validación híbrida cliente/servidor
- [x] **CSRF Protection**: Protección contra ataques de falsificación de solicitudes
- [x] **Panel de Administración**: Django Admin configurado para gestión de contenido
- [x] **Comandos Personalizados**: Scripts para poblar datos automáticamente
- [x] **Tests Automatizados**: Suite de pruebas para modelos y vistas principales

### ⚠️ Funcionalidades Parcialmente Implementadas
- [x] **Notificaciones**: Sistema básico con SweetAlert2 (solo para listas personales)
- [ ] **Sistema de Búsqueda**: Frontend implementado pero sin funcionalidad backend
- [ ] **Filtros Avanzados**: Interfaz creada pero sin lógica de filtrado

### ❌ Funcionalidades Pendientes (No Implementadas)
- [ ] **Sistema de Reseñas y Calificaciones**: Modelos creados pero sin interfaz funcional
- [ ] **Sistema de Foros**: Completamente ausente
- [ ] **Comentarios en Películas**: Sin implementar
- [ ] **Sistema de Recomendaciones**: No desarrollado
- [ ] **Notificaciones Push**: No implementado
- [ ] **API REST**: Sin desarrollar
- [ ] **Integración con APIs Externas**: No implementado
- [ ] **Sistema de Moderación**: Básico en Django Admin únicamente

## 🚀 Instalación y Configuración

### Prerrequisitos
- **Python 3.8 o superior**: Lenguaje de programación principal
- **pip**: Gestor de paquetes de Python (incluido con Python)
- **Git**: Para clonar el repositorio (opcional si descargas ZIP)

### Instalación Completa - Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/NathanielMuller/FilmScoperProyect.git
cd FilmScoperProyect
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias de Python
```bash
# Instalar las librerías principales del proyecto
pip install Django==5.2.6
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install Pillow
```

**Librerías y extensiones de Python utilizadas:**
- **Django 5.2.6**: Framework web principal para el desarrollo del proyecto
- **django-crispy-forms**: Para formularios elegantes y responsivos
- **crispy-bootstrap5**: Integración de crispy-forms con Bootstrap 5
- **Pillow**: Biblioteca de procesamiento de imágenes para ImageField (fotos de perfil, posters de películas)

**Alternativa (instalación rápida):**
```bash
pip install Django django-crispy-forms crispy-bootstrap5 Pillow
```

### 4. Configurar Base de Datos
```bash
python manage.py migrate
```

### 5. Cargar Datos de Ejemplo
```bash
python manage.py poblar_peliculas
python manage.py agregar_peliculas
```

### 6. Crear Superusuario (Opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## 📁 Estructura del Proyecto

```
FilmScoperProyect/
├── film_scoper/                 # Configuración principal del proyecto
│   ├── settings.py             # Configuraciones de Django
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Configuración WSGI
├── core/                       # Aplicación principal
│   ├── models.py               # Modelos de datos
│   ├── views.py                # Lógica de vistas
│   ├── forms.py                # Formularios Django
│   ├── urls.py                 # URLs de la aplicación
│   ├── admin.py                # Configuración del admin
│   ├── tests.py                # Pruebas automatizadas
│   ├── management/             # Comandos personalizados
│   │   └── commands/
│   │       ├── poblar_peliculas.py
│   │       └── agregar_peliculas.py
│   ├── static/core/            # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/core/         # Templates Django
│       ├── base.html
│       ├── index.html
│       ├── categoria.html
│       └── ...
├── db.sqlite3                  # Base de datos SQLite
├── manage.py                   # Utilidad de Django
└── README.md                   # Este archivo
```

## 🎮 Uso de la Aplicación

### Para Usuarios (Funcionalidades Disponibles)
1. **Registro**: Crear cuenta con email, fecha de nacimiento y géneros favoritos
2. **Exploración**: Navegar por categorías de películas
3. **Perfil**: Personalizar información personal y foto de perfil
4. **Listas**: Agregar/quitar películas de favoritos y "ver más tarde"
5. **Visualización**: Ver detalles completos de cada película

### Para Administradores
1. **Panel Admin**: Acceder a `/admin/` con credenciales de superusuario
2. **Gestión de Contenido**: Agregar/editar películas y categorías
3. **Gestión de Usuarios**: Administrar cuentas y perfiles
4. **Comandos**: Usar comandos personalizados para poblar datos

### ⚠️ Limitaciones Actuales
- **Sin Sistema de Calificación**: No se pueden calificar películas (pendiente)
- **Sin Búsqueda Funcional**: El buscador no procesa consultas
- **Sin Foros**: No hay sistema de discusión entre usuarios
- **Sin Recomendaciones**: No hay sugerencias personalizadas

## 🧪 Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas con verbosidad
python manage.py test -v 2

# Ejecutar pruebas específicas
python manage.py test core.tests.PeliculaModelTest
```

## 🛠️ Tecnologías y Dependencias

### Backend - Python y Django
- **Django 5.2.6**: Framework web de Python para el desarrollo principal
- **SQLite**: Base de datos incorporada (incluida con Python)
- **django-crispy-forms**: Formularios elegantes y responsivos
- **crispy-bootstrap5**: Integración de crispy-forms con Bootstrap 5
- **Pillow**: Biblioteca de procesamiento de imágenes para ImageField

### Frontend
- **Bootstrap 5.3.7**: Framework CSS responsivo (CDN)
- **SweetAlert2**: Notificaciones elegantes (CDN)
- **JavaScript ES6**: Funcionalidades interactivas
- **CSS3**: Estilos personalizados

### Funcionalidades Django Utilizadas
- **Django ORM**: Para manejo de base de datos y modelos
- **Django Forms**: Formularios con validación híbrida
- **Django Auth**: Sistema de autenticación y usuarios
- **Django Admin**: Panel de administración
- **Django Templates**: Sistema de plantillas
- **Django Static Files**: Manejo de archivos estáticos
- **Django Test Framework**: Pruebas automatizadas
- **Django Management Commands**: Comandos personalizados para poblar datos

### Herramientas de Desarrollo
- **Django Debug Toolbar**: Para debugging en desarrollo (opcional)
- **Git**: Control de versiones
- **VS Code**: Editor recomendado con extensiones de Python y Django

## 📊 Modelos de Datos

### Principales Entidades (Implementadas)
- **Usuario**: Sistema completo de autenticación Django
- **PerfilUsuario**: Información extendida con foto y géneros favoritos
- **Película**: Catálogo completo con posters, banners e información detallada
- **Categoría**: Sistema de clasificación por géneros
- **Listas Personales**: Favoritos y "Ver más tarde" (ManyToMany)

### Entidades Creadas pero Sin Interfaz
- **Reseña**: Modelo completo para calificaciones (1-5 estrellas) y comentarios
- **Sistema de Puntuación**: Validación de rangos implementada

### Relaciones Implementadas
- Usuario → PerfilUsuario (1:1) ✅
- Usuario → Listas Personales (M:M) ✅  
- Película → Categoría (M:M) ✅
- Usuario → Reseña (1:N) ⚠️ *Modelo creado, interfaz pendiente*
- Película → Reseña (1:N) ⚠️ *Modelo creado, interfaz pendiente*

### Relaciones Pendientes
- Usuario → Foros (No implementado)
- Película → Comentarios (No implementado)
- Usuario → Seguimiento (No planificado)

## 🚀 Despliegue en Producción

### Configuraciones Recomendadas
1. **Variables de Entorno**: Usar archivos `.env` para secretos
2. **Base de Datos**: PostgreSQL para producción
3. **Archivos Estáticos**: Configurar servidor web (Nginx)
4. **SSL**: Implementar HTTPS
5. **Monitoreo**: Logs y métricas de rendimiento

### Checklist de Seguridad
- [ ] `DEBUG = False` en producción
- [ ] SECRET_KEY en variable de entorno
- [ ] ALLOWED_HOSTS configurado
- [ ] Configurar cabeceras de seguridad
- [ ] Backup automático de base de datos

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

- **Desarrollador**: Nathaniel Muller
- **GitHub**: [@NathanielMuller](https://github.com/NathanielMuller)
- **Proyecto**: [FilmScoperProyect](https://github.com/NathanielMuller/FilmScoperProyect)

## 🎯 Roadmap y Desarrollo Futuro

### 🚧 Próximas Implementaciones (Prioridad Alta)
- [ ] **Sistema de Reseñas Completo**: Interfaz para calificar y comentar películas
- [ ] **Búsqueda Funcional**: Backend para búsqueda por título, género, año
- [ ] **Sistema de Foros**: Discusiones por categorías y películas específicas
- [ ] **Notificaciones Completas**: Sistema integral de notificaciones

### 🎯 Funcionalidades Planificadas (Prioridad Media)
- [ ] **API REST**: Para posibles aplicaciones móviles
- [ ] **Sistema de Recomendaciones**: Sugerencias basadas en preferencias
- [ ] **Integración con APIs de Películas**: TMDB para datos actualizados
- [ ] **Filtros Avanzados**: Por año, director, duración, calificación
- [ ] **Sistema de Seguimiento**: Seguir a otros usuarios
- [ ] **Estadísticas de Usuario**: Dashboard personal con métricas

### 💡 Ideas Futuras (Prioridad Baja)
- [ ] **Chat en Tiempo Real**: Comunicación entre usuarios
- [ ] **Sistema de Logros**: Gamificación de la experiencia
- [ ] **Modo Oscuro/Claro**: Personalización de tema
- [ ] **Listas Colaborativas**: Listas compartidas entre usuarios
- [ ] **Sistema de Moderación Avanzado**: Reportes y moderación automática
- [ ] **Aplicación Móvil**: App nativa para iOS/Android

### 🛠️ Mejoras Técnicas Pendientes
- [ ] **Optimización de Base de Datos**: Índices y consultas optimizadas
- [ ] **Sistema de Cache**: Redis para mejor rendimiento
- [ ] **Logs y Monitoreo**: Sistema de logging completo
- [ ] **Tests de Integración**: Cobertura de testing al 90%+
- [ ] **Documentación de API**: Swagger/OpenAPI documentation
- [ ] **CI/CD Pipeline**: Automatización de despliegue

---

**FilmScoper - Proyecto en Desarrollo Activo 🚧**

*Este es un proyecto académico en desarrollo. Algunas funcionalidades mostradas en el diseño están pendientes de implementación. Consulta la sección "Alcance y Estado del Proyecto" para conocer qué está completamente funcional.*

**¡Gracias por explorar FilmScoper! 🍿**