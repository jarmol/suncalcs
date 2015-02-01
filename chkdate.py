import sys
def validate(args):
    if (len(args) == 1):
        print "\n*** Usage:\t python varidatesun.py year month day\t ***\n"
        er = 3
        return er

    try:
        if int(args[1]) in range(1900, 2101):
            year = int(args[1])
        else:
            print ("Year %s not in range 1900 ... 2100" % args[1])
            er = 1
            return er

    except ValueError:
        print ("Not an integer %s "% args[1])
        er = 2
        return er

    try:
        if int(args[2]) in range(1, 13):
            month = int(args[2])
        else:
            print ("Month %s not in range 1 ... 12" % args[2])
            er = 1
            return er

    except ValueError:
        print ("Not an integer %s "% args[2])
        er = 2
        return er

    try:
        if int(args[3]) in range(1, 32):
            day = int(args[3])
#            print ("Date %s.%s.%s" % (day, month, year)) 
        else:
            print ("Day %s is not in the range 1 ... 31" % args[3])
            er = 1
            return er

    except ValueError:
        print ("Not an integer %s "% args[3])
        er = 2
        return er

    er = 0
    year =  int(args[1])
    month = int(args[2])
    day =   int(args[3])

# Succesfull
    return year, month, day
