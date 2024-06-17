from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('', views.index, name="index"),
    path('project/create', views.createProject, name="createProject"),
    path('project/view/<int:project_id>', views.projectView, name="projectView"),
    path('project/table/<int:project_id>', views.table, name="table"),
    path('fields/<int:table_id>', views.fields, name="fields"),
    path('table/view/<int:table_id>', views.tables, name="tables"),
    path('table/export/<int:table_id>', views.outputCSV, name="outputCSV"),
    path('table/delete/<int:table_id>/<int:Order>', views.delete, name="delete"),
]
