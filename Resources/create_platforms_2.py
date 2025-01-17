import requests
import json

url = 'https://cloud.distributed-avionics.com/app/simulation/addBatchSimulation'

purdue_airport = {"headingDeg": 50, "location": {"latDeg": 40.40861,"lngDeg": -86.93839,"altM": 9.143999707392009}}
dahnke_airport = {"headingDeg": 0 , "location": {"latDeg": 40.50865,"lngDeg": -86.89334,"altM": 9.143999707392009}}
wyandotte_airport = {"headingDeg": 90, "location": {"latDeg": 40.34918,"lngDeg": -86.76400,"altM": 9.143999707392009}}
timber_house_airport = {"headingDeg": 90, "location": {"latDeg": 40.28505,"lngDeg": -86.85516,"altM": 9.143999707392009}}

#Chuhao's account
headers = {
    'Content-Type': 'application/json',  
    'Cookie': r'.AspNetCore.Antiforgery.lQyFYtd3Sfw=CfDJ8DZsQj3dVo1KtJO1pAUIJAqO194WpWzFlJasPZExAqGHDU8Jqsu-Cd-Ct4lil26iRWSVBJhtKaiBZj-AJvLkS8UBXsVfhZsT3vGY0BShDOU2HyrFVPdc7hGnMfXt-dcHLcXmlYLxbUVONI6BHwL2tgM; .DA-CC-Identity=CfDJ8DZsQj3dVo1KtJO1pAUIJAqjMRDSC4pZCaDYTVePLoKcu2cg5_lfAcY5AW0pjGz7VZ-24ihDXbCUOf2AVKR7lKloYJ6QJ4hZYwjjHX18LbpFwpRw_p3b3rKTVe-P4CU7Xy_TnONPTCo5Wtfw5rmRF49VsMCwPYLvmvK42HTorQ-znyferKuXZORhPBstfw9kcdZeL3MNYbNyXsf5uYlRfE9yUcplk55dGBqdpUC7eHfGYjjHmQgY0eIkNlLRvi8lf0Di71JdIuELvU_YhQoyERooCTIuFf1eTjU0a-aKD_X1X8-wI2nrbOlzqulvFNT_SZThX8l_lxdeiSWeqLReU5rJ6lMd1iL-xSj9ZEv4W9VZFyQDWaU__dKLObJqE8zsa7FkIa-NvTvnSX3L8xgANQtKWiUox4G-bZ1dzMPUM7GDoyrotm1She5j5m3MlPsiFyiElKW1qQqejCwebLSoTeFSdfI1jFE3FjG5obaLtw7As7jb4jX7D9wXtdltGUA6oO9n13FkYjF-J6UFnNl61xC0_q5ACRrY_2vfM-ve2w7WBkNX1l5WFN6buw5xGFb1Gqy5s7XoF4cQCbTrXsSPbozwnECOybpOfZu5XE_jIC9nryePasu64QCvpsy-zntE4f1Yevb8D8Uoyru4oh7U7UyFltrk0emLI19p_-VAEXC-mADgA6QTMOGBeh0boexjXooILGDBAwKy5u1vPoB3oA5dfgeIlnVLSm3jKy4qR9UW8ClqlHc4l_j0SnM31aqDrq08BliD9myfcPu4QP0PpH15PUiIiDBE98ia6KorafOSF-9QTOxoomBeWfcQ90NFfw',  # Add any authorization token if required
}

payloads = [
    # {"numberOfInstances": 1, "prefix": "test_trial ", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    # {"numberOfInstances": 1, "prefix": "trial1_Purdue_Dahnke", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    # {"numberOfInstances": 1, "prefix": "trial1_sec_Purdue_Dahnke", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    # {"numberOfInstances": 1, "prefix": "Dahnke_marker", "simulationType": "ProductionSim-Peregrine", "headingDeg": dahnke_airport["headingDeg"], "location": dahnke_airport["location"]},
    {"numberOfInstances": 1, "prefix": "trial2_Purdue_Wyandotte", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    {"numberOfInstances": 1, "prefix": "trial2_Purdue_TimberHouse", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    {"numberOfInstances": 1, "prefix": "trial2_sec_Purdue_Wyandotte", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    {"numberOfInstances": 1, "prefix": "trial2_sec_Purdue_TimberHouse", "simulationType": "ProductionSim-Peregrine", "headingDeg": purdue_airport["headingDeg"], "location": purdue_airport["location"]},
    {"numberOfInstances": 1, "prefix": "Wyandotte_marker", "simulationType": "ProductionSim-Peregrine", "headingDeg": wyandotte_airport["headingDeg"], "location": wyandotte_airport["location"]},
    {"numberOfInstances": 1, "prefix": "timber_house_marker", "simulationType": "ProductionSim-Peregrine", "headingDeg": timber_house_airport["headingDeg"], "location": timber_house_airport["location"]},
    {"numberOfInstances": 1, "prefix": "intruder", "simulationType": "ProductionSim-Peregrine", "headingDeg": timber_house_airport["headingDeg"], "location": timber_house_airport["location"]},
    ]

for payload in payloads:
    json_payload = json.dumps(payload)

    try:
        response = requests.post(url, headers=headers, data=json_payload)

        if response.status_code == 200:
            print("POST request successful!")
            print("Response:", response.json())
        else:
            print("POST request failed with status code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("An error occurred:", str(e))