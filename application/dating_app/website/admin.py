from django.contrib import admin
import models


class AdminModel(admin.ModelAdmin):
    pass

admin.site.register(models.Dater, AdminModel)
