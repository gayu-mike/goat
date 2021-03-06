from django import forms
from django.core.exceptions import ValidationError

from lists.models import Todo, List


DUPLICATE_INPUT_ERROR = "You've already got this in your list"
EMPTY_INPUT_ERROR = "You can't have an empty input"


class TodoForm(forms.models.ModelForm):

    class Meta:
        model = Todo
        fields = ('task',)
        widgets = {
            'task': forms.fields.TextInput(attrs={
                'placeholder': 'What do you want to do?',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'task': {'required': EMPTY_INPUT_ERROR}
        }


class ExistingListTodoForm(TodoForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'task': [DUPLICATE_INPUT_ERROR]}
            self._update_errors(e)


class NewListForm(TodoForm):

    def save(self, user):
        if user.is_authenticated:
            ls = List.create_new(
                first_todo=self.cleaned_data['task'],
                user=user
            )
        else:
            ls = List.create_new(first_todo=self.cleaned_data['task'])
        return ls
