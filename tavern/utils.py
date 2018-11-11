def rating_stars_html(rating):
    # round to nearest 0.5
    rating = round(rating * 2) / 2

    # html template for an empty star
    empty_star = '<i class="far fa-star"></i>'

    # html template for a half star
    half_star = '<i class="fas fa-star-half-alt"></i>'

    # html template for a full star
    full_star = '<i class="fas fa-star"></i>'

    if rating == 0:
        html = empty_star * 5
    elif rating % 1 == 0:
        html = (full_star * int(rating)) + (empty_star * int(5 - rating))
    elif rating % 1 == 0.5:
        html = (full_star * int(rating - 0.5)) + half_star + (empty_star * int(5 - rating - 0.5))

    return html
