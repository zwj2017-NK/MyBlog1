# BuTian Vulnerabilities Spider
**B**utian **Vulnerabilities** *S*pider

## Usage
```
usage: ButianVul.py [options]

* BuTian Vulnerabilities Spider *

optional arguments:
  -h, --help         show this help message and exit
  -s StartPage       Start page for crawling (default: 1)
  -e EndPage         End page for crawling (default: 2)
  -ct CompanyThread  Num of company threads (default: 10)
  -vt VulThread      Num of vul threads (default: 10)
  --company          Company Spider (default: False)
  --vul              Vulnerability Spider (default: False)
  --evul             Vul Exists (default: False)

```

### Instruction
```
1. Python 2.7.11 && BeautifulSoup4 4.3.2 && pymongo && requests
2. s - 起始页面，e - 终止页面（包括），ct - 爬取漏洞厂商线程，vt - 爬取漏洞名线程
3. company - 是否爬取漏洞厂商，vul - 是否爬取漏洞名，evul - 爬取漏洞名的厂商是否 vul 字段已经存在 
4. 运行第一步，先爬取所有的厂商，保存至数据库
5. 运行第二步，爬取漏洞名，保存至数据库
6. 运行第三步，查看是否有漏爬的漏洞名
7. 期间会有各种无法连接，因为没用代理池，所以只能隔一段时间继续爬，只要数据库建好，之后每天晚上爬一遍当天的漏洞即可，大概 1-11 页
8. 至5月8日，一共爬取 32000 多漏洞厂商，漏洞 10W +
```

### Example
```
python ButianVul.py -s 1 -e 11 --company --vul --evul
python ButianVul.py --vul
```
