from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Entry, Topic
from .forms import TopicForm, EntryForm


def index(request):
    """Main page for learning_log"""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Shows particular topic and every entry related to it"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != "POST":
        # No data was passed, creating new form
        form = TopicForm()
    else:
        # Data sent by POST, let's process them
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # Return to topics page after successful save
            return redirect("learning_logs:topics")

    # Display empty form
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
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


@login_required
def edit_entry(request, entry_id):
    """Edit entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # No data was passed, showing existing data in the form
        form = EntryForm(instance=entry)
    else:
        # Data sent by POST, let's process them
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            # Return to topics page after successful save
            return redirect("learning_logs:topic", topic_id=topic.id)

    # Display empty form
    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
