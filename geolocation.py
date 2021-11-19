import geocoder

#def geo():
g = geocoder.ip('me')
location = g.latlng
print(location)
    #file = open("user_current_location.txt", "w")
    #file.write(str(location))
    #file.close()
