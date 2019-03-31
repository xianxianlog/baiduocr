from django.shortcuts import render,redirect
from django.http import JsonResponse
from aip import AipOcr
import time
from django.views.generic import View
# Create your views here.

class IndexView(View):
    def get(self,request):
        return render(request,"index.html",{})

def form_ocr(request):
    """接收图片获取图片数据并向百度发送请求获取响应"""
    if request.method=='POST':
        # 1.获取图片
        print("开始工作")
        print(request.FILES)
        try:
            pic=request.FILES['pic']
            print(pic.size)
            print(pic.name)

            # 2.读取图片数据
            img=pic.read()
            #print(img)
        except:
            return JsonResponse({'return_msg':0})

        # 3.向百度发送请求获取响应
        AK = '自己的AK'
        SK = '自己的SK'
        app_id = "自己的app_id"
        client = AipOcr(app_id, AK, SK)
        options={}
        options['result_type']='excel'
        result_id = client.tableRecognitionAsync(img,options)
        try:
            request_id = result_id['result'][0]['request_id']
            print(request_id)
        except:
            request_id = ""

        return_msg=0
        file_url=""
        if request_id:
            try_times=0
            while True:
                time.sleep(10)
                result = client.getTableRecognitionResult(request_id)
                print(result)
                try:
                    msg = result['result']['ret_msg']
                except:
                    print("出错")
                    # 返回给前端的数据信息
                    return_msg=0
                    break
                if msg == "已完成":
                    file_url = result['result']['result_data']
                    return_msg=1
                    break
                else:
                    try_times+=1
                    print('try_times',try_times)
                    if try_times>2:
                        print("网络繁忙，请稍后再试")
                        return_msg=0
                        break
                    continue
            else:
                return_msg=0

        return JsonResponse({'return_msg':return_msg,'file_url':file_url})

