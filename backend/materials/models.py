from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DateTimeField
from django.db.models.deletion import CASCADE

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Тег',
        help_text='Укажите тег',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг тега',
        help_text='Здесь слаг тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.title}'


class Price(models.Model):
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0.00,
        verbose_name='Стоимость скачивания',
        help_text='Укажите стоимость скачивания',
    )
    measurement_unit = models.CharField(max_length=10,
                                        verbose_name='Валюта платежа',
                                        help_text='Введите валюту платежа',)

    class Meta:
        verbose_name = 'Стоимость'
        verbose_name_plural = 'Стоимость'

    def __str__(self):
        return f'{self.amount} {self.measurement_unit}'


class Material(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите заголовок документа',
    )
    author = models.ForeignKey(
        related_name='materials',
        to=User,
        on_delete=CASCADE,
        verbose_name='Автор документа',
        help_text='Укажите автора документа'
    )
    description = models.TextField(
        verbose_name='Описание документа',
        help_text='Введите описание документа',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    price = models.ManyToManyField(
        related_name='materials',
        to=Price,
        verbose_name='Стоимость материала',
        help_text='Укажите стоимость материала'
    )
    preview = models.ImageField(
        upload_to='materials/',
        null=True,
        verbose_name='Превью файла',
        help_text='Загрузите фото',
    )
    file = models.FileField(
        upload_to='materials/',
        null=True,
        verbose_name='Файл',
        help_text='Загрузите файл',
    )
    tags = models.ManyToManyField(
        related_name='materials',
        to=Tag,
        verbose_name='Теги',
        help_text='Здесь теги', )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.title


class Favorite(models.Model):
    """Модель избранных материалов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Файл'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'material'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.material}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик на автора материала'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Автор',
        help_text='Автор материала'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_object'
        )]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    material = models.ForeignKey(
        Material,
        verbose_name='Материалы',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
