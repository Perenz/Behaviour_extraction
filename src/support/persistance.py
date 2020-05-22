import json

def check_user_last(id):
    #Implement DB persistance

    #1093586351549804544
    ids = [1, 2, 3, 1093586351549804544]
    print("Checking")
    if int(id) in ids:
        with open('profile.json') as f:
            data = json.load(f)
        last = data.get('last')
        print(last)
        return last
    else:
        return None