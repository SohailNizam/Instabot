import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep, strftime
from random import randint
import pandas as pd

#this part goes to the instagram login page
#edit the path to wherever chromedriver lives
chromedriver_path = './chromedriver_win32/chromedriver.exe'
webdriver = selenium.webdriver.Chrome(chromedriver_path)
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('') #add your username in the quotes
password = webdriver.find_element_by_name('password')
password.send_keys('') #add your password in the quotes


#button_login = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
button_login = webdriver.find_element_by_xpath("//button[@type='submit']")
button_login.click()
sleep(3)

#list of hashtags for the day
hashtag_list = [] #add hashtages in quotes, comma separated

#get the list of users we've already run this on
prev_user_data = pd.read_excel("./insta_data.xlsx", header=0)

#TODO
#Go through the excel sheet and unfollow
#those we've followed for >= 3 days

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0


for hashtag in hashtag_list:
	tag += 1
	webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
	sleep(3)

	first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
	sleep(4)
	first_thumbnail.click()
	sleep(randint(1,2))

	try:

		#cycle through the top 2 pictures using the current hashtag
		for x in range(1,10):

			#get the username of the current profile
			username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
			print(username)
			print()
			#if we have not hit this user yet
			if username not in prev_user_data["username"]:
				print("not following yet")
				print()
				follow_button = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
				
			#if follow_button.text == 'Follow':
				
				#follow the current user
				follow_button.click()
				print("followed")
				print()
				#add new user to pandas datframe of users
				user = {'username': [username],
						'date_followed': [strftime("%m/%d/%Y")], 
						'status': ['following']}
				prev_user_data = prev_user_data.append(pd.DataFrame(user))
				print("new data added")
				print()
				
				#increase counter of num followers
				followed += 1
				
				#get the like button
				like_button = webdriver.find_elements_by_css_selector("[aria-label=Like]")
				print("got like button")
				#click the like button
				like_button[0].click()
				print("liked")
				#increase like counter
				likes += 1
				sleep(randint(5,10))
				
				
				#also like their 2 most recent posts
				#sequence of clicks:
				#username (go to user page)
				user_button = webdriver.find_element_by_xpath("//div[@class='e1e1d']")
				user_button.click()
				print("reached user page")
				print()
				sleep(2)
				#newest post
				newest_post = webdriver.find_element_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")
				newest_post.click()
				#click next button
				webdriver.find_element_by_link_text('Next').click()
				print("reached second most recent post")
				print()
				sleep(1)
				
				
				#like button
				like_button = webdriver.find_elements_by_css_selector("[aria-label=Like]")
				like_button[0].click()
				print("liked second most recent post")
				print()
				sleep(3)
				
				#next button
				webdriver.find_element_by_link_text('Next').click()
				sleep(1)
				#like button
				like_button = webdriver.find_elements_by_css_selector("[aria-label=Like]")
				like_button[0].click()
				print("liked third most recent post")
				#x button
				close_button = webdriver.find_elements_by_css_selector("[aria-label=Close]")
				#back button 5 times
				webdriver.execute_script("window.history.go(-5)")
				#now back to the hashtag page
				print("back to hashtag page")
				sleep(1)
					
				#click on top post again
				newest_post = webdriver.find_element_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")
				newest_post.click()
				sleep(.5)
				
				#hit next x times (x=iteration we're on)
				#to move to next picture/profile
				for i in range(x):
					webdriver.find_element_by_link_text('Next').click()
					
			
				
			else: #if we've already hit this user
				
				#move on to next picture
				webdriver.find_element_by_partial_link_text('Next').click()


    # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
	except:
		continue
        




#overwrite old csv with new
prev_user_data.to_excel("./insta_data.xlsx", index = False)
#print how many photos liked and how many users followed
print('Liked {} photos.'.format(likes))
print('Followed {} new people.'.format(followed))







