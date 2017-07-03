import requests
import sys
import os
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

class LogInfo:
    viewstate = ''
    cookies = {}
    response = 0
    soup = 0
    referer = ''

    def setCookie(self, cookie):
        #从字符串设置cookie
        for c in cookie.split(';'):
            name, value=c.split('=', 1)
            name = name.replace(' ','')
            self.cookies[name] = value
            #print('Cookie: ' + name + ': ' + value)

    def getViewstate(self):
        # 获得viewstate
        #print("获取viewstate...");
        r = requests.get('http://newjwc.tyust.edu.cn')
        soup = BeautifulSoup(r.text, 'html.parser')
        self.setCookie(r.headers['Set-Cookie'])
        self.viewstate = soup.find(attrs = {'name': '__VIEWSTATE'}).attrs['value']

    def getVerifyCode(self):
        r = requests.get('http://newjwc.tyust.edu.cn/CheckCode.aspx', cookies=self.cookies)
        image = Image.open(BytesIO(r.content));
        print('请输入打开的图片上看到的字符。')
        image.show();
        code = input("  验证码: ")
        return code

    def login(self, user, pwd, code):
        data = {
            '__VIEWSTATE': self.viewstate,
            'txtUserName': user,
            'TextBox2': pwd,
            'txtSecretCode': code,
            'RadioButtonList1': ('学生').encode('gb2312'),
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': ''
        }
        headers = {'host': 'newjwc.tyust.edu.cn'}
        r = requests.post('http://newjwc.tyust.edu.cn/Default2.aspx', data=data, headers=headers, cookies=self.cookies)
        if (r.url.find('xs_main.aspx') == -1):
            return 0;
        self.response = r
        self.referer = r.url
        self.soup = BeautifulSoup(r.text, 'html.parser')
        return 1;

    def query_grade(self, year, semester):
        print('正在查询成绩...')
        headers = {'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }
        r = requests.get(
            'http://newjwc.tyust.edu.cn/' + self.soup.find(attrs={'onclick': 'GetMc(\'成绩查询\');'}).attrs['href'],
            headers=headers, cookies=self.cookies)
        soup_init = BeautifulSoup(r.text, 'html.parser')
        data = {
            '__VIEWSTATE': soup_init.find(attrs = {'name': '__VIEWSTATE'}).attrs['value'],
            '__EVENTTARGET': soup_init.find(attrs={'name': '__EVENTTARGET'}).attrs['value'],
            '__EVENTARGUMENT': soup_init.find(attrs={'name': '__EVENTARGUMENT'}).attrs['value'],
            'ddlXN': year,
            'ddlXQ': semester,
            'ddl_kcxz': '',
            'hidLanguage': '',
            'btn_xq': ''
        }
        headers = {'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }
        r1 = requests.post('http://newjwc.tyust.edu.cn/'+self.soup.find(attrs = {'onclick': 'GetMc(\'成绩查询\');'}).attrs['href'], data=data, headers=headers, cookies=self.cookies)
        print('   ' + year + '学年第' + semester + '学期的成绩')
        #print (r1.text)
        soup = BeautifulSoup(r1.text, 'html.parser')
        data = soup.find(attrs={'class': 'datelist'}).find_all('tr')
        datalen = data.__len__()
        for i in range(1, datalen):
            d = data[i].find_all('td')
            cname = d[3].string
            xf = d[6].string
            jd = d[7].string.replace(' ', '')
            fs = d[8].string.replace(' ', '')
            print('('+str(i)+') '+cname+'\n      分数：'+fs+'    学分:'+xf+'    绩点:'+jd)


info = LogInfo()


print ('太原科技大学成绩查询\n')

print('正在获取必要的信息...')
info.getViewstate()

usernames = ''
passwords = ''
username = ''
password = ''

while True:
    print ('输入你的信息：')
    username = input('   学号['+usernames+']:')
    password=  input('   密码['+passwords+']:')

    if (username == ''):
        username = usernames
    else:
        usernames = username

    if (password == ''):
        password = passwords
    else:
        passwords = password

    print ('获取验证码...')
    code = info.getVerifyCode();


    print('正在登录教务系统..')

    if info.login(username, password, code) == 1:
        break
    print('登录失败。请检查你的输入是否正确。')

print('\n登陆成功。')
soup = BeautifulSoup(info.response.text, 'html.parser')
name = soup.find(id='xhxm').string
print('  姓名：'+name)
print('\n')
info.query_grade('2016-2017', '2')


