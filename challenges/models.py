from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Notebook(models.Model):
    brand = models.CharField(
        max_length=100,
        choices=[("Apple", "Apple"), ("HP", "HP"), ("Lenovo", "Lenovo"), ("Asus", "Asus"), ("Acer", "Acer")],
        default="Apple"
    )
    issue_year = models.IntegerField()
    ram = models.CharField(max_length=10)
    hdd = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)


class BlogPost(models.Model):
    """
    В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
    (опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).
    """
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=256)
    author_name = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=[("published", "Published"), ("unpublished", "Unpublished"), ("banned", "Banned")],
        default="unpublished"
    )
    creation_date = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField()
    category = models.CharField(
        max_length=50,
        choices=[("general", "general"), ("programming", "programming"), ("sport", "sport"), ("food", "food")],
        default=None
    )
