from django.db import models
from django.core.exceptions import ValidationError


def validate_question_type(value):
    if value not in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('The question type is incorrect!')


OPTION_TYPES = ['CHOICE', 'MULTIPLE_CHOICE']


class Assessment(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(
        verbose_name='Описание теста',
        help_text='Введите описание теста',
    )


class Question(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,)
    type = models.CharField(max_length=30, validators=[validate_question_type])
    max_point = models.FloatField(default=1, verbose_name='Максимальный балл')
    text = models.TextField()

    @property
    def has_option_type(self):
        return self.type in OPTION_TYPES

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Choice(models.Model):
    """Вариант ответа"""
    question = models.ForeignKey(
        Question,
        related_name='choices',
        on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    text = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"


class Submission(models.Model):
    """Заполненный опрос"""
    user_id = models.PositiveIntegerField(db_index=True)
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE
    )
    submit_time = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    """Ответ на вопрос"""
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    questionType = models.CharField(max_length=30, validators=[validate_question_type])
    questionText = models.CharField(max_length=300)
    answerText = models.CharField(max_length=300)
