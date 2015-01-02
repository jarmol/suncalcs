import math, time, datetime

znt_official = 90.833		# fixed earlier 90.0 / JL 25.12.2014
znt_civil = 96.0 		# degrees
znt_nautical = 102.0 		# degrees
znt_astronomical = 108.0 	# degrees
d2r = math.pi/180.0		# conversion of angles in degrees to radians
ldt = [0.0, 0.0, 0.0, 0.0]		# Save for sunrise, sunset and declination => daylength and altitude calculation

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
    h=decimhours  	# floating hours
    s = 3600*h		# seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

def yday(year, month, day):
    print("Date: %d-%d-%d" % (year, month, day))
    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
    ydN = N1 - (N2 * N3) + day - 30
    return ydN

#  I have added day and localOffset to suncalc function / JL 
def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith):
    N = yday(year, month, day)
    print("Zenith %.3f degrees used for %s" % (zenith, suncalctype))

#  2. convert the longitude to hour value and calculate an approximate time
    longitude = lot1
    lngHour = longitude / 15

    if (suncalctype == "SUNRISE"):
        t = N + ((6 - lngHour) / 24)
    else:
        t = N + ((18 - lngHour) / 24)

#  3. calculate the Sun's mean anomaly
    M = (0.9856 * t) - 3.289

#  4. calculate the Sun's true longitude
    L = M + (1.916 * math.sin(d2r*M)) + (0.020 * math.sin(2 * M*d2r)) + 282.634

#  NOTE: L potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
 
    if (L > 360.0):
        L-= 360.0
    elif (L < -360.0):
        L+= 360 

#  5a. calculate the Sun's right ascension
    RA = math.atan(0.91764 * math.tan(d2r*L))

# Correction: added converting RA to degrees / JL 25.12.2014
    RA /= d2r

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
#  Added this JL 25.12.2014
    if (RA > 360.0):
        RA-= 360.0
    elif (RA < -360.0):
        RA+= 360

#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant = (math.floor( L/90)) * 90
    RAquadrant = (math.floor(RA/90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

# 5c. right ascension value needs to be converted into hours
    RA = RA / 15

# 6. calculate the Sun's declination
    sinDec = 0.39782 * math.sin(d2r*L)
    cosDec = math.cos(math.asin(sinDec))
    declin = math.atan(sinDec/cosDec)/d2r
    ldt[2] = declin	# Save declination 

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1

#    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    if (cosH > 1):
        print "the sun never rises on this location (on the specified date.\n"

    if (cosH < -1):
        print "the sun never sets on this location (on the specified date)\n"

#  7b. finish calculating H and convert into hours   
    H = math.acos(cosH)/d2r # converted to degrees

#  if rising time is desired:
    if (suncalctype == "SUNRISE" ):
        H = 360 - H
	prtx = "Sunrise"
    else:
        prtx = "Sunset" 

#  degrees to hours:
    H = H / 15

#  8. calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622

#  9. adjust back to UTC
    UT = (T - lngHour) % 24
        
#    print("%s UT %s" % (prtx, human(UT)))

# 10. convert UT value to local time zone of latitude/longitude
    localT = UT + localOffset
    
    print("%s local time %s" % (prtx, human(localT)))
    return UT

# end of suncalc()

# Main begin

now = datetime.datetime.now()
nyear = now.year
nmonth = now.month
nday = now.day

dnr = yday(nyear, nmonth, nday)
print("Day of the year = %.1f \n" % dnr)

# Print the common data only once
latitude = 48.1482; longitude = 17.1067; tzone = 1.0

print("Latitude %.2f degrees, longitude %.2f degrees" % (latitude, longitude))
print("Local offset %.1f hours\n-------\n" % tzone)

print "1. SUNRISE"
UT = suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_official)
ldt[0] = UT	# Save sunrise
ldt[3] = ldt[2]

print "\n2. CIVIL TWILIGHT"
suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_civil)

print "\n3. NAUTICAL TWILIGHT"
suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_nautical)

print "\n4. ASTRONOMICAL TWILIGHT"
suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_astronomical)

print "\n-------\n"

print "1. SUNSET"
UT = suncalc(nyear, nmonth, nday, "SUNSET", latitude, longitude, tzone, znt_official)
ldt[1] = UT	# Save sunset time
 
print "\n2. CIVIL TWILIGHT"
suncalc(nyear, nmonth, nday, "SUNSET", latitude, longitude, tzone, znt_civil)

UT1 = ldt[0]
UT2 = ldt[1]
dlt = UT2 - UT1		# Daylength
tnoon = UT1 + 0.5*dlt	# Noontime
LT1 = UT1 + tzone	# Locan Sunrise
locnoon = tnoon + tzone	# Local noon time
LT2 = UT2 + tzone	# Local Sunset
mdecl = 0.5*(ldt[3] + ldt[2])	# Declination average of sunrise and sunset times

print 3*"--------------", "\n"
print("Sunrise  UTC %s \tLocal %s" % (human(UT1), human(LT1)))
print("Noontime UTC %s \tLocal %s" % (human(tnoon), human(locnoon)))
print("Sunset   UTC %s \tLocal %s" % (human(UT2), human(LT2)))
print("Daylength    %s\n" % human(dlt))
print("Declination %.2f\tLatitude %.2f degrees" % (mdecl, latitude))
print("Sun elevation at noon\t%.2f degrees\n" % (mdecl + latitude))
