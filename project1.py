import sys
import math

seed = int(sys.argv[1])
lmda = float(sys.argv[2])
upperBound = int(sys.argv[3])
numProcesses = int(sys.argv[4])
tcs = sys.argv[5]
alpha = sys.argv[6]
timeSlice = sys.argv[7]
if(len(sys.argv) == 9): # change to handle incorrect args
	addEnd = sys.argv[8]
else:
	addEnd = "END"

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
	isSwitching = False
	switchTime = 0
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
		if(self.isSwitching):
			self.switchTime+=1
		self.waitTime += 1
		self.turnAroundTime += 1
	def block(self):
		self.blockedTime+=1
		self.waitTime+=1
		self.turnAroundTime+=1


def SRT(processes, preemptions,lmda,alpha,tcs):
	print("time 0 ms: Simulation started for SRT")
	processList = processes.copy()
	guess = int(1/lmda)
	readyQueue = []
	CPU = []
	blocked=[]
	conSwitching = False
	switchTime = int(int(tcs)/2)
	time = 0
	#This program will execute as long as there are processes waiting to arrive, in the ready queue, or in the blocked queue
	while(len(processList) > 0 or len(readyQueue)>0 or len(blocked) > 0 or len(CPU) > 0 or conSwitching == True):

		if(len(processList) == 0 and len(readyQueue)==0 and len(blocked) == 0 and len(CPU) == 0):
			time+=1
			print("time", str(time)+"ms: Simulator ended for SRT", end = " ")
			printQueue(readyQueue)
			break
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

		if(switchTime == int(tcs)/2):
			conSwitching = False
		if(conSwitching):
			switchTime += 1





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
			if(x.switchTime == int(int(tcs)/2)):
				x.isSwitching=False

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

		


		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) >1 and switchTime == int(int(tcs)/2)):
			print("time", str(time)+"ms:",CPU[0].ID , "completed a CPU burst;",len(CPU[0].burstTimes)-1,"bursts to go", end = " ")
			printQueue(readyQueue)
			guess = float(alpha) * CPU[0].burstTimes[0] + (1-float(alpha))*guess
			guess = math.ceil(guess)
			print("time",str(time)+"ms: Recalculated tau =",str(guess)+"ms for process",CPU[0].ID, end = " ")
			printQueue(readyQueue)
			print("time", str(time)+"ms: Process",CPU[0].ID,"switching out of CPU; will block on I/O until time",time+CPU[0].IOTimes[0]+int(int(tcs)/2), end = " ")
			printQueue(readyQueue)
			CPU[0].runTime = 0
			CPU[0].switchTime = 0
			CPU[0].isSwitching = True
			blocked.append(CPU[0])
			CPU[0].burstTimes.pop(0)
			CPU.remove(CPU[0])
			conSwitching = True
			switchTime = 0 

		if(len(CPU) == 0 and len(readyQueue) > 0 and switchTime == int(int(tcs)/2) ):
			CPU.append(readyQueue[0])
			readyQueue.remove(readyQueue[0])
			conSwitching = True
			switchTime = 0
			print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			printQueue(readyQueue)	
		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) ==1 and switchTime == int(int(tcs)/2)):
			print("time", str(time)+"ms:",CPU[0].ID , "terminated", end = " ")
			printQueue(readyQueue)
			CPU.pop(0)
			conSwitching = True
			switchTime = 0




		
		
		time +=1


def RR(processes, tSlice, insertSide,tcs):
	processList = processes.copy()
	readyQueue = []
	CPU = []
	blocked = []
	time = 0 # keeps track of the global cpu runtime
	# timeRan = 0 # keeps track of how long a given process has run. Checked against tSlice
	# contextLag = tcs # used for counting context switch time
	while(len(processList)>0 or len(readyQueue)>0 or len(blocked)>0 or len(CPU)>0):
		# this will loop through the list of processes that have yet to arrive and 
		# if their arrival time matches the current time they will be moved to the 
		# process queue
		for x in processList:
			if(time == x.getAT() ):
				if(insertSide == "BEGINNING"):
					readyQueue.insert(0,x)
				else:
					readyQueue.append(x)
				processList.remove(x)
				print("process", x.getID(), " added to readyQueue")
		for z in readyQueue:
			print(z.getID, "arrived at", z.getAT() )

		## running of process in CPU and ones in blocked/readyQueue
		if(len(CPU)==0 and len(readyQueue)>0):
			CPU += [readyQueue.pop(0)]
			print("time", str(time)+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			printQueue(readyQueue)
		elif(len(CPU)==1):
			if( (CPU[0].runTime < tSlice) and (CPU[0].runTime < CPU[0].burstTimes[0]) ):
				CPU[0].tick()
				for x in blocked:
					x.block()
				for y in readyQueue:
					y.wait()
			elif(CPU[0].runTime == tSlice): ## check later if burst == tSlice as well
				if(len(readyQueue)==0):
					print("time", str(time)+"ms: Time slice expired; no preemption because ready queue is empty", end = " ")
					printQueue(readyQueue)
					CPU[0].burstTimes[0] -= tSlice
					CPU[0].runTime = 0
				else:
					# time 457ms: Time slice expired; process B preempted with 78ms to go [Q A]
					print("time", str(time)+"ms: Time slice expired; process",CPU[0].ID , "preempted with",str(CPU[0].burstTimes[0]-tSlice)+"ms to go", end = " ")
					printQueue(readyQueue)
					CPU[0].burstTimes[0] -= tSlice
					CPU[0].runTime = 0
					blocked += [CPU.pop()]
					CPU += [readyQueue.pop(0)]
					



		# if(timeRan == tSlice or timeRan == readyQueue[pIndex].burstTimes[0]):
		# 	if(readyQueue[pIndex].burstTimes[0] > tSlice):
		# 		readyQueue[pIndex].burstTimes[0] -= timeRan
		# 		readyQueue += [readyQueue.pop(pIndex)]
		# 	else:
		# 		readyQueue[pIndex].burstTimes.pop(0)
		# 		readyQueue += [readyQueue.pop(pIndex)]
		# 	pIndex = 0
		# 	timeRan = 0
		# 	contextLag = 0
		# else:
		# 	timeRan += 1
		# 		# WORKING: accounting for context switch lag when running
		# if(len(processList)==0):
		# 	break
		time += 1



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
	print("Process",chr(65+ID),"[NEW] (arrival time",arrivalTime,"ms)",bursts,"CPU bursts" )
	ID += 1
	processes.append(z)
### processes is a list of the generated process objects




# SRT(processes, True, lmda, alpha, tcs)
RR(processes,timeSlice, addEnd, tcs)

















