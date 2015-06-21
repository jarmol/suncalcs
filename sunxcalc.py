import math, time

znt_official = 90.8333  # incl air refraction and the upper edge of the sun limb in horizon degrees 
znt_civil = 96.00 	# Sun 6 degrees below horizon
znt_nautical = 102.00 	# Sun 12 degrees below horizon
znt_astronomical = 108.00 # Sun 18 degrees below horizon
d2r = math.pi/180.0	# conversion of angles in degrees to radians
# m_formula = 2		# mean anomaly in P Schlyter's way
m_formula = 1		# mean anomaly acc to KM formulas

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
    h=decimhours  	# floating hours
    s = 3600*h		# seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

def adjust(big_value, good_max):
    x = float(big_value)
    y = float(good_max)

# negative values adjusted to be positive < 360
    if (x > y):
       x-= y*(x // y)
    elif (x < 0):
       x+= y*(1 + (-x // y))

    return x


def opcomdat(year, month, day, N):
# Output common data avoiding repeats
    print("Date: %d-%d-%d" % (year, month, day))
    print("Day of the year: %d" % N)


def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith, pflag):
    N1 = (275 * month // 9)
    N2 = ((month + 9) // 12)
    N3 = 1 + ((year - 4*(year // 4) + 2) // 3)
    N = N1 - (N2 * N3) + day - 30
    if (pflag == 1): opcomdat(year, month, day, N)	# print header

    print("Zenith %.1f degrees" % zenith)

# PS: d = 367*y - 7 * ( y + (m+9)/12 ) / 4 + 275*m/9 + D - 730530
    d = 367*year - 7*(year + (month+9)//12)/4 + 275*month//9 + day - 730530
    if (pflag == 1): print ("Daynumber d = %d since 31.12.1999" % d)

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
#    if (Mo > 360.0): Mo = Mo % 360.0
    Mo = adjust(Mo, 360.0)

    Mx = (0.9856 * t) - 3.289	# KM: mean anomaly degr
    Mx = adjust(Mx, 360.0)
    if m_formula == 2: M = Mo	# PS: mean anomaly

#    if (pflag == 1):
    print("PS: mean anomaly M = %f degrees adjusted" % Mo)
    print("KM: mean anomaly M = %f degrees adjusted" % Mx)

    pflag = 0

    if m_formula == 1: M = Mx	# KM: mean anomaly

#  4. calculate the Sun's true longitude
#  NOTE: L potentially needs to be adjusted into the range [-360,360) by 
#  adding/subtracting 360
    Lx = M + (1.916 * math.sin(d2r*M)) + (0.020 * math.sin(2*M*d2r)) + 282.634 # KM
    Lx = adjust(Lx, 360.0)
    w = 282.9404 + 4.70935E-5 * d # PS: Mean longitude of perihelion
    L = Mo + w 			# PS: Sun's mean longitude
    L = adjust(L, 360.0)
    print ("KM: True longitude L = %f" % Lx)
    print ("PS: Mean longitude L = %.4f, w = %.4f, M = %.4f" % (L, w, Mo))

    if m_formula == 1:
        L = Lx
        print ("Used KM: ")
    else:
        print ("Used PS: L = %f" % L)

#  5a. calculate the Sun's right ascension
    RAo = math.atan(0.91764 * math.tan(d2r*L)) # Result in radians!
    RA = RAo/d2r	# converted to degrees

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
    RA = adjust(RA, 360)

#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant  = ( L // 90)*90
    RAquadrant = (RA // 90)*90
    RA1 = RA + (Lquadrant - RAquadrant)

# 5c. right ascension value needs to be converted into hours
    RA = RA1/15
    print("KM: Right ascension RA = %f degr = %s h" % (RA1, human(RA)))

# 6. calculate the Sun's declination
    sinDec = 0.39782 * math.sin(d2r*L)
    cosDec = math.cos(math.asin(sinDec))
    sundeclin = math.asin(sinDec)/d2r
    print ("Sun declination = %.3f degr" % sundeclin)

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1
    if (pflag == 1):
        print("Latitude = %.2f degrees ( = %.4f radians ), longitude = %.2f degrees" % (lat1, latitude, longitude))
        print("Local offset %.1f hours" % localOffset)

    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    if (cosH > 1):
        print "the sun never rises on this location (on the specified date.\n"

    if (cosH < -1):
# avoid mathematical errors
        cosH = -1
        print "the sun never sets on this location (on the specified zenith)\n"

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
#    print("%s UT is %.4f hours = %s" % (riset, UT, human(UT)))

# 10. convert UT value to local time zone of latitude/longitude
    localT = UT + localOffset
    print("%s local time is %s (UT + %.1f h)\n" % (riset, human(localT), localOffset))

# end of suncalc()

# Main begin
# Enter month and day of the year 2014
year = int(raw_input('Enter year  --> '))
month = int(raw_input('Enter month --> '))
day = int(raw_input('Enter day --> '))

# Call suncalc()
# Using location Bratislawa and zenith_official as in
# http://calendar.zoznam.sk/sunset-sk.php?city=3060972
# Calculation for time zone CET (UT + 1 hr)
# Bratislawa longitude 17.1067E, latitude 48.1482
yrloc = "Bratislawa"
lat1 = 48.1482
lon1 = 17.1067
tz = 1

# Helsinki
yrloc = "Helsinki"
lat1 = 60.18
lon1 = 24.93
tz = 2

print "1. SUNRISE / SUNSET for", yrloc
suncalc(year, month, day, "SUNRISE", lat1, lon1, tz, znt_official, 1)
suncalc(year, month, day, "SUNSET", lat1, lon1, tz, znt_official, 0)

print "\n2. CIVIL TWILIGHT"
suncalc(year, month, day, "SUNRISE", lat1, lon1, tz, znt_civil, 0)
suncalc(year, month, day, "SUNSET", lat1, lon1, tz, znt_civil, 0)

print "\n3. NAUTICAL TWILIGHT"
suncalc(year, month, day, "SUNRISE", lat1, lon1, tz, znt_nautical, 0)

print "\n4. ASTRONOMICAL TWILIGHT for", yrloc
suncalc(year, month, day, "SUNRISE", lat1, lon1, tz, znt_astronomical, 0)

