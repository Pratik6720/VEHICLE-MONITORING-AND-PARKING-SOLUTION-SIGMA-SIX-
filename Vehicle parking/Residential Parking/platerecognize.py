import json
import requests


# Fetch Number PLate String using API
def ocr():
    regions = ['fr', 'it']
    with open('cropped.jpeg', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token api'})
    fetch_data = response.json()
    # pprint(fetch_data)

    # fetch data form api and  save in json format
    with open('data.json', 'w') as f:
        json.dump(fetch_data, f)

    # open data.json file and load it
    with open("data.json") as f_check:
        data = json.load(f_check)
    # print(data)

    # display the plate value
    for p in data['results']:
        l = p['plate']
        # print("plate :" + l)

        # Numberplate Save in text file
        with open('numberplate.txt', 'w') as f:
            f.write(l.upper())
            f.close()

        # Open Numberplate.txt file
        f = open("numberplate.txt", "r")
        pratik = f.read()

        print("===============================================================")
        print("Number Plate :", pratik)
        import rto_testing_video as vk
        vk.checkValue(pratik)  # Here it checks in database and identifies whether he is a resident or a visitor
# ocr()
