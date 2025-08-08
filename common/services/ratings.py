from store.models import Rating


def create_or_update_rating(user, product, rating_value):
    rating, created = Rating.objects.update_or_create(
        user=user,
        product=product,
        defaults={'value': rating_value}
    )
    return rating
