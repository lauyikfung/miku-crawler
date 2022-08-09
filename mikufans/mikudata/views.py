from django.shortcuts import render
from django.http import HttpResponse
import time
from .models import allup
from .models import allvideo
# Create your views here.
def toMainPage(request):
    return render(request, 'mikufans.html')
def toUplistPage(request):
    return render(request, 'uplist.html')
def toVideoListPage(request):
    return render(request, 'videolist.html')
def toUpspace(request):
    if request.POST:
        ordering = int(request.POST['ord'])
        return render(request, 'upspace.html', context={'ord': ordering})
    else:
        return HttpResponse('please visit us with POST')
def toVideo(request):
    if request.POST:
        ordering = int(request.POST['ord'])
        return render(request, 'video.html', context={'ord': ordering})
    else:
        return HttpResponse('please visit us with POST')
def searchUp(request):
    if request.POST:
        keyword = request.POST['keyword']
        keyer = request.POST['keyword']
        start_t = time.time()
        result_list1 = allup.objects.filter(upname__contains=keyword).values_list('id', flat=True)
        result_list2 = allup.objects.filter(upsign__contains=keyword).values_list('id', flat=True)
        result_set = set(result_list1).union(set(result_list2))
        result_list = list(result_set)
        num = len(result_list)
        timer = round((time.time() - start_t) * 1000, 2)
        return render(request, 'search_result_up.html',
                      context={'result': result_list, 'num': num, 'time': timer, 'keys': str(keyer)})
    else:
        return HttpResponse('please visit us with POST')
def searchVideo(request):
    if request.POST:
        keyword = request.POST['keyword']
        keyer = request.POST['keyword']
        start_t = time.time()
        result_list1 = allvideo.objects.filter(vtitle__contains=keyword).values_list('id', flat=True)
        result_list2 = allvideo.objects.filter(vdesc__contains=keyword).values_list('id', flat=True)
        result_set = set(result_list1).union(set(result_list2))
        result_list = list(result_set)
        num = len(result_list)
        timer = round((time.time() - start_t) * 1000, 2)
        return render(request, 'search_result_video.html', context={'result':result_list, 'num':num, 'time': timer,
                                                                    'keys': str(keyer)})
    else:
        return HttpResponse('please visit us with POST')