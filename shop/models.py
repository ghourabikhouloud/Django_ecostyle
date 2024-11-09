from django.db import models
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    image = models.ImageField(upload_to='categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def get_category_slug_url(self):
        return reverse('shop:categries', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    date_joined_for_format = models.DateTimeField(auto_now_add=True)
    last_login_for_format = models.DateTimeField(auto_now=True)
    def created(self):
        return self.date_joined_for_format.strftime('%B %d %Y')
    def updated(self):
        return self.last_login_for_format.strftime('%B %d %Y')

    def __str__(self):
        return self.name
    
    def averageRating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def get_prodcut_details_url(self):
        return reverse('shop:product_details', args=[self.category.slug, self.slug])
    
    def average_positive_probability(self):
        avg_positive_prob = ReviewRating.objects.filter(
            product=self
        ).aggregate(average=Avg('positive_probab'))['average']
        
        # Si aucune probabilité positive n'est trouvée, retourner N/A
        return avg_positive_prob if avg_positive_prob is not None else 'N/A'
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-date_joined_for_format',)
    


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choices = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True)
    # subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=700, blank=True)
    # review = models.FloatField(null=True, blank=True)  # Store probability as a float

    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    positive_probab = models.FloatField(null=True, blank=True)  # Pour stocker la probabilité positive


    def update_at(self):
        return self.updated_at.strftime('%B %d, %Y')

    def hour_update(self):
        return self.updated_at.strftime('%H:%M:%S')

    def __str__(self):
        return self.review
    

    # @classmethod
    # def average_positive_probability_for_product(cls, product_id):
    #     reviews = cls.objects.filter(product_id=product_id)
    #     if reviews.exists():
    #         total = sum(review.positive_probab for review in reviews if review.positive_probab is not None)
    #         count = reviews.count()
    #         return total / count if count > 0 else 0
    #     return 0



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery')
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

    def __str__(self):
        return self.product.name






#AZIZ
class Wishlist(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='wishlist')
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist"
    


class WishlistItem(models.Model):
    from shop.models import Product
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s Wishlist"




class Notification(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    target_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_read = models.BooleanField(default=False)
    message = models.CharField(max_length=255)
    notify_on_sale = models.BooleanField(default=False) 

    def __str__(self):
        return f"Notification for {self.user.username} - {self.product.name}"