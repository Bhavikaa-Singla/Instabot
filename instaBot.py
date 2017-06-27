import requests,urllib

#Token owner
APP_ACCESS_TOKEN = "3988867676.7a2b6a6.c2358b1f590241b882ad58cfb23e9b41"
BASE_URL = "https://api.instagram.com/v1/"



def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s")%(APP_ACCESS_TOKEN)
    print "GET request url: %s " %(request_url)
    user_info = requests.get(request_url)
    user_info = user_info.json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "Owner's information : "
            print "Username : %s" %(user_info["data"]["username"])
            print "No. of followers : %s" %(user_info["data"]["counts"]["followed_by"])
            print "No. of people you are following : %s" % (user_info["data"]["counts"]["follows"])
            print "No. of posts : %s" % (user_info["data"]["counts"]["media"])
        else:
            print "User does not exist!"

    else:
        print "Status code other than 200 received!!"




def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s")%(insta_username,APP_ACCESS_TOKEN)
    print "GET request url: %s" %(request_url)
    user_info = requests.get(request_url)
    user_info = user_info.json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


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
            print "Another User's Information : "
            print "Username: %s" % (user_info["data"]["username"])
            print "No. of followers: %s" % (user_info["data"]["counts"]["followed_by"])
            print "No. of people you are following: %s" % (user_info["data"]["counts"]["follows"])
            print "No. of posts: %s" % (user_info["data"]["counts"]["media"])
        else:
            print "There is no data for this user!"
    else:
        print "Status code other than 200 received!"



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


self_info()

t = get_user_id("pooja_bharti_arya")
print "User ID: " + t

get_user_info("pooja_bharti_arya")

get_own_post()

get_user_post("pooja_bharti_arya")