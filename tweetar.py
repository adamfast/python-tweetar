import twitter
import urllib2

NOAA_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations/*station_id*.TXT"

def retrieve_and_post(conf):
    post = False

    pull_url = NOAA_URL.replace('*station_id*', conf['station'])
    request = urllib2.Request(pull_url, None)
    response = urllib2.urlopen(request)
    metar = response.read().split('\n')[1] # NOAA includes a "real" timestamp as the first line of the response

    if conf.get('hashtag', False):
        metar = '%s #%s' % (metar, conf['hashtag'])

    api = twitter.Api()
    api.SetCredentials(username=conf['oauth_consumer_key'], password=conf['oauth_consumer_secret'], access_token_key=conf['access_token_key'], access_token_secret=conf['access_token_secret'])

    # get the last posted message and make sure it's different before attempting to post. Twitter isn't supposed to allow dupes through but I'm seeing it happen anyway
    past_statuses = api.GetUserTimeline(conf['twitter_user'])

    try:
        if past_statuses[-0].text != metar.strip(): # the text has changed. Post!
            post = True
    except IndexError: # it's brand new, nothing there. Post!
        post = True

    if conf.get('djtweetar_exception', False):
        te = conf['djtweetar_exception']
        te.metar_from_noaa = metar
        te.last_twitter_post = past_statuses[-0].text or None
        te.metar_posted = post
        te.save()

    if post:
        api.PostUpdate(metar)

if __name__ == '__main__':
    retrieve_and_post({'station': '<station_id>', 'twitter_user': '<twitter_user>', 'oauth_consumer_key': '<oauth_consumer_key>', 'oauth_consumer_secret': '<oauth_consumer_secret>', 'access_token_key': '<access_token_key>', 'access_token_secret': '<access_token_secret>'})
