# FilmScoper 🎬

## 🔑 Usuarios de Prueba Disponibles

### Para Evaluación y Testing
El proyecto incluye usuarios pre-configurados para facilitar la evaluación:

| Usuario | Email | Tipo | Contraseña | Descripción |
|---------|-------|------|------------|-------------|
| `admin` | admin@filmscoper.com | **Administrador** | Adminx123. | Acceso completo al panel admin `/admin/` |
| `User1` | Emailejemplo@filmscoper.com | Usuario normal | Prueba123x. | Usuario estándar con datos de prueba |

### 🎯 Accesos Rápidos
- **Panel de Administración**: http://127.0.0.1:8000/admin/
- **Aplicación Principal**: http://127.0.0.1:8000/
- **Categorías**: Cada categoría tiene películas pre-cargadas
- **Listas Personales**: Los usuarios tienen favoritos y listas configuradas

### 📝 Datos de Prueba Incluidos
- ✅ **26 películas activas** distribuidas en 5 categorías (29 total, 3 desactivadas)
- ✅ **22 calificaciones oficiales** (IMDb) pre-cargadas
- ✅ **10+ reseñas de usuarios** con calificaciones activas
- ✅ **Sistema de comentarios avanzado** con límites por usuario y respuestas anidadas
- ✅ **5 foros por categoría** auto-generados
- ✅ **Usuarios con perfiles** completos y géneros favoritos
- ✅ **Listas personalizadas** con películas agregadas
- ✅ **Imágenes y contenido** listo para usar

---

## Descripción

FilmScoper es una plataforma web moderna desarrollada con Django que permite a los usuarios descubrir, explorar y calificar películas. El proyecto integra funcionalidades avanzadas de gestión de usuarios, sistema de reseñas, categorización de películas y una interfaz de usuario elegante con Bootstrap 5.

## 🚀 Últimas Mejoras Implementadas (Octubre 2025)

### 🔧 Sistema de Comentarios Avanzado
- **Límites Inteligentes**: 5 comentarios padre + 10 respuestas por usuario por película
- **Rotación Automática**: Los comentarios rotan cada 5 segundos con controles de pausa/play
- **Interfaz Mejorada**: Botones compactos, diseño responsivo y formularios optimizados
- **Validación Robusta**: Corrección de errores de formularios y redirecciones
- **Threading Completo**: Respuestas anidadas con identificación clara del usuario

### 🎨 Mejoras de UI/UX
- **Botones Compactos**: Tamaño `btn-sm` para favoritos, listas y calificaciones
- **Calificación Integrada**: Estrellas posicionadas debajo de los botones de acción
- **Diseño Responsive**: Optimizado para dispositivos móviles y desktop
- **Mensajes de Confirmación**: Feedback inmediato para todas las acciones del usuario

### 🐛 Correcciones Técnicas
- **URLs Corregidas**: Solucionados errores `NoReverseMatch` en redirecciones
- **Formularios Sincronizados**: Campos de formulario alineados entre templates y vistas
- **Base de Datos Optimizada**: Películas activas/inactivas gestionadas correctamente
- **Validación de Estado**: Verificación de límites y permisos antes de acciones

---

## 🎯 Alcance y Estado del Proyecto

### ✅ Funcionalidades Completamente Implementadas
- [x] **Catálogo de Películas**: Navegación por categorías (Acción, Comedia, Documentales, Romance, Terror)
- [x] **Sistema de Usuarios**: Registro, login, logout con validaciones completas
- [x] **Perfil de Usuario**: Gestión de información personal, foto de perfil y géneros favoritos
- [x] **Base de Datos**: 26 películas activas distribuidas en 5 categorías (29 total)
- [x] **Paginación**: Navegación optimizada en listados (12 películas por página)
- [x] **Interfaz Responsiva**: Compatible con dispositivos móviles y desktop con diseño Bootstrap 5
- [x] **Listas Personalizadas**: Sistema de favoritos y "Ver más tarde" completamente funcional
- [x] **Sistema de Reseñas y Calificaciones**: Interfaz completa para calificar películas (1-5 estrellas) con AJAX integrado
- [x] **Sistema Doble de Calificaciones**: IMDb/Oficial + Promedio FilmScoper en tarjetas y detalles
- [x] **Sistema Avanzado de Comentarios**: 
  - Límites por usuario: 5 comentarios padre + 10 respuestas por película
  - Respuestas anidadas con threading completo
  - Rotación automática de comentarios con controles manuales
  - Validación completa de formularios con corrección de errores
  - Interfaz compacta con botones pequeños y diseño optimizado
