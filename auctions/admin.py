
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User
# from django.utils.translation import ugettext_lazy as _ 
# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
	model = Auction
	# fields = ('category','title','description','image','image_preview','price','is_active','slug','wishlist','current_bid','creator', 'buyer','creation_date'), 
	list_display = ('image_preview','title','short_description','creation_date')
	# list_display_links = ['title',]
	list_filter = ['title','creation_date']
	date_hierarchy = 'creation_date'
	readonly_fields = ('creation_date','image_preview', 'slug','wishlist','creator')

	

	

	# __str__.short_description = 'Image Preview'
	# __str__.allow_tags = True


admin.site.register(Auction, AuctionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category,)
admin.site.register(Comment,)
admin.site.register(Bid,)
admin.site.register(AuctionSpecification,)
admin.site.register(AuctionType,)
admin.site.register(AuctionProcess,)
admin.site.register(AuctionSpecificationValue,)

