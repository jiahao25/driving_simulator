class Field:
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def within_boundary(self,curr_x,curr_y):
        if 0 <= curr_x < self.width and 0 <= curr_y < self.height:
            return True
        else:
            return False
        
class CarStates:
    def __init__(self,car_init_state):
        self.car_curr_state = car_init_state

    def return_state(self,car_name,var):
        if var == 'x':
            return self.car_curr_state[car_name][0]
        elif var == 'y':
            return self.car_curr_state[car_name][1]
        elif var == 'dir':
            return self.car_curr_state[car_name][2]
        elif var == 'state':
            return self.car_curr_state[car_name][3]
        elif var == 'collide_with':
            return self.car_curr_state[car_name][4]
        elif var == 'collide_turn':
            return self.car_curr_state[car_name][5]
        
    def update_state(self, car_name, var, val):
        if var == 'x':
            self.car_curr_state[car_name][0] = val
        elif var == 'y':
            self.car_curr_state[car_name][1] = val
        elif var == 'dir':
            self.car_curr_state[car_name][2] = val
        elif var == 'state':
            self.car_curr_state[car_name][3] = val
        elif var == 'collide_with':
            self.car_curr_state[car_name][4].append(val)
        elif var == 'collide_turn':
            self.car_curr_state[car_name][5].append(val)
        
class Car:
    def __init__(self,name,init_x,init_y,init_dir,commands,car_states,field):
        self.name = name
        self.init_x = init_x
        self.init_y = init_y
        self.init_dir = init_dir
        self.commands = commands
        self.car_states = car_states
        self.field = field

    def move(self,turn):

        # retrieve current values
        curr_x = self.car_states.return_state(self.name,'x')
        curr_y = self.car_states.return_state(self.name,'y')
        curr_dir = self.car_states.return_state(self.name,'dir')
        curr_state = self.car_states.return_state(self.name,'state')

        other_car = []
        other_car_pos = []
        for car, state_list in self.car_states.car_curr_state.items():
            if car != self.name:
                other_car.append(car)
                other_car_pos.append((state_list[0],state_list[1]))

        if curr_state == 'collided':
            #print('Turn: {}, Name: {}, Status: {}, Action: No move (collided), Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,curr_state,curr_x,curr_y,curr_dir))
            pass
        elif curr_state == 'stopped':
            #print('Turn: {}, Name: {}, Status: {}, Action: No move (no more commands), Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,curr_state,curr_x,curr_y,curr_dir))
            pass
        else: # state = 'moving'
            if len(self.commands) == 0 or turn+1 == len(self.commands):
                self.car_states.update_state(self.name,'state','stopped')

            if self.commands[turn] == 'F':
                # determine next movement coordinates
                if curr_dir == 'N':
                    next_pos_x = curr_x
                    next_pos_y = curr_y + 1
                elif curr_dir == 'S':
                    next_pos_x = curr_x
                    next_pos_y = curr_y - 1
                elif curr_dir == 'E':
                    next_pos_x = curr_x + 1
                    next_pos_y = curr_y
                elif curr_dir == 'W':
                    next_pos_x = curr_x - 1
                    next_pos_y = curr_y

                if self.field.within_boundary(next_pos_x,next_pos_y) == False: # if moving outside of boundary
                    #print('Turn: {}, Name: {}, Status: {}, Action: No move (due to boundary), Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,curr_state,curr_x,curr_y,curr_dir))
                    pass # no move
                elif (next_pos_x,next_pos_y) in other_car_pos: # collided to another vehicle
                    self.car_states.update_state(self.name,'x',next_pos_x)
                    self.car_states.update_state(self.name,'y',next_pos_y)
                    self.car_states.update_state(self.name,'state','collided')
                    next_state = self.car_states.return_state(self.name,'state')
                    for idx in range(len(other_car)):
                        if (next_pos_x,next_pos_y) == other_car_pos[idx]:
                            self.car_states.update_state(self.name,'collide_with',other_car[idx])
                            self.car_states.update_state(self.name,'collide_turn',turn+1)
                            self.car_states.update_state(other_car[idx],'state','collided')
                            self.car_states.update_state(other_car[idx],'collide_with',self.name)
                            self.car_states.update_state(other_car[idx],'collide_turn',turn+1)
                    #print('Turn: {}, Name: {}, Status: {}, Action: Moved forward and collided, Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,next_state,next_pos_x,next_pos_y,curr_dir))
                else: # move without collision
                    self.car_states.update_state(self.name,'x',next_pos_x)
                    self.car_states.update_state(self.name,'y',next_pos_y)
                    #print('Turn: {}, Name: {}, Status: {}, Action: Moved forward, Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,curr_state,next_pos_x,next_pos_y,curr_dir))

            elif self.commands[turn] == 'L':
                if curr_dir == 'N':
                    next_dir = 'W'
                    self.car_states.update_state(self.name,'dir',next_dir)
                elif curr_dir == 'W':
                    next_dir = 'S'
                    self.car_states.update_state(self.name,'dir',next_dir)
                elif curr_dir == 'S':
                    next_dir = 'E'
                    self.car_states.update_state(self.name,'dir',next_dir)
                elif curr_dir == 'E':
                    next_dir = 'N'
                    self.car_states.update_state(self.name,'dir',next_dir)
                #print('Turn: {}, Name: {}, Status: {}, Action: Turned left, Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,curr_state,curr_x,curr_y,next_dir))
                
            elif self.commands[turn] == 'R':
                if curr_dir == 'N':
                    next_dir = 'E'
                    self.car_states.update_state(self.name,'dir',next_dir)
                elif curr_dir == 'E':
                    next_dir = 'S'
                    self.car_states.update_state(self.name,'dir',next_dir)
                elif curr_dir == 'S':
                    next_dir = 'W'
                    self.car_states.update_state(self.name,'dir',next_dir)
                elif curr_dir == 'W':
                    next_dir = 'N'
                    self.car_states.update_state(self.name,'dir',next_dir)
                #print('Turn: {}, Name: {}, Status: {}, Action: Turn right, Coordinates: ({},{}), Direction: {}'.format(turn + 1,self.name,curr_state,curr_x,curr_y,next_dir))

    
