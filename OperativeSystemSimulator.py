import random
import simpy 

MAX_RAM = 10
MAX_INSTRUCTIONS = 10
CPU_CYCLE = 3
CPU_INSTRUCTIONS_PER_CYCLE = 3
IO_TIMEOUT = 5

random.seed(1)

class Program:

    def __init__(self, name, env, instructions, needed_ram, available_ram, processor):
        self.env = env
        self.name = name
        self.instructions = instructions
        self.needed_ram = needed_ram
        self.available_ram = available_ram
        self.processor = processor


    def run(self):
        with self.available_ram.get(self.needed_ram) as ram_req: #Get RAM
            yield ram_req

            print(f"{env.now} {self.name} obtuvo {self.needed_ram} de RAM y esta ready")
            while(self.instructions > 0):

                with self.processor.request() as processor_req:
                    yield processor_req
                    print(f"{env.now} {self.name} obtuvo acceso al CPU")

                    if(self.instructions < CPU_INSTRUCTIONS_PER_CYCLE):
                        self.instructions = 0
                        print(f"{env.now} {self.name} libera CPU antes de tiempo pues tiene menos de {CPU_INSTRUCTIONS_PER_CYCLE} instrucciones")
                    else:
                        self.instructions = self.instructions - CPU_INSTRUCTIONS_PER_CYCLE
                        print(f"{env.now} {self.name} sale del CPU con {self.instructions} instrucciones restantes")
                        yield env.timeout(CPU_CYCLE)

                needs_io = random.randint(1,2)
                if(needs_io == 1 and self.instructions > 0):
                    print(f"{env.now} {self.name} solicita IO...")
                    yield env.timeout(IO_TIMEOUT)

        print(f"{env.now} {self.name} termina por completo y debería liberar {self.needed_ram} de RAM")



def simulation(env, available_ram, processor, program_amount):
    for i in range(program_amount):

        name = f"process_{i}"
        needed_ram = random.randint(1, 10)
        instructions = random.randint(1, MAX_INSTRUCTIONS)
        newProgram = Program(name, env, instructions, needed_ram, available_ram, processor)

        env.process(newProgram.run())
        yield env.timeout(random.expovariate(1.0/10))

env = simpy.Environment()
processor = simpy.Resource(env, capacity=1)
available_ram = simpy.Container(env, init = 100, capacity=100)
program_amount = 5

env.process(simulation(env, available_ram, processor, program_amount))
env.run()
























