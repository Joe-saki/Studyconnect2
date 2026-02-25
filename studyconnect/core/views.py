from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .forms import SignupForm
from .models import Course, Note, Meeting, StudySession, Message, Notification, CustomUser


def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "core/signup.html", {"form": form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("dashboard")
    return render(request, "core/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    course_id = request.GET.get("course")

    notes = Note.objects.all()
    meetings = Meeting.objects.all()

    if course_id:
        notes = notes.filter(course_id=course_id)
        meetings = meetings.filter(course_id=course_id)

    courses = Course.objects.all()

    return render(request, "core/dashboard.html", {
        "notes": notes[:5],
        "meetings": meetings[:5],
        "courses": courses
    })


@login_required
def upload_note(request):
    courses = Course.objects.all()

    if request.method == "POST":
        course_id = request.POST.get("course")
        title = request.POST.get("title")
        file = request.FILES.get("file")

        if course_id and file and title:
            Note.objects.create(
                uploaded_by=request.user,
                course_id=course_id,
                title=title,
                file=file
            )
            return redirect("dashboard")

    return render(request, "core/upload_note.html", {"courses": courses})


@login_required
def schedule_meeting(request):
    courses = Course.objects.all()

    if request.method == "POST":
        Meeting.objects.create(
            course_id=request.POST.get("course"),
            creator=request.user,
            date=request.POST.get("date"),
            topic=request.POST.get("topic")
        )
        return redirect("dashboard")

    return render(request, "core/schedule.html", {"courses": courses})


from .models import Notification

@login_required
def join_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.participants.add(request.user)

    Notification.objects.create(
        user=meeting.creator,
        message=f"{request.user.username} joined your meeting '{meeting.topic}'"
    )

    return redirect("dashboard")

@login_required
def profile(request):
    return render(request, "core/profile.html", {"user": request.user})


@login_required
def chat(request, user_id):
    try:
        other_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect("dashboard")
    
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text
            )
        return redirect("chat", user_id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("timestamp")
    
    # Get list of users the current user has chatted with
    chat_users = CustomUser.objects.filter(
        Q(sent_messages__receiver=request.user) |
        Q(messages_received__sender=request.user)
    ).distinct().exclude(id=request.user.id)
    
    return render(request, "core/chat.html", {
        "messages": messages,
        "other_user": other_user,
        "chat_users": chat_users
    })


@login_required
def get_messages(request, user_id):
    """API endpoint for AJAX to get new messages"""
    try:
        other_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("timestamp").values("id", "sender__username", "text", "timestamp")
    
    return JsonResponse({"messages": list(messages)})


@login_required
def users_list(request):
    """List all users for messaging"""
    all_users = CustomUser.objects.exclude(id=request.user.id).order_by("username")
    
    return render(request, "core/users_list.html", {
        "users": all_users
    })