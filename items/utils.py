def create_item_copy(item, user):
    item.pk = None
    item.is_published = False
    item.user = user
    item.save()
