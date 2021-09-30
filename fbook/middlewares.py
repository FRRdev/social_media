from .models import BookUser

def social_context_processor(request):
    context = {}
    context['all'] = ''
    pk = request.user.pk
    if pk:
        user =BookUser.objects.get(pk=pk)
        count = user.to_user
        context['count'] = count
    return context