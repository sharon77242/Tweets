# # Twitter API credentials
# c_consumer_key = "zBlIrsX4n5c1Z43FxsKFGJITY"
# c_consumer_secret = "s4NniXqLAbjTtDdPKBvRtDPTUbvRSScX7UvXqLNKRAHQrPingc"
# c_access_key = "931836587142537216-hjJ0SkbYLM8HjZRmY5gaTycaBEHfUB4"
# c_access_secret = "zbhC62mh7mR9ioilqinajIHE2lXJ0dpNfI1YYZuC1jav7"
# c_new_york_token = [c_consumer_key, c_consumer_secret, c_access_key, c_access_secret]
#
# # Second token credentials
# c2_consumer_key = "23DbpBPOAFVsM9FjppwY4UduI"
# c2_consumer_secret = "r2q6mvQDCKFWwV2l12urtU97e5EOzx5hSi1uFAtFKhRbA1SxND"
# c2_access_key = "931872988236009473-Qlvvj3twozcvYiz9HsxYtEvnwrSmvu5"
# c2_access_secret = "Uq2JUbf0uFwQJhvH0AU7UOsIfupsnOyOoF5407FkCD9dk"
# c_los_angeles_token = [c2_consumer_key, c2_consumer_secret, c2_access_key, c2_access_secret]
#
# # Third token credentials
# c3_consumer_key = "XvZjdyUBxKYC7ZKbmevM6IxdT"
# c3_consumer_secret = "npNmNrzT9XyLZ4CBsuM0BVTgH9A9uVPGlmhQZbbDjMWUrLG51G"
# c3_access_key = "196559721-oIcQtDXnquxNMGbBD4lZhNwuaC3KR7TFza3MyAWp"
# c3_access_secret = "Gj41I8RqrkGcW6hvr7ZkvR5AIXYn3LokbAN6QnT1YIeCE"
# c_california_token = [c3_consumer_key, c3_consumer_secret, c3_access_key, c3_access_secret]


# Twitter API credentials
CONSUMER_KEY = "23DbpBPOAFVsM9FjppwY4UduI"
CONSUMER_SECRET = "r2q6mvQDCKFWwV2l12urtU97e5EOzx5hSi1uFAtFKhRbA1SxND"
ACCESS_KEY = "931872988236009473-Qlvvj3twozcvYiz9HsxYtEvnwrSmvu5"
ACCESS_SECRET = "Uq2JUbf0uFwQJhvH0AU7UOsIfupsnOyOoF5407FkCD9dk"

NEW_YORK = "new york"
LOS_ANGELES = "los angeles"
CALIFORNIA = "california"

COUNTRIES_DICT = {" ny": NEW_YORK,
                  "nyc": NEW_YORK,
                  NEW_YORK: NEW_YORK,
                  ", la": LOS_ANGELES,
                  LOS_ANGELES: LOS_ANGELES,
                  ", ca ": CALIFORNIA,
                  CALIFORNIA: CALIFORNIA
                  }

COUNTRIES = ["new york", "california", "los angeles"]

COUNTRIES_FILTER = list(COUNTRIES_DICT.keys())

URL = 'localhost'
TEXT = 'text'
USER = 'user'
LOCATION = 'location'
PLACE = 'place'
FULL_NAME = 'full_name'
TWEETS = 'tweets'
time_end = ''
TXTS = 'txts'
BEST_TWEETS = 'bestTweets'