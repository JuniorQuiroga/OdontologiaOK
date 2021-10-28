dics={
    "09:00:00":"0",
    "09:30:00":"0",
    "10:00:00":"0",
    "10:30:00":"0",
    "11:00:00":"0",
    "11:30:00":"0",
    "12:00:00":"0",
    "12:30:00":"0",
    "13:00:00":"0",
    "13:30:00":"0",
    "14:00:00":"0",
    "14:30:00":"0",
    "15:00:00":"0",
    "15:30:00":"0",
    "16:00:00":"0",
    "16:30:00":"0",
    "17:00:00":"0",
    "17:30:00":"0",
    "18:00:00":"0",
}

ocupados=["10:30:00","11:00:00"] #lo que nos devuelve la consulta

horasO=[]

tupla= (("10:30:00"),("11:00:00")) 

for fila in tupla:
    horasO.append(fila)

for turno in horasO:
    dics.pop(turno)

for d in dics.keys():
    print(d)









"""
# lo que tira la BD
tupla=((10,30),(11,00))
horarios = []


for fila in tupla:
    horarios.append({str(fila[0])+str(fila[1])})

for i in horarios[1]:
    dics.pop(i)
    print(i)


for turno in ocupados:
    dics.pop(turno)

for d in dics.keys():
    print(d)"""