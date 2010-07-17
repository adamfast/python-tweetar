import twitter
import urllib2

NOAA_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations/*station_id*.TXT"

def retrieve_and_post(conf):
    post = False

    pull_url = NOAA_URL.replace('*station_id*', conf['station'])
    request = urllib2.Request(pull_url, None)
    response = urllib2.urlopen(request)
    metar = response.read().split('\n')[1] # NOAA includes a "real" timestamp as the first line of the response

    api = twitter.Api(username=conf['twitter_user'], password=conf['twitter_password'])

    # get the last posted message and make sure it's different before attempting to post. Twitter isn't supposed to allow dupes through but I'm seeing it happen anyway
    past_statuses = api.GetUserTimeline(conf['twitter_user'])
    if past_statuses[-0].text != metar:
        post = True

    if post:
        api.PostUpdate(metar)

if __name__ == '__main__':
    retrieve_and_post({'station': '<station_id>', 'twitter_user': '<twitter_user>', 'twitter_password': '<twitter_pass>'})
