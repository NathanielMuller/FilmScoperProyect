# Roadmap FilmScoper - Implementación API REST

## 🎬 Contexto del Proyecto

**FilmScoper** será una aplicación web de reseñas y descubrimiento de películas que cumple con todos los requerimientos de la actividad sumativa. El proyecto se enfocará en crear una plataforma donde los usuarios puedan descubrir, reseñar y calificar películas, con integración de APIs externas de cine y APIs propias para compartir datos.

---

## 🗺️ Roadmap de Implementación

### Fase 1: Configuración Base y Infraestructura (Semana 1)

#### 🔧 Configuración del Entorno
- **Día 1-2:**
  - [ ] Configurar proyecto Django con estructura modular
  - [ ] Configurar conexión con Oracle Database
  - [ ] Setup inicial de Git y estructura de carpetas
  - [ ] Configurar entorno virtual Python

#### 🎨 Identidad Visual y Branding
- **Día 3:**
  - [ ] Diseñar logo de FilmScoper
  - [ ] Definir paleta de colores (azul oscuro, dorado, blanco)
  - [ ] Seleccionar tipografías
  - [ ] Crear wireframes básicos de la interfaz

### Fase 2: Base de Datos y Modelos (Semana 1-2)

#### 📊 Diseño de Base de Datos (Mínimo 6 tablas)
- **Día 4-5:**
  - [ ] **Tabla Users:** usuarios del sistema
  - [ ] **Tabla Roles:** roles de usuario (Admin, Crítico, Usuario Regular)
  - [ ] **Tabla Movies:** información de películas
  - [ ] **Tabla Reviews:** reseñas de usuarios
  - [ ] **Tabla Ratings:** calificaciones numéricas
  - [ ] **Tabla Categories:** géneros cinematográficos
  - [ ] **Tabla Favorites:** películas favoritas por usuario
  - [ ] **Tabla Comments:** comentarios en reseñas

#### 🏗️ Implementación de Modelos Django
- **Día 6-7:**
  - [ ] Crear modelos Django correspondientes
  - [ ] Configurar relaciones entre modelos
  - [ ] Crear migraciones
  - [ ] Implementar scripts de datos iniciales

### Fase 3: Sistema de Autenticación y Usuarios (Semana 2)

#### 🔐 Autenticación Base
- **Día 8-10:**
  - [ ] Implementar sistema de login/logout
  - [ ] Crear página de registro con validaciones
  - [ ] Implementar recuperación de contraseña
  - [ ] Sistema de roles y permisos

#### 👤 Gestión de Usuarios
- **Día 11-12:**
  - [ ] Página de perfil de usuario
  - [ ] Edición de perfil
  - [ ] Validaciones de contraseña (4 criterios mínimo):
    - Longitud mínima 8 caracteres
    - Al menos un carácter especial
    - Al menos un número
    - Al menos una letra mayúscula

### Fase 4: Frontend Responsive (Semana 2-3)

#### 📱 Desarrollo de Interfaz
- **Día 13-16:**
  - [ ] Implementar Bootstrap 5 con sistema de grid
  - [ ] Crear layout base responsive (3 breakpoints mínimo)
  - [ ] Desarrollar componentes reutilizables
  - [ ] Implementar navegación principal

#### 🖥️ Páginas Principales
- **Día 17-19:**
  - [ ] Página de inicio (dashboard)
  - [ ] Catálogo de películas
  - [ ] Página de detalles de película
  - [ ] Página de perfil de usuario
  - [ ] Páginas de autenticación (login, registro, recover)

### Fase 5: APIs REST Propias (Semana 3-4)

