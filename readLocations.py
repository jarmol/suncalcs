cityTable = []
cityList = []
nr = 6 # Number of cities
myData = open("locationData.txt", "rb")
print "File: ", myData.name
if myData.closed:
   print "not open!"
else:
   print "open mode ", myData.mode
 
cityTable = myData.read().split('\n')
myData.close()

print "The raw data:\n", cityTable, "\n", "-"*12
print "file length", len(cityTable)

for i in range(0,nr):
    cityRow = cityTable[i]
    print cityRow
    cityList = cityRow.split(' ')
    print cityList
    city = cityList[0]
    latitude = cityList[1]
    longitude = cityList[2]
    timeZone = cityList[3]
    print "City: %s Latitude: %s Longitude: %s Timezone: %s " % (city, latitude, longitude, timeZone)
    print "Pohjoisnavalle matkaa: %6.2f astetta\n" % (90.0 - float(latitude))
