from django.contrib import admin
from .models import Category, Question, TestResult, Module, Topic, ContentBlock, Presentation

# --- 1. TESTLAR BO'LIMI ---
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'category')
    list_filter = ('category',)
    search_fields = ('text',)

    def text_short(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_short.short_description = "Savol matni"

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'score', 'date')
    readonly_fields = ('full_name', 'category', 'score', 'date')
    list_filter = ('category', 'date')
    search_fields = ('full_name',)

# --- 2. MODULLAR VA MAVZULAR IERARXIYASI ---

class ContentBlockInline(admin.StackedInline):
    """ Mavzu ichida matnli bloklarni qo'shish uchun """
    model = ContentBlock
    extra = 1
    fields = ('title', 'content', 'file')

class TopicInline(admin.TabularInline):
    """ Modul ichida mavzularni ro'yxat ko'rinishida qo'shish uchun """
    model = Topic
    extra = 1
    show_change_link = True # Mavzuning o'ziga o'tib matn yozish uchun havola

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    inlines = [TopicInline]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module',)
    list_editable = ('order',)
    inlines = [ContentBlockInline]

# --- 3. MODELLARNI RO'YXATDAN O'TKAZISH ---
admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(ContentBlock) # Matnlarni alohida tahrirlash uchun ham
admin.site.register(Presentation)