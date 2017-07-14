import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored

# this is the app access token
APP_ACCESS_TOKEN = '3063548436.a42c93b.67ddd0dedd7c4bb3b755b9acbb7aea42'

# this is base url
BASE_URL = 'https://api.instagram.com/v1/'

# list for disasters for testing natural calamity test.
disasters = ['KARTING','AVALANCHES','AVALANCHE','LANDSLIDES','LANDSLIDE','EARTHQUAKES','EARTHQUAKE','SINKHOLES','SINKHOLE','VOLCANIC ERUPTIONS','VOLCANIC ERUPTION','FLOODS','FLOOD','LIMNIC ERUPTIONS','LIMNIC ERUPTION','TSUNAMI','BLIZZARDS','BLIZZARD','CYCLONIC STORMS','CYCLONIC STORM','DROUGHTS','DROUGHT','THUNDERSTORMS','THUNDERSTORM','HAILSTORMS','HAILSTORM','HEAT WAVE','HEAT WAVES','TORNADOES','TORNADOE','WILDFIRES','WILDFIRE','AIRBURST','SOLAR FLARES','SOLAR FLARE']


# to get the information of selfie
def self_info():
    # our request url
    request_url = (BASE_URL + 'users/self/?access_token=%s') % APP_ACCESS_TOKEN
    print 'GET request url : %s' % request_url
    # sending request
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print colored('Username: %s','blue') %(user_info['data']['username'])
            print colored('No. of followers: %s','blue') %(user_info['data']['counts']['followed_by'])
            print colored('No. of people you are following: %s','blue') % (user_info['data']['counts']['follows'])
            print colored('No. of posts: %s','blue') % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist'
    else:
        print 'status code other than 200 received'


# to get the user id
def get_user_id(insta_username):
    # our url and sending request
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') %(insta_username,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


# to get the info about the user
def get_user_info(insta_username):
    # user id is stored in this
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()
    # showing the user info
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print colored('Username: %s','green') % (user_info['data']['username'])
            print colored('No. of followers: %s','green') % (user_info['data']['counts']['followed_by'])
            print colored('No. of people you are following: %s','green') % (user_info['data']['counts']['follows'])
            print colored('No. of posts: %s','green') % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


# function to get self post
def get_own_post():
    # url to get the recent post posted by self
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % APP_ACCESS_TOKEN
    print 'GET request url : %s' % request_url
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            # this will download the image
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# to get user post
def get_user_post(insta_username):
    # to get the recent post posted by the user
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            # download the image by the user
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# get user post id
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    # the json object of media of the post is stored here
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            # return the post id of the user
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


# to like a post
def like_a_post(insta_username):
    # getting media id of user from the get_post_id function
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % media_id
    # defined body for post request sending method
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'post request url : %s' % request_url
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like successfull'
    else:
        print 'please try again, it unsuccessful'


# to post a comment
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("please type your comment")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % media_id
    print 'POST request url : %s' % request_url
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['data'] == 200:
        print 'succesfull comment added'
    else:
        print 'try again, enter a comment'


# function to delete negative comment
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % comment_text
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'Delete request url : %s' % delete_url
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'comment successfully deleted'
                    else:
                        print 'try again'
                else:
                    print 'Positive comment : %s' % comment_text
        else:
            print 'There are no comments on the post'
    else:
        print 'status code other than 200 received'


# to get list of likes
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    like_info = requests.get(request_url).json()
    if like_info['meta']['code'] == 200:
        if len(like_info['data']):
            for x in range(0, len(like_info['data'])):
                print 'liked by: %s' % like_info['data'][x]['username']
                x = x + 1
        else:
            print 'no like on the data'
    else:
        print 'status code other than 200 received'


# to get list of comments
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                print 'comment list is: %s' % comment_info['data'][x]['text']
                x = x + 1
        else:
            print 'no comment on post'
    else:
        print 'status code other than 200 received'


# to check post with the natural calamity or disaster tag in user post
def natural_calamity_tags(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            for x in range(0,len(user_info['data'])):
                for y in range(0,len(user_info['data'][x]['tags'])):
                    # checking tags in disaster
                    if user_info['data'][x]['tags'][y].upper() in disasters:
                        print colored('image with disaster tag has been found','red')
                        # to print media id
                        media_id = user_info['data'][x]['id']
                        print 'the media id is' + media_id

                        image_name = user_info['data'][x]['id'] + '.jpeg'
                        image_url = user_info['data'][x]['images']['standard_resolution']['url']
                        print 'image url is: '+ image_url
                        # download the image by the user
                        urllib.urlretrieve(image_url, image_name)
                        print 'your image with tag disaster has been downloaded'




        else:
            print colored('there is no data or post found','red')
    else:
        print colored('status code other than 200 received','red')

'''
# to find captions with disaster related word and download image
def natural_calamity_captions(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            for x in range(0,len(user_info['data'])):
                # for loop in list of disasters
                for y in range(0,len(disasters)):
                    # checking if the word is available in caption
                    if disasters[y].upper() in user_info['data'][x]['caption']['text'].upper():
                        print colored('caption with disaster warning found','red')
                        # getting media id of the image
                         media_id = user_info['data'][x]['id']
                        print media_id
                        image_name = user_info['data'][x]['id'] + '.jpeg'
                        image_url = user_info['data'][x]['images']['standard_resolution']['url']
                        print 'image url is: ' + image_url
                        # download the image by the user
                        urllib.urlretrieve(image_url, image_name)
                        print 'your image with tag disaster has been downloaded'
                    else:
                        y = y + 1
                    x = x + 1
            else:
              print colored('there is no data or post found', 'red')
        else:
            print colored('status code other than 200 received', 'red')
'''


# to find image within given location
def location_search():
    latitude = raw_input('enter the latitude location')
    longitude = raw_input('enter the longitude location')
    request_url = (BASE_URL + 'media/search?lat=%s&lng=%s&access_token=%s') % (latitude,longitude,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            # for if there are multiple media between this range
            for x in range(0,len(media_info['data'])):
                print colored('image within given location has been found', 'red')
                media_id= media_info['data'][x]['id']
                print 'the media id is'+media_id
                image_name = media_info['data'][x]['id'] + '.jpeg'
                image_url = media_info['data'][x]['images']['standard_resolution']['url']
                print 'image url is: ' + image_url
                # download the image by the user
                urllib.urlretrieve(image_url, image_name)
                print 'your image within given location has been downloaded'

        else:
            print'no image found within given location'
    else:
        print'code error'






def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.for post with natural calamity tag\n"
        print "k.for post with natural calamity caption\n"
        print "l.for post within given location"
        print "m.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "j":
            insta_username = raw_input("enter the username of the user: ")
            natural_calamity_tags(insta_username)
        elif choice == 'l':
            location_search()


        elif choice=="m":
            exit()
        else:
            print "wrong choice"
        '''
        elif choice == 'k':
        insta_username = raw_input("enter the username of the user: ")
        natural_calamity_captions(insta_username)
        '''
start_bot()