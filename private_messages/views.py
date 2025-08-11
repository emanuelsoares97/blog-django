from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from django.db import models
from django.http import JsonResponse
from django.db.models import Q, Count

@login_required
def inbox(request):
    user = request.user

    # Busca utilizadores com quem o user já trocou mensagens
    contacts = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct()

    # Anotar para cada contacto quantas mensagens NÃO LIDAS o user tem vindo a receber deles
    contacts = contacts.annotate(
        unread_count=Count(
            'sent_messages',
            filter=Q(sent_messages__recipient=user, sent_messages__read=False)
        )
    )

    return render(request, 'private_messages/inbox.html', {'contacts': contacts})


@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    user = request.user

    messages_qs = Message.objects.filter(
        (models.Q(sender=user) & models.Q(recipient=other_user)) |
        (models.Q(sender=other_user) & models.Q(recipient=user))
    ).order_by('timestamp')

    unread = messages_qs.filter(recipient=user, read=False)
    unread.update(read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            new_message = Message.objects.create(
                sender=user, recipient=other_user, content=content
            )

            # Se o pedido for AJAX, devolvemos JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'sender': new_message.sender.username,
                    'content': new_message.content,
                    'timestamp': new_message.timestamp.strftime("%d/%m/%Y %H:%M")
                })

            return redirect('conversation', username=other_user.username)
    else:
        form = MessageForm()

    return render(request, 'private_messages/conversation.html', {
        'messages': messages_qs,
        'form': form,
        'other_user': other_user
    })

