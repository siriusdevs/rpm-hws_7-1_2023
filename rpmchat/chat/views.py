from django.http import JsonResponse
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from chat.models import Message

STATUS = (200, 405)


@login_required
def run_chat(request):
    name = get_user(request).username
    Message.create_message('Server', f'{name} joined chat!')
    return render(request, 'chat/base.html')


@login_required
def send_request(request):
    response_data = {'error': 'Method not allowed!'}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        request_data = json.load(request)
        if request_data['act'] == 'send':
            if request_data['var1']:
                name = get_user(request).username
                Message.create_message(name, request_data['var1'])
        resp = "<br>".join([
            f"<b>{msg.name}:</b>{msg.text}"
            for msg in Message.get_all_messages()
        ])
        response_data = {'data': resp}
        return JsonResponse(response_data)
    return JsonResponse(response_data, status=STATUS[1])


@login_required
def logout_request(request):
    response_data = {'error': 'Method not allowed!'}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        name = get_user(request).username
        request_data = json.load(request)
        if request_data['data'] == '/logout':
            response_data = {'repl': 'Method allowed!'}
            Message.create_message('Server', f'{name} disconnect!')
        return JsonResponse(response_data, status=STATUS[0])
    return JsonResponse(response_data, status=STATUS[1])
