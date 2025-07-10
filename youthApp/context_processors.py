from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = notifications.filter(is_read=False).count()
        return {
            'notifications': notifications,
            'unread_count': unread_count
        }
    return {}
