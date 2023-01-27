from django import forms

class Car(forms.Form):
    COLORS = [
        ("red", "Red"),
        ("blue", "Blue"),
        ("green", "Green"),
    ]

    name = forms.CharField(max_length=100)
    color = forms.ChoiceField(choices=COLORS)