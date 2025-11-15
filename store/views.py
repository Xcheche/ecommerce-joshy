from django.shortcuts import get_object_or_404, redirect, render

from store.models import Category, Product
from django.db.models import Q

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_at')[:4]
    context = {'products': products}
    return render(request, 'core/index.html', context)



def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)





# Category View
def category(request):
    """Display categories in the navbar"""
    all_category = Category.objects.all()
    return {"all_category": all_category}


# List Category
def list_category(request, category_slug=None):
    """List products by category"""
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        category = None
    products = Product.objects.filter(category=category)
    context = {"category": category, "products": products,"current_category": category,  # for selecting the current option
               "all_category": Category.objects.all()}  # for the category dropdown
    return render(request, "store/list_category.html", context)



#Search functionality
def search(request):
    import time  # noqa: F811

    time.sleep(1.5)
    query = request.GET.get("q")
    products = Product.objects.filter(is_available=True)  # start with all products

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()

    context = {
        "products": products,
        "query": query,
    }
    if not products.exists():
        context["message"] = "No products found."
    return render(request, "store/list_category.html", context)
