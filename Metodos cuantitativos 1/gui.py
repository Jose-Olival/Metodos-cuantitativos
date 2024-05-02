import tkinter
import asyncio
import random
import time
import tkinter.messagebox

tasks = []
waitTime = []
promedio = 0
atendidos = 0
cola = 0
queueCount = 0

async def servidores(queue, service):
    while True:
        entrada = await queue.get()
        await asyncio.sleep(service)
        queue.task_done()
        atendidos+= 1
        cola -= 1
        waitTime.append(time.monotonic() - entrada)


async def source(queue, arrival):
    global cola 
    while True:
        await asyncio.sleep(arrival)
        queue.put_nowait(time.monotonic())
        cola += 1


async def supervisor():
    global promedio
    while True:
        if(len(waitTime) > 0):
            sumatoria = 0
            for i in range(len(waitTime)):
                sumatoria += waitTime[i]
            
            promedio = (sumatoria/len(atendidos)) 
        await asyncio.sleep(1)

def stop():
    for task in tasks:
        task.cancel()

async def sim(cantidadServidores, arrival, service): 
    queue = asyncio.Queue()
    tasks.append(asyncio.create_task(source(queue, arrival)))
    tasks.append(asyncio.create_task(supervisor()))
    for i in range(cantidadServidores):
        tasks.append(asyncio.create_task(servidores(queue, service)))

    await asyncio.gather(*tasks, return_exceptions=True)

def comprobar(inp):
    print(inp)
    try:
        numero  =  float(inp)
        return numero
    except  ValueError:
        return random.uniform(0.1,3)
        

def play():
    global ICantidad
    global IArrival
    global IService
    
    inpCantidad = ICantidad.get("1.0",'end-1c')
    inpCantidad = int(inpCantidad)

    inpArrival = IArrival.get("1.0",'end-1c')
    inpArrival = comprobar(inpArrival)

    inpService = IService.get("1.0",'end-1c')
    inpService = comprobar(inpService)

    asyncio.run(sim(inpCantidad,inpArrival,inpService)) 

frame = tkinter.Tk()
frame.geometry("800x495")
frame.configure(bg='#CAF2D7')

blank = tkinter.PhotoImage()

#Labels
x1 = 100
x2 = 450
y1 = 150
y2 = 250
y3 = 350

lTitulo = tkinter.Label(frame,text= "Simulador de cola")
lTitulo.place(x=250, y=50)

lCantidad = tkinter.Label(frame,text= "Cantidad de servidores")
lCantidad.place(x=x1, y=y1)

lArrival = tkinter.Label(frame,text= "Tasa de llegada")
lArrival.place(x=x1, y=y2)

lService = tkinter.Label(frame,text= "Tasa de servicio")
lService.place(x=x1, y=y3)

lPromedio = tkinter.Label(frame,text= "Promedio de tiempo en el sistema")
lPromedio.place(x=x2, y=y1)

lAtendidos = tkinter.Label(frame,text= "Cantidad de atentidos")
lAtendidos.place(x=x2, y=y2)

lQueue = tkinter.Label(frame,text= "Cantidad de objetos en la cola")
lQueue.place(x=x2, y=y3)

labels = [lTitulo,lCantidad,lArrival,lService,lPromedio,lAtendidos,lQueue]
for i in range(len(labels)):
    labels[i].configure(fg='#60A9A6',bg='#CAF2D7',font=("Agency FB",16,"bold")) 
    if(i == 0):
        labels[i].configure(font=("Agency FB",32,"bold"))

lShowAverage = tkinter.Label(frame,text= "",textvariable=promedio)
lShowAverage.place(x=(x2 + 250), y=(y1+7))

lShowAtendidos = tkinter.Label(frame,text= "",textvariable=atendidos)
lShowAtendidos.place(x=(x2 + 250), y=(y2+7))

lShowQueueu = tkinter.Label(frame,text= "",textvariable=queueCount)
lShowQueueu.place(x=(x2 + 250), y=(y3+7))

labelsShow = [lShowAverage,lShowAtendidos,lShowQueueu]
for i in range(len(labelsShow)):
    labelsShow[i].configure(fg='#EFFBF3',bg='#60A9A6',font=("Agency FB",16,"bold"), image=blank, width=45,height=20) 


# Text inputs
ICantidad = tkinter.Text(frame,height = 1, width = 6)
ICantidad.place(x=270,y=(y1+7))

IArrival = tkinter.Text(frame,height = 1, width = 6)
IArrival.place(x=270,y=(y2+7))

IService = tkinter.Text(frame,height = 1, width = 6)
IService.place(x=270,y=(y3+7))


# Boton
bPlay = tkinter.Button(text="Calcular",fg='#EFFBF3',bg='#60A9A6',font=("Agency FB",20,"bold"),command=play)
bPlay.place(x=350, y=400)

frame.mainloop()