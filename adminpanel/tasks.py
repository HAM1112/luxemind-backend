from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from adminpanel.models import CustomUser


logger = get_task_logger(__name__)


@shared_task
def send_mail_to_related_students(subject, course_name):
    users_email = (
        CustomUser.objects.filter(purchase__course__subject__name=subject)
        .values_list("email", flat=True)
        .distinct()
    )
    subject = "New Course Published"
    message = f'New Courses:"{course_name}" have been Published that You might enjoy!!!!!!!!!!!! Be the one to purchase this exciting Course. ONLY IN LUXEMINDS'
    from_email = "wjdevswj@gmail.com"
    recipient_list = users_email
    send_mail(subject, message, from_email, recipient_list)
    logger.info("Send emails")
    return
