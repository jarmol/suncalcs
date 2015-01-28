import Location		# My module
from Location import Location, Solar, Dates

znt_official = 90.833

d1  = Dates(2015, 1, 26)
dnr = d1.yday()
sd =  d1.getdate()
print("\nDate %s (Day number %d) \n" % (sd, dnr))

p1 = Location("Helsinki", 60.18, 24.93, 2)
p1.printrecord()

sol1a = Solar(dnr, p1, "SUNRISE", znt_official)
sol1b = Solar(dnr, p1, "SET", znt_official)

s1 = sol1a.suncalc()
s2 = sol1b.suncalc()
print "Sunrise", s1
print ("Sunset %s\n------\n"% s2)

p2 = Location("Tornio", 65.83, 24.18, 2)
p2.printrecord()	# Tornio

sol2a = Solar(dnr, p2, "SUNRISE", znt_official)
sol2b = Solar(dnr, p2, "SET", znt_official)

s1 = sol2a.suncalc()
s2 = sol2b.suncalc()
print "Sunrise", s1
print ("Sunset %s\n------\n"% s2)

p3 = Location("Vancouver B.C.", 49.217, -123.1, -8)
p3.printrecord()	# Vancouver

sol3a = Solar(dnr, p3, "SUNRISE", znt_official)
sol3b = Solar(dnr, p3, "SET", znt_official)

s1 = sol3a.suncalc()
s2 = sol3b.suncalc()
print "Sunrise", s1
print ("Sunset %s\n------\n"% s2)

print("Declination %.2f degrees" % sol1a.Declination)
print("Declination %.2f degrees" % sol1b.Declination)

