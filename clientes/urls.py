from django.urls import path
from .views import (persons_list,
                    persons_new,
                    persons_update,
                    persons_delete,
                    PersonList)

urlpatterns = [
    path('list/', persons_list, name="person_list"),
    path('new/', persons_new, name="person_new"),
    path('update/<int:id>/', persons_update, name="persons_update"),
    path('delete/<int:id>/', persons_delete, name="persons_delete"),
    path('person-list/', PersonList.as_view(), name='list_person')
]
