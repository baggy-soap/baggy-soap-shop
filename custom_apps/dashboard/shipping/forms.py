from django import forms

from oscar.core.loading import get_model


class WeightBasedForm(forms.ModelForm):

    class Meta:
        model = get_model('shipping', 'WeightBased')
        fields = ['name', 'description', 'default_weight', 'send_multiples', 'countries']
