from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
# Yangi modellarni import qilamiz: Topic va ContentBlock
from .models import Category, Question, TestResult, Module, Topic, ContentBlock, Presentation
from .forms import QuestionForm

# --- ASOSIY SAHIFA ---
def home(request):
    categories = Category.objects.all()
    return render(request, 'main/home.html', {'categories': categories})

# --- TESTLAR BO'LIMI ---
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

def take_test(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = category.questions.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        total_score = 0
        for q in questions:
            answer_value = request.POST.get(f'question_{q.id}')
            if answer_value:
                total_score += int(answer_value)

        result = TestResult.objects.create(
            full_name=full_name,
            category=category,
            score=total_score
        )
        return render(request, 'main/test_success.html', {'result': result})

    return render(request, 'main/take_test.html', {'category': category, 'questions': questions})

# --- MODULLAR VA MAVZULAR (Yangi struktura) ---
def module_list(request):
    # 'prefetch_related' yordamida Modul -> Topic -> ContentBlock zanjirini
    # bazaga ortiqcha yuk tushirmasdan bittada olib kelamiz
    modules = Module.objects.prefetch_related('topics__blocks').all()
    return render(request, 'main/module_list.html', {'modules': modules})

# --- TAQDIMOTLAR ---
def presentation_list(request):
    presentations = Presentation.objects.all()
    return render(request, 'main/presentation_list.html', {'presentations': presentations})

# --- ADMIN PANEL FUNKSIYALARI ---
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def manage_questions(request):
    questions = Question.objects.all()
    return render(request, 'main/manage_questions.html', {'questions': questions})

@user_passes_test(is_admin)
def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_questions')
    else:
        form = QuestionForm()
    return render(request, 'main/question_form.html', {'form': form})

@user_passes_test(is_admin)
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('manage_questions')

@user_passes_test(is_admin)
def test_results_list(request):
    # Faqat adminlar kira oladi
    results = TestResult.objects.select_related('category').all().order_by('-date')
    return render(request, 'main/test_results_list.html', {'results': results})