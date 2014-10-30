import math, time

znt_official = 90.8333  # degrees 
znt_civil = 96.00 	# degrees
znt_nautical = 102.00 	# degrees
znt_astronomical = 108.00 # degrees
d2r = math.pi/180.0	# conversion of angles in degrees to radians
m_formula = 2		# mean anomaly in P Schlyter's way
# m_formula = 1		# mean anomaly acc to KM formulas

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
    h=decimhours  	# floating hours
    s = 3600*h		# seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

#  I have added day and localOffset to suncalc function! 
def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith):
    print("Date: %d-%d-%d" % (year, month, day))
    print("Zenith %.1f degrees used" % zenith)
    N1 = (275 * month // 9)
    N2 = ((month + 9) // 12)
    N3 = 1 + ((year - 4*(year // 4) + 2) // 3)
    N = N1 - (N2 * N3) + day - 30
#   print("N1 = %.1f, N2 = %.1f, N3 = %.1f, N = %.1f \n" % (N1, N2, N3, N))
    print("Day of the year: %d" % N)

# PS: d = 367*y - 7 * ( y + (m+9)/12 ) / 4 + 275*m/9 + D - 730530
    d = 367*year - 7*(year + (month+9)//12)/4 + 275*month//9 + day - 730530
    print ("Daynumber d = %d" % d)

#  2. convert the longitude to hour value and calculate an approximate time
    longitude = lot1
    lngHour = longitude / 15

    if (suncalctype == "SUNRISE"):
        t = N + ((6 - lngHour) / 24)
    else:
        t = N + ((18 - lngHour) / 24)

#  3. calculate the Sun's mean anomaly
#  M = 356.0470_deg + 0.9856002585_deg * d   (PS: mean anomaly)
    Mo = 356.0470 + 0.9856002585 * d   # PS: mean anomaly
    if (Mo > 360.0): Mo = Mo % 360.0
    Mx = (0.9856 * t) - 3.289	# KM: mean anomaly degr
    if m_formula == 2: M = Mo	# PS: mean anomaly
    print("PS: mean anomaly M = %f degrees" % Mo)
    print("KM: mean anomaly M = %f degrees" % Mx)
    if m_formula == 1: M = Mx	# KM: mean anomaly

#  4. calculate the Sun's true longitude
    L = M + (1.916 * math.sin(d2r*M)) + (0.020 * math.sin(2*M*d2r)) + 282.634

#  NOTE: L potentially needs to be adjusted into the range [0,360) by 
#  adding/subtracting 360

    print("Test a) L = %f before" % L)
 
    if (L > 360.0):
        L-= 360.0
    elif (L < -360.0):
        L+= 360 

    print("Test b) L = %f adjusted" % L)

#  5a. calculate the Sun's right ascension
    RAo = math.atan(0.91764 * math.tan(d2r*L)) # Result in radians!
    RA = RAo/d2r	# converted to degrees

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant  = ( L // 90)*90
    RAquadrant = (RA // 90)*90
    RA = RA + (Lquadrant - RAquadrant)
# 5c. right ascension value needs to be converted into hours
    RA = RA / 15
# 6. calculate the Sun's declination
    sinDec = 0.39782 * math.sin(d2r*L)
    cosDec = math.cos(math.asin(sinDec))

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1
    print("Latitude = %.2f degrees ( = %.4f radians ), longitude = %.2f degrees" % (lat1, latitude, longitude))
    print("Local offset %.1f hours" % localOffset)

    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    if (cosH > 1):
        print "the sun never rises on this location (on the specified date.\n"

    if (cosH < -1):
        print "the sun never sets on this location (on the specified date)\n"

#  7b. finish calculating H and convert into hours

#  if setting time is desired:
    H = math.acos(cosH)/d2r # degrees

#  if rising time is desired:
    if (suncalctype == "SUNRISE" ):
        H = 360 - H

    H = H/15

#  8. calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622
#  9. adjust back to UTC
    UT = (T - lngHour) % 24
# NOTE: UT potentially needs to be adjusted into the range [0,24) by
# adding/subtracting 24

    riset = "Sunset"
    if (suncalctype == "SUNRISE"): riset = "Sunrise"        
    print("%s UT is %.4f hours = %s" % (riset, UT, human(UT)))

# 10. convert UT value to local time zone of latitude/longitude
    localT = UT + localOffset
    print("%s local time is %.4f hours = %s" % (riset, localT, human(localT)))

# end of suncalc()

# Main begin
# Enter month and day of the year 2014
year = int(raw_input('Enter year  --> '))
month = int(raw_input('Enter month --> '))
day = int(raw_input('Enter day --> '))

# Call suncalc()
# Using location Bratislawa and zenith_official as in
# http://calendar.zoznam.sk/sunset-sk.php?city=3060972
# Calculation for time zone CET (UT + 2 hr)

print "1. SUNRISE / SUNSET"
suncalc(year, month, day, "SUNRISE", 48.1482, 17.1067, 1.0, znt_official)
suncalc(year, month, day, "SUNSET", 48.1482, 17.1067, 1.0, znt_official)

print "\n2. CIVIL TWILIGHT"
suncalc(year, month, day, "SUNRISE", 48.1482, 17.1067, 1.0, znt_civil)

print "\n3. NAUTICAL TWILIGHT"
suncalc(year, month, day, "SUNRISE", 48.1482, 17.1067, 1.0, znt_nautical)

print "\n4. ASTRONOMICAL TWILIGHT"
suncalc(year, month, day, "SUNRISE", 48.1482, 17.1067, 1.0, znt_astronomical)

