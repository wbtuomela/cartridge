from django.template.defaultfilters import slugify
from mezzanine.conf import settings
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.views import paginate

from cartridge.shop.models import Category, Product


# The site registers its own @processor_for(Category, exact_page=True) in
# jaanj/page_processors.py. Registration prepends and PageMiddleware stops at
# the first HttpResponse, so keeping both registrations would make category
# handling order-dependent.
#@processor_for(Category, exact_page=True)
def category_processor(request, page):
    """
    Add paging/sorting to the products for the category.
    """
    settings.clear_cache()
    products = (
        Product.objects.published(for_user=request.user)
        .filter(page.category.filters())
        .distinct()
    )
    sort_options = [
        (slugify(option[0]), option[1]) for option in settings.SHOP_PRODUCT_SORT_OPTIONS
    ]
    sort_by = request.GET.get(
        "sort", sort_options[0][1] if sort_options else "-date_added"
    )
    products = paginate(
        products.order_by(sort_by),
        request.GET.get("page", 1),
        settings.SHOP_PER_PAGE_CATEGORY,
        settings.MAX_PAGING_LINKS,
    )
    products.sort_by = sort_by
    sub_categories = page.category.children.published()
    child_categories = Category.objects.filter(id__in=sub_categories)
    return {"products": products, "child_categories": child_categories}
