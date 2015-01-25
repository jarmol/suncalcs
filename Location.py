import datetime, time, math
from time import gmtime, strftime
from datetime import date

znt_official = 90.833

rad  = lambda x: math.pi*x/180.0
cosd = lambda x: math.cos(rad(x))
sind = lambda x: math.sin(rad(x))
tand = lambda x: math.tan(rad(x))
degr = lambda x: 180.0*x/math.pi

def chif(cval, yval, nval):
    if (cval):
        rval = yval
    else:
        rval = nval

    return rval

class Location(object):

# Geographic locations

    def __init__(self, city, latitude, longitude, timezone): 
        self.Cityname = city 
        self.Latitude = latitude 
        self.Longitude = longitude
        self.Timezone = timezone

    def getname(self): 
        return self.Cityname

    def getlatitude(self): 
        return self.Latitude

    def getlongitude(self): 
        return self.Longitude

    def gettimezone(self):
        return self.Timezone

    def printrecord(self):
        cityx = self.Cityname
        latx  = self.Latitude
        lonx  = self.Longitude
        tzx   = self.Timezone

        suflat = chif(latx < 0.0, 'S', 'N')
        suflon = chif(lonx < 0.0, 'W', 'E')
        pretz  = chif(tzx  < 0.0, '', '+')
        print("%s latitude %s %s longitude %s %s timezone UTC%s%d\n" % (cityx, abs(latx), suflat, abs(lonx), suflon, pretz, tzx))            

class Dates(object):

    def __init__(self, year, month, day):
        self.Year = year
        self.Month = month
        self.Day = day
 

    def yday(self):
        N1 = math.floor(275*self.Month/9)
        N2 = math.floor((self.Month + 9)/12)
        N3 = (1 + math.floor((self.Year - 4*math.floor(self.Year/4) + 2)/3))
        ydN = N1 - (N2 * N3) + self.Day - 30
        return ydN

    def printdate(self):
        print("%d.%d.%d\n" % (self.Day, self.Month, self.Year))

    def printtime(self):
        print "Test within Dates object", human(16.075)

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
# Not embedded to any object
    h=decimhours        # floating hours
    s = 3600*h          # seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

class Solar(object):

# Solar calculations

    def __init__(self, daynr=0, latitude=0.0, longitude=0.0, whichway="SUNRISE", zenith=znt_official):
        self.Daynr = daynr
        self.Latitude = latitude
        self.Longitude = longitude
        self.Whichway  = whichway
        self.Zenith    = zenith
        self.Declination = 0.0

    def getsolar(self):
        print("%s at daynr %d for zenith %.2f\n" % (self.Whichway, self.Daynr, self.Zenith))

    def suncalc(self):
#  2. convert the longitude to hour value and calculate an approximate time
        lngHour = self.Longitude/15.0 

        if (self.Whichway == "SUNRISE"):
            t = self.Daynr + (6.0 - lngHour)/24.0
        else:
            t = self.Daynr + (18.0 - lngHour)/24.0

#  3. calculate the Sun's mean anomaly
        M = 0.9856*t - 3.289

#  4. calculate the Sun's true longitude
        L = M + (1.916*sind(M)) + 0.020*sind(2*M) + 282.634

#  NOTE: L potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
 
        if (L > 360.0):
            L-= 360.0
        elif (L < -360.0):
            L+= 360.0 

#  5a. calculate the Sun's right ascension
        RA = math.atan(0.91764*tand(L))
        RA = degr(RA)

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
        if (RA > 360.0):
            RA-= 360.0
        elif (RA < -360.0):
            RA+= 360.0

#  5b. right ascension value needs to be in the same quadrant as L
        Lquadrant  = (math.floor(L/90.0))*90.0
        RAquadrant = (math.floor(RA/90.0))*90.0
        RA = RA + (Lquadrant - RAquadrant)

# 5c. right ascension degrees needs to be converted into hours
        RA = RA/15.0

# 6. calculate the Sun's declination
        sinDec = 0.39782*sind(L)
        cosDec = math.cos(math.asin(sinDec))
        declin = degr(math.atan(sinDec/cosDec))
        self.Declination = declin     # Save declination
