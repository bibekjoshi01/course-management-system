from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('This category already exists.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')

        # Ensure only one level of subcategories
        if parent and parent.parent:
            self.add_error('parent', 'A category can only have one level of subcategories.')

        return cleaned_data
