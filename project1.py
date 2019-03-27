import sys
import math

# OpSys Project 1: CPU Scheduling algorithms simulator
# Team: Max Escaler, Brian Connolly

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
	printString = False
	printTime = 0
	readyQueue = []
	waitTimes=[]
	burstTimes=[]
	numContextSwitches = 0
	numPreemptions = 0
	turnAroundTimes = []
	avgTurnAroundTime = 0
	addedString = ""
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
				if(time < 1000):
					print("time", str(int(time)) + "ms: Process", x.ID,"(tau", str(int(x.guess)) +"ms) arrived; added to ready queue" , end = " ")  
					printQueue(readyQueue)


		

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
						if(time < 1000):
							print("time", str(int(time)) + "ms: Process", x.ID,"(tau", str(x.guess) +"ms) completed I/O; added to ready queue" , end = "")
						x.turnAroundTime = 0
						#x.waitTime = 0
						readyQueue = [x] + readyQueue
						if(time < 1000):
							printQueue(readyQueue)
						readyQueue = readyQueue[:2] + [CPU[0]] + readyQueue[2:]
						CPU.remove(CPU[0])
						blocked.remove(x)
						preempted = False
						numContextSwitches -= 1
						continue




					if(len(CPU) >0 and (CPU[0].guess - CPU[0].runTime) > (x.guess - x.runTime) and (switchTime == int(int(tcs)/2) or switchTime==int(tcs)) and preemptions):
						if(time < 1000):
							print("time", str(int(time))+"ms: Process",x.ID , "(tau", str(x.guess) +"ms) completed I/O and will preempt",CPU[0].ID, end = " ")
							if(len(readyQueue)>0):
								temp = readyQueue.pop(0)	
								readyQueue = [x] + readyQueue
								printQueue(readyQueue)
								readyQueue.pop(0)
								readyQueue = [temp] + readyQueue
							else:
								readyQueue = [x] + readyQueue
								printQueue(readyQueue)
								readyQueue.pop(0)

						x.turnAroundTime = 0
						#x.waitTime = 0

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
					
							
					#This handles placing processes back into the ready queue
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

							if(ord(readyQueue[i].ID) > ord(x.ID) and int(readyQueue[i].guess - readyQueue[i].runTime) == int(x.guess - x.runTime)):
								index = i
								found2 = True
								break

					if (found or found2):
						readyQueue = readyQueue[:index] + [x] + readyQueue[index:]
					else:
						readyQueue.append(x)
					blocked.remove(x)
					y-=1
					x.turnAroundTime = 0

					if(time < 1000):
						print("time", str(int(time)) + "ms: Process", x.ID,"(tau", str(x.guess) +"ms) completed I/O" , end = "") 
						#x.waitTime = 0
						print("; added to ready queue",end = " ")
						printQueue(readyQueue)
				y+=1

		
		#To handle printing when a process preempts directly from I/O
		if(preempted and switchTime == int(tcs) and plop):
			if(time < 1000):
				print("time", str(int(time))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
				printQueue(readyQueue)
			plop = False
		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) >1 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted ) )):
			if(time < 1000):
				if(len(CPU[0].burstTimes)-1 > 1):
					print("time", str(int(time))+"ms: Process",CPU[0].ID , "completed a CPU burst;",len(CPU[0].burstTimes)-1,"bursts to go",end = " ")
				else:
					print("time", str(int(time))+"ms: Process",CPU[0].ID , "completed a CPU burst;",len(CPU[0].burstTimes)-1,"burst to go", end = " ")

				printQueue(readyQueue)
			turnAroundTimes.append(CPU[0].turnAroundTime+2)
			waitTimes.append(CPU[0].waitTime)
			CPU[0].waitTime = 0
			CPU[0].turnAroundTime = 0
			CPU[0].guess = float(alpha) * CPU[0].burstTimes[0] + (1-float(alpha))*CPU[0].guess
			CPU[0].guess = math.ceil(CPU[0].guess)
			if(time < 1000):
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
			if(time < 1000):
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
			if(time < 1000):
				if(CPU[0].runTime == 0):
					addedString = "time "+ str(int(int(time) + int(tcs)/2))+"ms: Process "+ str(CPU[0].ID)+ " started using the CPU for "+str(CPU[0].burstTimes[0])+"ms burst"
					
				else:
					addedString = "time "+ str(int(int(time) + int(tcs)/2))+"ms: Process "+ str(CPU[0].ID)+ " started using the CPU with "+str(CPU[0].burstTimes[0] - CPU[0].runTime)+"ms remaining"
			printString = True
			printTime = int(time) + int(tcs)/2
			CPU[0].isSwitching = True
			numContextSwitches += 1
		if(len(CPU) >0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) ==1 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted ) )):
			print("time", str(int(time))+"ms: Process",CPU[0].ID , "terminated", end = " ")
			printQueue(readyQueue)
			turnAroundTimes.append(CPU[0].turnAroundTime+2)
			endQueue.append(CPU.pop(0))
			preempted = False
			conSwitching = True
			switchTime = 0
		if(printString == True and int(time) == printTime):
			if(time < 1000):
				print(addedString, end = " ")
				printQueue(readyQueue)
			printString = False




		
		
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
	f = open("simout.txt", "a")
	if(preemptions):
		f.write("Algorithm SRT\n")
	else:
		f.write("Algorithm SJF\n")
	ABT = "-- average CPU burst time: "+ '%.3f'%avgBurstTimes + " ms\n"
	f.write(ABT)
	AWT = "-- average wait time: "+'%.3f'%avgWaitTime+ " ms\n"
	f.write(AWT)
	ATAT = "-- average turnaround time: "+ '%.3f'%avgTurnAroundTime+ " ms\n"
	f.write(ATAT)
	CS = "-- total number of context switches: "+str(numContextSwitches)+ "\n"
	f.write(CS)
	NP = "-- total number of preemptions: "+ str(numPreemptions)+ "\n"
	f.write(NP)
	f.write("\n")


