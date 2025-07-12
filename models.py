from django.db import models

# Create your models here.
class InfoUser(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField()
    image = models.ImageField(upload_to='infouser/', verbose_name="Фотография")
    work = models.CharField(max_length=255, verbose_name="Работа")
    description = models.TextField(verbose_name="Описание")
    twitter = models.URLField(verbose_name="Твиттер")
    telegram = models.URLField(verbose_name="Телеграм")
    linkedin = models.URLField(verbose_name="Линкед Ин")
    github = models.URLField(verbose_name="Гитхаб")
    
    def __str__(self):
        return f"{self.id} / {self.name} / {self.email} / {self.work}"
    
    class Meta:
        verbose_name = "Информация о пользователе"
        verbose_name_plural = "Информация о пользователях"

class Services(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")

    def __str__(self):
        return f"ID: {self.id} || Title: {self.title}"
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Experience(models.Model):
    start_year = models.IntegerField(verbose_name="Начало опыта")
    last_year = models.IntegerField(verbose_name="ٌКонец опыта")
    work = models.CharField(max_length=255, verbose_name="Должность")
    location = models.CharField(max_length=255, verbose_name="Локация")

    def __str__(self):
        return f"ID: {self.id} || Начало и конец опыта: {self.start_year}-{self.last_year} || Должность: {self.work}"
    
    class Meta:
        verbose_name = 'Год опыта'
        verbose_name_plural = 'Годы опыта'




class Education(models.Model):
    start_year = models.IntegerField(verbose_name="Начало обучения")
    last_year = models.IntegerField(verbose_name="ٌКонец обучения")
    work = models.CharField(max_length=255, verbose_name="напрвление")
    location = models.CharField(max_length=255, verbose_name="учебное учереждение")

    def __str__(self):
        return f"ID: {self.id} || Начало и конец обучения: {self.start_year}-{self.last_year} || Напрвление: {self.work}"
    
    class Meta:
        verbose_name = 'Год обучения'
        verbose_name_plural = 'Годы обучения'



class Resume(models.Model):
    experience = models.IntegerField(verbose_name = "опыт")
    completed_projects = models.ChargerField(max_length=255, verbose_name = "ٌзавешенные проекты")
    happy_clients = models.CharField(max_length = 255, verbose_name = "довольные клиенты")
    

    def __str__(self):
        return f"ID: {self.id} || Опыт: {self.experience} || Завешенные проекты: {self.completed_projects}"
    
    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Завершенные проекты'