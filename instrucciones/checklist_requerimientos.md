# Checklist de Requerimientos - API REST

## ✅ Aspectos Generales del Proyecto

### Organización y Colaboración
- [ ] Formar equipo de trabajo
- [ ] Definir y aprobar tema de la aplicación
- [ ] Configurar repositorio GIT para colaboración
- [ ] Establecer herramientas colaborativas del equipo

### Entregables
- [ ] Crear archivo comprimido (.zip o .7-zip) con:
  - [ ] Código fuente de la aplicación
  - [ ] Script de la base de datos
  - [ ] Script con datos iniciales de las tablas

## ✅ Frontend y UI/UX

### Tecnologías y Responsive Design
- [ ] Implementar HTML en versión actual
- [ ] Implementar CSS en versión actual
- [ ] Implementar Bootstrap en versión actual
- [ ] Implementar JavaScript/jQuery en versiones actuales
- [ ] Crear interfaz adaptada a mínimo 3 tamaños de pantalla
- [ ] Usar GRID de 12 columnas (Bootstrap)

### Páginas Obligatorias
- [ ] Página de inicio de sesión
- [ ] Página de registro de usuarios
- [ ] Página de recuperar contraseña
- [ ] Página de modificación de perfil
- [ ] Páginas internas según funcionalidades del tema elegido

### Validaciones Frontend
- [ ] Validaciones en todos los formularios
- [ ] Validaciones correspondientes para cada campo
- [ ] Validaciones de contraseña con mínimo 4 criterios:
  - [ ] Longitud mínima
  - [ ] Caracteres especiales
  - [ ] Números obligatorios
  - [ ] Letras obligatorias
  - [ ] Longitud máxima (opcional)

## ✅ Backend y Lógica de Negocio

### Framework y Tecnología
- [ ] Implementar backend con Framework Django
- [ ] Configurar correctamente el entorno Django
- [ ] Estructura de proyecto Django organizada

### Sistema de Autenticación y Usuarios
- [ ] Lógica de inicio de sesión implementada
- [ ] Sistema de autenticación funcional
- [ ] Mínimo 2 roles de usuario con privilegios diferentes
- [ ] Funcionalidad de creación de usuarios
- [ ] Funcionalidad de modificación de usuarios
- [ ] Funcionalidad de eliminación de usuarios
- [ ] Seguridad de acceso a URLs mediante autenticación

### Lógica de la Aplicación
- [ ] Implementar solución lógica según el tema elegido
- [ ] Desarrollar funcionalidades específicas del dominio
- [ ] Manejar casos de uso principales del sistema

## ✅ Base de Datos

### Configuración y Estructura
- [ ] Configurar Oracle como manejador de base de datos
- [ ] Crear mínimo 6 tablas en la base de datos
- [ ] Diseñar relaciones adecuadas entre tablas
- [ ] Implementar claves primarias y foráneas
- [ ] Crear script de creación de base de datos
- [ ] Crear script con datos iniciales

## ✅ APIs y Servicios Web

### APIs REST Propias
- [ ] Desarrollar mínimo 2 APIs REST propias
- [ ] Documentar endpoints de las APIs
- [ ] Implementar métodos HTTP apropiados (GET, POST, PUT, DELETE)
- [ ] Configurar serialización de datos
- [ ] Manejar respuestas JSON correctamente
- [ ] Implementar manejo de errores en APIs

### Consumo de Servicios Externos
- [ ] Identificar 2 servicios web externos públicos relacionados al tema
- [ ] Implementar consumo del primer servicio externo
- [ ] Implementar consumo del segundo servicio externo
- [ ] Mostrar información de servicios externos en páginas internas
- [ ] Mantener lógica de desarrollo al integrar servicios externos
- [ ] Manejar errores de conexión con servicios externos

## ✅ Funcionalidades Específicas por Tema

### Ventas o Arriendos
- [ ] Carrito de compras
- [ ] Registro/modificación de productos
- [ ] Manejo de inventario
- [ ] Monitoreo de compras por usuario
- [ ] Mantenedores para clientes
- [ ] Mantenedores para usuarios
- [ ] Mantenedores para productos

### Foros
- [ ] Secciones de foro
- [ ] Comentarios identificados por usuario
- [ ] Sistema de valoraciones
- [ ] Monitoreo de temas por usuario
- [ ] Mantenedor para baneo de comentarios/temas
- [ ] Mantenedores para usuarios
- [ ] Mantenedores para secciones

### Servicios
- [ ] Generación de órdenes de servicio
- [ ] Modificación/eliminación de órdenes
- [ ] Monitoreo de equipos en servicio
- [ ] Ruta de procesos internos
- [ ] Mantenedores para usuarios
- [ ] Mantenedores para servicios
- [ ] Mantenedores para montos
- [ ] Mantenedores para tipos de servicios

### Consultas Médicas/Reservas
- [ ] Mantenedor para especialistas
- [ ] Mantenedor para usuarios
- [ ] Mantenedor para clientes/pacientes
- [ ] Reservar horas
- [ ] Modificar reservas
- [ ] Eliminar reservas
- [ ] Sistema de atención médica
- [ ] Manejo de cobros
- [ ] Historial médico
- [ ] Visualización de reservas por médicos
- [ ] Visualización de atenciones por pacientes

## ✅ Aspectos de Seguridad y Calidad

### Seguridad
- [ ] Validación de datos de entrada
- [ ] Protección contra inyección SQL
- [ ] Manejo seguro de sesiones
- [ ] Encriptación de contraseñas
- [ ] Validación de permisos por rol

### Testing y Calidad
- [ ] Pruebas de funcionalidad básica
- [ ] Validación de responsive design
- [ ] Pruebas de APIs REST
- [ ] Verificación de consumo de servicios externos
- [ ] Pruebas de autenticación y autorización

## ✅ Elementos de Identidad

### Diseño y Branding
- [ ] Definir colores del proyecto
- [ ] Crear/seleccionar logo
- [ ] Definir nombre del proyecto
- [ ] Seleccionar imágenes apropiadas
- [ ] Mantener originalidad en el diseño

## ✅ Simulaciones y Casos Especiales

### Pagos (si aplica)
- [ ] NO implementar sistemas de pago reales
- [ ] Crear página de simulación de pago exitoso
- [ ] Implementar flujo de pago falso pero funcional

---

## 📋 Notas de Implementación

- Los casos pueden ser similares pero no iguales entre equipos
- Subir información del tema al AVA para recibir sugerencias del docente
- Mantener originalidad aunque se guíen de páginas existentes
- Documentar el proceso de desarrollo en el repositorio GIT