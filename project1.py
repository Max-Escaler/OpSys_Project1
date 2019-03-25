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
	runTime = 0
	blockedTime = 0
	isSwitching = False
	switchTime = 0
	guess = 0
	t = ""
	def __init__(self,at, b,bt,iot,ID,lmda,t):
		self.arrivalTime = at
		self.bursts = b
		self.burstTimes = bt
		self.IOTimes = iot
		self.ID = chr(ID)
		self.guess = 1/lmda
		self.t = t
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
		if(self.isSwitching):
			self.switchTime+=1
		if(not self.isSwitching):
			self.waitTime += 1

		self.turnAroundTime += 1
	def block(self):
		self.blockedTime+=1


def SRT(processes, preemptions,lmda,a,t):
	endQueue = []
	readyQueue = []
	waitTimes=[]
	burstTimes=[]
	numContextSwitches = 0
	numPreemptions = 0
	turnAroundTimes = []
	avgTurnAroundTime = 0
	if(not preemptions):
		print("time 0ms: Simulator started for SJF", end = " ")
	else:
		print("time 0ms: Simulator started for SRT", end = " ")



	for x in processes:
		for y in x.burstTimes:
			burstTimes.append(y)
	
	printQueue(readyQueue)
	processList = list(processes)
	guess = int(1/lmda)
	alpha = a
	tcs = t
	CPU = []
	blocked=[]
	conSwitching = False
	preempted = False
	switchTime = int(int(tcs)/2)
	time = 0
	index = 0
	#This program will execute as long as there are processes waiting to arrive, in the ready queue, or in the blocked queue
	while(len(processList) > 0 or len(readyQueue)>0 or len(blocked) > 0 or len(CPU) > 0 or conSwitching == True):
		if(len(processList) == 0 and len(readyQueue)==0 and len(blocked) == 0 and len(CPU) == 0):
			time+=1
			if(not preemptions):
				print("time", str(int(time))+"ms: Simulator ended for SJF", end = " ")
			else:
				print("time", str(int(time))+"ms: Simulator ended for SRT", end = " ")
			printQueue(readyQueue)
			break
		# We check through all of the processes for an arrival on every tick of the sim
		for x in processList:
			## if we find one that is arriving, we add it in the correct place in the readyQueue
			if(time == x.getAT()):
				found = False
				found2 = False
				foundLongest = False
				for i in range(len(readyQueue)):
					if((readyQueue[i].guess - readyQueue[i].runTime) > (x.guess - x.runTime)):
						index =i
						found = True
						break

				if (found == False):
					if(len(readyQueue) > 0 and (readyQueue[-1].guess - readyQueue[-1].runTime) < (x.guess-x.runTime) ):
							foundLongest = True

					for i in range(len(readyQueue)):
						if(foundLongest):
							break
						if(ord(readyQueue[i].ID) > ord(x.ID)  and (readyQueue[i].guess - readyQueue[i].runTime) == (x.guess - x.runTime)):
							index = i
							found2 = True
							break

				if (found or found2):
					readyQueue = readyQueue[:index] + [x] + readyQueue[index:]
				else:
					readyQueue.append(x)
				processList.remove(x)
				print("time", str(int(time)) + "ms: Process", x.ID,"(tau", str(int(x.guess)) +"ms) arrived; added to ready queue" , end = " ")  
				printQueue(readyQueue)


		if((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted) ):
			conSwitching = False
		if(conSwitching):
			switchTime += 1
		#This section of code handles all of the running and waiting and blocking of processes
		if(len(CPU) ==1):
			if(conSwitching):
				CPU[0].wait()
			else:
				CPU[0].tick()
			for x in readyQueue:
				x.wait()


			if(conSwitching):
				for x in blocked:
					if(x.isSwitching):
						x.wait()
					else:
						x.block()
			else:
				for x in blocked:
					x.block()
		else:
			for x in readyQueue:
				x.wait()
			if(conSwitching):
				for x in blocked:
					if(x.isSwitching):
						x.wait()
					else:
						x.block()
			else:	
				for x in blocked:
					x.block()

		for x in blocked:
			if((x.switchTime == int(int(tcs)/2) and not preempted) or (x.switchTime == int(tcs) and preempted) ) :
				x.isSwitching=False
		for x in readyQueue:
			if((x.switchTime == int(int(tcs)/2) and not preempted) or (x.switchTime == int(tcs) and preempted) ) :
				x.isSwitching=False

		#this section of code handles all of the blocked list and checking if anything is coming off blocking			
		if(len(blocked) > 0):
			y=0
			while (y < len(blocked)):
				x = blocked[y]
				if(x.blockedTime == x.IOTimes[0]):
					# print(x.ID, x.guess-x.runTime)
					# for p in readyQueue:
					# 		print(p.ID,p.guess-p.runTime)
					x.IOTimes.pop(0)
					x.blockedTime = 0
					if(len(CPU)>0 and len(readyQueue)>0 and preempted and (switchTime in range(0,int(int(tcs)/2)+1)) and (readyQueue[0].guess - readyQueue[0].runTime) > (x.guess - x.runTime)  and (CPU[0].guess - CPU[0].runTime) > (x.guess - x.runTime)):
						CPU.append(readyQueue[0])
						readyQueue = [CPU[0]] + readyQueue
						CPU.remove(CPU[0])
						readyQueue.remove(readyQueue[1])
						print("time", str(int(time)) + "ms: Process", x.ID,"(tau", str(x.guess) +"ms) completed I/O; added to ready queue" , end = "")
						x.turnAroundTime = 0
						#x.waitTime = 0
						readyQueue = [x] + readyQueue
						printQueue(readyQueue)
						readyQueue = readyQueue[:2] + [CPU[0]] + readyQueue[2:]
						CPU.remove(CPU[0])
						blocked.remove(x)
						preempted = False
						numContextSwitches -= 1
						continue




					if(len(CPU) >0 and (CPU[0].guess - CPU[0].runTime) > (x.guess - x.runTime) and (switchTime == int(int(tcs)/2) or switchTime==int(tcs)) and preemptions):
						print("time", str(int(time))+"ms: Process",x.ID , "(tau", str(x.guess) +"ms) completed an I/O burst and will preempt",CPU[0].ID, end = " ")
						x.turnAroundTime = 0
						#x.waitTime = 0
						printQueue(readyQueue)
						conSwitching=True
						switchTime=0
						CPU[0].switchTime = 0
						CPU[0].isSwitching = True
						x.switchTime = 0 
						x.isSwitching = True
						CPU.append(x)
						blocked.remove(x)
						#Adding removed process into ready from CPU
						for i in range(len(readyQueue)):
							if((readyQueue[i].guess - readyQueue[i].runTime) > (CPU[0].guess - CPU[0].runTime)):
								index =i
								found = True

								for j in range(index):
									if((readyQueue[j].guess - readyQueue[j].runTime) == (CPU[0].guess - CPU[0].runTime)):
										for k in range(j,index):
											if(ord(readyQueue[k].ID) > ord(CPU[0].ID)):
												index = k
												break
								break
						readyQueue = readyQueue[:index] + [CPU[0]] + readyQueue[index:]
						CPU.remove(CPU[0])
						preempted = True
						plop = True
						numPreemptions +=1
						numContextSwitches += 1
						continue
					found = False
					found2 = False
					foundLongest = False
					for i in range(len(readyQueue)):
						if((readyQueue[i].guess - readyQueue[i].runTime) > (x.guess - x.runTime)):
							index =i
							found = True

							for j in range(index):
								if((readyQueue[j].guess - readyQueue[j].runTime) == (x.guess - x.runTime)):
									for k in range(j,index):
										if(ord(readyQueue[k].ID) > ord(x.ID)):
											index = k
											break
							break


					if (found == False):
						if(len(readyQueue) > 0 and (readyQueue[-1].guess - readyQueue[-1].runTime) < (x.guess-x.runTime) ):
								foundLongest = True

						for i in range(len(readyQueue)):
							if(foundLongest):
								break
							if(ord(readyQueue[i].ID) > ord(x.ID) and (readyQueue[j].guess - readyQueue[j].runTime) == (x.guess - x.runTime)):
								index = i
								found2 = True
								break

					if (found or found2):
						readyQueue = readyQueue[:index] + [x] + readyQueue[index:]
					else:
						readyQueue.append(x)
					blocked.remove(x)
					y-=1
					
					print("time", str(int(time)) + "ms: Process", x.ID,"(tau", str(x.guess) +"ms) completed I/O" , end = "") 
					x.turnAroundTime = 0
					#x.waitTime = 0
					print("; added to ready queue",end = " ")
					printQueue(readyQueue)
				y+=1

		

		if(preempted and switchTime == int(tcs) and plop):
			print("time", str(int(time))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			printQueue(readyQueue)
			plop = False
		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) >1 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted ) )):
			if(len(CPU[0].burstTimes)-1 > 1):
				print("time", str(int(time))+"ms: Process",CPU[0].ID , "completed a CPU burst;",len(CPU[0].burstTimes)-1,"bursts to go", end = " ")
			else:
				print("time", str(int(time))+"ms: Process",CPU[0].ID , "completed a CPU burst;",len(CPU[0].burstTimes)-1,"burst to go", end = " ")

			printQueue(readyQueue)
			turnAroundTimes.append(CPU[0].turnAroundTime+2)
			waitTimes.append(CPU[0].waitTime)
			CPU[0].waitTime = 0
			CPU[0].turnAroundTime = 0
			CPU[0].guess = float(alpha) * CPU[0].burstTimes[0] + (1-float(alpha))*CPU[0].guess
			CPU[0].guess = math.ceil(CPU[0].guess)
			print("time",str(int(time))+"ms: Recalculated tau =",str(CPU[0].guess)+"ms for process",CPU[0].ID, end = " ")
			printQueue(readyQueue)
			print("time", str(int(time))+"ms: Process",CPU[0].ID,"switching out of CPU; will block on I/O until time",str(time+CPU[0].IOTimes[0]+int(int(tcs)/2)) + "ms", end = " ")
			printQueue(readyQueue)
			CPU[0].runTime = 0
			CPU[0].switchTime = 0
			CPU[0].isSwitching = True
			blocked.append(CPU[0])
			CPU[0].burstTimes.pop(0)
			CPU.remove(CPU[0])
			conSwitching = True
			preempted = False
			switchTime = 0
		if(len(CPU) > 0 and len(readyQueue)>0 and  (CPU[0].guess - CPU[0].runTime) > (readyQueue[0].guess - readyQueue[0].runTime) and switchTime == int(int(tcs)/2) and preemptions):
			print("time", str(int(time))+"ms: Process",readyQueue[0].ID , "will preempt",CPU[0].ID, end = " ")
			printQueue(readyQueue)
			conSwitching=True
			switchTime=0
			preempted = True
			CPU[0].switchTime = 0
			CPU[0].isSwitching = True
			readyQueue[0].switchTime = 0 
			readyQueue[0].isSwitching = True
			CPU.append(readyQueue[0])
			readyQueue.remove(readyQueue[0])
			readyQueue = [CPU[0]]+readyQueue
			CPU.remove(CPU[0])
			numContextSwitches +=1
			numPreemptions += 1


		if(len(CPU) == 0 and len(readyQueue) > 0 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted ) ) ):
			CPU.append(readyQueue[0])
			readyQueue.remove(readyQueue[0])
			conSwitching = True
			switchTime = 0
			preempted = False
			if(CPU[0].burstTimes[0] - CPU[0].runTime == CPU[0].burstTimes[0]):
				print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			else:
				print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU with",str(CPU[0].burstTimes[0] - CPU[0].runTime)+"ms remaining", end = " ")
			printQueue(readyQueue)
			numContextSwitches += 1
		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) ==1 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted ) )):
			print("time", str(int(time))+"ms: Process",CPU[0].ID , "terminated", end = " ")
			printQueue(readyQueue)
			turnAroundTimes.append(CPU[0].turnAroundTime+2)
			endQueue.append(CPU.pop(0))
			preempted = False
			conSwitching = True
			switchTime = 0




		
		
		time +=1

	avgWaitTime = 0
	avgBurstTimes = 0
	for x in turnAroundTimes:
		avgTurnAroundTime += x
	avgTurnAroundTime = avgTurnAroundTime/len(turnAroundTimes)
	for x in waitTimes:
		avgWaitTime +=x
	avgWaitTime = avgWaitTime / len(waitTimes)
	for x in burstTimes:
		avgBurstTimes += x
	avgBurstTimes = avgBurstTimes / len(burstTimes)

	print("Average Burst Times:", '%.3f'%avgBurstTimes)
	print("Average Wait Times:",'%.3f'%avgWaitTime)
	print("Average Turn Around Time:", '%.3f'%avgTurnAroundTime)
	print("Context Switches:",numContextSwitches)
	print("Preemptions:", numPreemptions)
