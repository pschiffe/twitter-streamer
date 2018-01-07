# twitter-streamer

Simple script using [Tweepy](http://www.tweepy.org/) python library for streaming tweets, configurable by ini config file. Tweets are stored in a csv file and printed to the `stdout`.

## Requirements

Tweepy library. Install with your package manager, e.g. on Fedora:
```
sudo dnf install python3-tweepy
```

or with pip:
```
pip3 install tweepy
```

## Configuration

Copy `config.ini.example` to `config.ini` and modify according to your needs.
```
cp config.ini.example config.ini
```

## Usage

Just run in the terminal:
```
./twitter_streamer.py
```
