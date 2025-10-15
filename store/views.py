from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)[0:2]
    context = {'products': products}
    return render(request, 'core/index.html', context)



def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)