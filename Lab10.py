#!/usr/bin/python

import urllib2
import json
from flask import Flask, abort, render_template, render_template_string, request, make_response
app = Flask(__name__)

DRIVE = 0;
FUSION = 1;
AI = 2;
SPACE = 3;

curTheme = ""
currentPage = ""


##--------------------------------------------------------------------------------##
##-----------------------------------[PAGES]--------------------------------------##
##--------------------------------------------------------------------------------##


##### Index route path!
@app.route('/')
def index_page():
    
    global curTheme 
    global currentPage
    currentPage = "/"
    ## Check to see if the cookie exists and is valid.
    try:
        theme = unscramble(request.cookies['zdtvhimlp-theme'])
        if (theme != 'normal' and theme != 'dark' and theme != 'orange'):
            raise KeyError('')
        curTheme = theme
        return render_template('index.html', setTheme=curTheme)
    ## Failsafe in case the cookie is inexistent, invalid or tampered with.
    except (KeyError):
        curTheme = 'normal'
        resp = make_response(render_template('index.html', setTheme=curTheme))
        resp.set_cookie('zdtvhimlp-theme', scramble('normal'))
        return resp

##### Vehicles route path!
@app.route('/vehicles')
def vehicles_page():

    global curTheme
    global currentPage 
    currentPage = "/vehicles"
    ## Check to see if the cookie exists and is valid.
    try:
        theme = unscramble(request.cookies['zdtvhimlp-theme'])
        if (theme != 'normal' and theme != 'dark' and theme != 'orange'):
            raise KeyError('')
        curTheme = theme
        return render_template('vehicles.html', setTheme=curTheme)
    ## Failsafe in case the cookie is inexistent, invalid or tampered with.
    except (KeyError):
        curTheme = 'normal'
        resp = make_response(render_template('vehicles.html', setTheme=curTheme))
        resp.set_cookie('zdtvhimlp-theme', scramble('normal'))
        return resp

##### Fusion route path!
@app.route('/fusion')
def fusion_page():

    global curTheme
    global currentPage
    currentPage = "/fusion"
    ## Check to see if the cookie exists and is valid.
    try:
        theme = unscramble(request.cookies['zdtvhimlp-theme'])
        if (theme != 'normal' and theme != 'dark' and theme != 'orange'):
            raise KeyError('')
        curTheme = theme
        return render_template('fusion.html', setTheme=curTheme)
    ## Failsafe in case the cookie is inexistent, invalid or tampered with.
    except (KeyError):
        curTheme = 'normal'
        resp = make_response(render_template('fusion.html', setTheme=curTheme))
        resp.set_cookie('zdtvhimlp-theme', scramble('normal'))
        return resp

##### AI route path!
@app.route('/ai')
def ai_page():

    global curTheme
    global currentPage
    currentPage = "/ai"
    ## Check to see if the cookie exists and is valid.
    try:
        theme = unscramble(request.cookies['zdtvhimlp-theme'])
        if (theme != 'normal' and theme != 'dark' and theme != 'orange'):
             raise KeyError('')
        curTheme = theme
        return render_template('ai.html', setTheme=curTheme)
    ## Failsafe in case the cookie is inexistent, invalid or tampered with.
    except (KeyError):
        curTheme = 'normal'
        resp = make_response(render_template('ai.html', setTheme=curTheme))
        resp.set_cookie('zdtvhimlp-theme', scramble('normal'))
        return resp

##### Space route path!
@app.route('/space')
def space_page():

    global curTheme
    global currentPage
    currentPage = "/space"
    ## Check to see if the cookie exists and is valid.
    try:
        theme = unscramble(request.cookies['zdtvhimlp-theme'])
        if (theme != 'normal' and theme != 'dark' and theme != 'orange'):
            raise KeyError('')
        curTheme = theme
        return render_template('space.html', setTheme=curTheme)
    ## Failsafe in case the cookie is inexistent, invalid or tampered with.
    except (KeyError):
        curTheme = 'normal'
        resp = make_response(render_template('space.html', setTheme=curTheme))
        resp.set_cookie('zdtvhimlp-theme', scramble('normal'))
        return resp




##---------------------------------------------------------------------------------##
##--------------------------------[GET REQUESTS]-----------------------------------##
##---------------------------------------------------------------------------------##


