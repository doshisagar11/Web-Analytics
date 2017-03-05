import os
import json
import random+
import requests
import time

from flask import Flask, request, Response


application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'Sagar_Bot'
my_slack_username = 'sdoshi'


slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    # Adding a delay so that all bots don't answer at once (could overload the API).
    # This will randomly choose a value between 0 and 10 using a uniform distribution.
    delay = random.uniform(0, 1)
    time.sleep(delay)

    print '========POST REQUEST @ /slack========='
    response = {'username': 'Sagar_Bot', 'icon_emoji': ':robot_face:'}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    print text
    print type(text)

    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if username in [my_slack_username, 'sdoshi','zac.wentzell']:
        # Your code for the assignment must stay within this if statement
        c_date = []
        # A sample response:
        #Task 1
        if text == "&lt;BOTS_RESPOND&gt;":
        # you can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = "Hello, my name is Sagar_bot. I belong to sdoshi. I live at 54.212.194.255."
            print 'Response text set correctly'
            print response['text']
            r = requests.post(slack_inbound_url, json=response)


        bool='[' in text

        if not bool:#Task 2
          if '&lt;I_NEED_HELP_WITH_CODING&gt;' in text:

            print 'imside if'
            z = text.split(':')
            first=z[0]
            second=z[1]
            payload = {'order':'desc', 'sort':'activity', 'q':second, 'accepted':'true', 'answers':5, 'site':'stackoverflow'}
            output = requests.get('https://api.stackexchange.com/2.2/search/advanced', params=payload).json()
            print output
            counter = 0
            while (counter < 5):
                response = {'username': 'Sagar_Bot', 'icon_emoji': ':robot_face:'}
                datetime = c_date.append(str(time.strftime("%a %d %b %Y %H:%M:%S GMT",time.gmtime(output['items'][counter]['creation_date']))))
                response['text']=str(output['items'][counter]['title'])+'\t'+str(output['items'][counter]['link'])+'\t'+str(output['items'][counter]['answer_count'])+'\t'+c_date[counter]
                print response['text']
                r = requests.post(slack_inbound_url, json=response)
                counter=counter+1

            print 'loop last line'

        #Task 3
        else:
            print 'inside if'
            z = text.split(':')
            full_text=z[1].split('[')
            query=full_text[0]
            tagged=full_text[1][:-1]
            body=full_text[2][:-1]
            payload = {'order':'desc', 'sort':'activity', 'q':query, 'body':body, 'accepted':'true', 'answers':5, 'tagged':tagged, 'site':'stackoverflow'}
            output = requests.get('https://api.stackexchange.com/2.2/search/advanced', params=payload).json()
            print output
            counter = 0
            while (counter < 5):
                response = {'username': 'Sagar_Bot', 'icon_emoji': ':robot_face:'}
                datetime = c_date.append(str(time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(output['items'][counter]['creation_date']))))
                response['text'] = str(output['items'][counter]['title']) + '\t' + str(output['items'][counter]['link']) + '\t' + str(output['items'][counter]['answer_count']) + '\t' + c_date[counter]
                print response['text']
                r = requests.post(slack_inbound_url, json=response)
                counter=counter+1

            print 'loop last line'

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
