import dropbox
import webbrowser

APP_KEY = 'on05eegr9q45xib'
APP_SECRET = 'ymdv0q3j7pmo35r'



def main():
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    authorize_url = flow.start()
    webbrowser.open(authorize_url)
    print 'Copy the authorization code'
    code = raw_input('>> ').strip()
    access_token, user_id = flow.finish(code)
    ## Make sure to store the access token somewhere
    ## For reference, my access code is gOfuLaE0lPIAAAAAAAAAEMtLloMwBWgGc4BgBBOKBGc
    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()



if __name__ == '__main__':
    main()