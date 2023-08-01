#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author:  peter --<pjl@hpc.com.py>
# Purpose: Insert users info from a xls file
# Created: 22/12/11


# this is the module that help me with the xls file
#http://pypi.python.org/pypi/xlrd
import xlrd
import codecs
import re

coma = re.compile(",")
enie = re.compile("ñ")

#----------------------------------------------------------------------
def InsertFromods(filename):
    """make a ldap entry from a ods file"""
    wb = xlrd.open_workbook(filename)
   
    sh = wb.sheet_by_index(0)

    #for every entry we make a ldif
    filen = codecs.open("LdapImportPt3.ldif", "a+", "utf-8")
    #the last uidNumber attribute in the ldap directory
    val = 100
   
    for rownum in range(sh.nrows):
        row = sh.row_values(rownum)
        value = sh.row_values(rownum)[1].lower()
       
        value = value.replace(u"ñ", u"n")       
        #try to organizate the second column values
        if  coma.search(value):
            ape = value.split(",")[0].strip()
            nom = value.split(",")[-1].strip()
        else:
            ape = value.split()[0].strip()
            nom = value.split()[-1].strip()
          
        #pass
        val = val + 1
        filen.write("dn: inum= %s,ou=people,o=gluu\n" % round(row[0]))
        filen.write("objectClass: eduPerson\n")
        filen.write("objectClass: gluuCustomPerson\n")
        filen.write("objectClass: gluuPerson\n")
        filen.write("objectClass: top\n")
        filen.write("cn: %s\n" % row[1])
        filen.write("displayName: %s\n" % row[1])
        filen.write("employeeType: false \n")
        filen.write("gluuStatus: active \n")
        filen.write("inum: %s\n" % round(row[0]))
        filen.write("mail: %s\n" % row[2])
        #filen.write("oxTrustEmail: {'value':'%s','display':null,'type':null,'primary':false} \n" % row[2])
        #filen.write("value : %s }\n" % row[2])
        #filen.write("oxCreationTimestamp: 0210930025400.901Z\n")
        filen.write('oxTrustEmail: {"value":"%s","display":null,"type":null,"primary:"false}\n' % row[2])
        #filen.write("updatedAt: 20210930025400.901Z\n")
        filen.write("uid: %s\n" % round(row[0]))
        #filen.write("uid: %s%s\n" % (nom, ape))                       
        #filen.write("uidNumber: %s\n"  % str(val))
        #filen.write("gidNumber: %s\n"  % str(val))
        #filen.write("homeDirectory: /homedirs/%s%s\n" % (nom, ape))
        filen.write("\n")
        filen.write("\n")           
    filen.close()
   
#----------------------------------------------------------------------

if __name__=='__main__':
    InsertFromods('LdapImportPt3.xls')