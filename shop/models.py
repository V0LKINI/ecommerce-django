from django.db import models
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length=300, unique=True)
	slug = models.SlugField(max_length=300, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='category/', blank=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def get_url(self):
		return reverse('products_by_category', args=[self.slug])

	def __str__(self):
		return self.name


class Product(models.Model):
	title = models.CharField(max_length=300)
	image = models.ImageField(upload_to='product_images/')
	slug = models.SlugField(max_length=300, unique=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	stock = models.IntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('title',)
		verbose_name = 'product'
		verbose_name_plural = 'products'

	def get_url(self):
		return reverse('product_detail', args=[self.category.slug, self.slug])

	def __str__(self):
		return self.title


class Cart(models.Model):
	cart_id = models.CharField(max_length=250, blank=True)
	data_added = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ['data_added']
		db_table = 'Cart'

	def __str__(self):
		return self.cart_id


class Cart_Item(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	active = models.BooleanField(default=True)

	class Meta:
		db_table = 'Cart_Item'

	def sub_total(self):
		return self.product.price * self.quantity

	def __str__(self):
		return self.product