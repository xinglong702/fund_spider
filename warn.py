import xlrd
import time

# 设置初始日期和当前日期
startDate = '2021-04-26'
startDate1 = '2012-5-12'
# 今日日期
endDate = time.strftime('%Y-%m-%d')

# 根据日期拼出相应的excel文件路径
startPath = 'fund数据(' + startDate + ').xls'
startPath1 = 'fund数据(' + startDate1 + ').xls'
endPath = 'fund数据(' + endDate + ').xls'

warnList = []


def warn():
    # 分别获取这两日的数据，并保存成字典
    startBook = xlrd.open_workbook(startPath)
    startSheet = startBook.sheets()[0]
    startDict = dict(zip(startSheet.col_values(0, 1), startSheet.col_values(3, 1)))

    startBook1 = xlrd.open_workbook(startPath1)
    startSheet1 = startBook1.sheets()[0]
    startDict1 = dict(zip(startSheet1.col_values(0, 1), startSheet1.col_values(3, 1)))

    try:
        endBook = xlrd.open_workbook(endPath)
    except Exception as e:
        return warnList

    endSheet = endBook.sheets()[0]
    endDict = dict(zip(endSheet.col_values(0, 1), endSheet.col_values(3, 1)))

    for fund in endDict:
        endNet = float(endDict[fund])
        # 防止有些自选是后面加进去的
        if fund in startDict:
            startNet = float(startDict[fund])
            startNet1 = float(startDict1[fund])
            diff1 = (startNet - endNet) / startNet
            diff1_1 = (startNet1 - endNet) / startNet1
            diff2 = (endNet - startNet) / startNet
            if diff1 > 0.1:
                warnList.append(fund + '相对于' + startDate + '跌了' + str(round(diff1, 3) * 100) + '%')
            if diff1 > 0.05:
                warnList.append(fund + '相对于' + startDate + '跌了' + str(round(diff1, 3) * 100) + '%')
            if diff1_1 > 0.05:
                warnList.append(fund + '相对于' + startDate1 + '跌了' + str(round(diff1_1, 3) * 100) + '%')
            if diff2 > 0.1:
                warnList.insert(0, '恭喜基金' + fund + '相对于' + startDate + '涨了' + str(round(diff2, 4) * 100) + '%')
            if diff2 > 0.2:
                warnList.insert(0, '恭喜基金' + fund + '相对于' + startDate + '涨了' + str(round(diff2, 4) * 100) + '%')
    return warnList
