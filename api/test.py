from http import cookies

C = cookies.SimpleCookie()
C["local"] = "false"
C["unique_token"] = "1231244wefgwefwev"

print(C) # generate HTTP headers
print(cookies.Morsel.coded_value()) # generate HTTP headers