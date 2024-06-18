from django.shortcuts import render, redirect
from .models import Table, Fields, Data, Project
import csv
from django.http import HttpResponse

def index(request):
    projects = Project.objects.all()
    return render(request, "dashboard.html", context={"projects":projects})

def projectView(request, project_id):
    project = Project.objects.get(id = project_id)
    tables = Table.objects.filter(Project_id = project_id)
    return render(request, "projectView.html", context={"project":project, "tables":tables})

def fields(request, table_id):
    table = Table.objects.get(id = table_id)
    project_id = table.Project_id
    number = table.Fields
    numbers = []
    for i in range(0,number):
        numbers.append(i)
    if request.method == 'POST':
        for i in range(0,number):
            field = request.POST.get(str("fieldName" + str(i)))
            choices = request.POST.get(str("fieldChoices" + str(i)))
            Fields.objects.create(Field = field, Type = choices, Table_id = table_id, Order = i)
        return redirect("tables", table_id)
    return render(request, "fields.html", context = {"numbers":numbers, "project_id": project_id})

def tableSize(table_id):
    data = Data.objects.filter(Table_id = table_id)
    fields = Fields.objects.filter(Table_id = table_id).count()
    if data is None:
        return 0
    else:
        return int(Data.objects.filter(Table_id = table_id).count()/fields)    

def createProject(request):
    if request.method == 'POST':
        name = request.POST.get('projectTitle')
        description = request.POST.get('projectDescription')
        if name and description:
            Project.objects.create(Title=name, Description=description)
            return redirect("index")

def exportTableData(table_id):
    fields = Fields.objects.filter(Table_id = table_id)
    return_arr = []
    for i in range(0,tableSize(table_id)):
        temp = []
        for field in fields:   
            temp.append(Data.objects.get(Field_id = field.id, Table_id = table_id, Order = i).Data)
        return_arr.append(temp)
    return return_arr

def tableData(table_id):
    fields = Fields.objects.filter(Table_id = table_id)
    return_arr = []
    for i in range(0,tableSize(table_id)):
        temp = []
        for field in fields:
            if len(temp) == int(Fields.objects.filter(Table_id = table_id).count() -1):    
                temp.append({"data":Data.objects.get(Field_id = field.id, Table_id = table_id, Order = i).Data, "id":int(Data.objects.get(Field_id = field.id, Table_id = table_id, Order = i).Order), "status":True})
            else:
                temp.append({"data":Data.objects.get(Field_id = field.id, Table_id = table_id, Order = i).Data, "id":int(Data.objects.get(Field_id = field.id, Table_id = table_id, Order = i).Order), "status":False})
        return_arr.append(temp)
    return return_arr

def delete(request, table_id, Order):
    size = tableSize(table_id)
    data = Data.objects.filter(Table_id = table_id, Order = Order)
    for item in data:
        item.delete()
    if Order + 1 != size:
        data = Data.objects.filter(Table_id = table_id, Order__gt = Order)
        for item in data:
            item.Order = item.Order - 1
            item.save()
    return redirect("tables", table_id)

def outputCSV(request, table_id):
    data = exportTableData(table_id)
    fields = Fields.objects.filter(Table_id=table_id).order_by("Order")
    headers = [field.Field for field in fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="output_{table_id}.csv"'
    writer = csv.writer(response)
    if headers:
        writer.writerow(headers)
    writer.writerows(data)
    return response

def tables(request, table_id):
    table_title = Table.objects.get(id = table_id).Title
    fields = Fields.objects.filter(Table_id = table_id).order_by("Order")
    project = Project.objects.get(id = Table.objects.get(id = table_id).Project_id)
    if(fields.count() == 0):
        return redirect("fields", table_id)
    table_arr = tableData(table_id)
    type_arr = []
    head = []
    for field in fields:
        head.append(field.Field)
        temp = {}
        if field.Type == "Character":
            temp = {
            "type" :  "text",
            "val" : str(field.id)
            }
        elif field.Type == "Integer":
            temp = {
            "type" :  "number",
            "val" : str(field.id)
            }
        type_arr.append(temp)
    if request.method == 'POST':
        for item in type_arr:
            data = request.POST.get(item["val"])
            Data.objects.create(Data = data, Field_id = int(item["val"]), Table_id = table_id, Order = tableSize(table_id))
        return redirect("tables", table_id)
    return render(request, "tables.html", context = {"tables":table_arr,"project":project, "head":head, "type":type_arr, "table_id":table_id, "title":table_title})

def table(request, project_id):
    project = Project.objects.get(id = project_id)
    if request.method == 'POST':
        name = request.POST.get('tableName')
        number = request.POST.get('fieldNumber')
        if name and number:
            Table.objects.create(Title=name, Fields=number, Project_id = project_id)
            table_id = Table.objects.get(Title=name, Fields=number, Project_id = project_id).id
            return redirect("fields", table_id)
    return render(request, "table.html", context = {"project":project})