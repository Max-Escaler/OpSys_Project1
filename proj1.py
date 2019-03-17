import sys
import math

seed = int(sys.argv[1])
lmda = float(sys.argv[2])
upperBound = int(sys.argv[3])
numProcesses = int(sys.argv[4])
tcs = sys.argv[5]
alpha = sys.argv[6]
timeSlice = sys.argv[7]

def printQueue(queue):
	new = []
	newQueue = "[Q"
	for x in queue:
		new.append(x.ID)
	for x in new:
		newQueue += " " + x
	if(len(queue) == 0):
		newQueue = newQueue + " <empty>"
	newQueue = newQueue+"]"
	print(newQueue)

class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    def lrand(self):
        return self.next() >> 17
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n 





class Process:
	ID =""
	arrivalTime = 0
	bursts = 0
	burstTimes = []
	IOTimes= []
	waitTime = 0
	turnAroundTime = 0
	runTime = 0.0
	blockedTime = 0
	def __init__(self,at, b,bt,iot,ID):
		self.arrivalTime = at
		self.bursts = b
		self.burstTimes = bt
		self.IOTimes = iot
		self.ID = chr(ID)
	def getID(self):
		return self.ID
	def getAT(self):
		return int(self.arrivalTime)

	def getCPUBursts(self):
		return self.burstTimes
	def getIOBursts(self):
		return self.IOTimes

	def getRunTime(self):
		return self.runTime
	def tick(self):
		self.runTime +=1
		self.turnAroundTime += 1
	def wait(self):
		self.waitTime += 1
		self.turnAroundTime += 1
	def block(self):
		self.blockedTime+=1
		self.waitTime+=1
		self.turnAroundTime+=1


