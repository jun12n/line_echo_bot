CHANNEL_SECRET = '4a9405b9fec7bcfa3921bb604639262c'
CHANNEL_ACCESS_TOKEN = 'j6ZsuHxHHQ5CfW+VxyrAVclMOrToYk/kRuNfpVu1XIos8Th4Nr41wtE6lU4DoOHRySH9m90GToTyBs60+WAzvrVA7EUAxviv9rnSSN4kh6hSLPvocKlU6l5V4BnIxyAHkWQxHVdhgsg7tP8m2pu6qQdB04t89/1O/w1cDnyilFU='


def get_token(token_name):
    if token_name == 'channel_secret':
        return CHANNEL_SECRET
    elif token_name == 'channel_access_token':
        return CHANNEL_ACCESS_TOKEN
    else:
        print('Wrong token name')