from django.contrib import admin
import maker.models as maker_models

admin.site.register(maker_models.User)
admin.site.register(maker_models.Company)
admin.site.register(maker_models.Branch)
admin.site.register(maker_models.Cuisine)
admin.site.register(maker_models.Review)
admin.site.register(maker_models.Favorite)