from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView

from .forms import LoginForm, RegUser, ChangeProfileForm
from .models import Product, Categories, Busket


# Create your views here.
class IndexPageView(TemplateView):
    template_name = 'shop/index.html'


class ProductsView(TemplateView):
    template_name = 'shop/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.GET:
            filter = self.request.GET['filter']
            context['products'] = Product.objects.filter(categorie__url=filter)
        else:
            context['products'] = Product.objects.all()
        context['cats'] = Categories.objects.all()
        user_products_in_busket = Busket.objects.filter(user_id=self.request.user.id).all()
        context['in_busk'] = list()
        for product_in_busk in user_products_in_busket:
            for product in context['products']:
                if product.id in context['in_busk']:
                    continue
                elif product.id == product_in_busk.product_id:
                    context['in_busk'].append(product.id)
                    break

        return context

    def post(self, request):
        if 'add_product' in request.POST and 'product_id' in request.POST:
            product = Product.objects.get(pk=request.POST['product_id'])
            busket = Busket(
                user=request.user,
                product=product
            )
            busket.save()
        elif 'del_product' in request.POST and 'product_id' in request.POST:
            user_busk = Busket.objects.get(product_id=request.POST['product_id']).delete()
        return HttpResponseRedirect(reverse('store:catalog'))


class LoginPageView(LoginView):
    template_name = 'shop/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('store:profile')


class RegistrationView(CreateView):
    template_name = 'shop/register.html'
    form_class = RegUser
    model = User
    success_url = reverse_lazy('store:catalog')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('store:catalog'))


@login_required
def profile(request):

    form = ChangeProfileForm(instance=request.user)

    if request.method == 'POST':
        if 'add_one_product' in request.POST:
            product_id = request.POST.get('product')
            busket_user_product = Busket.objects.filter(user_id=request.user.id).filter(product_id=product_id).first()
            busket_user_product.count += 1
            busket_user_product.save()
        elif 'del_one_product' in request.POST:
            product_id = request.POST.get('product')
            busket_user_product = Busket.objects.filter(user_id=request.user.id).filter(product_id=product_id).first()
            if busket_user_product.count == 1:
                busket_user_product.delete()
            else:
                busket_user_product.count -= 1
                busket_user_product.save()
        else:
            form = ChangeProfileForm(data=request.POST, files=request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('store:profile'))

    products_in_busk = Busket.objects.filter(user_id=request.user.id).all()

    total_price = 0
    count_all_products = len(products_in_busk)

    for pr in products_in_busk:
        total_price += pr.product.price * pr.count

    context = {'form': form, 'products_in_busk': products_in_busk, 'total_price': total_price,
               'count_all_products': count_all_products}
    return render(request, 'shop/profile.html', context=context)


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:login'))
