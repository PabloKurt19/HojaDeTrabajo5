# Universidad del Valle de Guatemala
# Algoritmos y Estructura de datos
# Pablo Ortiz 15533
# Andrea Maybell
# Hoja de trabajo 5
# El codigo simula los procesos realizados por el procesador. Esta basado en los codigos de ejmplo de calse



import simpy
import random


def proceso(simpyEnv, tiempoProceso, name, ram, cantidadMem, cantidadInstrucciones, velpros):
    global tiempoTotal
    global tmps
    
    #Tiempo de proceso (new)
    yield simpyEnv.timeout(tiempoProceso)
    print('tiempo: %f - %s (new) solicita %d de memoria ram' % (simpyEnv.now, name, cantidadMem))
    tiempollegada = simpyEnv.now 
    
    #ram a utilizar (admited - ready)
    yield ram.get(cantidadMem)
    print('tiempo: %f - %s (admited) solicitud aceptada por %d de memoria ram' % (simpyEnv.now, name, cantidadMem))

    #Instrucciones completadas
    completed = 0
    
    while completed < cantidadInstrucciones:

    
        #Cpu connection (ready)
        with cpu.request() as req:
            yield req
            #instruccionss a realizarse
            if (cantidadInstrucciones-completed)>=velpros:
                realizar=velpros
            else:
                realizar=(cantidadInstrucciones-completed)

            print('tiempo: %f - %s (ready) cpu ejecutara %d instrucciones' % (simpyEnv.now, name, realizar))
            #tiempo de instrucciones a ejecutar
            yield simpyEnv.timeout(realizar/velpros)

            #instrucciones completadas
            completed += realizar
            print('tiempo: %f - %s (runing) cpu (%d/%d) completado' % (simpyEnv.now, name, completed, cantidadInstrucciones))

        #1 espera en cola 2 ready
        atender = random.randint(1,2)

        if atender == 1 and completed<cantidadInstrucciones:
         
            with waiting.request() as req2:
                yield req2
                #tiempo de operaciones de entrada y salida
                yield simpyEnv.timeout(1)                
                print('tiempo: %f - %s (waiting) realizadas operaciones (entrada/salida)' % (simpyEnv.now, name))
    

    #(exit - terminated)
    #cantidad de ram que devuelve
    yield ram.put(cantidadMem)
    print('tiempo: %f - %s (terminated), retorna %d de memoria ram' % (simpyEnv.now, name, cantidadMem))
    tiempoTotal += (simpyEnv.now -tiempollegada) #tiempo de todos los procesos
    tmpos.append(simpyEnv.now - tiempollegada) 
#Variables
velpros = 3.0 # instrucciones por tiempo
memoria_ram= 100 #cantidad de ram
cant_procesos = 25 #procesos a ejecutar
tiempoTotal=0.0 #inicializa la variable que almacenara el tiempo total de los procesos
tmpos=[] #se guardara cada tiempo individual para extraer la desviacion estandar


simpyEnv = simpy.Environment()  #ambiente simpy
cpu = simpy.Resource (simpyEnv, capacity=2) #acceso a cpu (cola)
ram = simpy.Container(simpyEnv, init=memoria_ram, capacity=memoria_ram) #ssimulador de ram
waiting = simpy.Resource (simpyEnv, capacity=2) #acceso a operaciones entrada/salida (cola9

#Semilla de random 
random.seed(1904)
rank = 1 # numero de intervalos a ejecutar


# procesos que se simularán
for inicial in range(cant_procesos):
    tiempoProceso = random.expovariate(1.0 / rank)
    cantidadInstrucciones = random.randint(1,10) #Canitdad de instrucciones
    cantidadMem = random.randint(1,10) #memoria ram a utilizar 
    simpyEnv.process(proceso(simpyEnv, tiempoProceso, 'Proceso %d' % inicial, ram, cantidadMem, cantidadInstrucciones, velpros))

#Simulation starts here!
simpyEnv.run()

#promedio de accessos 
print " "
promedio=(tiempoTotal/cant_procesos)
print('El tiempo promeido es: %f' % (promedio))


#Desvest
suma=0

for xinicial in tmpos:
    suma+=(xinicial-promedio)**2

desvest=(suma/(cant_procesos-1))**0.5

print " "
print('La desviacion estandar es: %f' %(desvest))