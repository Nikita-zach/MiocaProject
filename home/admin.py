from django.contrib import admin
from compare.models import Compare, CompareItem
from .models import Feature, NewsletterSubscriber, Banner, Deal, Slider
from wishlist.models import Wishlist, WishlistItem
from product.models import Products, ProductImage, Category, Review
from cart.models import Cart, CartItem
from info_pages.models import FAQ, Testimonials, Stuff, BrandIcons, ServiceSection
from payments.models import Order
from accounts.models import UserModel
from contact.models import ContactMessage
from blog.models import BlogWindow, BlogSection, Comment


class CompareItemInline(admin.TabularInline):
    model = CompareItem
    extra = 1
    show_change_link = True


@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    list_display = ('user','created_at', 'updated_at')
    inlines = [CompareItemInline]


@admin.register(CompareItem)
class CompareItemAdmin(admin.ModelAdmin):
    list_display = ('compare', 'product')
    list_filter = ('compare', 'product')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    show_change_link = True


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
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


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('name', 'email', 'message', 'product__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('product', 'name', 'email', 'rating', 'message', 'created_at')
        }),
    )



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price', 'payment_method')
    list_filter = ('created_at', 'payment_method')
    date_hierarchy = 'created_at'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question',)
    date_hierarchy = 'created_at'


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle_1', 'subtitle_2', 'created_at', 'updated_at')
    search_fields = ('title', 'subtitle_1')
    date_hierarchy = 'created_at'


@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'is_visible', 'created', 'updated')
    list_editable = ('is_visible',)
    list_filter = ('is_visible', 'created')
    search_fields = ('name', 'profession')
    date_hierarchy = 'created'


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(BrandIcons)
class BrandIconsAdmin(admin.ModelAdmin):
    list_display = ('image', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    date_hierarchy = 'created_at'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product','added_at')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [WishlistItemInline]


@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'by_user', 'date')
    search_fields = ('title', 'by_user')
    date_hierarchy = 'date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog_section', 'name', 'date')
    search_fields = ('name', 'message')
    date_hierarchy = 'date'


@admin.register(BlogWindow)
class BlogWindowAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'main_description')
    filter_horizontal = ('blogs',)


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'city', 'country')
    search_fields = ('username', 'email')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    date_hierarchy = 'created_at'

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_visible', 'sort')
    list_filter = ('is_visible', 'category')

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('background_image', 'created_at')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('background_image', 'created_at')