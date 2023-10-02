from configobj import ConfigObj
import requests

class InstagramSearch():
	def __init__(self):
		config = ConfigObj('wordhound.conf')
		instaConf = config['Instagram']

		self.atoken = instaConf['IsessionID']
		if (len(self.atoken) == 0):
			input("[x] Error: Have you put in yout Instagram Session ID? Its easy to setup (wordhound.conf)")

	def searchByProfile(self, profile):
		print ("[+] Queryng instagram for {0}".format(profile))
		queryURL = "https://instagram.com/{0}".format(profile)
		params = { '__a': 1, '__d': 1 }
		cookies = { 'sessionid': self.atoken}
		response = get(url, params, cookies=cookies)
		if response.status_code == 200:
    		bio = on_success(response)
		else:
			bio = None
    		on_error(response)

	def on_success(response)
		profile_data_json = response.text
		parsed_data = loads(profile_data_json)

		bio = (parsed_data['graphql']['user']['biography']).split('')
		return bio

	def on_error(response):
    	# Printing the error if something went wrong
    	print('Something went wrong')
    	print('Error Code:', response.status_code)
    	print('Reason:', response.reason)