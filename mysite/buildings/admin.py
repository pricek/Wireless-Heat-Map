from django.contrib import admin

from .models import Building, Floor, Room

admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)

# Register your models here.
