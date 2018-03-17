#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
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
            try:
                tid = status.id_str
            except AttributeError:
                tid = ''
            try:
                created_at = status.created_at
            except AttributeError:
                created_at = ''
            try:
                user_name = status.user.screen_name.replace('"', "'")
            except AttributeError:
                user_name = ''
            try:
                user_place = status.user.location.replace('"', "'")
            except AttributeError:
                user_place = ''
            try:
                place = status.place.full_name.replace('"', "'")
            except AttributeError:
                place = ''
            try:
                coord = ','.join(map(str, status.coordinates.coordinates).reverse())
            except AttributeError:
                coord = ''
            try:
                polygon0 = ','.join(map(str, status.place.bounding_box.coordinates[0][0]).reverse())
                polygon1 = ','.join(map(str, status.place.bounding_box.coordinates[0][1]).reverse())
                polygon2 = ','.join(map(str, status.place.bounding_box.coordinates[0][2]).reverse())
                polygon3 = ','.join(map(str, status.place.bounding_box.coordinates[0][3]).reverse())
            except AttributeError:
                polygon0 = ''
                polygon1 = ''
                polygon2 = ''
                polygon3 = ''
            try:
                text = status.extended_tweet['full_text']
            except AttributeError:
                try:
                    text = 'RT @{0}: {1}'.format(status.retweeted_status.user.screen_name, status.retweeted_status.extended_tweet['full_text'])
                except AttributeError:
                    try:
                        text = 'RT @{0}: {1}'.format(status.retweeted_status.user.screen_name, status.retweeted_status.text)
                    except AttributeError:
                        text = status.text if status.text else ''
            text = text.replace('"', "'").replace('\n', ' || ')
            csv_row = '"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}"\r\n'.format(tid, created_at, user_name, user_place, coord, place, polygon0, polygon1, polygon2, polygon3, text)
            print(text)
            #print(csv_row)
            #print(json.dumps(status._json, indent=4) + '\n')
            csv.write(csv_row)


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
