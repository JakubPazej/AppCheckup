import sys
import requests
import re
import progressbar
import itertools
import random
from bs4 import BeautifulSoup
from colored import fg, bg, attr

google_play_url = 'https://play.google.com/store/apps/details?id='
home_url = 'https://apksfull.com'
version_url = 'https://apksfull.com/version/'
search_url = 'https://apksfull.com/search/'
dl_url = 'https://apksfull.com/dl/'

#Made to fake and rotate agent lists in an attempt to get around download restrictions
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
]

user_agent = random.choice(user_agent_list)

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
}

def show_connection_error():
    print(fg('red') + '[!] ERROR: ' + 'Make sure your link on apksfull.com is reachable.'+ attr('reset'))

def show_arg_error():
    print(fg('red') + '[!] ERROR: ' + 'Invalid Format\nShould be of the format `python download.py {{PACKAGE_ID}}`'+ attr('reset'))

#When user specifies invalid id to download the APK from
def show_invalid_id_err():
    print('%s PackageId is invalid %s' % (fg('red'), attr('reset')))

#Progress bar to visualize downloading in shell
def make_progress_bar():
    return progressbar.ProgressBar(
        redirect_stdout=True,
        redirect_stderr=True,
        widgets=[
            progressbar.Percentage(),
            progressbar.Bar(),
            ' (',
            progressbar.AdaptiveTransferSpeed(),
            ' ',
            progressbar.ETA(),
            ') ',
        ])

def main():
    #Get the argument from the command line
    if len(sys.argv) != 2:
        show_arg_error()

    print('%sDownload script starting up%s' % (fg('cornflower_blue'), attr('reset')))

    #Take the package_id from the user
    package_id = sys.argv[1]

    print('%sGetting download link... %s' % (fg('light_yellow'), attr('reset')))

    #Verify google_play_url with packageId string
    g_play_res = requests.get(google_play_url + package_id, headers=headers, allow_redirects=True)
    if(g_play_res.status_code != 200):
        show_invalid_id_err()

    #Search the web page using the package id
    search_res = requests.get(search_url + package_id, headers=headers, allow_redirects=True)

    #Check the statuscode and verify it
    if search_res.status_code != 200:
        show_connection_error()

    #There will be a list of apps that show on the website
    soup = BeautifulSoup(search_res.content, 'html.parser')

    tbody_children = soup.findAll('a')

    sub_dl_links = []

    # loop through the children and get the href
    for item in tbody_children:
        # get href of the child
        link = item.get('href')
        # if link contains "download"
        if link.find("/download/") != -1:
            # append the link to the list
            sub_dl_links.append(home_url+link)

    #Establish a connection to the first link
    sub_dl_res = requests.get(sub_dl_links[0], headers=headers, allow_redirects=True)
    if sub_dl_res.status_code != 200:
        show_connection_error()

    #Locate the script, get the contents
    script_text = BeautifulSoup(sub_dl_res.content, 'html.parser').findAll("script")

    #Find the last but one script tag
    last_script = script_text[-2].contents[0]

    #Query the token from the script
    token = re.findall("token','([^\']+)", last_script)[0]

    #Make a request to the download link
    dl_res = requests.post(dl_url, data={'token': token}, headers=headers)
    if dl_res.status_code != 200:
        show_connection_error()
    dl_res_json = dl_res.json()

    #Get the download_link from the json response
    try:
        download_link = dl_res_json['download_link']
    except KeyError:
        print("%s[!] ERROR: you most likely reached the download limit on apksfull.com:%s" %
             (fg('red'), attr('reset')))
        print(dl_res_json)
        quit()

    #Download the apk
    print('%sDownloading APK%s' % (fg('yellow'), attr('reset')))

    index = package_id.find('.')+1
    app_name = package_id[index:]
    output_file = "output/" + app_name + ".apk"

    r = requests.get(download_link, allow_redirects=True, stream=True)
    with open(output_file, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        bar = make_progress_bar()
        bar.start(total_length)
        dl = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                dl += len(chunk)
                f.write(chunk)
                bar.update(dl)
        bar.finish()
    print('%sAPK Downloaded%s' % (fg('light_green'), attr('reset')))

    tmp="%sFile located in "+output_file+"%s"
    print( tmp % (fg('green'), attr('reset')))

#Run the main
main()