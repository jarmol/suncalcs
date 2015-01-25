import Location		# My module

p1=Location.Location("Helsinki", 60.18, 24.93, 2)
d1=Location.Dates(2015, 1, 25)
dnr = d1.yday()
d1.printdate()
print("Day number %d \n" % dnr)
p1.printrecord()	# Helsinki

sol1a = Location.Solar(dnr, p1.Latitude, p1.Longitude)
sol1a.getsolar()	# Sunrise official zenith
sol1b = Location.Solar(dnr, p1.Latitude, p1.Longitude, "SET", 96.0)
sol1b.getsolar()	# Sunset zenith civil

sol1a.suncalc()
print("Declination %.2f degrees" % sol1a.Declination)
sol1b.suncalc()
print("Declination %.2f degrees" % sol1b.Declination)

p2=Location.Location("Tornio", 65.83, 24.18, 2)
p3=Location.Location("Vancouver B.C.", 49.217, -123.1, -8)

p2.printrecord()	# Tornio
p3.printrecord()	# Vancouver

