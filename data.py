import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd

def getToken():
    with open("creds.txt", "r") as f:    
        creds = f.read().split("\n")

    auth_url = "https://www.strava.com/oauth/token"
    authorize_url = "https://www.strava.com/oauth/authorize"

    print("Getting authorization")
    payload = {
        'client_id': creds[0],
        'redirect_uri': "http://localhost/exchange_token",
        'scope' : "activity:read_all"
    }
    res = requests.post(authorize_url, data=payload, verify=False)

    print("Requesting Token...\n")
    payload = {
            'client_id': creds[0],
            'client_secret': creds[1],
            'refresh_token': creds[2],
            'grant_type': "refresh_token",
            'f': 'json',
        }

    payload = {
        'client_id': creds[0],
        'client_secret': creds[1],
        'refresh_token': creds[2],
        'grant_type': "authorization_code",
        'code': creds[3],
        'f': 'json',
    }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))
    return access_token

def loop_data():
    # Create the dataframe ready for the API call to store your activity data
    access_token = getToken()
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    header = {'Authorization': 'Bearer ' + access_token, 'scope' : "activity:read_all"}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    df = pd.json_normalize(my_dataset)

    activities = pd.DataFrame(
        columns = [
                "id",
                "name",
                "start_date_local",
                "type",
                "distance",
                "moving_time",
                "elapsed_time",
                "total_elevation_gain",
                "end_latlng",
                "external_id"
        ]
    )
    page = 1

    while True:
        # get page of activities from Strava
        r = requests.get(activites_url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        
        # if no results then exit loop
        if (not r):
            break
        
        # otherwise add new data to dataframe
        for x in range(len(r)):
            activities.loc[x + (page-1)*200,'id'] = r[x]['id']
            activities.loc[x + (page-1)*200,'name'] = r[x]['name']
            activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
            activities.loc[x + (page-1)*200,'type'] = r[x]['type']
            activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
            activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
            activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
            activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
            activities.loc[x + (page-1)*200,'end_latlng'] = r[x]['end_latlng']
            activities.loc[x + (page-1)*200,'external_id'] = r[x]['external_id']
        # increment page
        page += 1
        activities.to_csv('strava_activities.csv')