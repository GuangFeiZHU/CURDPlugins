from django.shortcuts import render


# Create your views here.
# popup 练习
def test(request):
    if request.method == 'GET':
        return render(request, 'test_for_popup.html')
