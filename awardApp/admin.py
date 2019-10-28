from django.contrib import admin
from .models import Location,tags, Image, Project, Profile, Review
# Register your models here.

class ImageAdmin(admin.ModelAdmin):
     filter_horizontal =('tags',)
class ProjectAdmin(admin.ModelAdmin):
     list_dispaly=('title',)
class ProfileAdmin(admin.ModelAdmin):
      list_dispaly=('user',)

class ReviewAdmin(admin.ModelAdmin):
     models = Review
     list_dispaly=('project','usability_rating','content_rating','design_rating','user','comment','image',)
     list_filter=['user',]
     search_fields=['comment',]

admin.site.register(Location)
admin.site.register(tags)
admin.site.register(Image,ImageAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Review,ReviewAdmin)
