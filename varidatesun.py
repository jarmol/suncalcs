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

p1 = Location("Helsinki", 60.18, 24.93, 2)
p1.printrecord()

sol1a = Solar(dnr, p1, "SUNRISE", znt_official)
sol1b = Solar(dnr, p1, "SET", znt_official)

delivery(sol1a, sol1b, p1)

p2 = Location("Oulu", 65.02, 25.47, 2)
p2.printrecord()

sol2a = Solar(dnr, p2, "SUNRISE", znt_official)
sol2b = Solar(dnr, p2, "SET", znt_official)

delivery(sol2a, sol2b, p2)

p3 = Location("Vancouver B.C.", 49.217, -123.1, -8)
p3.printrecord()	# Vancouver

sol3a = Solar(dnr, p3, "SUNRISE", znt_official)
sol3b = Solar(dnr, p3, "SET", znt_official)

delivery(sol3a, sol3b, p3)

print("Declination %.2f degrees at sunrise" % sol1a.Declination)
print("Declination %.2f degrees at sunset" % sol1b.Declination)

meandecl = getdeclination(sol1a, sol1b)
print("Declination %.2f degrees at noon" % meandecl)