def RR(processes, tSlice, insertSide,tcs):
	endQueue = []
	printString = False
	printTime = 0
	readyQueue = []
	waitTimes=[]
	burstTimes=[]
	numContextSwitches = 0
	numPreemptions = 0
	turnAroundTimes = []
	avgTurnAroundTime = 0

	for x in processes:
		for y in x.burstTimes:
			burstTimes.append(y)

	processList = processes.copy()
	readyQueue = []
	CPU = []
	blocked = []
	conSwitching = False
	preempted = False
	switchTime = int(int(tcs)/2)
	plop = False
	time = 0 # keeps track of the global cpu runtime
	# timeRan = 0 # keeps track of how long a given process has run. Checked against tSlice
	# contextLag = tcs # used for counting context switch time
	
	if(tSlice != sys.maxsize):
		print("time 0ms: Simulator started for RR", end = " ")
	else:
		print("time 0ms: Simulator started for FCFS", end = " ")
	printQueue(readyQueue)
	
	while(len(processList)>0 or len(readyQueue)>0 or len(blocked)>0 or len(CPU)>0 or conSwitching == True):
		
		if(len(processList) == 0 and len(readyQueue)==0 and len(blocked) == 0 and len(CPU) == 0):
			time+=1
			if(tSlice != sys.maxsize):
				print("time", str(time)+"ms: Simulator ended for RR", end = " ")
			else:
				print("time", str(time)+"ms: Simulator ended for FCFS", end = " ")

			printQueue(readyQueue)
			break


		if((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted) ):
			conSwitching = False	
		if(conSwitching):
			switchTime += 1

		if(len(CPU) == 1):
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
		else: # No process in the CPU
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
			# if((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted) ):
			if(switchTime == int(int(tcs)/2)):
				x.isSwitching = False
		for x in readyQueue:
			if((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted) ):
				x.isSwitching = False
		# if(len(CPU) > 0):
		# 	if(CPU[0].isSwitching and switch2 == True and CPU[0].switchTime == int(int(tcs))/2):
		# 		CPU[0].isSwitching = False

		x = len(blocked)-1
		blocked.sort(key=lambda process: process.ID, reverse=True)
		while(x>=0):

			if(blocked[x].blockedTime == blocked[x].IOTimes[0]):
				blocked[x].blockedTime = 0
				blocked[x].IOTimes.pop(0)
				blocked[x].turnAroundTime = 0
				if(insertSide == "BEGINNING"):
					readyQueue = [blocked[x]] + readyQueue
					
				else:
					readyQueue = readyQueue + [blocked[x]]
				if(time<1000):	
					print("time", str(time)+"ms: Process",blocked[x].ID,"completed I/O; added to ready queue", end= " ")
					printQueue(readyQueue)
				blocked.remove(blocked[x])
			x -= 1
		
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
				print("time", str(time) + "ms: Process", x.ID,"arrived; added to ready queue" , end = " ")  
				printQueue(readyQueue)

		if(((preempted and switchTime == int(tcs)) or (not preempted and switchTime == int(int(tcs)/2))) and plop and (len(CPU) > 0) ):
			# print((preempted and switchTime == int(tcs)), (not preempted and switchTime == int(int(tcs)/2)), plop, (len(CPU) > 0))
			if(time < 1000):
				if(CPU[0].guess == 1): # repurposed guess to determine if a process had been preempted
					print("time", str(int(time))+"ms: Process", CPU[0].ID,"started using the CPU with",str(CPU[0].burstTimes[0])+"ms remaining", end = " ")
				else:
					print("time", str(int(time))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
				printQueue(readyQueue)
			# print("time", str(int(time))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			# printQueue(readyQueue)
			plop = False # need to print out CPU usage

		
		if(len(CPU)==1 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted)) ):
			
			if(CPU[0].runTime == int(tSlice) and len(CPU[0].burstTimes) >= 1 and (CPU[0].burstTimes[0] != int(tSlice))):
				if(len(readyQueue)==0):
					if(time < 1000):
						print("time", str(time)+"ms: Time slice expired; no preemption because ready queue is empty", end = " ")
						printQueue(readyQueue)
					turnAroundTimes.append(CPU[0].turnAroundTime + int(int(tcs)/2))
					waitTimes.append(CPU[0].waitTime)
					CPU[0].burstTimes[0] -= int(tSlice)
					CPU[0].runTime = 0
					CPU[0].waitTime = 0
					CPU[0].turnAroundTime = 0
				else:
					# time 457ms: Time slice expired; process B preempted with 78ms to go [Q A]
					if(time < 1000):
						print("time", str(time)+"ms: Time slice expired; process",CPU[0].ID , "preempted with",str(CPU[0].burstTimes[0]-int(tSlice))+"ms to go", end = " ")
						printQueue(readyQueue)
					turnAroundTimes.append(CPU[0].turnAroundTime+int(int(tcs)/2))
					waitTimes.append(CPU[0].waitTime)
					numPreemptions += 1
					numContextSwitches += 1
					CPU[0].burstTimes[0] -= int(tSlice)
					CPU[0].runTime = 0
					CPU[0].switchTime = 0
					CPU[0].isSwitching = True
					CPU[0].guess = 1
					CPU[0].waitTime = 0
					CPU[0].turnAroundTime = 0
					readyQueue[0].isSwitching = True
					readyQueue[0].switchTime = 0
					if(insertSide == "BEGINNING"):
						readyQueue = [CPU[0]] + readyQueue
						CPU.remove(0)
						CPU += [readyQueue.pop(1)]
					else:
						readyQueue += [CPU.pop()]
						CPU += [readyQueue.pop(0)]
					# if(time < 1000):
					# 	if(CPU[0].guess == 1): # repurposed guess to determine if a process had been preempted
					# 		print("time", str(int(int(time) + int(tcs)))+"ms: Process", CPU[0].ID,"started using the CPU with",str(CPU[0].burstTimes[0])+"ms remaining", end = " ")
					# 	else:
					# 		print("time", str(int(int(time) + int(tcs)))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
					# 	printQueue(readyQueue)
					conSwitching = True
					preempted = True
					switchTime = 0
					plop = True
			elif(CPU[0].runTime == CPU[0].burstTimes[0]  and len(CPU[0].burstTimes) > 1 ):	
				# time 177ms: Process B completed a CPU burst; 20 bursts to go [Q A]
				if(time < 1000):
					if(len(CPU[0].burstTimes) == 2):
						print("time", str(time)+"ms: Process",CPU[0].ID , "completed a CPU burst;",str(len(CPU[0].burstTimes)-1),"burst to go", end = " ")
					else:
						print("time", str(time)+"ms: Process",CPU[0].ID , "completed a CPU burst;",str(len(CPU[0].burstTimes)-1),"bursts to go", end = " ")
					printQueue(readyQueue)
					print("time", str(time)+"ms: Process",CPU[0].ID , "switching out of CPU; will block on I/O until time",str(time+CPU[0].IOTimes[0] + int(int(tcs)/2) )+"ms", end = " ")
					printQueue(readyQueue)

				turnAroundTimes.append(CPU[0].turnAroundTime+int(int(tcs)/2))
				waitTimes.append(CPU[0].waitTime)
				numContextSwitches += 1
				CPU[0].burstTimes.pop(0)
				CPU[0].runTime = 0
				CPU[0].switchTime = 0
				CPU[0].isSwitching = True 			## merge the logic of these two, very similar
				CPU[0].waitTime = 0 			## merge the logic of these two, very similar
				CPU[0].turnAroundTime = 0 			## merge the logic of these two, very similar
				if(len(readyQueue) > 0):
					readyQueue[0].isSwitching = True
					readyQueue[0].switchTime = 0
					CPU.append(readyQueue.pop(0) )
					# if(time < 1000):
					# 	if(CPU[1].guess == 1): # repurposed guess to determine if a process had been preempted
					# 		print("time", str(int(int(time) + int(tcs)))+"ms: Process", CPU[1].ID,"started using the CPU with",str(CPU[1].burstTimes[0])+"ms remaining", end = " ")
					# 	else:
					# 		print("time", str(int(int(time) + int(tcs)))+"ms: Process", CPU[1].ID,"started using the CPU for",str(CPU[1].burstTimes[0])+"ms burst", end = " ")
					# 	# print("time", str(int(int(time) + int(tcs)))+"ms: Process", CPU[1].ID,"started using the CPU for",str(CPU[1].burstTimes[0])+"ms burst", end = " ")
					# 	printQueue(readyQueue)
				CPU[0].guess = 0
				blocked.append(CPU.pop(0))
				conSwitching = True
				preempted = True
				switchTime = 0
				plop = True

		# elif(len(CPU)==0 and (switchTime == int(int(tcs)/2) and len(readyQueue) == 1)): # when process returns from I/O and another just moved out of CPU
		# 	CPU.append(readyQueue.pop(0))
		# 	if(CPU[0].guess == 1): # repurposed guess to determine if a process had been preempted
		# 		print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU with",str(CPU[0].burstTimes[0])+"ms remaining", end = " ")
		# 	else:
		# 		print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
		# 	printQueue(readyQueue)
		# 	CPU[0].isSwitching = True
		# 	CPU[0].switchTime = 0
		# 	conSwitching = True
		# 	preempted = False
		# 	switchTime = 0

		elif(len(CPU)==0 and ((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted)) and len(readyQueue) > 0):
			CPU.append(readyQueue.pop(0))
			# if(time < 1000):
			# 	if(CPU[0].guess == 1): # repurposed guess to determine if a process had been preempted
			# 		print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU with",str(CPU[0].burstTimes[0])+"ms remaining", end = " ")
			# 	else:
			# 		print("time", str(int(int(time) + int(tcs)/2))+"ms: Process", CPU[0].ID,"started using the CPU for",str(CPU[0].burstTimes[0])+"ms burst", end = " ")
			# 	printQueue(readyQueue)
			turnAroundTimes.append(CPU[0].turnAroundTime+int(int(tcs)/2))
			waitTimes.append(CPU[0].waitTime)
			# numContextSwitches += 1
			CPU[0].isSwitching = True
			CPU[0].switchTime = 0
			CPU[0].waitTime = 0
			CPU[0].turnAroundTime = 0
			conSwitching = True
			preempted = False
			switchTime = 0
			plop = True



		if(len(CPU) > 0 and CPU[0].runTime == CPU[0].burstTimes[0] and len(CPU[0].burstTimes) == 1 and \
		((switchTime == int(int(tcs)/2) and not preempted) or (switchTime == int(tcs) and preempted))):
			print("time", str(int(time))+"ms: Process",CPU[0].ID , "terminated", end = " ")
			printQueue(readyQueue)
			# turnAroundTimes.append(CPU[0].turnAroundTime+2)
			# endQueue.append(CPU.pop(0))
			CPU.pop(0)
			numContextSwitches += 1
			conSwitching = True
			preempted = False
			switchTime = 0


		time += 1



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
	f = open("simout.txt", "a")
	if(tSlice != sys.maxsize):
		f.write("Algorithm RR\n")
	else:
		f.write("Algorithm FCFS\n")
	ABT = "-- average CPU burst time: "+ '%.3f'%avgBurstTimes + " ms\n"
	f.write(ABT)
	AWT = "-- average wait time: "+'%.3f'%avgWaitTime+ " ms\n"
	f.write(AWT)
	ATAT = "-- average turnaround time: "+ '%.3f'%avgTurnAroundTime+ " ms\n"
	f.write(ATAT)
	CS = "-- total number of context switches: "+str(numContextSwitches)+ "\n"
	f.write(CS)
	NP = "-- total number of preemptions: "+ str(numPreemptions)+ "\n"
	f.write(NP)
	f.write("\n")



