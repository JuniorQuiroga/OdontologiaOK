dics={
    "0900":"0",
    "0930":"0",
    "1000":"0",
    "1030":"0",
    "1100":"0",
    "1130":"0",
    "1200":"0",
}

ocupados=["1030","1100"]

for turno in ocupados:
    dics.pop(turno)

for d in dics.keys():
    print(d)