## Driver Function

## Pseudo random generation of processes
rand = Rand48(seed)
rand.srand(seed)
ID = 0
processes = []
SRTprocesses=[]
for x in range(numProcesses):
	y=upperBound+1
	while (y>upperBound):
		r = rand.drand()
		y = -math.log(r)/lmda;
		
	arrivalTime =  math.floor(y)
	bursts = int(rand.drand() * 100)+1
	cpuBurst = []
	cpuBurst2 = []
	ioBurst = []
	ioBurst2=[]
	for q in range(bursts):
		if (q == bursts-1):
			p=upperBound+1
			while (p>upperBound):
				r = rand.drand()
				p = -math.log(r)/lmda;


			cpuBurst.append(math.ceil(p))
			cpuBurst2.append(math.ceil(p))
			break


		p=upperBound+1
		while (p>upperBound):
			r = rand.drand()
			p = -math.log(r)/lmda;


		cpuBurst.append(math.ceil(p))
		cpuBurst2.append(math.ceil(p))


		p=upperBound+1
		while (p>upperBound):
			r = rand.drand()
			p = -math.log(r)/lmda;
		ioBurst.append(math.ceil(p))
		ioBurst2.append(math.ceil(p))


	z = Process(arrivalTime,bursts,cpuBurst,ioBurst,65+ID,lmda,"SJF")
	q = Process(arrivalTime,bursts,cpuBurst2,ioBurst2,65+ID,lmda,"SRT")

	ID += 1
	processes.append(z)
	SRTprocesses.append(q)
### processes is a list of the generated process objects
for x in processes:
	print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU bursts" )
SRT(processes, False, lmda, alpha, tcs)
print("")
for x in SRTprocesses:
	print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU bursts" )
SRT(SRTprocesses, True, lmda, alpha, tcs)

















