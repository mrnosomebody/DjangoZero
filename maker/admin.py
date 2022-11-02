from django.contrib import admin

import maker.models as maker_models


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating')


admin.site.register(maker_models.User)
admin.site.register(maker_models.Company, CompanyAdmin)
admin.site.register(maker_models.Branch)
admin.site.register(maker_models.Cuisine)
admin.site.register(maker_models.Review)
admin.site.register(maker_models.Favorite)
admin.site.register(maker_models.CompanyCuisine)
