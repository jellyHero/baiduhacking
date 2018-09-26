#! /usr/bin/env python3
# encoding: utf-8
# author:Shelly
# time:2018-07-26
import asyncio
from pyppeteer import launch

#输入目标，如：qq.com
target_site = input('target site : ')

#百度高级搜索，格式如：
#{'stie':target_site,'filetype':'','inurl':'','intitle':'','keyword':''}
payload = [{'stie':target_site,'filetype':'','inurl':'wp-admin','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'','intitle':'HTTP Server Test Page','keyword':''},{'stie':target_site,'filetype':'','inurl':'config','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'password=','intitle':'','keyword':''},{'stie':target_site,'filetype':'txt','inurl':'','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'menu.jsp','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'','intitle':'','keyword':'Apache Tomcat'},{'stie':target_site,'filetype':'','inurl':'','intitle':'Index of','keyword':''},{'stie':target_site,'filetype':'','inurl':'web-console','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'','intitle':'','keyword':'Powered by'},{'stie':target_site,'filetype':'','inurl':'','intitle':'Struts Problem Report','keyword':''},{'stie':target_site,'filetype':'','inurl':'','intitle':'','keyword':'MySQL Error:'},{'stie':target_site,'filetype':'','inurl':'','intitle':'Content Server Error','keyword':''},{'stie':target_site,'filetype':'','inurl':'','intitle':'','keyword':'Unexpected Problem Occurred!'},{'stie':target_site,'filetype':'','inurl':'','intitle':'','keyword':'sql syntax'},{'stie':target_site,'filetype':'','inurl':'url=','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'login','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'admin','intitle':'','keyword':''},{'stie':target_site,'filetype':'','inurl':'home','intitle':'','keyword':''}]

#存放百度高级搜索结果页面的url
result = []

#拼接百搭搜索url
def getSearchUrl(input_data):
	wd_data = 'wd='
	if input_data['stie']:
		wd_data = wd_data + 'site%3A('+input_data['stie']+')%20'
	if input_data['filetype']:
		wd_data = wd_data + 'filetype%3A'+input_data['filetype']+'%20'
	if input_data['inurl']:
		wd_data = wd_data + 'inurl%3A' + input_data['inurl'] + '%20'
	if input_data['intitle']:
		wd_data = wd_data + 'intitle%3A' + input_data['intitle'] + '%20'
	if input_data['keyword']:
		wd_data = wd_data + input_data['keyword']
	url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baiduadv&'+wd_data
	return url

#判断结果是否不只有百度翻译,如果只有翻译，返回false，否则返回true
#剔除百度翻译带来的误报。btw ：中间的空格不要删除。
def isNotOnlyBaiDuFanYi(content):
	fanyi= '''<div class="c-gap-top-small"><span class="c-showurl">fanyi.baidu.com </span></div> 
        
    
</div>

    
	    	

								
		
						
			
	
	
				
	
	
	
	

	
	

</div>

	
        <div style="clear:both;height:0;"></div>
	    
        
    <div id="rs"><div class="tt">相关搜索</div><table cellpadding="0">'''
	if fanyi in content:
		return False
	else:
		return True

#判断搜索结果是否为空，如果为空，返回true。
def isFindNothing(content):
	if '<div class="content_none"><div class="nors"><p>很抱歉，没有找到与<span style="font-family:宋体">“</span><em>' not in content:
		return True
	else :
		return False

#百度hack主函数，调用headless浏览器访问，并将包含结果的搜索url保存到result
async def baiduHacking():
	browser = await launch(headless=False, args=['--disable-xss-auditor'])
	for input_data in payload:
		close_flag = True
		page = await browser.newPage()
		url = getSearchUrl(input_data)
		await page.goto(url)
		content = await page.content()
		if isNotOnlyBaiDuFanYi(content):
			if isFindNothing(content):
				close_flag = False
				result.append(url)
				print (url)
		if close_flag :
			await page.close()
		else :
			pass

#回调函数，循环搜索完成后，打印result，并确定是否退出浏览器
def done_callback(futu):
	print (result)
	open_flag = input('close the page by KeyboardInterrupt [Y/n]: ')
	if open_flag == 'n' :
		print ('Please input CTRC + C to exit .')
	else :
		raise KeyboardInterrupt

#循环主函数
def main():
	loop = asyncio.get_event_loop()
	futu = asyncio.ensure_future(baiduHacking())
	futu.add_done_callback(done_callback)
	#loop.run_until_complete(futu)
	loop.run_forever()

if __name__ == '__main__':
	main()