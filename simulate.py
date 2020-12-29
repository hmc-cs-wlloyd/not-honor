import random

def simulate(years, equipment_totals):
            
    dead = False

    for i in range(int(years/200)):
        current_year = 2000+(200*(i+1))
        usability, visibility, likability, respectability, \
        understandability = get_stats(current_year, equipment_totals)
        
        print("year is " + str(current_year) + " and stats are")
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
                  ", so mining did happen by year " + str(current_year))
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
                  ", so archaeology did happen by year " + str(current_year))
            dead = True
            return dead
        else:
            print("I rolled " + str(arch_die) +
                  ", so no archaeology happened by year " + str(current_year))
            
        if current_year > 5000:
            aliens = alien_prob(sot, current_year)
            print("200 year prob of aliens is " + str(aliens))
            alien_die = random.random()
            if alien_die < aliens:
                print("I rolled " + str(alien_die) +
                 ", so aliens attacked by year " + str(current_year))
                dead = True
                return dead
            else:
                print("I rolled " + str(alien_die) +
                 ", so no aliens happened by year " + str(current_year))
                                

    return dead
        
        
        
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

def get_stats(equipment_totals, current_year):
    #PLACEHOLDER
    usability = random.random()
    visibility = random.random()
    likability = random.random()
    respectability = random.random()
    understandability = random.random()
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
    
    bhr = .05 #magic! was 83 in source, but then you always lose

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

def alien_prob(state_of_tech, start_year):
    """gives total probability of destructive alien contact over 200 years,
    given start year"""
    if state_of_tech == 2:
        prob = .05
    elif state_of_tech == 1:
        prob = .01
    else:
        prob = 0
    return prob
