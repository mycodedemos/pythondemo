from app.common.third.wx import MediaPlatform

mp = MediaPlatform()
if __name__ == '__main__':
    token = mp.get_access_token()
    print(token)
    mp.create_menu(token['access_token'])
