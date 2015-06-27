import sys, types, chkdate
import Location		# My module
from Location import *

# Jarmo Lammi 2015
# Solar calculator powered with Python 2.7.6

znt_official = 90.833

code = chkdate.validate(sys.argv)

if isinstance(code, types.IntType):
    print "Error code: %d" % code
    exit(code)
else:
    year = code[0]
    month = code[1]
    day   = code[2]
    d1  = Dates(year, month, day)
    dnr = d1.yday()
    sd =  d1.getdate()
    print("\nDate %s (Day number %d) \n" % (sd, dnr))

cityTable = getTable("locationData.txt")
nr = len(cityTable) - 1 # Number of cities

for i in range(0, nr):
   city, latitude, longitude, timeZone = getRowdata(cityTable[i])
   pl = Location(city, latitude, longitude, timeZone)
   pl.printrecord()

   solpa = Solar(dnr, pl, "SUNRISE", znt_official)
   solpb = Solar(dnr, pl, "SET", znt_official)
   delivery(solpa, solpb, pl)

   meandecl = getdeclination(solpa, solpb)
   print("Declination %.2f degrees at noon" % meandecl)
   print("-----------\n")
