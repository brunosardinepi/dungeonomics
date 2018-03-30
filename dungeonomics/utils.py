from django.conf import settings


def image_is_valid(request, form):
    if form.is_valid():
        image_raw = form.cleaned_data.get('image', False)
        if image_raw:
            if type(image_raw) == 'django.core.files.uploadedfile.InMemoryUploadedFile':
                image_type = image_raw.content_type.split('/')[0]
                if image_type in settings.UPLOAD_TYPES:
                    if image_raw._size <= settings.MAX_IMAGE_UPLOAD_SIZE:
                        return True
                    else:
                        return "bad size"
                else:
                    return "bad type"