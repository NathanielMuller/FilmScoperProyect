from django.core.management.base import BaseCommand
from core.models import Categoria, ForoCategoria

class Command(BaseCommand):
    help = 'Crear foros para todas las categorías existentes'

    def handle(self, *args, **options):
        self.stdout.write('Creando foros para categorías...')
        
        categorias = Categoria.objects.all()
        foros_creados = 0
        
        for categoria in categorias:
            foro, created = ForoCategoria.objects.get_or_create(
                categoria=categoria,
                defaults={
                    'descripcion': f'Foro de discusión para películas de {categoria.nombre.lower()}. Comparte tus opiniones, recomendaciones y debates sobre este género.',
                    'activo': True
                }
            )
            
            if created:
                foros_creados += 1
                self.stdout.write(f'  ✓ Foro creado para: {categoria.nombre}')
            else:
                self.stdout.write(f'  - Foro ya existe para: {categoria.nombre}')
        
        self.stdout.write(
            self.style.SUCCESS(f'¡Proceso completado! Se crearon {foros_creados} foros nuevos.')
        )