## For changing themes:
@app.route('/theme_update')
def update_theme():

    global curTheme
    global currentPage
    ## Get the user-selected setting and set the cookie.
    theme = request.args.get('theme')
    curTheme = theme
    response = None
    if currentPage == '/':
        response = make_response(render_template_string(index_page()))
    elif currentPage == '/vehicles':
        response = make_response(render_template_string(vehicles_page()))
    elif currentPage == '/fusion':
        response = make_response(render_template_string(fusion_page()))
    elif currentPage == '/ai':
        response = make_response(render_template_string(ai_page()))
    elif currentPage == '/space':
        response = make_response(render_template_string(space_page()))
    response.set_cookie('zdtvhimlp-theme', scramble(theme))
    return response



##### Routing for article searches.
@app.route('/articles/<int:topic_id>/<int:num_articles>')
def nyt_pull(topic_id, num_articles):

    ## Make a request to the NYT server for the topic requested
    try:
        if (topic_id == DRIVE):
            query = '("Driverless%20Car"%20"Driverless%20Vehicle"%20"Driverless"%20"Autonomous%20Car"%20"Autonomous%20Vehicle")'
        elif (topic_id == FUSION):
            query = '("Cold%20Fusion"%20"LENR"%20"CMNS"%20"Condensed%20Matter")'
        elif (topic_id == AI):
            query = '("Artificial%20Intelligence"%20"Neural%20Network"%20"Intelligent%20Agent")'
        elif (topic_id == SPACE):
            query = '("Space%20Travel"%20"Exoplanet"%20"Astrobiology"%20"life%20as%20we%20know%20it")'
        else:
            abort(404)


        response = urllib2.urlopen('http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=%s&begin_date=20000101&api-key=a1c66561e40579b16dc69010cb9f2ccc%%3A4%%3A72961152' % (query))
    
    except urllib2.URLError:
        abort(404)

    ## Grab the JSON data which results from the pull.
    data = json.load(response)

    


    ## Record and send back the data the user would like to see.
    if (num_articles == 1): 
        fTitle1 = data['response']['docs'][0]['headline']['main'].replace('&#8217;', "'").replace('&#8230;', "...")
        fTagline1 = data['response']['docs'][0]['snippet'].replace('&#8217;', "'").replace('&#8230;', "...")
        fUrl1 = data['response']['docs'][0]['web_url']

        return render_template('embed.html', title1=fTitle1, tagline1=fTagline1, url1=fUrl1, setTheme=curTheme)


    elif (num_articles == 5):
        fTitle1 = data['response']['docs'][0]['headline']['main'].replace('&#8217;', "'").replace('&#8230;', "...")
        fDate1 = data['response']['docs'][0]['pub_date'][:10]
        fUrl1 = data['response']['docs'][0]['web_url']
        fAuthor1 = ""
        fTagline1 = ""
        fPicture1 = "http://img2.wikia.nocookie.net/__cb20130511180903/legendmarielu/images/b/b4/No_image_available.jpg"
        try:
            fAuthor1 = data['response']['docs'][0]['byline']['original']
            fPicture1 = "http://nytimes.com/" + data['response']['docs'][0]['multimedia'][1]['url']
            fTagline1 = data['response']['docs'][0]['snippet'].replace('&#8217;', "'").replace('&#8230;', "...")
        except (TypeError):
            pass
        except (IndexError): 
            pass
        except (KeyError):
            pass

        fTitle2 = data['response']['docs'][1]['headline']['main'].replace('&#8217;', "'").replace('&#8230;', "...")
        fDate2 = data['response']['docs'][1]['pub_date'][:10]
        fUrl2 = data['response']['docs'][1]['web_url']
        fAuthor2 = ""
        fTagline2 = ""
        fPicture2 = "http://img2.wikia.nocookie.net/__cb20130511180903/legendmarielu/images/b/b4/No_image_available.jpg" 
        try:
            fAuthor2 = data['response']['docs'][1]['byline']['original']
            fPicture2 = "http://nytimes.com/" + data['response']['docs'][1]['multimedia'][1]['url']
            fTagline2 = data['response']['docs'][1]['snippet'].replace('&#8217;', "'").replace('&#8230;', "...")
        except (TypeError):
            pass
        except (IndexError):
            pass
        except (KeyError):
            pass

        fTitle3 = data['response']['docs'][2]['headline']['main'].replace('&#8217;', "'").replace('&#8230;', "...")
        fDate3 = data['response']['docs'][2]['pub_date'][:10]
        fUrl3 = data['response']['docs'][2]['web_url']
        fAuthor3 = ""
        fTagline3 = ""
        fPicture3 = "http://img2.wikia.nocookie.net/__cb20130511180903/legendmarielu/images/b/b4/No_image_available.jpg"
        try:
            fAuthor3 = data['response']['docs'][2]['byline']['original']
            fPicture3 = "http://nytimes.com/" + data['response']['docs'][2]['multimedia'][1]['url']
            fTagline3 = data['response']['docs'][2]['snippet'].replace('&#8217;', "'").replace('&#8230;', "...")
        except (TypeError):
            pass
        except (IndexError): 
            pass
        except (KeyError):
            pass

        fTitle4 = data['response']['docs'][3]['headline']['main'].replace('&#8217;', "'").replace('&#8230;', "...")
        fDate4 = data['response']['docs'][3]['pub_date'][:10]
        fUrl4 = data['response']['docs'][3]['web_url']
        fAuthor4 = ""
        fTagline4 = ""
        fPicture4 = "http://img2.wikia.nocookie.net/__cb20130511180903/legendmarielu/images/b/b4/No_image_available.jpg"
        try:
            fAuthor4 = data['response']['docs'][3]['byline']['original']
            fPicture4 = "http://nytimes.com/" + data['response']['docs'][3]['multimedia'][1]['url']
            fTagline4 = data['response']['docs'][3]['snippet'].replace('&#8217;', "'").replace('&#8230;', "...")
        except (TypeError):
            pass
        except (IndexError): 
            pass
        except (KeyError):
            pass

        fTitle5 = data['response']['docs'][4]['headline']['main'].replace('&#8217;', "'").replace('&#8230;', "...")
        fDate5 = data['response']['docs'][4]['pub_date'][:10]
        fUrl5 = data['response']['docs'][4]['web_url']
        fAuthor5 = ""
        fTagline5 = ""
        fPicture5 = "http://img2.wikia.nocookie.net/__cb20130511180903/legendmarielu/images/b/b4/No_image_available.jpg"
        try:
            fAuthor5 = data['response']['docs'][4]['byline']['original']
            fPicture5 = "http://nytimes.com/" + data['response']['docs'][4]['multimedia'][1]['url']
            fTagline5 = data['response']['docs'][4]['snippet'].replace('&#8217;', "'").replace('&#8230;', "...")
        except (TypeError):
            pass
        except (IndexError): 
            pass
        except (KeyError):
            pass

        return render_template('display.html', title1=fTitle1, author1=fAuthor1, date=fDate1, tagline1=fTagline1, url1=fUrl1, picture1=fPicture1, title2=fTitle2, author2=fAuthor2, date2=fDate2, tagline2=fTagline2, url2=fUrl2, picture2=fPicture2, title3=fTitle3, author3=fAuthor3, date3=fDate3, tagline3=fTagline3, url3=fUrl3, picture3=fPicture3, title4=fTitle4, author4=fAuthor4, date4=fDate4, tagline4=fTagline4, url4=fUrl4, picture4=fPicture4, title5=fTitle5, author5=fAuthor5, date5=fDate5, tagline5=fTagline5, url5=fUrl5, picture5=fPicture5, setTheme=curTheme)

    else:
        return '<font style="color: red">Couldn\'t fetch the articles...</font>'





##-------------------------------------------------------------------------------##
##-------------------------------------[MISC]------------------------------------##
##-------------------------------------------------------------------------------##


## For encryption and decryption!
## Just a simple Caesar cipher, nothing special.
def scramble(inString):
    newStr = ""
    for i in range(0, len(inString)):
        newStr += chr(ord(inString[i]) + 1)
    return newStr

def unscramble(inString):
    newStr = ""
    for i in range(0, len(inString)):
        newStr += chr(ord(inString[i]) - 1)
    return newStr


#####
if __name__ == '__main__':
    app.run()

