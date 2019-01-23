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

    def teach_eval(self, url):
        r = requests.get(
            url,
            headers={'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }, cookies=self.cookies)
        r.encoding = 'gbk'
        bs = BeautifulSoup(r.text, 'html.parser')
        course_id = bs.find('select', attrs={'name': 'pjkc'}).find('option', attrs={'selected': 'selected'})['value'];
        course_name = bs.find('select', attrs={'name': 'pjkc'}).find('option', attrs={'selected': 'selected'}).string;
        print('正在评价课程：'+course_name+"  ID: "+course_id+"", end='')
        data = {
            '__VIEWSTATE': bs.find(attrs={'name': '__VIEWSTATE'}).attrs['value'],
            '__EVENTTARGET': bs.find(attrs={'name': '__EVENTTARGET'}).attrs['value'],
            '__EVENTARGUMENT': bs.find(attrs={'name': '__EVENTARGUMENT'}).attrs['value'],
            'pjkc': course_id,
            'DataGrid1:_ctl2:JS1': 'A',
            'DataGrid1:_ctl2:txtjs1:': '',
            'DataGrid1:_ctl3:JS1': 'A',
            'DataGrid1:_ctl3:txtjs1:': '',
            'DataGrid1:_ctl4:JS1': 'A',
            'DataGrid1:_ctl4:txtjs1:': '',
            'DataGrid1:_ctl5:JS1': 'A',
            'DataGrid1:_ctl5:txtjs1:': '',
            'DataGrid1:_ctl6:JS1': 'A',
            'DataGrid1:_ctl6:txtjs1:': '',
            'DataGrid1:_ctl7:JS1': 'A',
            'DataGrid1:_ctl7:txtjs1:': '',
            'DataGrid1:_ctl8:JS1': 'A',
            'DataGrid1:_ctl8:txtjs1:': '',
            'DataGrid1:_ctl9:JS1': 'B',
            'DataGrid1:_ctl9:txtjs1:': '',
            'pjxx': '',
            'txt1': '',
            'TextBox1': '',
            'Button1': ''
        }
        r1 = requests.post(
            url,
            data=data, headers={'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }, cookies=self.cookies)
        if r1.status_code == requests.codes.ok:
            print("   Done\n")
        else:
            print("   Failed\n")

    def submit_teach_eval(self, url):
        r = requests.get(
            url,
            headers={'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }, cookies=self.cookies)
        r.encoding = 'gbk'
        bs = BeautifulSoup(r.text, 'html.parser')
        course_id = bs.find('select', attrs={'name': 'pjkc'}).find('option', attrs={'selected': 'selected'})['value'];
        course_name = bs.find('select', attrs={'name': 'pjkc'}).find('option', attrs={'selected': 'selected'}).string;
        print('正在提交评价', end='')
        data = {
            '__VIEWSTATE': bs.find(attrs={'name': '__VIEWSTATE'}).attrs['value'],
            '__EVENTTARGET': bs.find(attrs={'name': '__EVENTTARGET'}).attrs['value'],
            '__EVENTARGUMENT': bs.find(attrs={'name': '__EVENTARGUMENT'}).attrs['value'],
            'pjkc': course_id,
            'DataGrid1:_ctl2:JS1': 'A',
            'DataGrid1:_ctl2:txtjs1:': '',
            'DataGrid1:_ctl3:JS1': 'A',
            'DataGrid1:_ctl3:txtjs1:': '',
            'DataGrid1:_ctl4:JS1': 'A',
            'DataGrid1:_ctl4:txtjs1:': '',
            'DataGrid1:_ctl5:JS1': 'A',
            'DataGrid1:_ctl5:txtjs1:': '',
            'DataGrid1:_ctl6:JS1': 'A',
            'DataGrid1:_ctl6:txtjs1:': '',
            'DataGrid1:_ctl7:JS1': 'A',
            'DataGrid1:_ctl7:txtjs1:': '',
            'DataGrid1:_ctl8:JS1': 'A',
            'DataGrid1:_ctl8:txtjs1:': '',
            'DataGrid1:_ctl9:JS1': 'B',
            'DataGrid1:_ctl9:txtjs1:': '',
            'pjxx': '',
            'txt1': '',
            'TextBox1': '',
            'Button2': ''
        }
        r1 = requests.post(
            url,
            data=data, headers={'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }, cookies=self.cookies)
        if r1.status_code == requests.codes.ok:
            print("   Done\n")
        else:
            print("   Failed\n")

    def get_eval_url(self):
        urls = []
        links = self.soup.find_all('a')
        print(links)
        for i in range(0, links.__len__()):
            if (links[i].has_attr('href') and 'xsjxpj.aspx' in links[i]['href']):
                urls.append({ 'name': links[i].string, 'url': links[i]['href'] })
        #print(urls)
        return urls

    def query_grade(self, year, semester):
        print('正在查询成绩...')

        r = requests.get(
            'http://newjwc.tyust.edu.cn/' + self.soup.find(attrs={'onclick': 'GetMc(\'成绩查询\');'}).attrs['href'],
            headers={'host': 'newjwc.tyust.edu.cn', 'referer': self.referer }, cookies=self.cookies)
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
urls = info.get_eval_url()
for i in range(0, urls.__len__()):
    info.teach_eval('http://newjwc.tyust.edu.cn/'+urls[i].get('url'))
info.submit_teach_eval('http://newjwc.tyust.edu.cn/'+urls[0].get('url'))