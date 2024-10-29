from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Clientes(BaseModel):
    id: Optional[int] = 0
    nome: str
    data: str
    tipo: str
    atendido: bool = False


db_clientes = [
    Clientes(id = 1, nome= "Marcelo", data = "11/03/2024", tipo="P", atendido = False),
    Clientes(id = 2, nome= "João", data = "12/03/2024", tipo="P", atendido = False),
    Clientes(id = 3, nome= "Maria", data = "12/03/2024", tipo="N", atendido = False),
    Clientes(id = 4, nome= "Igor", data = "13/03/2024", tipo="N", atendido = False),
]

@app.get("/")
def root():
    return {"Mensagem": "Bem vindo!!"}    


@app.get("/fila", status_code=status.HTTP_200_OK)
def fila():
    if len(db_clientes) == 0:
        return {"Não tem clientes na fila"}
    else:
        return {"Clientes": db_clientes}


@app.get("/fila/{id}")
def dados_cliente(id: int):
    busca = [clientes for clientes in db_clientes if clientes.id==id]
    if busca:
        return {"Cliente": busca}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não existe")


controle = False
@app.post("/fila")
def novo_cliente(clientes: Clientes):
    global controle
    clientes.id = db_clientes[-1].id + 1
    if len(clientes.nome) <= 20:
        if len(clientes.tipo) == 1:
            if clientes.tipo == "P" and (len(db_clientes) < 2 or db_clientes[len(db_clientes)-1].tipo != "P" and controle == False):
                db_clientes.insert(len(db_clientes) - 1, clientes)
                controle = True
            else:
                db_clientes.append(clientes)
                controle = False
        else:
            return {"Mensagem": "Aceito um digito apenas"}
    else:
        return {"Mensagem": "Nome não aceito"}  
    for index, cliente in enumerate(db_clientes, start=1):
        cliente.id = index  
    return {"Mensagem": "Novo cliente entrou na fila!"}
    

@app.put("/fila/{id}")
def atualizar_cliente(id: int):
    for clientes in db_clientes:
        if clientes.id > 0:
            clientes.id -= 1
            if clientes.id == 0:
                clientes.atendido = True 
    for index, cliente in enumerate([cliente for cliente in db_clientes if not cliente.atendido], start=1):
        cliente.id = index
    return {"Mensagem": "Cliente Atendido!"}    
         
@app.delete("/fila/{id}")
def deletar_cliente(id: int):
    clientes = [clientes for clientes in db_clientes if clientes.id == id]
    if not clientes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não existe")
    db_clientes.remove(clientes[0])
    for index, cliente in enumerate([cliente for cliente in db_clientes if not cliente.atendido], start=1):
        cliente.id = index
    return {"Mensagem": "Cliente removido!"}