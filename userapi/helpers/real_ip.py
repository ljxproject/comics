import json
import urllib3


class RealIP(object):
    @classmethod
    def get_real_ip(cls, request):
        if 'HTTP_X_REAL_IP' in request.META.keys():
            ip = request.META['HTTP_X_REAL_IP']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip

    @classmethod
    def send(cls, ip):
        url = "http://ip.taobao.com/service/getIpInfo.php"
        http = urllib3.PoolManager()
        r_obj = http.request("GET", url, fields={"ip": ip}, retries=3, timeout=2)
        ip_obj = json.loads(r_obj.data, encoding="utf-8")
        return cls.get_country(ip_obj)

    @classmethod
    def get_country(cls, ip_obj):
        return ip_obj["data"]["country"] if ip_obj["code"] == 0 else None


real_ip = RealIP()
