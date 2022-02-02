#include <stdio.h>
#include <math.h>

// Setup
// Location Tornio
double latitude = 65.85;
double longitude = 24.18;

int testOpt = 0;

// Date
float TZ  = 2.0; // timezone hours
int qday, qmonth; // you enter
int day = 2;
int month = 2;
int year = 2022;

// Calculate the day of the year
// Convert floats to integer
int toInt(n){
      return n;
}

int dayNr(y, m, d) 
        {
          int N1 = 275*m/9;
          int N2 = (month + 9)/12;
          int N3 = 1 + toInt((y - 4 * toInt(y/4) + 2)/3);
          int dayNr  = N1 - (N2*N3) + d - 30;
          return dayNr;
        }

// 2. convert the longitude to hour value and calculate
// an approximate time
// convert integer to float
double toFloat(r) {return r;}


double tLongRise(double longit, int N) {
        double lngHour =  longit / 15.0 ;
        double t = toFloat(N) + (6.0 - lngHour) / 24.0;
        return t;
       }


// Calculate the Sun's mean anomaly for Sunrise and Sunset
double meanAnomaly(double rstime) {
        double mA = (0.9856*rstime) - 3.289;
        return mA;
     }

// Calculate Sun's true longitude in degrees
double trueLong(double rstime) { 
        double M = meanAnomaly(rstime);
        double pi = acos(-1.0);
        double toRad = pi/180.0;
        double tL = M+(1.916*sin(M*toRad))+(0.020*sin(2*M*toRad))+282.634;
        // printf("π = %f \n",pi);
        double tLN = tL;
        if (tL > 360.0) tLN = tL - 360.0; 
        return tLN;
}

// calculate the Sun's right ascension
// RA = atan(0.91764 * tan(L) in degrees
double calcRA(double L) {
    double tL =trueLong(L);
    double pi = acos(-1.0);
    double toRad = pi/180.0;
    if (testOpt) {
        printf("true Long  = %f\n", tL);
        printf("L = %f\n", L);
    }
    double RA = atan(0.91764 * tan(tL*toRad))/toRad;
    return RA;
}

// RA and L must be in the same quadrant
// Lquadrant  = (int( L/90)) * 90
// Raquadrant = (int(RA/90)) * 90
// RA = RA + (Lquadrant – RAquadrant) / Sunrise or Sunset

double correctQuadr(double L, double RA) {
    double Lquadrant  = floor(L/90)*90;
    double RAquadrant = floor(RA/90)*90;
    double cRA = RA + (Lquadrant - RAquadrant);

    if (testOpt) {
        printf("Check L %f and RA %f\n", L, RA);
        printf("Check Lquadr %f and %f Raquadr\n", Lquadrant, RAquadrant);
        printf("Right quadr. RA = %f\n", cRA); // sunrise 305.1277
    }
    return cRA; 
}


// Calculate the Sun's local hour angle
double calcCosH(double zenith, double timeLX, double latitude) {
       double pi = acos(-1.0);
       double toRad = pi/180.0;
       double  sinDecSX = 0.39782 * sin(toRad*trueLong(timeLX));
       double  cosDecSX = cos(asin(sinDecSX));
       double  cosH=(cos(toRad*zenith)-(sinDecSX*sin(toRad*latitude)))/(cosDecSX*cos(toRad*latitude)); //  Sunrise
       return cosH;
}

// Azimuth, Sunrise 180 - z or Sunset 180 +z
//          sin(Az) = sin(HourAngle)*cos(delta)/cos(altit)
//          z = asin(sin(Az)
//          (180 – z) = Az
//
       double azimuthRS(double hourAngle, double decl, double altit) {
            double toRad = acos(-1)/180;
            double sinAz = sin(hourAngle*toRad)*cos(decl*toRad)/cos(altit*toRad);
            double z = asin(sinAz)/toRad;
            return z;
       }      


