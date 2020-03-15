from django.shortcuts import render
from vote_app import models
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import F
from django.db import transaction

# Create your views here.


def home(request):
    """投票首页"""
    if request.method == 'GET':
        activity_record = models.Activity.objects.first()
        return render(request, 'home_page.html', {'record': activity_record})
    return HttpResponse('ok')


def index(request, activity_id):
    IP = request.META.get('REMOTE_ADDR')
    activity_record = models.Activity.objects.get(id=activity_id)
    # 活动详情记录
    ad_records = models.ActivityDetail.objects.filter(activity_id=activity_id)
    # 活动详情已投票记录
    voted_records = models.VoteRecord.objects.filter(IP=IP, activity_detail_id__activity_id=activity_id).values_list('activity_detail_id')
    voted_ids = set(map(lambda v: v[0], voted_records))
    return render(request, 'index.html', {'ad_records': ad_records, 'a_record': activity_record, 'voted_ids': voted_ids})


def voting(request):
    IP = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        activity_detail_id = request.POST.get('activity_detail_id')
        ad_record = models.ActivityDetail.objects.get(id=activity_detail_id)
        if not ad_record:
            return HttpResponseBadRequest('Error request data by activity_detail_id!')
        # 投票上限判断
        v_records = models.VoteRecord.objects.filter(IP=IP, activity_type=ad_record.activity_type_id,
                                                     activity_detail_id__activity_id=ad_record.activity_id)

        if len(v_records) >= 1:
            return JsonResponse({'code': 202, 'msg': '已经超过投票限制'})

        # 添加事务
        with transaction.atomic():
            models.VoteRecord.objects.create(IP=IP, activity_detail_id=ad_record, activity_type=ad_record.activity_type_id)
            models.ActivityDetail.objects.filter(id=activity_detail_id).update(vote_count=F('vote_count') + 1)
        return JsonResponse({'code': 200, 'msg': '您已投票成功'})

    return JsonResponse({'code': 500, 'msg': '投票失败'})
