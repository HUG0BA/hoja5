import random
import simpy 
import csv

MAX_RAM = 10
MAX_INSTRUCTIONS = 10
CPU_CYCLE_TIME = 3
CPU_FAST_CYCLE_TIME = 1
CPU_INSTRUCTIONS_PER_CYCLE = 3
IO_TIMEOUT = 5

random.seed(1)
class Program:

    def __init__(self, name, env, instructions, needed_ram, available_ram, processor, writer):
        self.env = env
        self.name = name
        self.instructions = instructions
        self.needed_ram = needed_ram
        self.available_ram = available_ram
        self.processor = processor
        self.total_time = 0
        self.writer = writer


    def run(self):
        with self.available_ram.get(self.needed_ram) as ram_req: #Get RAM
            yield ram_req
            self.start_time = env.now #Get moment of access to RAM
            print(f"start_time: {self.start_time}")

            print(f"{env.now} {self.name} obtuvo {self.needed_ram} de RAM y esta ready")
            while(self.instructions > 0):

                with self.processor.request() as processor_req:
                    yield processor_req
                    #self.start_time = env.now #Get moment of access to CPU
                    #print(f"start_time: {self.start_time}")
                    print(f"{env.now} {self.name} obtuvo acceso al CPU")

                    if(self.instructions < CPU_INSTRUCTIONS_PER_CYCLE):
                        yield env.timeout(CPU_FAST_CYCLE_TIME)
                        self.instructions = 0
                        print(f"{env.now} {self.name} libera CPU antes de tiempo pues tiene menos de {CPU_INSTRUCTIONS_PER_CYCLE} instrucciones")

                        #self.end_time = env.now #Get moment of leaving CPU
                        #print(f"end_time: {self.end_time}")
                    else:
                        yield env.timeout(CPU_CYCLE_TIME)
                        self.instructions = self.instructions - CPU_INSTRUCTIONS_PER_CYCLE
                        print(f"{env.now} {self.name} sale del CPU con {self.instructions} instrucciones restantes")

                        
                        #self.end_time = env.now #Get moment of leaving CPU
                        #print(f"end_time: {self.end_time}")

                #self.total_time = self.total_time + (self.end_time - self.start_time )
                #print(f"total_time: {self.total_time}") #Add current cycle time

                needs_io = random.randint(1,2)
                if(needs_io == 1 and self.instructions > 0):
                    print(f"{env.now} dv {self.name} solicita IO...")
                    yield env.timeout(IO_TIMEOUT)

        with self.available_ram.put(self.needed_ram) as ram_deposit:
            yield ram_deposit
        self.end_time = env.now #Get moment of liberating RAM
        print(f"end_time: {self.end_time}")
        self.total_time = self.total_time + (self.end_time - self.start_time )
        print(f"total_time: {self.total_time}") #Add current cycle time
        self.writer.writerow([self.name, self.total_time, self.needed_ram])
        print(f"{env.now} {self.name} termina por completo y debería liberar {self.needed_ram} de RAM")

def simulation(env, available_ram, processor, program_amount, writer):
    for i in range(program_amount):

        name = f"process_{i}"
        needed_ram = random.randint(1, MAX_RAM)
        instructions = random.randint(1, MAX_INSTRUCTIONS)
        newProgram = Program(name, env, instructions, needed_ram, available_ram, processor,writer)

        env.process(newProgram.run())
        yield env.timeout(random.expovariate(1.0/10))



#Inciso a

#---------------------------------------------------------------------25 procesos ---------------------------------------------------------------------
env = simpy.Environment()
processor = simpy.Resource(env, capacity=1)
available_ram = simpy.Container(env, init = 100, capacity=100)
program_amount = 25

with open("25Process.csv", "w") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Process", "Time"])
    env.process(simulation(env, available_ram, processor, program_amount, csv_writer))
    env.run()

#---------------------------------------------------------------------50 procesos---------------------------------------------------------------------
# env = simpy.Environment()
# processor = simpy.Resource(env, capacity=1)
# available_ram = simpy.Container(env, init = 100, capacity=100)
# program_amount = 50

# env.process(simulation(env, available_ram, processor, program_amount))
# env.run()

#---------------------------------------------------------------------100 procesos---------------------------------------------------------------------

# env = simpy.Environment()
# processor = simpy.Resource(env, capacity=1)
# available_ram = simpy.Container(env, init = 100, capacity=100)
# program_amount = 100

# env.process(simulation(env, available_ram, processor, program_amount))
# env.run()

#---------------------------------------------------------------------150 procesos---------------------------------------------------------------------

# env = simpy.Environment()
# processor = simpy.Resource(env, capacity=1)
# available_ram = simpy.Container(env, init = 100, capacity=100)
# program_amount = 150

# env.process(simulation(env, available_ram, processor, program_amount))
# env.run()

#---------------------------------------------------------------------200 procesos---------------------------------------------------------------------

# env = simpy.Environment()
# processor = simpy.Resource(env, capacity=1)
# available_ram = simpy.Container(env, init = 100, capacity=100)
# program_amount = 200

# env.process(simulation(env, available_ram, processor, program_amount))
# env.run()

























