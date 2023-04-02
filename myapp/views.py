from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, ProfileUpdateForm, UserUpdateForm, DocumentForm
from .models import Profile, Document, Mark
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import matplotlib.pyplot as plt
import io


# Create your views here.
def home(request):
    return render(request, 'home.html')


def commerce(request):
    return render(request, 'commerce.html')


@login_required(login_url='/login')
def faculty(request):
    return render(request, 'faculty.html')


def contactus(request):
    return render(request, 'contactus.html')


@login_required(login_url='/login')
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def documents(request):
    documents = Document.objects.filter(user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user  # Set the user field
            document.save()
            return redirect('documents')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'documents': documents
    }
    return render(request, 'documents.html', context)


def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('documents')


def dashboard(request):
    user = request.user

    # Retrieve the marks for the logged in student
    marks = Mark.objects.filter(student__user=user)
    print(len(marks))
    data = {}
    if len(marks) > 0:
    # Extract the subject names and marks from the marks queryset

        for mark in marks:
            data[mark.subject.name] = mark.marks

        max_data = max(data.values())
        max_sub = [i for i in data if data[i] == max_data]
        min_data = min(data.values())
        min_sub = [i for i in data if data[i] == min_data]

        failed_sub = [i for i in data if data[i] < 10]
    else:
        print("____________recahed outside marks__________")
        data: ''
        max_sub = ''
        min_sub = ''
        failed_sub = ''

    # Render the template with the context
    # Create a dictionary to pass to the template
    context = {
        'marks': marks,
        'data': data,
        'max_sub': max_sub,
        'min_sub': min_sub,
        'failed_sub': failed_sub
    }
    return render(request, 'dashboard.html', context)

def login_request(request):
    if request.method == "POST":

        username = request.POST['user1']
        password = request.POST['password_login']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("home")
        else:
            return redirect('login')
    else:
        messages.error(request, "Invalid username or password.")
        return render(request, 'login.html')


def register_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

    # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    # Check if username is already taken

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('register')

    # Create the user
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=firstname,
                                        last_name=lastname)
        user.save()
        messages.success(request, f'Account created for {username}!')
        return redirect('login')
    else:
        return render(request, 'register.html')


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return redirect("/password_reset/done/")
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request, 'password/password_reset.html',
                  context={"password_reset_form": password_reset_form})
