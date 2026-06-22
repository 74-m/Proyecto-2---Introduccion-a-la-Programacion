import os
import json as js
def guardar(nombre,rol):
    archivo='ranking.json'
    if os.path.exists(archivo):
        with open(archivo,'r') as f:
            ranking=js.load(f)
    else:
        ranking={}
    if nombre in ranking:
        ranking[nombre]+=1
    else:
        ranking[nombre]=1
    with open(archivo,'w') as f:
        js.dump(ranking,f)
    archivo=f"cuentas/{nombre}.json"
    with open(archivo,"r",encoding='utf-8') as file:
            datos= js.load(file)
    if rol == 0:
            datos["winsDefensor"] += 1
    elif rol == 1:
            datos["winsAtacante"] += 1
            
    with open(archivo, "w", encoding='utf-8') as file:
        js.dump(datos, file, indent=4,ensure_ascii=False)
    