## Driver Function

## Pseudo random generation of processes
rand = Rand48(seed)
rand.srand(seed)
ID = 0
processes = []
SRTprocesses=[]
FCFSprocesses=[]
RRprocesses=[]
for x in range(numProcesses):
	y=upperBound+1
	while (y>upperBound):
		r = rand.drand()
		y = -math.log(r)/lmda;
		
	arrivalTime =  math.floor(y)
	bursts = int(rand.drand() * 100)+1
	cpuBurst = []
	cpuBurst2 = []
	cpuBurst3 = []
	cpuBurst4 = []
	ioBurst = []
	ioBurst2=[]
	ioBurst3=[]
	ioBurst4=[]
	for q in range(bursts):
		if (q == bursts-1):
			p=upperBound+1
			while (p>upperBound):
				r = rand.drand()
				p = -math.log(r)/lmda;


			cpuBurst.append(math.ceil(p))
			cpuBurst2.append(math.ceil(p))
			cpuBurst3.append(math.ceil(p))
			cpuBurst4.append(math.ceil(p))
			break


		p=upperBound+1
		while (p>upperBound):
			r = rand.drand()
			p = -math.log(r)/lmda;


		cpuBurst.append(math.ceil(p))
		cpuBurst2.append(math.ceil(p))
		cpuBurst3.append(math.ceil(p))
		cpuBurst4.append(math.ceil(p))


		p=upperBound+1
		while (p>upperBound):
			r = rand.drand()
			p = -math.log(r)/lmda;
		ioBurst.append(math.ceil(p))
		ioBurst2.append(math.ceil(p))
		ioBurst3.append(math.ceil(p))
		ioBurst4.append(math.ceil(p))


	z = Process(arrivalTime,bursts,cpuBurst,ioBurst,65+ID,lmda,"SJF")
	q = Process(arrivalTime,bursts,cpuBurst2,ioBurst2,65+ID,lmda,"SRT")
	f = Process(arrivalTime,bursts,cpuBurst3,ioBurst3,65+ID,lmda,"FCFS")
	r = Process(arrivalTime,bursts,cpuBurst4,ioBurst4,65+ID,lmda,"RR")

	ID += 1
	processes.append(z)
	SRTprocesses.append(q)
	FCFSprocesses.append(f)
	RRprocesses.append(r)
### processes is a list of the generated process objects

fcfsTSlice = sys.maxsize

for x in processes:
	if(x.bursts >1):
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU bursts" )
	else:
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU burst" )

SRT(processes, False, lmda, alpha, tcs)
print("")

for x in SRTprocesses:
	if(x.bursts >1):
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU bursts" )
	else:
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU burst" )

SRT(SRTprocesses, True, lmda, alpha, tcs)
print("")

for x in FCFSprocesses:
	if(x.bursts >1):
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU bursts" )
	else:
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU burst" )

RR(FCFSprocesses, fcfsTSlice, addEnd, tcs)
print("")

for x in RRprocesses:
	if(x.bursts >1):
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU bursts" )
	else:
		print("Process",x.ID,"[NEW] (arrival time",x.arrivalTime,"ms)",x.bursts,"CPU burst" )

RR(RRprocesses, timeSlice, addEnd, tcs)
print("")
















