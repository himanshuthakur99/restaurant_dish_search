from django.shortcuts import render
from .models import Dish
from .forms import SearchForm
import json  

def search(request):
    form = SearchForm()
    results = []
    query = ''  # Initialize query
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            dishes = Dish.objects.filter(items__icontains=query).order_by('-rating')  # Order by rating in descending order
            for dish in dishes:
                matching_items = [f"{item.strip()} - {price}" for item, price in json.loads(dish.prices).items() if query.lower() in item.lower()]
                if matching_items:
                    results.append({
                        'id': dish.id, # type: ignore
                        'name': dish.name,
                        'location': dish.location,
                        'items': matching_items,
                        'rating': dish.rating
                    })
    return render(request, 'search_app/search.html', {'form': form, 'results': results, 'query': query})
