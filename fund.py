# coding = utf-8

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import datetime

# 引入预警函数
from warn import warn

# 引入发邮件函数
from auto_email import auto_email

# choiceFund = ['007916']
choiceFund = ['519674', '163406', '004433', '005609', '005968', '320007', '161725', '005827', '006327', '110011',
              '001875', '162605', '001679', '003095']

title = ['银河创新成长混合', '兴全合润混合(LOF)', '南方有色金属ETF联接C', '富国军工主题混合A', '创金合信工业周期股票A', '诺安成长混合', '招商中证白酒指数(LOF)', '易方达蓝筹精选混合',
         '易方达中证海外联接人民币A', '易方达中小盘混合', '前海开源沪港深优势精选混合A', '景顺长城鼎益混合(LOF)', '前海开源中国稀缺资产混合A']

# 正则模式
findTitle = re.compile(r'<div class="fundDetail-tit"><div style="float: left">(.*?)<span>')
findDate1 = re.compile(r'单位净值</a></span> \(</span>(.*?)\)</p>')
findNet1 = re.compile(r'<span class="ui-font-large ui-color-[a-z]+ ui-num">(.*?)<\/span>')
findScale = re.compile(r'基金规模</a>：(.*?)</td>')

# 基金名称单独获取
findList = [findDate1, findNet1, findScale]


def main():
    # 基础url，根据基金代码拼成最终的url，例如
    baseUrl = 'http://fund.eastmoney.com/'
    # excel文件保存路径，每天的文件按日期拼接成最终的路径，例如’fund数据(2021-04-22).xls‘
    savePath = 'fund数据'

    print('爬虫启动！！！')
    print('#' * 66)
    # 计时
    old = datetime.datetime.now()
    # 获取数据列表
    dataList = getData(baseUrl)
    new = datetime.datetime.now()
    print('#' * 66)
    print('爬取完毕，共耗时%s秒\n' % (new - old).seconds)

    # 保存数据到excel
    print('保存数据中......')
    saveData(savePath, dataList)
    print('保存完毕,请查看当前文件夹下的今日数据......\n')

    # 生成预警基金列表
    print('生成预警基金列表中......')
    warnList = warn()
    print('生成完毕，将自动发送邮件，请注意查收！！！')
    print('#' * 66)

    # 自动发送邮件
    if len(warnList) != 0:
        auto_email(warnList)


def getData(baseUrl):
    dataList = []
    i = 1
    # 遍历自选基金爬取
    for choice in choiceFund:
        # 构建url
        url = baseUrl + choice + '.html'
        # 获取对应html
        html = askUrl(url)
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        # 获取基金名称
        for item in soup.find_all('div', class_='fundDetail-tit'):
            item = str(item)
            title = re.findall(findTitle, item)[0]
            print('%d.爬取%s(%s)的数据中......' % (i, title, choice))
            data.append(title)
        data.append(choice)
        # 循环获取剩余数据
        for item in soup.find_all('div', class_='fundInfoItem'):
            item = str(item)
            for find in findList:
                data.append(re.findall(find, item)[0])
        print(data)
        dataList.append(data)
        i = i + 1
    return dataList


# 根据最终url,获取对应html，并由getData()函数调用
def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/"
                      "90.0.4430.72Safari/537.36Edg/90.0.818.42 "
    }
    request = urllib.request.Request(url, headers=head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html


# 保存数据，不同日期的数据保存到不同的excel文件中
def saveData(savePath, dataList):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('fund数据' + dataList[0][2], cell_overwrite_ok=True)
    col = ('基金名称', '基金代号', '净值日期', '基金净值', '基金规模')
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])

    for i in range(1, len(choiceFund)):
        for j in range(0, len(col)):
            sheet.write(i, j, dataList[i - 1][j])

    # 由基础路径和日期组合实际路径
    book.save(savePath + '(' + dataList[0][2] + ').xls')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        auto_email(str(e))
        raise e
    finally:
        print('done')
