#coding=utf-8
import tool.driver as driver
import os
import requests,json,time,webbrowser

config = {
    "questionURL": {
    "danxuan" : "https://blog-static.cnblogs.com/files/FSHOU/guoan_danxuan.js",
    "duoxuan" : "https://blog-static.cnblogs.com/files/FSHOU/guoan_duoxuan.js",
    "panduan" : "https://blog-static.cnblogs.com/files/FSHOU/guoan_panduan.js",
    },
    "schoolInfoURL" : "https://blog-static.cnblogs.com/files/FSHOU/guoan_school.js",
    "newsURL" : "https://blog-static.cnblogs.com/files/FSHOU/guoan_news.js"
}
info = {
    "题库": {
        "danxuan": [], "duoxuan": [], "panduan": []
    },
    "学校信息": [],
    "最新消息":{}
}
htmlData = ''

def questionRequest():
    tkTypeList = ["单选","多选","判断"]
    num = 0
    for i in config["questionURL"]:
        print(f"正在获取最新[{tkTypeList[num]}]题库...")
        info["题库"][i] = eval(requests.get(config["questionURL"][i]).text)

        num+=1
    print("加载题库完毕")


def getSchoolInfo():
    info["学校信息"] = json.loads(requests.get(config["schoolInfoURL"]).text)
# print(info["学校信息"])
# print(info["最新消息"])

def getNews():
    info["最新消息"] = json.loads(requests.get(config["newsURL"]).text)

#检查版本信息
def checkVersion(version):
    if info["最新消息"]["latestVersion"] > version:
        print(info["最新消息"]["updateMsg"])
        if info["最新消息"]["level"] == 3:
            print("本次更新非常必要，不更新将无法正常使用该程序，请前往项目进行下载更新")
            print("https://github.com/aqz236/guoan")
            input("按Enter键跳帮你跳转到项目地址...")
            webbrowser.open("https://github.com/aqz236/guoan")
        return 1
    elif info["最新消息"]["latestVersion"] == version:
        print("当前使用的是最新版本！v_",str(version))
        print('''  ______   _                   
 |  ____| | |                  
 | |__ ___| |__   _____      __
 |  __/ __| '_ \ / _ \ \ /\ / /
 | |  \__ \ | | | (_) \ V  V / 
 |_|  |___/_| |_|\___/ \_/\_/  
                               
                               ''')
        print(info["最新消息"]["msg"])

        return 0
    else:
        return 2
#操作手进行工作
def run(schoolId,userId,passwd,allData):
    check = driver.login(schoolId,userId,passwd,allData)
    return check
#学校名称校验
def checkSchoolName(name):
    try:
        for i in info["学校信息"]:
            if name == i['char']:
                return i['code']
    except:
        print("没匹配到学校，请尝试重新输入，如果确认输入无误请联系作者添加学校信息")
        checkInput()
#输入校验
def checkInput():
    global htmlData
    while True:
        schoolCode = checkSchoolName(input("请输入学校名称 (Enter键入以下一步)："))
        userId = input("请输入学号 (Enter键入以下一步)：")
        userPasswd = input("请输入密码 (Enter键入以运行程序)：")
        check = run(schoolCode, userId, userPasswd, info)
        if check['code'] == 123321:
            print("【登录失败】 ",check['msg'])
            checkInput()
        elif check['code'] == 460064:
            print(check['msg'])
            main()
        elif check['code'] == 5211314:
            print(check['msg'],"---- 即将打开网页，方便用户截图")
            print("")
            htmlData = check['data']
            # myFlask.getHtmlData(htmlData)
            try:
                os.remove(f'{userId}国家安全知识考试.html')
            except:
                pass
            with open(f'{userId}国家安全知识考试.html', 'a',  encoding='utf-8')as f2:  # f2为文件描述符
                f2.write(htmlData)
            webbrowser.open(f'{userId}国家安全知识考试.html')
            print("得分页面已打开，如果提示请选择浏览器打开，随便选择一个点击确定")
            time.sleep(10)
            os.remove(f'{userId}国家安全知识考试.html')



def main():
    version = 1.1
    print(f"当前版本：{version}")
    getNews()  # 获取公告以及版本信息
    checkCode = checkVersion(version)
    if checkCode == 0:
        getSchoolInfo(), questionRequest()  # 获取学校信息, 获取题库信息
        data = checkInput()
        return data
    elif checkCode == 1:
        print("程序未更新,程序退出")
        exit()
    else:
        print("程序出错退出")
        exit()
if __name__ == '__main__':
    main()












# def run(schoolName,userId,userPasswd):
#     code = driver.login(userId,userPasswd,schoolName,info["题库"],info["学校信息"])
#     return code




