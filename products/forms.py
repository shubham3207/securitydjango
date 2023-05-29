from django.forms import ModelForm
from .models import Product, Review


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value':'Rate',
            'body':'Add your comment with your rating'
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ImageForm(ModelForm):
    class Meta:
        model = Product
        fields = ('image',)
