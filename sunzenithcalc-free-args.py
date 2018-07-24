import math, time

znt_official = 90.833		# fixed earlier 90.0 / JL 25.12.2014
znt_civil = 96.0 		# degrees
znt_nautical = 102.0 		# degrees
znt_astronomical = 108.0 	# degrees
d2r = math.pi/180.0		# conversion of angles in degrees to radians

def sin(alfa):
   return math.sin(d2r*alfa)

def cos(alfa):
   return math.cos(d2r*alfa)

def floor(x):
   return math.floor(x)

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
    h = decimhours  	# floating hours
    s = 3600*h		# seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

def dayNr(yyyy, mm, dd):
   # Calculate the day number of the given date
    N1 = floor(275*mm/9)
    N2 = floor((mm + 9)/12)
    N3 = (1 + floor((yyyy - 4 * floor(yyyy/4) + 2)/3))
    N = N1 - (N2*N3) + dd - 30
    return N 

#  I have added day and localOffset to suncalc function / JL 
def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith):
    print("Date: %d-%d-%d" % (year, month, day))
    N = dayNr(year, month, day)
    print("Day of the year N = %.1f \n" % N)
    print("Zenith %.3f degrees used for %s" % (zenith, suncalctype))

#  2. convert the longitude degree to hour value and calculate an approximate time
    longitude = lot1	# degrees
    lngHour = longitude / 15 # hours
    t0 =  N + ((6 - lngHour) / 24)
    if (suncalctype == "SUNRISE"):
        t = t0
    else:
        t = t0 + 0.5

#  3. calculate the Sun's mean anomaly
    M = (0.9856 * t) - 3.289

#  4. calculate the Sun's true longitude
    L = M + (1.916*sin(M)) + (0.020*sin(2*M)) + 282.634

#  NOTE: L potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
    print("Test a) L = %f before" % L)
 
    L %= 360
    print("Test b) L = %f adjusted" % L)

#  5a. calculate the Sun's right ascension
    RA = math.atan(0.91764 * math.tan(d2r*L))

# Correction: added converting RA to degrees / JL 25.12.2014
    RA /= d2r

#  NOTE: RA potentially needs to be adjusted into the range [0, 360) by adding/subtracting 360
#  Added this JL 25.12.2014
    RA %= 360 	# works for positive and negative values

#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant = (floor( L/90)) * 90
    RAquadrant = (floor(RA/90)) * 90
    RA = RA + (Lquadrant - RAquadrant)
# 5c. right ascension value needs to be converted into hours
    RA /= 15

# 6. calculate the Sun's declination
    sinDec = 0.39782 * sin(L)
    cosDec = math.cos(math.asin(sinDec))
    declination = math.acos(cosDec)/ d2r  # as degrees

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1
    print("Latitude = %.2f degrees ( = %.4f radians), longitude = %.2f degrees" % (lat1, latitude, longitude))
    print("Local offset %.1f hours" % localOffset)

    cosH = (cos(zenith) - (sinDec*sin(lat1))) / (cosDec*cos(lat1))
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

    return UT, declination, H, localOffset
# end of suncalc()

# Main begin
# Enter year, month and day
year  = int(raw_input('Enter year  --> '))
month = int(raw_input('Enter month --> '))
day = int(raw_input('Enter day --> '))
city = raw_input('T = Tornio: latitude 65.85')
if (city == 'T'):
   Latitude = 65.85
   Longitude = 24.18
else: 
   Latitude = 60.16 
   Longitude = 24.96

TimeZone = 2.0 	# always
zenit1 =  raw_input('Civil Y/N').upper()
zenit2 =  raw_input('Nautical Y/N').upper()
zenit4 =  raw_input('Astronomical Y/N').upper()
# Call suncalc()
calctype = "SUNRISE"
print "\n1.", calctype
UT1, declination1, H, locOffset = suncalc(year, month, day, calctype, Latitude, Longitude, TimeZone, znt_official)
H1 = 24.0 - H
print("UT1 %.4f Declination %.4f" % (UT1, declination1)) 
print("Hour angle %.4f hours = %s" %(H1, human(H1)))

if zenit1 == 'Y':
   print "\n2. CIVIL TWILIGHT"
   suncalc(year, month, day, calctype, Latitude, 24.96, 2.0, znt_civil)
   print "\n-------\n"

if zenit2 == 'Y': 
   print "\n2. NAUTICAL TWILIGHT"
   suncalc(year, month, day, calctype, Latitude, 24.96, 2.0, znt_nautical)
   print "\n-------\n"

calctype = "SUNSET"
print "\n1.", calctype
UT2, declination2, H2, locOffset = suncalc(year, month, day, calctype, Latitude, 24.96, 2.0, znt_official)
print("UT2 %.4f Declination %.4f" % (UT2, declination2))
noon1 = UT1 + H1 + locOffset
print ("Noontime %s" % human(noon1))
print("Hour angle %.4f hours = %s" %(H2, human(H2)))
print("Daylengt from hour angles %.4f = %s" % (H1 + H2, human(H1 + H2))) 
print("Daylength as difference of Sunrise and Sunset %.4f hours = %s" % ((UT2 - UT1), human(UT2 - UT1)))
avgDeclination =  0.5*(declination1 + declination2)
noonElevation = avgDeclination - Latitude + 90.0
print ("Average declination %.4f" % avgDeclination)
print ("Elevation (Sun angle) at noon:  %.4f" % noonElevation)

if zenit1 == 'Y':
   print "\n2. CIVIL TWILIGHT"
   suncalc(year, month, day, calctype, Latitude, 24.96, 2.0, znt_civil)

if zenit2 == 'Y': 
   print "\n2. NAUTICAL TWILIGHT"
   suncalc(year, month, day, calctype, Latitude, 24.96, 2.0, znt_nautical)
   print "\n-------\n"

