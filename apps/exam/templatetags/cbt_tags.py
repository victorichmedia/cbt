from django import template

register = template.Library()


@register.simple_tag
def get_user_choice(option, user):
    choice = option.user_choice(user)
    if choice == 1:
        return "check"
    elif choice == 2:
        return "close"
    else:
        return ""
