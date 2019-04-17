# -*- coding: utf-8 -*-
import json

import requests
from django.http import JsonResponse

from account.decorators import login_exempt
from common.mymako import render_mako_context
from  common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.esb_helper import cc_search_biz, cc_search_set, run_fast_execute_script, cc_search_host, \
    get_job_instance_log, get_host_ip_list, cc_get_job_detail, run_execute_job, cc_fast_push_file


def home(request):
    """
    首页
    """
    id = request.GET.get('id')
    return render_mako_context(request, '/home_application/home.html',{ "id":id})


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    return render_json({"result": True, "message": "success", "data": request.user.username})


def modal(request):
    """
    测试
    """
    return render_mako_context(request, '/home_application/modal.html')


def getJson(request):
    data = [
        {'time': '1月1日',  'cpu': 89.3, 'men': 96.4, 'disk':88},
        {'time': '1月2日',  'cpu': 79.3, 'men': 88.4, 'disk': 78},
        {'time': '1月3日',  'cpu': 88.3, 'men': 78.4, 'disk': 84},
        {'time': '1月4日', 'cpu': 78.3, 'men': 63.4, 'disk': 76},
        {'time': '1月5日',  'cpu': 74.3, 'men': 94.4, 'disk': 79},
        {'time': '1月6日',  'cpu': 85.3, 'men': 87.4, 'disk': 98}
    ]
    return render_json({"result": True,"data": data})
# 返回echarts 图标拼接格式数据
# series 下面的type 表示需要渲染哪种图表类型
# line:折线图   bar:柱状图
def getEchartsJson(request):
    data ={
        "xAxis": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "series": [
            {
                "name": "cpu",
                "type": "line",
                "data": [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
            },
            {
                "name": "men",
                "type": "line",
                "data": [3.6, 6.9, 8.0, 21.4, 23.7, 78.7, 165.6, 152.2, 68.7, 28.8, 7.0, 8.3]
            },
            {
                "name": "disk",
                "type": "bar",
                "data": [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
            }
        ]
    }
    return render_json({"result": True,"data": data})
# 该方法一般不作修改
def search_biz(request):
    data = cc_search_biz(request.user.username)
    return JsonResponse(data)


def search_set(request):
    """
    传递参数
    :param 业务id   biz_id
    :param request:
    :return:
    """
    biz_id = request.GET.get('biz_id')
    data = cc_search_set(biz_id)
    return JsonResponse(data)


def search_host(request):
    """
    :param request:
    传递参数
    :param 业务id   biz_id,
    biz_id,ip_list = ['10.92.190.214','10.92.190.215']
    get请求获取的ip_list，转换成列表，请调用get_host_ip_list
    :return:
    """
    biz_id = request.GET.get('biz_id')
    ip_list = []
    if 'ip' in request.GET:
        ip = request.GET.get('ip')
        ip_list = get_host_ip_list(ip)
    data = cc_search_host(biz_id,ip_list)
    return JsonResponse(data)


def fast_execute_script(request):
    """
    :param request:
    传递参数
    :param 业务id   biz_id,
         ip_list = [
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.214"
            }
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.215"
            }
        ]
    :return:
    """
    biz_id = request.GET.get('biz_id')
    script_content = """
         df -h
    """
    ip_list = [
        {
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    data = run_fast_execute_script(biz_id,script_content,ip_list,request.user.username)
    return JsonResponse(data)


def execute_job(request):
    """
    :param request:
    传递参数
    :param 业务id       biz_id,
    :param 作业模板id    job_id,
    :param ip列表     ip_list = [
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.214"
            }
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.215"
            }
        ]
    :return:
    """
    biz_id = request.GET.get('biz_id')
    job_id = request.GET.get('job_id')
    ip_list = [
        {
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    data = run_execute_job(biz_id, job_id, ip_list,request.user.username)
    return JsonResponse(data)


def get_log_content(request):
    """
        :param request:
        传递参数
        :param 业务id       biz_id,
        :param 作业实例id    instance_id,
        :return:
        """
    biz_id = request.GET.get('biz_id')
    job_instance_id = request.GET.get('instance_id')
    result = get_job_instance_log(biz_id, job_instance_id,request.user.username)
    data = {
        "data": result
    }
    return JsonResponse(data)


def job_detail(request):
    """
        :param request:
        传递参数
        :param 业务id       biz_id,
        :param 作业实例id    instance_id,
        :return:
        """
    biz_id = request.GET.get('biz_id')
    job_id = request.GET.get('job_id')
    data = cc_get_job_detail(biz_id, job_id, request.user.username)
    return JsonResponse(data)


def fast_push_file(request):
    biz_id = request.GET.get('biz_id')
    file_target_path = "/tmp/"
    target_ip_list = [{
      "bk_cloud_id": 0,
      "ip": "192.168.240.52"
    },
        {
      "bk_cloud_id": 0,
      "ip": "192.168.240.55"
    }
    ]
    file_source_ip_list = [{
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    file_source = ["/tmp/test12.txt","/tmp/test123.txt"]
    data = cc_fast_push_file(biz_id, file_target_path, file_source, target_ip_list, file_source_ip_list,request.user.username)
    return JsonResponse(data)

