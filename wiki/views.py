from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


# def wiki_home(request, section_pk=None):
#     if section_pk:
#         this_section = get_object_or_404(models.Section, pk=section_pk)
#         return render(request, 'wiki/wiki_home.html', {'this_section': this_section})
#     else:
#         sections = sorted(models.Section.objects.all(),
#             key=lambda section: section.title)
#         if len(sections) > 0:
#             this_section = sections[0]
#         return render(request, 'wiki/wiki_home.html', {'this_section': this_section})

def wiki_home(request):
    return HttpResponse("wiki")