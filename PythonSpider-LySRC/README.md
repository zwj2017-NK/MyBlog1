# LySRC Public Vulnerabilities
**Ly**SRC **P**ublic **Vulnerabilities**

## Usage
```
usage: LySrc.py [options]

* LySRC Public Vulnerabilities *

optional arguments:
  -h, --help    show this help message and exit
  -n VulPages   Total pages (default: 6)
  -s VulSpeed   Speed of pages (default: 6)
  -t ThreadNum  Num of threads (default: 10)

```

### Instruction
```
1. Python 2.7.11 && BeautifulSoup4 4.3.2
2. 自定义线程数量，VulSpeed线程数代表获取漏洞列表，ThreadNum线程数代表获取漏洞详情
3. 如果两个漏洞名一样，暂时未解决（目前只有 微信机票一处越权 这个漏洞是重名）
```

### Example
```
python lysrc.py -s 5
```
