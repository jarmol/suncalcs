#  Hello
#  could you help me please update this your source code for using multiple zenits
import math
znt_official = 90 
znt_civil = 96 # degrees
znt_nautical = 102 # degrees
znt_astronomical = 108 # degrees
d2r = math.pi/180.0	# conversion of angles in degrees to radians
# Example
# suncalc(2014,8,SUNRISE,48.142,17.099,znt_official){
# 
#  where to assing zenits value ?
#  ----
#  double suncalc(int year,char month,day,suncalctype, double lat1,lot1, char zenith);
#  example
#  suncalc(2014,8,SUNRISE,48.142,17.099,znt_official){
#  Your day and localOffset is missing! 
# double longitude = lot1;
# double latitude = lat1;
#  1. first calculate the day of the year
#  double   N1,N2,N3,N;
#  double   M,L,H,T;
#  double   Lquadrant,Rquadrant,RA;
#  double   sinDec,cosDec,cosH;
#  double UT,localT,localOffset,lngHour;

def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith):
# Using date 20-August-2014, latitude 48.142 and longitude 17.099
# suncalc(2014, 8, 20, "SUNRISE", 48.142, 17.099, 1, znt_official)
    print("Date: %d-%d-%d" % (year, month, day))
    print("Zenith %.1f degrees used" % zenith)
    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + day - 30
    print("N1 = %.1f, N2 = %.1f, N3 = %.1f, N = %.1f \n" % (N1, N2, N3, N))

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
#  5a. calculate the Sun's right ascension
    RA = math.atan(0.91764 * math.tan(d2r*L))

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant = (math.floor( L/90)) * 90
    RAquadrant = (math.floor(RA/90)) * 90
    RA = RA + (Lquadrant - RAquadrant)
# 5c. right ascension value needs to be converted into hours
    RA = RA / 15
# 6. calculate the Sun's declination
    sinDec = 0.39782 * math.sin(d2r*L)
    cosDec = math.cos(math.asin(sinDec))

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1
    print("Latitude = %.2f degrees (=%.4f radians), longitude = %.2f degrees" % (lat1, latitude, longitude))
    print("Local offset %.1f hours" % localOffset)

    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    if (cosH > 1):
        print "the sun never rises on this location (on the specified date.\n"

    if (cosH < -1):
        print "the sun never sets on this location (on the specified date)\n"

#  7b. finish calculating H and convert into hours
#  if rising time is desired:
    H = math.acos(cosH)/d2r # converted to degrees

    if (suncalctype == "SUNRISE" ):
        H = 360 - H

#  if setting time is desired:
    H = H / 15

#  8. calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622
#  9. adjust back to UTC
    UT = (T - lngHour) % 24
# NOTE: UT potentially needs to be adjusted into the range [0,24) by
# adding/subtracting 24
    
    print("Sunrise UT is %.4f hours" % UT)

# 10. convert UT value to local time zone of latitude/longitude
    localT = UT + localOffset
    print("Sunrise local time is %.4f hours" % localT)

# end of suncalc()

# Main begin
# Enter month and day of the year 2014
month = int(raw_input('Enter month --> '))
day = int(raw_input('Enter day --> '))

# Call suncalc()
print "1. SUNRISE"
suncalc(2014, month, day, "SUNRISE", 48.142, 17.099, 1.0, znt_official)

print "\n2. CIVIL TWILIGHT"
suncalc(2014, month, day, "SUNRISE", 48.142, 17.099, 1.0, znt_civil)

print "\n3. NAUTICAL TWILIGHT"
suncalc(2014, month, day, "SUNRISE", 48.142, 17.099, 1.0, znt_nautical)

print "\n4. ASTRONOMICAL TWILIGHT"
suncalc(2014, month, day, "SUNRISE", 48.142, 17.099, 1.0, znt_astronomical)

