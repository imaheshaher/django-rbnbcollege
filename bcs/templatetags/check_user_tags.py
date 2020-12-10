from django import template
from ..models import Students
from django.contrib.auth.models import User

register=template.Library()

@register.simple_tag
def check_is_student(studid):
    
    user=User.objects.get(id=studid)
    try:
        student=Students.objects.get(user=user)
        return student
    except:
        return False
    return 

@register.simple_tag
def get_subject(subname):
    subject = ['a','b','c']
    if subname in subject:
        return subject
    
    return

@register.simple_tag

def fetch_student(n):
    return n+1