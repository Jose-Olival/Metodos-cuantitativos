import asyncio
import random
import time

atendidos = 0
waitTime = []
tasks = []

async def servidores(id, queue, service):
    while True:
        entrada = await queue.get()
        await asyncio.sleep(service)
        queue.task_done()
        global atendidos
        atendidos += 1
        waitTime.append(time.monotonic() - entrada)
        print(f'El servidor {id} atendio a alguien')


async def source(queue, arrival):
    while True:
        await asyncio.sleep(arrival)
        queue.put_nowait(time.monotonic())
        print(f'Un objeto entro a la cola')


async def supervisor():
    while True:
        await asyncio.sleep(5)
        c = input("Imprimir informacion (s/n) ")
        if (c == "s"):
            print(f'\n\nTotal de atendidos por los servidores {atendidos}')

            if(len(waitTime) > 0):
                sumatoria = 0
                for i in range(len(waitTime)):
                    sumatoria += waitTime[i]
                
                promedio = sumatoria/len(waitTime)
                print(f'\nEl promedio de tiempo en el sistema es de {promedio}')

async def sim(cantidadServidores, arrival, service):  
    queue = asyncio.Queue()
    
    tasks.append(asyncio.create_task(source(queue, arrival)))
    tasks.append(asyncio.create_task(supervisor()))
    for i in range(cantidadServidores):
        tasks.append(asyncio.create_task(servidores(f'Servidores {i}', queue, service)))

    await asyncio.gather(*tasks, return_exceptions=True)

cantidad = int(input("¿Cuantos servidores tendra el sistema?: "))
c = input("¿Desea configurar la tasa de llegada?: (s/n)")
if(c == "s"):
    arrival = input("Introduce la tasa de llegada: ")
else:
    arrival = random.uniform(0.1,3)
c = input("¿Desea configurar la tasa de entrada?: (s/n)")
if(c == "s"):
    service = input("Introduce la tasa de entrada: ")
else:
    service = random.uniform(0.1,3)

asyncio.run(sim(cantidad,arrival,service)) 