

# Register your models here.
from django.contrib import admin
from coupons.models import Coupon, CouponUsers

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model           = CouponUsers
    readonly_fields = ('user','date_used','is_used')
    extra           = 0
    exclude         = ['amount']

class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code','amount','quantity','is_available','created')
    inlines      =  [OrderItemInline]

class CouponUsersAdmin(admin.ModelAdmin):
    list_display = ('user','coupon','amount','is_used','date_used')


admin.site.register(Coupon,CouponAdmin)
admin.site.register(CouponUsers,CouponUsersAdmin)