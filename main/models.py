from django.db import models

# 1-BO'LIM: TESTLAR (O'zgarishsiz qoladi)
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    class Meta:
        verbose_name_plural = "Kategoriyalar"
    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Savol matni")
    option_1 = models.CharField(max_length=255, verbose_name="1 balli javob", null=True, blank=True)
    option_2 = models.CharField(max_length=255, verbose_name="2 balli javob", null=True, blank=True)
    option_3 = models.CharField(max_length=255, verbose_name="3 balli javob", null=True, blank=True)
    option_4 = models.CharField(max_length=255, verbose_name="4 balli javob", null=True, blank=True)
    option_5 = models.CharField(max_length=255, verbose_name="5 balli javob", null=True, blank=True)

class TestResult(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Foydalanuvchi ismi")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(verbose_name="Umumiy to'plagan balli")
    date = models.DateTimeField(auto_now_add=True)

# 2-BO'LIM: MODULLAR, MAVZULAR VA KONTENT BLOKLARI (Yangi ierarxiya)

class Module(models.Model):
    """ 7 ta asosiy modul uchun """
    title = models.CharField(max_length=255, verbose_name="Modul nomi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Modul"
        verbose_name_plural = "1. Asosiy Modullar"

    def __str__(self):
        return self.title

class Topic(models.Model):
    """ Har bir modul ichidagi darslar/mavzular """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics', verbose_name="Qaysi modulga tegishli")
    title = models.CharField(max_length=255, verbose_name="Mavzu nomi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Mavzu"
        verbose_name_plural = "2. Mavzular"

    def __str__(self):
        return f"{self.module.title} -> {self.title}"

class ContentBlock(models.Model):
    """ Mavzu ichidagi matnli bloklar (Kirish, Asosiy qism va h.k.) """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='blocks', verbose_name="Qaysi mavzuga tegishli")
    title = models.CharField(max_length=255, verbose_name="Blok sarlavhasi (masalan: Kirish qismi)")
    content = models.TextField(verbose_name="Asosiy matn/kontent")
    file = models.FileField(upload_to='modules/files/', null=True, blank=True, verbose_name="Word fayli (ixtiyoriy)")

    class Meta:
        verbose_name = "Kontent bloki"
        verbose_name_plural = "3. Mavzu bloklari"

    def __str__(self):
        return f"{self.topic.title} -> {self.title}"

# 3-BO'LIM: TAQDIMOTLAR (O'zgarishsiz qoladi)
class Presentation(models.Model):
    title = models.CharField(max_length=255, verbose_name="Taqdimot nomi")
    file = models.FileField(upload_to='presentations/', verbose_name="Fayl (PDF/PPTX)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title