from django.shortcuts import render
from .forms import LabelForm
from PIL import Image
import pytesseract
import re, os

def normalize(text: str) -> str:
    """Normalize text for loose matching"""
    return re.sub(r'\s+', ' ', text.strip().lower())

def verify_text_matches(form_data, ocr_text):
    """Compare OCR output with form fields"""
    results = {}
    text_norm = normalize(ocr_text)

    for field, value in form_data.items():
        if not value:
            continue
        value_norm = normalize(value)
        if value_norm in text_norm:
            results[field] = {"match": True, "message": ""}
        else:
            results[field] = {"match": False, "message": f"'{value}' not found on label"}

    gov_warning = "government warning" in text_norm
    results["Government Warning"] = {
        "match": gov_warning,
        "message": "" if gov_warning else "Missing 'Government Warning' text"
    }
    return results

def label_form_view(request):
    context = {}
    if request.method == "POST":
        form = LabelForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["label_image"]
            image_path = os.path.join("media", image.name)
            os.makedirs("media", exist_ok=True)
            with open(image_path, "wb+") as dest:
                for chunk in image.chunks():
                    dest.write(chunk)

            try:
                ocr_text = pytesseract.image_to_string(Image.open(image_path))
            except Exception as e:
                context["error"] = f"OCR processing failed: {e}"
                return render(request, "verifier/form.html", context)

            form_data = {
                "Brand Name": form.cleaned_data["brand_name"],
                "Product Type": form.cleaned_data["product_type"],
                "Alcohol Content": form.cleaned_data["alcohol_content"],
                "Net Contents": form.cleaned_data["net_contents"],
            }

            context["results"] = verify_text_matches(form_data, ocr_text)
            context["ocr_text"] = ocr_text
            os.remove(image_path)
    else:
        form = LabelForm()

    context["form"] = form
    return render(request, "verifier/form.html", context)

