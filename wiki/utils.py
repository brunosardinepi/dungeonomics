def is_article_admin(user, article):
    if user in article.admins.all():
        return True
    return False
