#! /usr/bin/env python3
# encoding: utf-8
# author:Shelly
# time:2018-07-26
import asyncio
from pyppeteer import launch
import demjson

#输入目标，如：qq.com
target_site = input('target site : ')
fileName = './payload.txt'
#存放百度高级搜索结果页面的url
result = []



#百度高级搜索，格式如：
#{'filetype':'','inurl':'','intitle':'','keyword':''}
def getPayloads(fileName):
	payloads = []
	with open(fileName, 'r') as f:
		for line in f.readlines():
			payloads.append(demjson.decode(line.strip()))
	return payloads


#拼接百度搜索url
def getSearchUrl(target_site,input_data):
	wd_data = 'wd='
	wd_data = wd_data + 'site%3A('+target_site+')'
	if 'filetype' in input_data.keys():
		wd_data = wd_data + '%20filetype%3A'+input_data['filetype']
	if 'inurl' in input_data.keys():
		wd_data = wd_data + '%20inurl%3A' + input_data['inurl']
	if 'intitle' in input_data.keys():
		wd_data = wd_data + '%20intitle%3A' + input_data['intitle']
	if 'keyword' in input_data.keys():
		wd_data = wd_data +'%20'+input_data['keyword']
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
async def baiduHacking(target_site,payloads):
	browser = await launch(headless=False, args=['--disable-xss-auditor'])
	for input_data in payloads:
		close_flag = True
		page = await browser.newPage()
		url = getSearchUrl(target_site,input_data)
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
	payloads = getPayloads(fileName)
	loop = asyncio.get_event_loop()
	futu = asyncio.ensure_future(baiduHacking(target_site,payloads))
	futu.add_done_callback(done_callback)
	#loop.run_until_complete(futu)
	loop.run_forever()

if __name__ == '__main__':
	main()