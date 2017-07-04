import requests,urllib                          # import requests library which is a python module that we can use to send all kinds of HTTP requests
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
import pylab


#Token owner : bhavikaa_singla
#Sandbox Users : brar_japji,simranmadaan12
APP_ACCESS_TOKEN = "3988867676.7a2b6a6.c2358b1f590241b882ad58cfb23e9b41"
BASE_URL = "https://api.instagram.com/v1/"


#Function declaration to get your own information
def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s")%(APP_ACCESS_TOKEN)
    print "GET request url: %s " %(request_url)
    user_info = requests.get(request_url)
    user_info = user_info.json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "\n"
            print "Owner's information : "
            print "Username : %s" %(user_info["data"]["username"])
            print "No. of followers : %s" %(user_info["data"]["counts"]["followed_by"])
            print "No. of people you are following : %s" % (user_info["data"]["counts"]["follows"])
            print "No. of posts : %s" % (user_info["data"]["counts"]["media"])
        else:
            print "User does not exist!"

    else:
        print "Status code other than 200 received!!"



#Function declaration to get the ID of a user by username
def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s")%(insta_username,APP_ACCESS_TOKEN)
    print "GET request url: %s" %(request_url)
    user_info = requests.get(request_url)
    user_info = user_info.json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]     #it returns user id
        else:
            return None
    else:
        print "Status code other than 200 received!"
        exit()




#Function declaration to get the info of a user by username
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User does not exist!!"
        exit()
    request_url = (BASE_URL + "users/%s?access_token=%s") % (user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "\n"
            print "Another User's Information : "
            print "Username: %s" % (user_info["data"]["username"])
            print "No. of followers: %s" % (user_info["data"]["counts"]["followed_by"])
            print "No. of people you are following: %s" % (user_info["data"]["counts"]["follows"])
            print "No. of posts: %s" % (user_info["data"]["counts"]["media"])
        else:
            print "There is no data for this user!"
    else:
        print "Status code other than 200 received!"




#Function declaration to get your own recent post
def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") %(APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    own_media = requests.get(request_url).json()
    if own_media["meta"]["code"] == 200:
        if len(own_media["data"]):
            image_name = own_media["data"][0]["id"] + ".jpeg"
            image_url = own_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received"
    return None




#Function declaration to get the recent post of a user by username
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User does not exist!"
        exit()
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id,APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_media = requests.get(request_url).json()
    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            image_name = user_media["data"][0]["id"] + ".jpeg"
            image_url = user_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Image has been downloaded!"
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None




#Function declaration to get the ID of the recent post of a user by username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User does not exist!"
        exit()
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_media = requests.get(request_url).json()
    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            return user_media["data"][0]["id"]
        else:
            print "There is no recent post of the user!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()




#Function declaration to like the recent post of a user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes") % (media_id)
    payload = {"access_token" : APP_ACCESS_TOKEN}
    print "POST request url : %s" %(request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like["meta"]["code"] == 200:
        print "Like was successful!"
    else:
        print "Your like was unsuccessful. Try again!"




#Function declaration to make a comment on the recent post of the user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + "media/%s/comments") % (media_id)
    print "POST request url : %s" % (request_url)
    make_comment = requests.post(request_url, payload).json()
    if make_comment["meta"]["code"] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"




#Function declaration to get list of comments on the recent post of the user
def list_of_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") % (media_id ,APP_ACCESS_TOKEN)
    print "GET request url: %s" % (request_url)
    comments = requests.get(request_url).json()
    i = 0
    if comments["meta"]["code"] == 200:
            for ele in comments["data"]:
                print comments["data"][i]["from"]["username"] + ":" + comments["data"][i]["text"]
                i = i + 1
    else:
        print "Status code other than 200 received!"
        exit()




#Function declaration to get the recent media liked by the owner of the token
def recent_media_liked():
    request_url = (BASE_URL + "users/self/media/liked?access_token=%s") % (APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    user_media = requests.get(request_url).json()
    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            image_name = user_media["data"][0]["id"] + ".jpeg"
            image_url = user_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Image has been downloaded!"
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None




#Function declaration to fetch the list of users who have liked the recent media
def list_of_likes(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    likes = requests.get(request_url).json()
    i = 0
    if likes["meta"]["code"] == 200:
        if len(likes["data"]):
            for ele in likes["data"]:
                print likes["data"][i]["username"]
                i = i + 1
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None




#Function declaration to start the instabot application and in this, users have many choices to choose from
def start_bot():
    print "Hey! Welcome to instaBot!"
    while True:
        print "Here are your menu options:"
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e.Like the recent post of a user"
        print "f.Make a comment on the recent post of a user"
        print "g.Get the list of comments on the recent post of a user "
        print "h.Get the recent media liked by the owner of the token"
        print "i.Get the list of users who have liked the recent media"
        print "j.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
            print "\n"
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
            print "\n"
        elif choice == "c":
            get_own_post()
            print "\n"
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
            print "\n"
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
            print "\n"
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
            print "\n"
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            list_of_comments(insta_username)
            print "\n"
        elif choice == "h":
            recent_media_liked()
            print "\n"
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            list_of_likes(insta_username)
            print "\n"
        elif choice == "j":
            exit()
        else:
            print "wrong choice"

start_bot()









