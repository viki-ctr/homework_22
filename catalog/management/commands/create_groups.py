from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product


class Command(BaseCommand):
    help = 'Creates moderator group with permissions'

    def handle(self, *args, **options):
        # Создаем группу
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Добавляем права
        content_type = ContentType.objects.get_for_model(Product)

        # Право на удаление любого продукта (стандартное Django-право)
        delete_permission = Permission.objects.get(codename='delete_product', content_type=content_type)
        group.permissions.add(delete_permission)

        # Кастомное право на отмену публикации
        unpublish_permission = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        group.permissions.add(unpublish_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана!'))
