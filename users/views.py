from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        # Сохраняем форму, но не коммитим в БД
        self.object = form.save(commit=False)

        # Устанавливаем неактивным, пока не подтвердит email (опционально)
        self.object.is_active = True
        self.object.save()

        # Логиним пользователя
        login(self.request, self.object)

        # Отправка письма (лучше использовать Celery для асинхронности)
        try:
            send_mail(
                subject='Добро пожаловать!',
                message='Спасибо за регистрацию на нашем сайте.',
                from_email='noreply@yourdomain.com',  # Используйте реальный домен
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            # Можно добавить логирование ошибки

        return redirect(self.get_success_url())


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('catalog:product_list')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:product_list')