#coding=utf-8
import requests,re,json
import datetime
import random
#注册cookie信息
stuInfo = {}
cookieArr = {}
answer = []
userInfo = {}
danxuan = []
duoxuan = []
panduan = []
def regeditCookie():
    global cookieArr
    url = 'http://gjaqzsjs.haedu.cn/Login/isLogin'
    headers = {'Host': 'gjaqzsjs.haedu.cn', 'Connection': 'keep-alive', 'Content-Length': '0', 'Accept': '*/*',
               'Origin': 'http://gjaqzsjs.haedu.cn', 'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Referer': 'http://gjaqzsjs.haedu.cn/', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {}
    data = {}
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    XSRF_TOKEN = re.findall(r'XSRF-TOKEN=(.*?);', html.headers['Set-Cookie'], re.I)[0]
    laravel_session = re.findall(r'laravel_session=(.*?);', html.headers['Set-Cookie'], re.I)[0]
    cookieArr = {"XSRF_TOKEN":XSRF_TOKEN,"laravel_session":laravel_session}

def login(schoolId,userId,passwd,allData):
    global danxuan,duoxuan,panduan
    danxuan = allData["题库"]['danxuan']
    duoxuan = allData["题库"]['duoxuan']
    panduan = allData["题库"]['panduan']
    regeditCookie()#获取cookie
    global stuInfo,cookieArr,userInfo
    url = 'http://gjaqzsjs.haedu.cn/Login/auth'
    headers = {'Host': 'gjaqzsjs.haedu.cn', 'Connection': 'keep-alive', 'Content-Length': '48', 'Accept': '*/*',
               'Origin': 'http://gjaqzsjs.haedu.cn', 'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'http://gjaqzsjs.haedu.cn/', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {
               'XSRF-TOKEN': cookieArr["XSRF_TOKEN"],
               'laravel_session': cookieArr["laravel_session"]}
    data = {
        'unit_code': str(schoolId),
        'student_id': str(userId),
        'password': str(passwd)
    }
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    stuInfo = json.loads(html.text)#转中文
    if stuInfo['code'] == 2000:
        # print(stuInfo)
        userInfo = stuInfo['data']#拿到用户信息 用于最后生成前端页面
        check = getQuestionLists()
        return check
    else:
        return {'code' : 123321, 'msg':stuInfo['msg']}


def getQuestionLists():
    global cookieArr,answer
    print("获取试题")
    url = 'http://gjaqzsjs.haedu.cn/Answer/getQuestionLists'
    headers = {'Host': 'gjaqzsjs.haedu.cn', 'Connection': 'keep-alive', 'Content-Length': '0', 'Accept': '*/*',
               'Origin': 'http://gjaqzsjs.haedu.cn', 'X-Requested-With': 'XMLHttpRequest', 'Access-Token': 'null',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Referer': 'http://gjaqzsjs.haedu.cn/gjaq_dati/page/answer.html', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {
               'XSRF-TOKEN': cookieArr["XSRF_TOKEN"],
               'laravel_session': cookieArr["laravel_session"]}
    data = {}
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    questionLists = json.loads(html.text)
    if questionLists['code'] == 4400:
        print("今天已经答过题了哦，再给你看一下成绩页面吧 (*/ω＼*)~")
        print("解放双手F兽，点个星星不迷路。下面是这个项目地址，来交个朋友")
        print("https://github.com/aqz236/guoan")
        # 制作前端页面
        getCore()
        check2 = createHtml()
        return check2
    else:
        for o in questionLists['data']['question']:
            if o['type_char'] == '单选':
                print("是单选")
                title = o['question']
                for p in danxuan:
                    if p['question'] == title:
                        print(f"[{o['type_char']}] 题目：", o['question'])
                        print("此题答案：",p['answer'])
                        answer.append({"number":f"{o['number']}","answer":f"{p['answer']}"})

            elif o['type_char'] == '多选':
                print("是多选")
                title = o['question']
                for p in duoxuan:
                    if p['question'] == title:
                        print(f"[{o['type_char']}] 题目：", o['question'])
                        print("此题答案：", p['answer'])
                        answer.append({"number":f"{o['number']}","answer":f"{p['answer']}"})

            elif o['type_char'] == '判断':
                print("是判断")
                title = o['question']
                for p in panduan:
                    if p['question'] == title:
                        print(f"[{o['type_char']}] 题目：", o['question'])
                        print("此题答案：", p['answer'])
                        if p['answer'] == '对' or  p['answer'] == '对 ':
                            p['answer'] = 'A'
                        elif p['answer'] == '错' or p['answer'] == '错 ':
                            p['answer'] = 'B'
                        answer.append({"number":f"{o['number']}","answer":f"{p['answer']}"})
    check = senPage(answer)#交卷
    return check
#提交试卷
def senPage(answer):
    global cookieArr
    url = 'http://gjaqzsjs.haedu.cn/Answer/submitAnswer'
    headers = {'Host': 'gjaqzsjs.haedu.cn', 'Proxy-Connection': 'keep-alive', 'Content-Length': '1183', 'Accept': '*/*',
               'Access-Token': 'null', 'Origin': 'http://gjaqzsjs.haedu.cn', 'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040029)',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    cookies = {
               'XSRF-TOKEN': cookieArr["XSRF_TOKEN"],
               'laravel_session': cookieArr["laravel_session"]}
    data = {
        "answer" : str(answer).replace("\'","\""),
        "use_time" : f'{random.randint(300,450)}'
    }
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    jsonResu = json.loads(html.text)
    if jsonResu['code'] == 4600:
        print("提交成功")
        #制作前端页面
        getCore()
        check = createHtml()
        return check
    else:
        return {'code':460064,'msg':f"提交失败,{jsonResu['msg']}"}

#获取当日得分情况
def getCore():
    global cookieArr,jsonData
    url = 'http://gjaqzsjs.haedu.cn//Answer/getRecord'
    headers = {'Host': 'gjaqzsjs.haedu.cn', 'Connection': 'keep-alive', 'Content-Length': '13', 'Accept': '*/*',
               'Origin': 'http://gjaqzsjs.haedu.cn', 'X-Requested-With': 'XMLHttpRequest', 'Access-Token': 'null',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'http://gjaqzsjs.haedu.cn/gjaq_dati/page/record.html?date=20211201',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {
               'XSRF-TOKEN': cookieArr["XSRF_TOKEN"],
               'laravel_session': cookieArr["laravel_session"]}
    data = {
        'date': str(datetime.datetime.now().strftime('%Y%m%d'))
    }

    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    jsonData = json.loads(html.text)

#制作html标签
def createHtml():
    global jsonData,userInfo
    score = jsonData['data']['score']
    arr = jsonData['data']['arr']
    use_time = jsonData['data']['use_time']
    use_time_char = jsonData['data']['use_time_char']
    true_total = jsonData['data']['true_total']
    false_total = jsonData['data']['false_total']
    plan = jsonData['data']['plan']

    html = ''
    num = 1
    for i in arr:
        head = f'''<div class="title">
<div class="index_wrap">【{i['type_char']}】{num}.</div>
<div class="issue">{i['question']}</div>
</div>
<div class="options">'''
        body = ''
        for o in i['questions']:
            options_item = f'''<div class="options_item">
<div>{o['key']}.</div>
<div class="txt">{o['val']}</div>
</div>'''
            body += options_item

        foot = f'''</div>
<div class="answer_wrap"> 
<div class="your_score">您的答案：<span style="color: #D05722">{i['your_answer']}</span></div>  
<div class="right_answer">标准答案：<span style="color: #169078">{i['true_answer']}</span></div>
</div>'''
        html += head + body + foot
        num += 1

    mainHead = f'''<!DOCTYPE html>
<!-- saved from url=(0051)http://gjaqzsjs.haedu.cn/gjaq_dati/page/record.html -->
<html lang="en" ml-update="aware"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
		<title>2021年全省大学生国家安全知识竞赛</title>
		<link rel="stylesheet" href="http://gjaqzsjs.haedu.cn/gjaq_dati/css/main.css">
		<link rel="stylesheet" href="http://gjaqzsjs.haedu.cn/gjaq_dati/css/record.css">
		<link rel="stylesheet" href="http://gjaqzsjs.haedu.cn/gjaq_dati/css/answer.css">
	<style type="text/css"></style></head>
	<body style="overflow: scroll; height: 100%;">
		<div class="banner">
			<img src="http://gjaqzsjs.haedu.cn/gjaq_dati/images/banner.png">
		</div>
		<div class="main">
			<div class="answer_userinfo">
				<div class="flex">
					<div>欢迎您，{userInfo['student_id']}</div>
					<div>{userInfo['unit_char']}</div>
					<div>{userInfo['name']}</div>
				</div>
				<div class="flex">
					<div class="cursor history_score">【历史成绩】</div>
					<div class="cursor exit">【注销】</div>
				</div>
			</div>
			<div class="question_wrap commen_content">
				<div class="date_wrap">
					<div class="date_txt">{plan}</div>
				</div>
				<!-- 得分 -->
				<div class="score">
					<div class="user_today_score">
						您的成绩：<span class="today_score" style="color: #d05722">{score}</span>
						分
					</div>
					<div class="desc_score">
						<div>
							用时：<span class="use_time" style="color: #d05722">{use_time}秒</span>
						</div>
						<div>
							答对：<span class="current_count" style="color: #169078">{true_total}</span>题
						</div>
						<div>
							答错：<span class="err_count" style="color: #d05722">{false_total}</span>题
						</div>
					</div>
				</div>
				<div class="question_list">'''
    mainFoot = f'''</div>
				<div class="submit_answer_btn">返回首页</div>
			</div>
		<div class="footer">
<div class="footer_content">
<div>技术支持：0371-56702890</div>
</div></div></div>

		<div class="info_dialog dialog">
			<!-- 标题 -->
			<div class="dialog_title">
				<img src="http://gjaqzsjs.haedu.cn/gjaq_dati/images/index/dialog_title_img.png" alt="">
				<div class="txt">进入答题前请先完善您的个人信息</div>
				<img src="http://gjaqzsjs.haedu.cn/gjaq_dati/images/index/dialog_title_img.png" alt="">
			</div>
			<!-- 输入框 -->
			<div class="dialog_content">
				<div class="card_item">
					<div class="desc">姓名：</div>
					<div class="input_wrap">
						<input type="text" placeholder="请输入您的姓名" name="name">
					</div>
				</div>
				<div class="card_item">
					<div class="desc">学校：</div>
					<div class="input_wrap search_input">
						<input type="text" placeholder="请输入您所在院校" name="school">
						<div class="search_btn">
							<img src="http://gjaqzsjs.haedu.cn/gjaq_dati/images/search.png" alt="">
						</div>

						<div class="school_list">
							<div class="list_wrap"></div>
						</div>
					</div>
				</div>
				<div class="card_item">
					<div class="desc">院系：</div>
					<div class="input_wrap">
						<input type="text" placeholder="请输入您所在院系" name="department">
					</div>
				</div>
				<div class="card_item">
					<div class="desc">专业：</div>
					<div class="input_wrap">
						<input type="text" placeholder="请输入您的专业" name="specialty">
					</div>
				</div>
				<div class="card_item">
					<div class="desc">学号：</div>
					<div class="input_wrap">
						<input type="text" placeholder="请输入您的学号" name="code">
					</div>
				</div>
				<div class="card_item">
					<div class="desc">身份证号：</div>
					<div class="input_wrap">
						<input type="text" placeholder="请输入您的身份证号" name="idcard">
					</div>
				</div>
			</div>
			<!-- 按钮 -->
			<div class="dialog_btns">
				<div class="cancel">取消</div>
				<div class="start_answer">进入答题</div>
			</div>
		</div>

    <div class="dialog_answer">
      <div class="dialog_answer_title">今日暂未答题，是否前往答题？</div>
      <div class="options btns_wrap">
        <div class="dialog_answer_cancel">取消</div>
        <div class="see">确定</div>
      </div>
    </div>
	

	<script src="http://gjaqzsjs.haedu.cn/gjaq_dati/js/jquery-1.8.3.min.js"></script>
	<script src="http://gjaqzsjs.haedu.cn/gjaq_dati/js/main.js"></script><link href="http://gjaqzsjs.haedu.cn/gjaq_dati/css/pc.css" rel="stylesheet" type="text/css" media="screen"><div class="fixed_btn home_btn"><img src="http://gjaqzsjs.haedu.cn/gjaq_dati/images/home.png" alt=""></div><div class="fixed_btn cancel_btn"><img src="http://gjaqzsjs.haedu.cn/gjaq_dati/images/cancel.png" alt=""></div>
	
	<script type="text/javascript" src="https://v1.cnzz.com/z_stat.ph1p?id=1280630837&web_id=1280630837"></script><script src="./2021年全省大学生国家安全知识竞赛_files/core.php" charset="utf-8" type="text/javascript"></script><a href="https://www.cnzz.com/stat/website.php?web_id=1280630837" target="_blank" title="站长统计">站长统计</a>

<div id="window-resizer-tooltip" style="display: none;"><a href="http://gjaqzsjs.haedu.cn/gjaq_dati/page/record.html#" title="编辑设置"></a><span class="tooltipTitle">窗口尺寸: </span><span class="tooltipWidth" id="winWidth">1178</span> x <span class="tooltipHeight" id="winHeight">883</span><br><span class="tooltipTitle">视窗尺寸: </span><span class="tooltipWidth" id="vpWidth">1178</span> x <span class="tooltipHeight" id="vpHeight">710</span></div></body></html>'''
    allHtml = mainHead+html+mainFoot
    return {'code':5211314,'msg':"html页面制作完成",'data':allHtml}


# login()
# # print(answer)
# senPage(answer)
# getCore()
# aa = createHtml()

# print(aa)
