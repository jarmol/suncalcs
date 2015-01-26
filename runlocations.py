import Location		# My module
znt_official = 90.833

d1=Location.Dates(2015, 1, 26)
dnr = d1.yday()
d1.printdate()
print("Day number %d \n" % dnr)

p1=Location.Location("Helsinki", 60.18, 24.93, 2)
p1.printrecord()

sol1a = Location.Solar(dnr, p1.Latitude, p1.Longitude, "SUNRISE", znt_official, p1.Timezone)
#sol1a.getsolar()	# Sunrise official zenith
sol1b = Location.Solar(dnr, p1.Latitude, p1.Longitude, "SET", znt_official, p1.Timezone)
#sol1b.getsolar()	# Sunset zenith official

s1 = sol1a.suncalc()
s2 = sol1b.suncalc()
print "Sunrise", s1
print ("Sunset %s\n------\n"% s2)

p2=Location.Location("Tornio", 65.83, 24.18, 2)
p2.printrecord()	# Tornio

sol2a = Location.Solar(dnr, p2.Latitude, p2.Longitude, "SUNRISE", znt_official, p2.Timezone)
sol2b = Location.Solar(dnr, p2.Latitude, p2.Longitude, "SET", znt_official, p2.Timezone)

s1 = sol2a.suncalc()
s2 = sol2b.suncalc()
print "Sunrise", s1
print ("Sunset %s\n------\n"% s2)

p3=Location.Location("Vancouver B.C.", 49.217, -123.1, -8)
p3.printrecord()	# Vancouver

sol3a = Location.Solar(dnr, p3.Latitude, p3.Longitude, "SUNRISE", znt_official, p3.Timezone)
sol3b = Location.Solar(dnr, p3.Latitude, p3.Longitude, "SET", znt_official, p3.Timezone)

s1 = sol3a.suncalc()
s2 = sol3b.suncalc()
print "Sunrise", s1
print ("Sunset %s\n------\n"% s2)

print("Declination %.2f degrees" % sol1a.Declination)
print("Declination %.2f degrees" % sol1b.Declination)

