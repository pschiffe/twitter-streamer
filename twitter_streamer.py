#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import tweepy
import configparser


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    _tweets_csv_path = None

    def __init__(self, api=None, tweets_csv_path=None):
        super().__init__(api=api)
        self._tweets_csv_path = tweets_csv_path

    def on_status(self, status):
        # store tweets in a csv file and print them to stdout
        with open(self._tweets_csv_path, mode='a') as csv:
            # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
            user_name = status.user.name.replace('"', "'") if status.user and status.user.name else ''
            place = status.user.location.replace('"', "'") if status.user and status.user.location else ''
            coord = ','.join(["%f" % n for n in status.coordinates['coordinates']]) if status.coordinates and status.coordinates['coordinates'] else ''
            text = status.text.replace('"', "'") if status.text else ''
            csv.write('"%s","%s","%s","%s"\r\n' % (user_name, place, coord, text))
        print(status.text)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    auth = tweepy.OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
    auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_token_secret'])

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener(tweets_csv_path=config['DEFAULT']['tweets_csv_path'])
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    try:
        # parameters: https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter.html
        myStream.filter(track=config['DEFAULT']['filter_track'].split(','), languages=config['DEFAULT']['filter_lang'].split(','))
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
