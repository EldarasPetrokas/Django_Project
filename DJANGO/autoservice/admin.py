from django.contrib import admin
from .models import AutomobilioModelis, Automobilis, Paslauga, Uzsakymas, UzsakymoEilute


class UzsakymoEiluteInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 1


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('id', 'automobilis', 'data', 'statusas')
    inlines = [UzsakymoEiluteInline]


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis')
    search_fields = ('valstybinis_nr', 'vin_kodas')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