double utToLocal(double ut, double tz) {
    double locT = ut + tz;
    if (locT < 0.0) locT += 24;
    return locT; 
}

// Convert decimal hours to hr, mn, sc
    void toHrMnSc(double hours) {
    int totSeconds = round(3600*hours);
    int hr = floor(hours);
    int mn = floor((totSeconds - 3600*hr)/60);
    int sc = (totSeconds - 3600*hr - 60*mn);
    printf("%d:%d:%d\n", hr, mn, sc);
}

// Approximated noon time
    void approxNoon(double riseT, double setT) {
    toHrMnSc(0.5*(riseT + setT));
}

// Max altitude at noon
double maxAltit(double declin, double latit) {
    return 90 + declin - latit ;
}

int main(void) {
      int rowNr;
      int rmax = 3;
      const char* sarots[3] = {"  Lat. ", "  Long.", " TZ"};
      const char* nimet[4] = {"Helsinki", "Tukholma", "Berliini", "Wien"};
      float taulukko[4][4] = { { 60.17, 24.95, 2.0 }, { 59.33, 18.07, 1.0 },
            { 52.52, 13.38, 1.0}, {48.22, 16.37, 1.0} };

      printf("  %9s", " Location");

      for (int j = 0; j < 3; ++j) {
         printf("%10s ", sarots[j]);
      }; putchar('\n');

      for (int i = 0; i < 4; ++i) {
         printf("%d) %8s ", i, nimet[i]);
         for (int j = 0; j < 3; ++j) {
            printf(" %8.2f   ", taulukko[i][j]);
         };
         putchar('\n');
      };

      printf("Select location by the row number: ");
      scanf("%d", &rowNr);
      // Check row number to be in range 0 ... rmax
      if (rowNr >= 0) if (rowNr <= rmax) {
         printf("row %d selected, city %s\n", rowNr, nimet[rowNr]);
         latitude = taulukko[rowNr][0];
         longitude = taulukko[rowNr][1];
         TZ = taulukko[rowNr][2];
         printf("   Latitude  %.2f\n", latitude);
         printf("   Longitude %.2f\n", longitude);
         printf("   Timezone  %.1f\n", TZ);
      }

      printf("default date %d-%d-%d\n",year, month, day);
      printf("Enter month (%d): ", month);
      scanf("%d", &qmonth);
      if (qmonth > 0) month = qmonth;
      printf("You entered month %d\n", month);
      printf("Enter day (%d): ", day);
      scanf("%d", &qday);
      if (qday > 0) day = qday;
      printf("You entered day %d\n", day);

      //printf("You entered day %d\n", day);

      int    dnr = dayNr(year, month, day); // 168
      double timeLR = tLongRise(longitude, dnr); // 168.1808
      double timeLS = timeLR + 0.5;              // 168.6808 12 h later
      double corRASunrise = correctQuadr(trueLong(timeLR), calcRA(timeLR));
      double corRASunset = correctQuadr(trueLong(timeLS), calcRA(timeLS));
      double hrSunriseRA = corRASunrise/15;
      double hrSunsetRA  = corRASunset/15;
      double pi = acos(-1);
      double toRad = pi/180.0;
      double zenith = 90.8333; // Sunrise and Sunset angles

      // Calculate the Sun's declination
      double sinDecSR = 0.39782 * sin(toRad*trueLong(timeLR));    // Sunrise
      double cosDecSR = cos(asin(sinDecSR));
      double sinDecSS = 0.39782 * sin(toRad*trueLong(timeLS));    // Sunset
      double cosDecSS = cos(asin(sinDecSS));
      double sinDecAverage = 0.5*(sinDecSR + sinDecSS);
      double declSunrise = asin(sinDecSR)/toRad;
      double declSunset  = asin(sinDecSS)/toRad;
      double declAverage = asin(sinDecAverage)/toRad;

     // Hour angle
      double cosLRH = calcCosH(zenith, timeLR, latitude);
      double cosLSH = calcCosH(zenith, timeLS, latitude);

      // Calculate H and convert into hours 
      // if rising time is desired:
      double riseH = 360 - acos(cosLRH)/toRad;
      double riseHhour = riseH/15;
      double setH  = acos(cosLSH)/toRad;
      double setHhour = setH/15;
      double riseAzim = azimuthRS(riseH, declSunrise, -0.8333);
      double setAzim  = azimuthRS(setH,  declSunset,  -0.8333);
     // Calculate local mean time of rising/setting
      double riseT = riseHhour + hrSunriseRA - (0.06571 * timeLR) - 6.622; // Sunrise
      double setT  = setHhour  + hrSunsetRA  - (0.06571 * timeLS) - 6.622; // Sunset
      if (riseT > 24.0) riseT -= 24.0;
     // Adjust back to UTC
      double lngHour = longitude/15;
      double riseUT = riseT - lngHour; //  Sunrise UT
      double setUT  = setT  - lngHour; //  Sunset UT

      double locRiseT = utToLocal(riseUT, TZ);
      double locSetT  = utToLocal(setUT,  TZ);
      // int dnr = dayNr(year, month, day);
      printf("Date %d-%d-%d\n", year, month, day);
      
      if (testOpt) {
        printf("Longitude converted to time %8.4f Sunrise ca  6:00\n", timeLR);
        printf("Longitude converted to time %8.4f Sunset  ca 18:00\n",  timeLS);
        printf("MeanAnomaly %f at rising time\n",     meanAnomaly(timeLR)); 
        printf("MeanAnomaly %f at setting time\n",    meanAnomaly(timeLS));
        printf("True longitude %7.3f rising time\n",  trueLong(timeLR));
        printf("True longitude %7.3f setting time\n", trueLong(timeLS));
        printf("Rectascension   RA = %f Sunrise\n",   calcRA(timeLR));
        printf("Right Quadrants RA = %f Sunrise\n",   corRASunrise);
        printf("Rectascension RA = %f Sunset\n",      calcRA(timeLS));
        printf("Right Quadrants RA = %f Sunset\n",    corRASunset);
        printf("Sunrise RA hours %6.4f, Sunset RA hours %6.4f\n", hrSunriseRA, hrSunsetRA);
        printf("sin(declin) Sunrise %7.4f \n", sinDecSR);
        printf("sin(declin) Sunrise %7.4f \n", sinDecAverage);
        printf("Sun declination average %7.4f \n", declAverage);
        printf("Sun declination Sunrise %7.4f \n", declSunrise);
        printf("Sun declination Sunset  %7.4f \n", declSunset);
      }


    if (testOpt) {
        printf("Sunrise cosH = %f, H = %f = %8.4f h\n", cosLRH, riseH, riseHhour);
        printf("Sunset  cosH = %f, H = %f = %8.4f h\n", cosLSH, setH,  setHhour);
        printf("Local meantime of rising %f\n", riseT);
        printf("Local meantime of set %f\n", setT);
        printf("Rise UTC %f\n", riseUT);
        printf("Set  UTC %f\n", setUT);
        printf("Local rise time %f, set time %f\n", locRiseT, locSetT);
    }

        printf("Rise time   "); toHrMnSc(locRiseT);
        printf("Rise azimuth %7.2f°\n", riseAzim + 180);
        printf("Set  time   "); toHrMnSc(locSetT);
        printf("Set  azimuth %7.2f°\n",  setAzim + 180);
        printf("Day length  "); toHrMnSc(locSetT - locRiseT);
        printf("Approximated noon time: "); approxNoon(locRiseT, locSetT);
        printf("Max altitude %5.2f° at noon\n", maxAltit(declAverage, latitude));

        if (cosLRH > 1)  printf("The Sun never rises here on the specified date.\n");
        if (cosLSH < -1) printf("The Sun never sets here on the specified date.\n");
      return 0;
	}

// c.f. Helsinki_June.ods
