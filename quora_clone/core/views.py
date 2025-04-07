from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, QuestionForm, AnswerForm
from .models import Question, Answer

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})  
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password"
    return render(request, 'core/login.html',{'error':error})

@login_required
def logout_view(request):
    """
    Single logout view. Having two identical functions with the same name
    causes one to override the other. This is the correct version.
    """
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'questions': questions})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')  # Returns an HttpResponseRedirect
    else:
        form = QuestionForm()
    # IMPORTANT: Must return a response in every code path
    return render(request, 'core/post_question.html', {'form': form})

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question=question)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)
        else:
            # Form invalid: re-render the page with errors
            return render(request, 'core/question_detail.html', {
                'question': question,
                'answers': answers,
                'form': form
            })
    else:
        # GET request: provide a blank form
        form = AnswerForm()

    # Render for GET or after a successful form submission
    return render(request, 'core/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })



@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = AnswerForm()
    return render(request, 'core/answer_question.html', {
        'question': question,
        'form': form
    })

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('question_detail', question_id=answer.question.id)


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id, user=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_detail', question_id=question.id)
    else:
        # For a GET request, prepopulate the form with the question data
        form = QuestionForm(instance=question)

    # IMPORTANT: we need a return statement even if it's a GET request
    return render(request, 'core/edit_question.html', {
        'form': form,
        'question': question
    })
    
@login_required
def delete_question(request,question_id):
    question = get_object_or_404(Question,pk=question_id,user=request.user)
    if request.method=="POST":
        question.delete()
        return redirect('home')
    
    return render(request,'core/delete_question_confirm.html',{
        'question':question
    })

