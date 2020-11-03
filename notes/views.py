from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import View

from . import forms
from .models import Note

from dungeonomics.utils import at_tagging


@login_required
def note_detail(request, pk=None):
    user = None
    if request.user.is_authenticated:
        user = request.user.pk
    notes = sorted(Note.objects.filter(user=user), key=lambda note: note.name.lower())
    if pk:
        note = get_object_or_404(Note, pk=pk)
        if note.user == request.user:
            return render(request, 'notes/note_detail.html', {'note': note, 'notes': notes})
        else:
            raise Http404
    elif len(notes) > 0:
        note = notes[0]
        if note.user == request.user:
            return render(request, 'notes/note_detail.html', {'note': note, 'notes': notes})
        else:
            raise Http404
    else:
        note = None
    return render(request, 'notes/note_detail.html', {'note': note, 'notes': notes})

@login_required
def note_create(request):
    data = at_tagging(request)
    form = forms.NoteForm(user=request.user)
    if request.method == 'POST':
        form = forms.NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.add_message(request, messages.SUCCESS, "Note created!")
            return HttpResponseRedirect(note.get_absolute_url())
    data['form'] = form
    return render(request, 'notes/note_form.html', data)

@login_required
def note_update(request, pk):
    data = at_tagging(request)
    note = get_object_or_404(Note, pk=pk)
    if note.user == request.user:
        form = forms.NoteForm(instance=note, user=request.user)
        if request.method == 'POST':
            form = forms.NoteForm(
                instance=note,
                data=request.POST,
                user=request.user,
            )
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated note: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(note.get_absolute_url())
    else:
        raise Http404
    data['form'] = form
    data['note'] = note
    return render(request, 'notes/note_form.html', data)

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.user == request.user:
        note.delete()
        messages.success(request, 'Note deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('notes:note_detail'))
    else:
        raise Http404

class NotesDelete(View):
    def get(self, request, *args, **kwargs):
        notes = Note.objects.filter(user=request.user).order_by('name')
        return render(request, 'notes/notes_delete.html', {'notes': notes})

    def post(self, request, *args, **kwargs):
        for note_pk in request.POST.getlist('note'):
            Note.objects.get(pk=note_pk).delete()
        return HttpResponseRedirect(reverse('notes:note_detail'))
