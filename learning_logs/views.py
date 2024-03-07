from django.shortcuts import redirect, render

from .models import Topic
from .forms import TopicForm, EntryForm


def index(request):
    """Main page for learning_log"""
    return render(request, "learning_logs/index.html")


def topics(request):
    """Show all topics"""
    topics = Topic.objects.order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """Shows particular topic and every entry related to it"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    """Add new topic"""
    if request.method != "POST":
        # No data was passed, creating new form
        form = TopicForm()
    else:
        # Data sent by POST, let's process them
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            # Return to topics page after successful save
            return redirect("learning_logs:topics")

    # Display empty form
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    """Add new entry to given topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # No data was passed, creating new form
        form = EntryForm()
    else:
        # Data sent by POST, let's process them
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # Return to topics page after successful save
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display empty form
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)
