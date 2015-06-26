cityTable =  [['Tornio', 65.85, 24.18, 2],
 ['Oulu', 65.02, 25.47, 2],
 ['Helsinki', 60.18, 24.93, 2],
 ['Oslo',   60.08, 10.66, 1],
 ['Copenhagen', 55.61, 12.65, 1],
 ['Vancouver', 49.217, -123.1, -8]]

myData = open("locationData.txt", "wb")
print "File: ", myData.name
if myData.closed:
   print "not open!"
else:
   print "open mode ", myData.mode
   print "file length", len(myData.name)
 
# myData.write(str(cityTable))
# myData.write("\n")

print "The raw data: ", cityTable, "\n", "-"*12

for i in range(0,6):
   city = cityTable[i][0]
   latitude = cityTable[i][1]
   longitude = cityTable[i][2]
   timeZone = cityTable[i][3]
   print "City: ", city, "Latitude: ", latitude, "Longitude: ", longitude, "Timezone: ", timeZone

# Tiedostoon
   myData.write(city); myData.write(' ')
   myData.write(str(latitude)); myData.write(' ')
   myData.write(str(longitude)); myData.write(' ')
   myData.write(str(timeZone)); myData.write('\n')

   print "Pohjoisnavalle matkaa: ", 90 - latitude

myData.close()
