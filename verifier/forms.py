from django import forms

class LabelForm(forms.Form):
    brand_name = forms.CharField(label="Brand Name", max_length=100)
    product_type = forms.CharField(label="Product Class/Type", max_length=100)
    alcohol_content = forms.CharField(label="Alcohol Content (% ABV)", max_length=20)
    net_contents = forms.CharField(label="Net Contents (e.g., 750 mL)", max_length=20, required=False)
    label_image = forms.ImageField(label="Upload Label Image")

