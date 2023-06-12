from .models import Profile


def check_status(profile: Profile):
    if profile.total_expenses <= 3000:
        profile.status = 'Iron'
        profile.save()
    elif profile.total_expenses <= 6000:
        profile.status = 'Bronze'
        profile.save()

    elif profile.total_expenses <= 12000:
        profile.status = 'Silver'
        profile.save()

    elif profile.total_expenses <= 24000:
        profile.status = 'Gold'
        profile.save()

    elif profile.total_expenses <= 48000:
        profile.status = 'Platinum'
        profile.save()