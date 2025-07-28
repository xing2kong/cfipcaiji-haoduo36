import requests
import re
import os

# 优选 IP 源
urls1 = [
    'https://ip.164746.xyz',
    'https://cf.090227.xyz',
    'https://stock.hostmonit.com/CloudFlareYes',
    'https://api.uouin.com/cloudflare.html',
    'https://www.wetest.vip/page/edgeone/address_v4.html',
    'https://www.wetest.vip/page/cloudfront/address_v4.html',
    'https://www.wetest.vip/page/cloudflare/address_v4.html'
]

# 优选 CNAME 源
urls2 = [
    'https://www.wetest.vip/page/cloudflare/cname.html'
]

# 正则表达式
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
cname_pattern = r'\b(?:[a-zA-Z0-9-]+\.)*cloudflare[a-zA-Z0-9-]*\.[a-zA-Z]{2,6}\b'

# 删除旧文件
for filename in ['ip.txt', 'cname.txt']:
    if os.path.exists(filename):
        os.remove(filename)

# 使用集合自动去重
unique_ips = set()
unique_cnames = set()

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; PythonBot/1.0)'
}

# 抓取 IP 地址
for url in urls1:
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            ip_list = re.findall(ip_pattern, resp.text)
            unique_ips.update(ip_list)
    except Exception as e:
        print(f"[IP源失败] {url} - {e}")

# 抓取 CNAME 地址
for url in urls2:
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            cname_list = re.findall(cname_pattern, resp.text)
            unique_cnames.update(cname_list)
    except Exception as e:
        print(f"[CNAME源失败] {url} - {e}")

# 写入 IP
if unique_ips:
    sorted_ips = sorted(unique_ips, key=lambda ip: [int(part) for part in ip.split('.')])
    with open('ip.txt', 'w') as f:
        for ip in sorted_ips:
            f.write(ip + '\n')
    print(f'已保存 {len(sorted_ips)} 个 IP 到 ip.txt')
else:
    print('未提取到任何 IP')

# 写入 CNAME
if unique_cnames:
    sorted_cnames = sorted(unique_cnames)
    with open('cname.txt', 'w') as f:
        for cname in sorted_cnames:
            f.write(cname + '\n')
    print(f'已保存 {len(sorted_cnames)} 个 CNAME 到 cname.txt')
else:
    print('未提取到任何 CNAME')
