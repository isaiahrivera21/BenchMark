from django import forms


class WeightEntryForm(forms.Form):
    weight = forms.FloatField()


class StepsEntryForm(forms.Form):
    steps = forms.IntegerField()
