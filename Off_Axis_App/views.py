from django.shortcuts import render

# Create your views here.


def components(request):
    return render(
        request,
        "components/index.html",
        {
            "test_options": [
                {"label": "United States", "value": "US"},
                {"label": "Canada", "value": "CA"},
                {"label": "Mexico", "value": "MX"},
            ]
        },
    )
