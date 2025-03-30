from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Очищает базу и добавляет тестовые продукты и категории'

    def handle(self, *args, **options):
        self.stdout.write("Удаление старых данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Создание категорий...")
        categories = [
            Category(name="Электроника", description="Гаджеты и устройства"),
            Category(name="Книги", description="Художественная литература"),
            Category(name="Одежда", description="Мужская и женская одежда"),
        ]
        Category.objects.bulk_create(categories)

        self.stdout.write("Создание продуктов...")
        products = []
        category_ids = list(Category.objects.values_list('id', flat=True))

        for i in range(1, 21):  # Создаем 20 тестовых продуктов
            products.append(Product(
                name=f"Тестовый продукт {i}",
                description=f"Описание тестового продукта {i}",
                cost=random.randint(100, 10000),
                category_id=random.choice(category_ids),
                created_at=date.today() - timedelta(days=random.randint(0, 365)),
                updated_at=date.today() - timedelta(days=random.randint(0, 30)),
            ))

        Product.objects.bulk_create(products)

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано: "
                               f"{Category.objects.count()} категорий и "
                               f"{Product.objects.count()} продуктов")
        )
