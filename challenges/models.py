from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(models.Model):
    BRANDS = [
        ("APPLE", "APPLE"),
        ("SAMSUNG", "SAMSUNG"),
        ("HUAWEI", "HUAWEI"),
        ("ASUS", "ASUS"),
        ("LENOVO", "LENOVO"),
    ]
    model = models.CharField(max_length=20)
    brand = models.CharField(max_length=10, choices=BRANDS)
    year_of_manufacture = models.SmallIntegerField()
    memory_size = models.IntegerField()
    hard_disk_size = models.IntegerField()
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    date_is_added = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            "model": self.model,
            "brand": self.brand,
            "year_of_manufacture": self.year_of_manufacture,
            "memory_size": self.memory_size,
            "hard_disk_size": self.hard_disk_size,
            "price": self.price,
            "quantity": self.quantity,
        }

    def __str__(self):
        return f"we have {self.quantity} laptop {self.model} by {self.brand} ({self.year_of_manufacture}) with price {self.price}"


class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS = [
        ("published", "Published"),
        ("unpublished", "Unpublished"),
        ("banned", "Banned"),
    ]

    title = models.CharField(max_length=256)
    text = models.TextField(max_length=1000)
    author_full_name = models.CharField(max_length=256)
    status = models.CharField(max_length=12, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )

    def to_json(self):
        return {
            "title": self.title,
            "text": self.text,
            "author_full_name": self.author_full_name,
            "status": self.status,
            "created_at": self.created_at,
            "published_at": self.published_at,
            "category": self.category.name if self.category else None,
        }

    def __str__(self):
        return f"{self.title} in {self.category} by {self.author_full_name}"
