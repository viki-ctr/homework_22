from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f"Получено сообщение от {name} ({phone}): {message}")

        messages.success(request, 'Ваше сообщение успешно отправлено!')

        return redirect('catalog:contacts')

    context = {
        'title': 'Контакты',
    }
    return render(request, 'contacts.html', context)