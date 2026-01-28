from django.shortcuts import render

# Create your views here.
def policyCategoriesList(request):
    template_name = 'policy/categories.html'
    return render(request,template_name=template_name)


def policyCategoriesCreate(request):
    template_name = 'policy/categorie-create.html'
    return render(request,template_name=template_name)


def policyCreateHelth(request):
    template_name = 'policy/policies-create-health.html'
    return render(request,template_name=template_name)