- [x] **Sistema de Foros**: Modelos de datos y estructura backend para foros por categorías
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
- [ ] **Interfaz de Foros**: Templates y vistas para navegación de foros (backend completo)
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
python manage.py poblar_calificaciones
python manage.py crear_foros
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
2. **Exploración**: Navegar por categorías de películas con calificaciones duales
3. **Calificación**: Puntuar películas del 1-5 estrellas con interfaz AJAX integrada
4. **Comentarios Avanzados**: 
   - Escribir hasta 5 comentarios principales por película
   - Responder hasta 10 veces por película con comentarios anidados
   - Sistema de rotación automática de comentarios con controles manuales
   - Formularios con validación completa y mensajes de confirmación
5. **Perfil**: Personalizar información personal y foto de perfil
6. **Listas Personalizadas**: Agregar/quitar películas de favoritos y "ver más tarde" con notificaciones
7. **Visualización Mejorada**: Ver detalles completos con ratings oficiales vs. comunidad, botones compactos y diseño responsive

### Para Administradores
1. **Panel Admin**: Acceder a `/admin/` con credenciales de superusuario
2. **Gestión de Contenido**: Agregar/editar películas y categorías
3. **Gestión de Usuarios**: Administrar cuentas y perfiles
4. **Comandos**: Usar comandos personalizados para poblar datos

### ⚠️ Limitaciones Actuales
- **Sin Búsqueda Funcional**: El buscador no procesa consultas
- **Sin Interfaz de Foros**: Backend completo pero sin templates de navegación
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
- **Bootstrap 5.3.7**: Framework CSS responsivo con diseño compacto y botones optimizados
- **SweetAlert2**: Notificaciones elegantes para confirmaciones de acciones
- **JavaScript ES6**: 
  - Funcionalidades interactivas avanzadas
  - Sistema de rotación de comentarios con auto-play
  - Controles dinámicos para formularios de respuesta
  - Validación client-side integrada
- **CSS3**: Estilos personalizados con diseño responsive

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

### Entidades Implementadas Completamente
- **Reseña**: Sistema completo de calificaciones (1-5 estrellas) con interfaz AJAX integrada
- **ComentarioPelicula**: Sistema avanzado de comentarios múltiples con límites por usuario (5+10), respuestas anidadas, rotación automática y validación completa
- **ForoCategoria/TemaDeForo/RespuestaForo**: Estructura completa de foros (sin interfaz)

### Relaciones Implementadas
- Usuario → PerfilUsuario (1:1) ✅
- Usuario → Listas Personales (M:M) ✅  
- Película → Categoría (M:M) ✅
- Usuario → Reseña (1:N) ✅ *Interfaz completa con AJAX*
- Película → Reseña (1:N) ✅ *Promedio automático*
- Usuario → ComentarioPelicula (1:N) ✅ *Sistema avanzado con límites (5 padre + 10 respuestas)*
- Película → ComentarioPelicula (1:N) ✅ *Threading completo con rotación y validación*
- Categoría → ForoCategoria (1:1) ✅ *Backend completo*

### Relaciones Pendientes
- Usuario → Seguimiento (No planificado)
- Usuario → Notificaciones (No implementado)
- Película → Recomendaciones (No implementado)

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
- [ ] **Interfaz de Foros**: Templates para navegación, creación de temas y moderación
- [ ] **Búsqueda Funcional**: Backend para búsqueda por título, género, año con filtros avanzados
- [ ] **Sistema de Moderación**: Reportes de comentarios, administración de contenido y moderación automática
- [x] ~~**Sistema de Comentarios Avanzado**: Límites, rotación y threading~~ ✅ **COMPLETADO**

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