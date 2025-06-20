import json

f = open("text.txt", "r")

# boshang'ich son berilgan 10+ (0, 0+ 10) (30, 30+10)
old_number = f.read()
try:
    dct = json.loads(old_number)
except:
    dct = {12345: "like"}


print(dct["12345"])
json_string = json.dumps(dct)


f = open("text.txt", "w")

f.write(json_string)