#### 🔌 API REST 1: Movies API
- **Día 20-22:**
  - [ ] **GET /api/movies/** - Listar todas las películas
  - [ ] **GET /api/movies/{id}/** - Obtener película específica
  - [ ] **POST /api/movies/** - Crear nueva película (solo admin)
  - [ ] **PUT/PATCH /api/movies/{id}/** - Actualizar película
  - [ ] **DELETE /api/movies/{id}/** - Eliminar película
  - [ ] Implementar paginación y filtros
  - [ ] Documentación con Django REST Framework

#### 🔌 API REST 2: Reviews API
- **Día 23-25:**
  - [ ] **GET /api/reviews/** - Listar reseñas
  - [ ] **GET /api/reviews/{id}/** - Obtener reseña específica
  - [ ] **POST /api/reviews/** - Crear nueva reseña
  - [ ] **PUT/PATCH /api/reviews/{id}/** - Actualizar reseña
  - [ ] **DELETE /api/reviews/{id}/** - Eliminar reseña
  - [ ] **GET /api/movies/{id}/reviews/** - Reseñas por película
  - [ ] Implementar validaciones y permisos

### Fase 6: Consumo de APIs Externas (Semana 4)

#### 🌐 API Externa 1: TMDB (The Movie Database)
- **Día 26-27:**
  - [ ] Configurar integración con TMDB API
  - [ ] Implementar búsqueda de películas externas
  - [ ] Importar información de películas populares
  - [ ] Mostrar trailers y posters desde TMDB
  - [ ] Página dedicada "Descubrir Películas"

#### 🌐 API Externa 2: OMDb API o Similar
- **Día 28-29:**
  - [ ] Configurar segunda API de películas
  - [ ] Implementar comparación de ratings
  - [ ] Mostrar información adicional (awards, box office)
  - [ ] Página "Estadísticas de Cine"

### Fase 7: Funcionalidades Específicas del Dominio (Semana 5)

#### 🎭 Sistema de Reseñas y Calificaciones
- **Día 30-32:**
  - [ ] Crear/editar reseñas de películas
  - [ ] Sistema de calificación por estrellas (1-5)
  - [ ] Comentarios en reseñas
  - [ ] Sistema de likes en reseñas
  - [ ] Moderación de contenido

#### 📋 Sistema de Listas y Favoritos
- **Día 33-34:**
  - [ ] Listas personalizadas de películas
  - [ ] Sistema de favoritos
  - [ ] Watchlist (películas por ver)
  - [ ] Historial de películas vistas

#### 🏆 Gamificación y Social
- **Día 35-36:**
  - [ ] Sistema de badges para usuarios activos
  - [ ] Rankings de mejores críticos
  - [ ] Seguimiento entre usuarios
  - [ ] Feed de actividad

### Fase 8: Funcionalidades Administrativas (Semana 5-6)

#### ⚙️ Panel de Administración
- **Día 37-39:**
  - [ ] Dashboard administrativo
  - [ ] CRUD completo de películas
  - [ ] Gestión de usuarios y roles
  - [ ] Moderación de reseñas
  - [ ] Estadísticas del sistema

#### 📊 Reportes y Analytics
- **Día 40-41:**
  - [ ] Reportes de actividad de usuarios
  - [ ] Estadísticas de películas más populares
  - [ ] Métricas de engagement
  - [ ] Exportación de datos

### Fase 9: Seguridad y Validaciones (Semana 6)

#### 🛡️ Implementación de Seguridad
- **Día 42-44:**
  - [ ] Validaciones completas en formularios
  - [ ] Protección CSRF
  - [ ] Sanitización de inputs
  - [ ] Rate limiting en APIs
  - [ ] Manejo de errores 404/500 personalizados

#### 🔒 Autorización y Permisos
- **Día 45:**
  - [ ] Middleware de autenticación
  - [ ] Decoradores de permisos
  - [ ] Protección de URLs sensibles
  - [ ] Logs de seguridad

### Fase 10: Testing y Optimización (Semana 7)

#### 🧪 Testing
- **Día 46-48:**
  - [ ] Tests unitarios para modelos
  - [ ] Tests de APIs REST
  - [ ] Tests de integración
  - [ ] Tests de interfaz (Selenium básico)

#### ⚡ Optimización
- **Día 49-50:**
  - [ ] Optimización de queries de base de datos
  - [ ] Implementar caché básico
  - [ ] Optimización de imágenes
  - [ ] Minificación de CSS/JS

### Fase 11: Despliegue y Documentación (Semana 7-8)

#### 📚 Documentación
- **Día 51-52:**
  - [ ] Documentación de APIs REST
  - [ ] Manual de usuario
  - [ ] Documentación técnica
  - [ ] README detallado del proyecto

#### 🚀 Preparación para Entrega
- **Día 53-56:**
  - [ ] Testing final en diferentes dispositivos
  - [ ] Preparación de scripts de BD
  - [ ] Creación de datos de prueba
  - [ ] Empaquetado final del proyecto

---

## 🎯 Funcionalidades Específicas por Rol

### 👑 Administrador
- Gestión completa de películas, usuarios y contenido
- Acceso a panel de administración
- Moderación de reseñas y comentarios
- Visualización de estadísticas y reportes

### 🎭 Crítico de Cine
- Creación de reseñas destacadas
- Acceso a funcionalidades avanzadas de análisis
- Badge especial en reseñas
- Prioridad en el feed de actividad

### 👤 Usuario Regular
- Creación de reseñas y calificaciones
- Gestión de listas personales
- Interacción social básica
- Acceso a funcionalidades de descubrimiento

---

## 🔧 Stack Tecnológico

### Backend
- **Framework:** Django 4.x
- **Base de Datos:** Oracle
- **API:** Django REST Framework
- **Autenticación:** Django Authentication + JWT para APIs

### Frontend
- **CSS Framework:** Bootstrap 5
- **JavaScript:** Vanilla JS + jQuery
- **Icons:** Font Awesome
- **Responsive:** Mobile-first approach

### APIs Externas
- **TMDB API:** Información de películas, trailers, imágenes
- **OMDb API:** Ratings adicionales y información complementaria

### Herramientas de Desarrollo
- **Control de Versiones:** Git
- **Entorno:** Python Virtual Environment
- **Testing:** Django TestCase + Coverage

---

## 📋 Entregables Finales

### Código Fuente
- [ ] Proyecto Django completo
- [ ] Estructura modular y bien organizada
- [ ] Comentarios y documentación en código
- [ ] Requirements.txt actualizado

### Base de Datos
- [ ] Script de creación de BD (Oracle)
- [ ] Script de datos iniciales
- [ ] Modelo de datos documentado
- [ ] Triggers y procedimientos si es necesario

### Documentación
- [ ] Manual de instalación
- [ ] Documentación de APIs
- [ ] Manual de usuario
- [ ] Guía de desarrollo

---

## 🚨 Consideraciones Importantes

1. **Priorización:** Funcionalidades core primero, features avanzadas después
2. **Testing Continuo:** Probar cada feature mientras se desarrolla
3. **Responsive Design:** Validar en móvil, tablet y desktop constantemente
4. **Performance:** Mantener tiempos de carga bajos
5. **Seguridad:** Implementar desde el inicio, no al final
6. **APIs:** Documentar endpoints mientras se desarrollan
7. **Git:** Commits frecuentes y descriptivos
8. **Backup:** Respaldos regulares de BD durante desarrollo

¡Con este roadmap FilmScoper cumplirá todos los requerimientos de la actividad mientras ofrece una experiencia de usuario excepcional! 🎬✨