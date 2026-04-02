from django.shortcuts import get_object_or_404, redirect, render

from store.models import Category, Product
from django.db.models import Q

"""Views for storefront browsing features.

Feature map:
- Home page with featured/latest products.
- Product detail page.
- Category listing.
- Search across product and category fields.
"""

def home(request):
    """Render home page with latest available products (limited set)."""

    products = Product.objects.all().filter(is_available=True).order_by('-created_at')[:4]
    context = {'products': products}
    return render(request, 'core/index.html', context)



def product_detail(request, product_slug):
    """Render a single product detail page by slug."""

    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)





# Category View
def category(request):
    """Context processor helper that exposes categories to templates."""
    all_category = Category.objects.all()
    return {"all_category": all_category}


# List Category
def list_category(request, category_slug=None):
    """List available products, optionally filtered by category slug."""
    category = None
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        "category": category,
        "products": products,
        "current_category": category,
        "all_category": Category.objects.all(),
    }
    return render(request, "store/list_category.html", context)



#Search functionality
def search(request):
    """Search available products by name, description, or category name."""

    query = (request.GET.get("q") or "").strip()
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
        "current_category": None,
        "all_category": Category.objects.all(),
    }
    if not products.exists():
        context["message"] = "No products found."
    return render(request, "store/list_category.html", context)
