from django.contrib import admin
from .models import Person, Documento


class PersonAdmin(admin.ModelAdmin):
    model = Person
    # fields = (('first_name', 'last_name'), ('age', 'salary'), 'bio', ('photo', 'doc'))
    list_display = ('first_name', 'last_name', 'age', 'salary', 'bio', 'photo', 'doc', 'has_photo', 'is_adult')
    fieldsets = (
        ('Basic Data', {
            'fields': ('first_name', 'last_name', 'age')
        }),
        ('Person salary', {
            'fields': ('salary', )
        }),
        ('Person description', {
            'fields': ('bio', 'photo')
        }),
        ('Person documentation', {
            'fields': ('doc', )
        })
    )
    list_filter = ('age', 'salary')
    search_fields = ('id', 'first_name')
    # readonly_fields = ('first_name', 'last_name')

    def has_photo(self, obj):
        if obj.photo:
            return 'Yes'
        return 'No'

    has_photo.short_description = 'Person has photo?'

    def is_adult(self, obj):
        if obj.age >= 18:
            return True
        return False

    is_adult.short_description = 'Is person adult?'


admin.site.register(Person, PersonAdmin)
admin.site.register(Documento)
