from .models import BookUser, Message


def social_context_processor(request):
    context = {}
    context['all'] = ''
    pk = request.user.pk
    if pk:
        count_of_message = 0
        user = BookUser.objects.get(pk=pk)
        count = user.to_user
        context['count'] = count
        chat_list_1 = user.first_user.all()
        chat_list_2 = user.second_user.all()
        chats = chat_list_1.union(chat_list_2)
        for chat in chats:
            if chat.first_user == user:
                another_user = chat.second_user
            else:
                another_user = chat.first_user
            count_of_message_test = Message.objects.filter(author=another_user, chat=chat, is_active=True).count()
            count_of_message += count_of_message_test

        context['count_of_messages'] = count_of_message

    return context
