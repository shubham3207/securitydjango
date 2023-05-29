from customer.models import Customer

def log_activity(user, activity):
    if user.is_authenticated:
        try:
            customer = Customer.objects.get(user=user)
            username = customer.username
        except Customer.DoesNotExist:
            username = 'Unknown'
    else:
        username = 'Anonymous'

    with open('activity_log.txt', 'a') as file:
        file.write(f"User: {username} | Activity: {activity}\n")