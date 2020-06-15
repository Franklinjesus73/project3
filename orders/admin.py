from django.contrib import admin
from .models import Name_pizza,Regular_pizza,Sicilian_pizza,Topping,Sub_extra,Pasta,Salad,Dinner_platter,Order,User_order,Counter

# Register your models here.

admin.site.register(Name_pizza)
admin.site.register(Regular_pizza)
admin.site.register(Sicilian_pizza)
admin.site.register(Topping)
admin.site.register(Sub_extra)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
admin.site.register(Order)
admin.site.register(User_order)
admin.site.register(Counter)