def SRT(processes, preemptions,lmda,alpha,tcs):
	print("0 ms: Simulation started for SRT")
	processList = processes.copy()
	guess = int(1/lmda)
	readyQueue = []
	CPU = []
	blocked=[]
	time = 0
	#This program will execute as long as there are processes waiting to arrive, in the ready queue, or in the blocked queue
	while(len(processList) > 0 or len(readyQueue)>0 or len(blocked) > 0 or len(CPU) > 0):
		conSwitched = False
		# We check through all of the processes for an arrival on every tick of the sim
		for x in processList:
			## if we find one that is arriving, we add it in the correct place in the readyQueue
			if(time == x.getAT()):
				if(len(readyQueue) == 0):
					print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ") 
					readyQueue.append(x)
					printQueue(readyQueue)
					processList.remove(x)
					continue
				elif(len(readyQueue) == 1):
					if(  (guess - readyQueue[0].getRunTime())  > (guess - x.getRunTime())  ):
						print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms) arrived; added to the ready queue" , end = " ")
						readyQueue = [x] + readyQueue
						printQueue(readyQueue)
						processList.remove(x)
						continue
					else:
						if(readyQueue[0].getID() < x.getID()):
							print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ")
							readyQueue.append(x)
							printQueue(readyQueue)
							processList.remove(x)
							continue
						else:
							print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ")
							readyQueue = [x] + readyQueue
							printQueue(readyQueue)
							processList.remove(x)
							continue
				elif(len(readyQueue) > 1):
					if(  (guess - readyQueue[0].getRunTime())  > (guess - x.getRunTime())  ):
						print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ")
						readyQueue = [x] + readyQueue
						processList.remove(x)
						printQueue(readyQueue)

					else:
						for z in range(0,len(readyQueue)):
								if((guess - readyQueue[z].getRunTime())  < (guess - x.getRunTime()) and (guess - readyQueue[z+1].getRunTime())  > (guess - x.getRunTime())):
									print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ")
									readyQueue.insert(z,x)
									printQueue(readyQueue)
									processList.remove(x)
									break
								elif((guess - readyQueue[z].getRunTime())  == (guess - x.getRunTime())):
									if(readyQueue[z].getID() > x.getID()):
										print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ")
										readyQueue.insert(z-1,x)
										printQueue(readyQueue)
										processList.remove(x)
										break
									else:
										print("time", str(time) + "ms: Process", x.ID,"(tau", str(guess) +"ms)arrived; added to the ready queue" , end = " ")
										readyQueue.insert(z,x)
										printQueue(readyQueue)
										processList.remove(x)
										break


		if(len(CPU) == 0 and len(readyQueue) > 0 ):
			CPU.append(readyQueue[0])
			readyQueue.remove(readyQueue[0])
			for x in range(0,int(tcs/2)):
				CPU[0].tick()
				for y in readyQueue:
					y.wait()
				for y in blocked:
					y.block()
				time+=1
			print("time", str(time)+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			printQueue(readyQueue)


		
		time +=1
		if(len(CPU) ==1): 
			CPU[0].tick()
			for x in readyQueue:
				x.wait()
			for x in blocked:
				x.block()
		else:
			for x in readyQueue:
				x.wait()
			for x in blocked:
				x.block()

		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) >1):
			print("time", str(time)+"ms:",CPU[0].ID , "completed a CPU burst;",len(CPU[0].burstTimes)-1,"bursts to go", end = " ")
			printQueue(readyQueue)
			guess = float(alpha) * CPU[0].burstTimes[0] + (1-float(alpha))*guess
			guess = int(guess)
			print("time",str(time)+"ms: Recalculated tau =",str(guess)+"ms for process",CPU[0].ID, end = " ")
			printQueue(readyQueue)
			print("time", str(time)+"ms: Process",CPU[0].ID,"switching out of CPU; will block on I/O until time",time+CPU[0].IOTimes[0], end = " ")
			printQueue(readyQueue)
			CPU[0].runTime = 0
			blocked.append(CPU[0])
			CPU[0].burstTimes.pop(0)
			CPU.remove(CPU[0])

		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) ==1):
			print("time", str(time)+"ms:",CPU[0].ID , "terminated", end = " ")
			printQueue(readyQueue)
			CPU.pop(0)




		if(len(blocked) > 0):
			for x in blocked:
				if(x.blockedTime == x.IOTimes[0]):
					print("time", str(time)+"ms: Process",x.ID,"(tau",str(guess)+"ms) completed I/O; added to ready queue", end= " ")
					x.IOTimes.pop(0)
					x.blockedTime = 0

					if(len(readyQueue) == 0):
						readyQueue.append(x)
						printQueue(readyQueue)
						blocked.remove(x)
						continue
					elif(len(readyQueue) == 1):
						if(  (guess - readyQueue[0].getRunTime())  > (guess - x.getRunTime())  ):
							readyQueue = [x] + readyQueue
							printQueue(readyQueue)
							blocked.remove(x)
							continue
						else:
							if(readyQueue[0].getID() < x.getID()):
								readyQueue.append(x)
								printQueue(readyQueue)
								blocked.remove(x)
								continue
							else:
								readyQueue = [x] + readyQueue
								printQueue(readyQueue)
								blocked.remove(x)
								continue
					elif(len(readyQueue) > 1):
						if(  (guess - readyQueue[0].getRunTime())  > (guess - x.getRunTime())  ):
							readyQueue = [x] + readyQueue
							blocked.remove(x)
							printQueue(readyQueue)

						else:
							for z in range(0,len(readyQueue)):
									if((guess - readyQueue[z].getRunTime())  < (guess - x.getRunTime()) and (guess - readyQueue[z+1].getRunTime())  > (guess - x.getRunTime())):
										readyQueue.insert(z,x)
										printQueue(readyQueue)
										blocked.remove(x)
										break
									elif((guess - readyQueue[z].getRunTime())  == (guess - x.getRunTime())):
										if(readyQueue[z].getID() > x.getID()):
											readyQueue.insert(z-1,x)
											printQueue(readyQueue)
											blocked.remove(x)
											break
										else:
											readyQueue.insert(z,x)
											printQueue(readyQueue)
											blocked.remove(x)
											break




## Driver Function

## Pseudo random generation of processes
rand = Rand48(seed)
rand.srand(seed)
ID = 0
processes = []
for x in range(numProcesses):
	y=upperBound+1
	while (y>upperBound):
		r = rand.drand()
		y = -math.log(r)/lmda;
		
	arrivalTime =  math.floor(y)
	bursts = int(rand.drand() * 100)+1
	cpuBurst = []
	ioBurst = []
	for q in range(bursts):
		if (q == bursts-1):
			p=upperBound+1
			while (p>upperBound):
				r = rand.drand()
				p = -math.log(r)/lmda;


			cpuBurst.append(math.ceil(p))
			break


		p=upperBound+1
		while (p>upperBound):
			r = rand.drand()
			p = -math.log(r)/lmda;


		cpuBurst.append(math.ceil(p))

		p=upperBound+1
		while (p>upperBound):
			r = rand.drand()
			p = -math.log(r)/lmda;
		ioBurst.append(math.ceil(p))

	z = Process(arrivalTime,bursts,cpuBurst,ioBurst,65+ID)
	ID += 1
	processes.append(z)
### processes is a list of the generated process objects




SRT(processes, True, lmda, alpha, tcs)


















