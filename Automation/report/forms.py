from Automation.report.models import * # Change as necessary
from django.forms import ModelForm

class TodoListForm(ModelForm):
  class Meta:
    model = TodoList

class TodoItemForm(ModelForm):
  class Meta:
    model = TodoItem
    exclude = ('list',)

