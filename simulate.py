import random
from marker import markers

def simulate(years, equipment_list):
            
    dead = False

    for i in range(int(years/200)):
        current_year = 2000+(200*(i+1))
        usability, visibility, likability, respectability, \
        understandability = get_stats(equipment_list, current_year)
        
        print("Simulating to " + str(current_year) + " and stats are")
        print(usability, visibility, likability, respectability,
              understandability)
        
        kop = knowledge_of_past(visibility, respectability, likability,
                      understandability)
        print("knowledge of past is " + str(kop))

        vom = value_of_materials(current_year)
        print ("value of materials is " + str(vom))

        sot = state_of_tech(current_year)
        print("state of tech is " + str(sot))

        miners = miner_prob(kop, vom, 200)
        print("200 year probability of mining is " + str(miners))
        mine_die = random.random()
        if mine_die < miners:
            print("I rolled " + str(mine_die) +
                  ", so mining did happen in year " +
                  str(current_year - random.randint(1,199)))
            dead = True
            return dead
        else:
            print("I rolled " + str(mine_die) +
                  ", so no mining happened by year " + str(current_year))

        archaeologists = arch_prob(kop, current_year-200)
        print("200 year probability of archaeologists is " +
              str(archaeologists))
        arch_die = random.random()
        if arch_die < archaeologists:
            print("I rolled " + str(arch_die) +
                  ", so archaeology did happen in year " +
                  str(current_year - random.randint(1,199)))
            dead = True
            return dead
        else:
            print("I rolled " + str(arch_die) +
                  ", so no archaeology happened by year " + str(current_year))

        event, event_year = get_random_event(current_year, sot)
        if event != "":
             print ("In the year " + str(event_year) + ", " + str(event) +
                    " happened!")
             print()
        else:
            print("Nothing interesting happened")
            print()

    return dead
        
def get_random_event(current_year, sot):

    event = ""
    #generate a year for the thing to have happened i 
    event_year = current_year - random.randint(0,199)
    
    
    die = random.random()

    if current_year > 5000 and sot == 2:
        if die < .05:
            event = "aliens"

    elif current_year > 2400:
        if die < .1:
            event = "culture_shift"

    elif current_year > 2600 and sot == 0:
        if die < .1:
            event = "vikings"

    elif die < .2:
        event = "earthquake"
    
    return event, event_year
        
def knowledge_of_past(visibility, respectability, likability,
                      understandability):
    '''returns 3 for precise knowledge, 2 for location only, 1 for myth,
    0 for none'''
    #note: usability does not come into this calculation
    #this is a deterministic calculation - no dice!
    
    kop = 0
    if understandability > .9:
        kop = 3
    elif visibility > .8:
        kop = 2
    elif likability > .7 or respectability > .7:
        kop = 1
    #else 0
    return kop
        
    

def value_of_materials(current_year):
    '''returns 1 if materials have high value, 0 if low'''
    #probabilities taken roughly from WIPP report
    if current_year < 2300:
        vom = random.randint(0,1)
    else:
        die = random.random()
        if die < .33:
            vom = 1
        else:
            vom = 0
    return vom
        

def state_of_tech(current_year):
    '''returns 0 for low tech, 1 for med, 2 for high'''
    #probabilities taken exactly from WIPP report
    die = random.random()
    if current_year <= 2300:
        if die <= .8:
            tech = 2
        elif die <= .95:
            tech =1
        else:
            tech =0
    elif current_year <= 5000:
        if die <= .7:
            tech = 2
        elif die <= .9:
            tech =1
        else:
            tech =0
    else:
        if die <=.8:
            tech = 2
        elif die <= .9:
            tech = 1
        else:
            tech = 0
    return tech


def get_stats(equipment_list, current_year):
    """gives the 5 stats given your equipment and the year"""
    
    usability = 1
    visibility = 0
    likability = 0
    respectability = 0
    understandability = 0
    
    for i in equipment_list:
        usability += markers[i].usability
        visibility += markers[i].visibility
        understandability += markers[i].understandability
        respectability += markers[i].respectability
        likability += markers[i].likability

    #some stats are dependent on visibility
    if visibility < 1:
        respectability *= .1
        likability *= .1
        understandability *= .1
    elif visibility <10:
        respectability *= .8
        likability *= .8
        understandability *= .8

    return usability, visibility, likability, respectability, understandability


def miner_prob(knowledge_of_past, value_of_materials, years):
    """gives probability that a miner digs a bad hole in the given time span"""
    
    #calculate value_multiplier - probabilistic
    die = random.random()
    if value_of_materials == 1: #high value
        if die <= .19:
            value_multiplier = .25
        elif die <= .38:
            value_multiplier = .5
        elif die <= .88:
            value_multiplier = 1
        elif die <= .94:
            value_multiplier = 2
        else:
            value_multiplier = 4
    else:
        if die <= .35:
            value_multiplier = .01
        elif die <= .85:
            value_multiplier = .1
        elif die <= .925:
            value_multiplier = .25
        else:
            value_multiplier = .5
    #print("value multiplier is " + str(value_multiplier))
        
    # calculate knowlege_multiplier - deterministic
    if knowledge_of_past == 3:
        knowledge_multiplier = .6
    elif knowledge_of_past == 2:
        knowledge_multiplier = .6
    elif knowledge_of_past == 1:
        knowledge_multiplier = .6
    else:
        knowledge_multiplier = 1
    
    bhr = .1 #magic! was 83 in source, but then you always lose

    #drill rate is the avg # of bores per sq m per 1000 yrs
    drill_rate = bhr * value_multiplier * knowledge_multiplier
    #print("drill rate is " + str(drill_rate))

    area = 16 #sqare milage from doc

    prob_per_year = (drill_rate*area)/1000
    #print("yearly probability is " + str(prob_per_year))

    prob = 1-((1-prob_per_year)**years)
    #print("total probability of mining is " + str(prob))

    return prob


def arch_prob(knowledge_of_past, start_year):
    """gives total probability of at least one disruptive archaeological
    dig over 200 years, given start year"""
    #should also take state_of_technology?
    if knowledge_of_past == 3:
        prob = 0
    elif knowledge_of_past == 2:
        if start_year < 2300:
            prob = 0
        elif start_year < 5000:
            prob = .05
        else:
            prob = .1
    elif knowledge_of_past == 1:
        if start_year < 2300:
            prob = .05
        elif start_year < 5000:
            prob = .1
        else:
            prob = .2
    else:
        if start_year < 2300:
            prob = .01
        elif start_year < 5000:
            prob = .05
        else:
            prob = .01
            
    return prob


