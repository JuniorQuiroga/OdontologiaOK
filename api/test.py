"""
from http import cookies

C = cookies.SimpleCookie()
C["local"] = "false"
C["unique_token"] = "1231244wefgwefwev"

print(C) # generate HTTP headers
print(cookies.Morsel.coded_value()) # generate HTTP headers
"""


#codigo[1] = codigo[1].split(":")
"""
if len(codigo[1].split(":")[0]) == 2:
    if len(codigo[1].split(":")[1]) == 2:
        codigo1 = codigo
    else:
        codigo1 = codigo[1].split(":")[0]+":0"+codigo[1].split(":")[1]
else:
    if len(codigo[1].split(":")[1]) == 2:
        codigo1 = "0"+codigo[1].split(":")[0]+":"+codigo[1].split(":")[1]
    else:
        codigo1 = "0"+codigo[1].split(":")[0]+":0"+codigo[1].split(":")[1]
print("codigo 1 "+codigo1)
"""

codigo = "4-10-2021;09:30"

codigo = codigo.split(";")
codigo[0] = codigo[0].split("-")
codigo[0] = codigo[0][2]+"-"+codigo[0][1]+"-"+codigo[0][0]

if len(str(codigo[1].split(":")[0]))==1:
    if codigo[1].split(":")[1] == "0":
        codigo = "{0} 0{1}:0{2}".format(codigo[0],codigo[1].split(":")[0],codigo[1].split(":")[1])
    else:
        codigo = "{0} 0{1}:{2}".format(codigo[0],codigo[1].split(":")[0],codigo[1].split(":")[1])
else:
    if codigo[1].split(":")[1] == "0":
        codigo = "{0} {1}:0{2}".format(codigo[0],codigo[1].split(":")[0],codigo[1].split(":")[1])
    else:
        codigo = "{0} {1}".format(codigo[0],codigo[1])

print(codigo)