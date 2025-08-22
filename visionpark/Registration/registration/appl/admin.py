from django.contrib import admin
from .models import Booking, phone_numbers

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'license_plate', 'location', 'selected_slot', 'start_time', 'end_time', "booking_type" ,'buffer_time', 'total_endtime', 'status', 'payment')
    search_fields = ('full_name', 'phone', 'license_plate', 'location')
    list_filter = ('location', 'selected_slot', 'start_time')
    ordering = ('start_time',)
admin.site.register(Booking, BookingAdmin)

class phone_numbersadmin(admin.ModelAdmin):
    list_display =('user', 'phone')
admin.site.register(phone_numbers, phone_numbersadmin)