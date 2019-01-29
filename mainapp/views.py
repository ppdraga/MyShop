from django.shortcuts import render
from basketapp.models import Basket
from mainapp.models import ProductCategory, Product
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
# Create your views here.

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    basket = get_basket(request.user)
    menu = [
        {
            'title': 'Главная',
            'url': '',
            'href': 'index.html'
        },
        {
            'title': 'Каталог',
            'url': 'products',
            'href': 'products.html'
        },
        {
            'title': 'Контакты',
            'url': 'contacts',
            'href': 'contacts.html'
        }
    ]
    content = {
        'title': title,
        'menu': menu,
        'basket' : basket
    }
    return render(request, 'mainapp/index.html', content)

def contacts(request):
    title = 'Контакты'
    basket = get_basket(request.user)
    menu = [
        {
            'title': 'Главная',
            'url': '',
            'href': 'index.html'
        },
        {
            'title': 'Каталог',
            'url': 'products',
            'href': 'products.html'
        },
        {
            'title': 'Контакты',
            'url': '',
            'href': 'contacts.html'
        }
    ]
    content = {
        'title': title,
        'menu': menu,
        'basket' : basket
    }
    return render(request, 'mainapp/contacts.html', content)

def products(request, pk=None, page=1):
    print(pk)
    title = 'Каталог'
    menu = [
        {
            'title': 'Главная',
            'url': '',
            'href': 'index.html'
        },
        {
            'title': 'Каталог',
            'url': '',
            'href': 'products.html'
        },
        {
            'title': 'Контакты',
            'url': 'contacts',
            'href': 'contacts.html'
        }
    ]
    links_menu = ProductCategory.objects.filter(is_active=True)

    basket = get_basket(request.user)

    if pk is not None:
        if pk is not None:
            if pk == 0:
                category = { 'pk' : 0, 'name' : 'все' }
                products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            else:
                category = get_object_or_404(ProductCategory, pk=pk)
                products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title' : title,
            'links_menu' : links_menu,
            'category' : category,
            'products' : products_paginator,
            'basket' : basket
        }
        return render(request, 'mainapp/products_list.html', content)
    
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)    
    products = Product.objects.filter(is_active=True)[1 : 4]
    content = {
        'title' : title,
        'links_menu' : links_menu,
        'same_products' : same_products,
        'products' : products,
        'menu' : menu,
        'hot_product' : hot_product,
        'same_products' : same_products,
        'basket' : basket
    }
    return render(request, 'mainapp/products.html', content)

def product(request, pk):
    title = 'продукты'
    content = {
        'title' : title,
        'links_menu' : ProductCategory.objects.all(),
        'product' : get_object_or_404(Product, pk=pk),
        'basket' : get_basket(request.user),
    }
    return render(request, 'mainapp/product.html' , content)