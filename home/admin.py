from django.contrib import admin
from .models import Category, Products, Cart, CartItem, Wishlist, WishlistItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_visible', 'sort', 'created_at', 'updated_at', 'visible_product_count')
    list_editable = ('is_visible', 'sort')
    list_filter = ('is_visible', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_visible', 'created_at', 'updated_at')
    list_editable = ('is_visible', 'price')
    list_filter = ('is_visible', 'categories', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    date_hierarchy = 'created_at'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product')
