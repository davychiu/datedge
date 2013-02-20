from datetime import date

def activation_required(user):
    return user.activation_set.filter(expiry__gte=date.today())
