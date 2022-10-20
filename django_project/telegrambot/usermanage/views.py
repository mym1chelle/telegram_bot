from django.shortcuts import render, redirect
from django_project.telegrambot.usermanage.forms import SendMessageForm
from data.config import BOT_TOKEN
from asgiref.sync import sync_to_async
import httpx
from .models import *
from utils.db_api import db_commands as commands

API_link = f'https://api.telegram.org/bot{BOT_TOKEN}'


# def send_message(request):
#     """Отправка сообщений пользователю синхронной функцией"""
#     form = SendMessageForm(request.POST)
#     if request.method == 'POST':  # сюда попадает уже заполненная форма и проверяется на корректнрость
#         if form.is_valid():
#             data = form.data
#             chat_id = data['user_id']
#             message = data['message']
#             print(message, chat_id)
            
#             requests.get(API_link + f'/sendMessage?chat_id={chat_id}&text={message}')
                
#             return redirect('send_message')
#         else:  # сюда попадает чистая не заполненная форма
#             form = SendMessageForm()  
#     return render(request, 'usermanage/send_message.html', {'form': form, 'title': 'Чат'})


async def send_message(request):
    """Отправка сообщений пользователю асинхронной функцией"""
    form = SendMessageForm(request.POST)
    purchases = await commands.select_all_purchase()
    if request.method == 'POST':  # сюда попадает уже заполненная форма и проверяется на корректнрость
        if form.is_valid():
            data = form.data
            chat_id = data['user_id']
            message = data['message']
            # отправка сообщений пользователю через бота не работает с помощью aiogram так как нужно.
            # Поэтому я отправляю сообщения напрямую через get-запрос к API (асинхронно)
            async with httpx.AsyncClient() as client:
                await client.get(API_link + f'/sendMessage?chat_id={chat_id}&text={message}')
                
            return await sync_to_async(redirect)('send_message')
        else:  # сюда попадает чистая не заполненная форма
            form = SendMessageForm()  
    return await sync_to_async(render)(request, 'usermanage/send_message.html', {'form': form, 'title': 'Чат', 'purchases': purchases})


