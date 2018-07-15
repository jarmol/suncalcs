import math, time

znt_official = 90.833		# fixed earlier 90.0 / JL 25.12.2014
znt_civil = 96.0 		# degrees
znt_nautical = 102.0 		# degrees
znt_astronomical = 108.0 	# degrees
d2r = math.pi/180.0		# conversion of angles in degrees to radians

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
    h = decimhours  	# floating hours
    s = 3600*h		# seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

#  I have added day and localOffset to suncalc function / JL 
def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith):
    print("Date: %d-%d-%d" % (year, month, day))
    print("Zenith %.3f degrees used for %s" % (zenith, suncalctype))
    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + day - 30
    print("Day of the year N = %.1f \n" % N)

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
#    print("Test a) L = %f before" % L)
 
    if (L > 360.0):
        L-= 360.0
    elif (L < -360.0):
        L+= 360 

#    print("Test b) L = %f adjusted" % L)

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
    declination = math.acos(cosDec)/ d2r  # as degrees

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1
    print("Latitude = %.2f degrees ( = %.4f radians), longitude = %.2f degrees" % (lat1, latitude, longitude))
    print("Local offset %.1f hours" % localOffset)

    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    if (cosH > 1):
        print "the sun never rises on this location (on the specified date.\n"

    if (cosH < -1):
        print "the sun never sets on this location (on the specified date)\n"

#  7b. finish calculating H and convert into hours
#  if rising time is desired:
    if (cosH > -1):
       H = math.acos(cosH)/d2r # converted to degrees
    else:
       H = 180.0 # degrees case never setting

    if (suncalctype == "SUNRISE" ):
        H = 360 - H

    H = H / 15	# Hourangleas hours

#  8. calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622
#  9. adjust back to UTC
    UT = (T - lngHour) % 24
# NOTE: UT potentially needs to be adjusted into the range [0,24) by
# adding/subtracting 24
    if (suncalctype == "SUNRISE"):    
       print("Sunrise UT is %.4f hours = %s" % (UT, human(UT)))
       localT = UT + localOffset
       print("Sunrise local time is %.4f hours = %s" % (localT, human(localT)))

# 10. convert UT value to local time zone of latitude/longitude

    if (suncalctype == "SUNSET"):
       print("Sunset UT is %.4f hours = %s" % (UT, human(UT)))
       localT = UT + localOffset
       print("Sunset local time is %.4f hours = %s" % (localT, human(localT)))

    return UT, declination, H
# end of suncalc()

# Main begin
# Enter month and day of the year 2018
month = int(raw_input('Enter month --> '))
day = int(raw_input('Enter day --> '))

# Call suncalc()
print "1. SUNRISE"
UT1, declination, H = suncalc(2018, month, day, "SUNRISE", 60.16, 24.96, 2.0, znt_official)
H1 = 24.0 - H
print("UT1 %.4f Declination %.4f" % (UT1, declination)) 
print("Hour angle %.4f hours = %s" %(H1, human(H1)))

print "\n2. CIVIL TWILIGHT"
suncalc(2018, month, day, "SUNRISE", 60.16, 24.96, 2.0, znt_civil)

print "\n3. NAUTICAL TWILIGHT"
suncalc(2018, month, day, "SUNRISE", 60.16, 24.96, 2.0, znt_nautical)

print "\n4. ASTRONOMICAL TWILIGHT"
suncalc(2018, month, day, "SUNRISE", 60.16, 24.96, 2.0, znt_astronomical)

print "\n-------\n"
print "1. SUNSET"
UT2, declination, H2 = suncalc(2018, month, day, "SUNSET", 60.16, 24.96, 2.0, znt_official)
print("UT2 %.4f Declination %.4f" % (UT2, declination))
print("Hour angle %.4f hours = %s" %(H2, human(H2)))
print("Daylengt from hour angles %.4f = %s" % (H1 + H2, human(H1 + H2))) 
print("Daylength as difference of Sunrise and Sunset %.4f hours = %s" % ((UT2 - UT1), human(UT2 - UT1)))

print "\n2. CIVIL TWILIGHT"
suncalc(2018, month, day, "SUNSET", 60.16, 24.96, 2.0, znt_civil)

