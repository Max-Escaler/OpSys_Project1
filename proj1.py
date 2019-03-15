import sys
import math

seed = int(sys.argv[1])
lmda = float(sys.argv[2])
upperBound = int(sys.argv[3])
numProcesses = int(sys.argv[4])
tcs = sys.argv[5]
alpha = sys.argv[6]
timeSlice = sys.argv[7]


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
	runTime = 0.0;
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


def SRT(processes, preemptions,lmda,alpha,tcs):
	print("0 ms: Simulation started for SRT")
	processList = processes.copy()
	guess = 1/lmda
	readyQueue = []
	blocked=[]
	time = 0
	while(len(processList) > 0 or len(readyQueue)>0):
		for x in processList:
			if(time == x.getAT()):
				if(len(readyQueue) == 0):
					print(str(time) + "ms: Process", x.ID,"Added to the ready queue")
					readyQueue.append(x)
					processList.remove(x)
					continue
				elif(len(readyQueue) == 1):
					if(  (guess - readyQueue[0].getRunTime())  > (guess - x.getRunTime())  ):
						print(str(time) + "ms: Process", x.ID,"Added to the ready queue and will preempt", readyQueue[0])
						readyQueue = [x] + readyQueue
						processList.remove(x)
						continue
					else:
						if(readyQueue[0].getID() < x.getID()):
							print(str(time) + "ms: Process", x.ID,"Added to the ready queue")
							readyQueue.append(x)
							processList.remove(x)
							continue
						else:
							print(str(time) + "ms: Process", x.ID,"arrived; added to the ready queue and will preempt",readyQueue[0])
							readyQueue = [x] + readyQueue
							processList.remove(x)
							continue
				elif(len(readyQueue) > 1):
					if(  (guess - readyQueue[0].getRunTime())  > (guess - x.getRunTime())  ):
						print(str(time) + "ms: Process", x.ID,"Added to the ready queue and will preempt", readyQueue[0])
						readyQueue = [x] + readyQueue
					else:
						for z in range(0,len(readyQueue)):
								if((guess - readyQueue[z].getRunTime())  < (guess - x.getRunTime()) and (guess - readyQueue[z+1].getRunTime())  > (guess - x.getRunTime())):
									print(str(time) + "ms: Process", x.ID,"Added to the ready queue")
									readyQueue.insert(z,x)
									processList.remove(x)
									break
								elif((guess - readyQueue[z].getRunTime())  == (guess - x.getRunTime())):
									if(readyQueue[z].getID() > x.getID()):
										print(str(time) + "ms: Process", x.ID,"Added to the ready queue")
										readyQueue.insert(z-1,x)
										processList.remove(x)
										break
									else:
										print(str(time) + "ms: Process", x.ID,"Added to the ready queue")
										readyQueue.insert(z,x)
										processList.remove(x)
										break



		time +=1	
		if(len(readyQueue) >1):
			readyQueue[0].tick()
			for x in range(1,len(readyQueue)):
				readyQueue[x].wait()
		if(len(readyQueue) ==1):
			readyQueue[0].tick()

		if(len(readyQueue) >0 and readyQueue[0].runTime == readyQueue[0].burstTimes[0]):
			print(str(time)+"ms:",readyQueue[0].ID , "completed a CPU burst")
			guess = float(alpha) * readyQueue[0].burstTimes[0] + (1-float(alpha))*guess
			print(str(time)+"ms: Recalculated tau =",guess,"for process",readyQueue[0].ID)
			readyQueue.remove(readyQueue[0])





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





for y in processes:
	print("Arrival time:", y.getAT())
	print("CPUBurst Times:",len(y.getCPUBursts()))
	print("IOBurst  Times:",len(y.getIOBursts()))

SRT(processes, True, lmda, alpha, tcs)


