class Simulation:
    def __init__(self):
        self.field = None
        self.car_name_list = [] 
        self.car_init_state = {} # {'carA':[init_pos_x,init_pos_y,state,collide_with,collide_turn,car_states], 'carB':[init_pos_x,init_pos_y,state,collide_with,collide_turn,car_states],..}


    def start_program(self):
        print("\nWelcome to Auto Driving Car Simulation! ")

        # create field dimensions
        while True:
            field_input = input("\nPlease enter the width and height of the simulation field in x y format: ")
            try:
                width = int(field_input.split()[0])
                height = int(field_input.split()[1])
                self.create_field(width,height)
                break
            except ValueError and IndexError:
                print("\nInvalid input")

        # player menu to add cars / start simulation
        menu = True
        max_commands = 0
        
        while menu == True:
            menu = self.option_menu()
            print('\nYour current list of cars are:')
            for idx in range(len(self.car_name_list)):
                print('- {}, ({},{}) {}, {}'.format(self.car_name_list[idx].name,self.car_name_list[idx].init_x,self.car_name_list[idx].init_y,self.car_name_list[idx].init_dir,self.car_name_list[idx].commands))
                if len(self.car_name_list[idx].commands) > max_commands:
                    max_commands = len(self.car_name_list[idx].commands)

        # Start Simulation
        print('\nStart Simulation')
        for car, init_state in self.car_init_state.items():
            print('Turn: 0, Name: {}, Coordinates: ({},{}), Direction: {}'.format(car,init_state[0],init_state[1],init_state[2]))
        car_states = CarStates(self.car_init_state)
        for car in self.car_name_list:
            car.car_states = car_states

        for turn in range(max_commands):
            for car in self.car_name_list:
                car.move(turn)

        # End Simulation
        print('\nAfter simulation, the result is:')
        all_car_states = car_states.car_curr_state
        for car, state_list in all_car_states.items():
            #print(car, state_list)
            if state_list[3] == 'collided':
                print('- {}, collides with {} at ({},{}) at step {}'.format(car,str(state_list[4]).strip('[]'),state_list[0],state_list[1],str(state_list[5]).strip('[]')))
            else: # car did not collide with other cars
                print('- {}, ({}.{}) {}'.format(car,state_list[0],state_list[1],state_list[2]))
        
        # Ask the user if they want to restart or exit
        while True:
            restart = input('\nPlease choose from the following options:\n[1] Start over\n[2] Exit\n')
            if restart == '1':
                return True  # Restart the simulation
            elif restart == '2':
                return False  # Exit the simulation
            else:
                print('\nInvalid input. Please choose 1 or 2.')

    def create_field(self,width,height):
        self.field = Field(width,height)
        print("\nYou have created a field of {} x {}.".format(width,height))

    def option_menu(self):
        choose = input("\nPlease choose from the following options:\n[1] Add a car to field\n[2] Run simulation\n")
        if choose == '1':
            car_commands = self.add_car(self.field.width,self.field.height)
            return True
        elif choose == '2':
            if len(self.car_name_list) == 0:
                print('\nNo cars added. Please at least add one car.')
                return True
            return False
        else:
            print('\nInvalid output')

    def add_car(self,width,height):
        # input car name
        while True:
            car_name = input("\nPlease enter the name of the car: ")
            if car_name == '':
                print('\nCar name cannot be empty')
            elif car_name in self.car_name_list:
                print("\nName already chosen. Choose another.")
            else:
                self.car_name_list.append(car_name)
                break
        
        # input car starting position and direction
        while True:
            car_start_pos = input("\nPlease enter initial position of car {} in x y Direction format: ".format(car_name))
            try:
                car_start_x = int(car_start_pos.split()[0])
                car_start_y = int(car_start_pos.split()[1])
                car_start_dir = car_start_pos.split()[2]

                if self.field.within_boundary(car_start_x,car_start_y) == True and car_start_dir in ['N','S','E','W']:
                    if [car_start_x, car_start_y, car_start_dir, 'moving',[],[]] in self.car_init_state.values():
                        print('\nCar spot already taken by another vehicle')
                    else:
                        self.car_init_state[car_name] = [car_start_x,car_start_y,car_start_dir,'moving',[],[]]
                        break
                elif car_start_dir not in ['N','S','E','W']:
                    print('\nPlease provide valid input for direction')
                else:
                    print('\nCar is out of boundary')
            
            except ValueError and IndexError:
                print("\nInvalid Input")

        # input car commands
        while True:
            invalid_command = 0
            car_commands = input('\nPlease enter the commands for car {}: '.format(car_name))
            for char in car_commands:
                if char not in ['F','L','R']:
                    invalid_command += 1
            if invalid_command == 0:
                break
            else:
                print('\nInvalid Commands')
    
        self.car_name_list[-1] = Car(car_name,car_start_x,car_start_y,car_start_dir,car_commands,None,self.field)

def main():
    while True:
        simulation = Simulation()
        restart = simulation.start_program() 
        if not restart:
            print('\nThank you for running the simulation. Goodbye!')
            break

if __name__ == '__main__':
    main()
