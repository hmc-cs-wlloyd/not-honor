"""Contains simulation code to test whether a nuclear waste site with a given set of markers remains undisturbed"""

import random
import math
from marker import markers

LOW_TECH = 0
MEDIUM_TECH = 1
HIGH_TECH = 2

def simulate(years, site_map, global_buffs): #pylint: disable=too-many-locals,too-many-statements
    """Runs the simulation"""

    dead = False
    out_strings = []

    for i in range(int(years/200)):
        current_year = 2000+(200*(i+1))
        print("Simulating to " + str(current_year))

        sot = state_of_tech(current_year)
        print("state of tech is " + str(sot))

        usability, visibility, respectability, likability, \
        understandability = get_stats(site_map, global_buffs, current_year, sot)

        usability, visibility, respectability, likability, \
        understandability = get_adjacency_bonus(site_map,usability, visibility, \
        respectability, likability, understandability)

        print("usability, visibility, respectability, likability, understandability:")
        print(usability, visibility,respectability,  likability,
              understandability)

        kop = get_knowledge_of_past(visibility, respectability, likability,
                      understandability)
        print("knowledge of past is " + str(kop))

        vom = get_value_of_materials(current_year)
        print ("value of materials is " + str(vom))

        miners = miner_prob(kop, vom, 200)
        print("200 year probability of mining is " + str(miners))
        mine_die = random.random()
        if mine_die < miners:
            mine_year = current_year - random.randint(1,199)
            print("I rolled " + str(mine_die) +
                  ", so mining did happen in year " +
                  str(mine_year))
            dead = True
            out_strings.append("Year " + str(mine_year) + ": miners breached the site!")
            return dead, out_strings
        print("I rolled " + str(mine_die) +
              ", so no mining happened by year " + str(current_year))

        archaeologists = arch_prob(kop, current_year-200)
        print("200 year probability of archaeologists is " +
              str(archaeologists))
        arch_die = random.random()
        if arch_die < archaeologists:
            arch_year = current_year - random.randint(1,199)
            print("I rolled " + str(arch_die) +
                  ", so archaeology did happen in year " +
                  str(arch_year))
            dead = True
            out_strings.append("Year " + str(arch_year) + ": archaelogists breached the site!")
            return dead, out_strings
        print("I rolled " + str(arch_die) +
              ", so no archaeology happened by year " + str(current_year))

        dams = dam_prob(kop, usability, current_year-200)
        print("200 year probability of dam builders is " +
              str(dams))
        dam_die = random.random()
        if dam_die < dams:
            dam_year = current_year - random.randint(1,199)
            print("I rolled " + str(dam_die) +
                  ", so dam bulidng did happen in year " +
                  str(dam_year))
            dead = True
            out_strings.append("Year " + str(dam_year) + ": dam builders breached the site!")
            return dead, out_strings
        print("I rolled " + str(dam_die) +
              ", so no dam building happened by year " + str(current_year))

        teens = teen_prob(visibility, respectability)
        print("200 year probability of teens is " +
              str(teens))
        teen_die = random.random()
        if teen_die < teens:
            teen_year = current_year - random.randint(1,199)
            print("I rolled " + str(teen_die) +
                  ", so teens did happen in year " +
                  str(teen_year))
            dead = True
            out_strings.append("Year " + str(teen_year) + ": teens breached the site!")
            return dead, out_strings
        print("I rolled " + str(teen_die) +
              ", so no teens happened by year " + str(current_year))

        transit_tunnel = transit_tunnel_prob(sot, understandability, visibility)
        print("200 year probability of transit tunnel is " + str(transit_tunnel))
        transit_tunnel_die = random.random()
        if transit_tunnel_die < transit_tunnel:
            transit_tunnel_year = current_year - random.randint(1, 199)
            print("I rolled " + str(transit_tunnel_die) + ", so a transit tunnel breached the site in year " +str(
                transit_tunnel_year))
            dead = True
            out_strings.append(
                "Year " + str(transit_tunnel_year) + ": site breached during the construction of a transit tunnel!")
            return dead, out_strings
        print("I rolled " + str(transit_tunnel_die) + ", so no transit tunnel disrupted the site by year " + str(
            current_year))

        event, event_year = get_random_event(current_year, sot, site_map)
        if event != "":
            print ("In the year " + str(event_year) + ", " + str(event) +
                    " happened!")
            print()
            out_strings.append("Year "+ str(event_year) + ": " + str(event) + " happened!")
        print("Nothing interesting happened")
        print()

    return dead, out_strings

def get_random_event(current_year, sot, site_map):
    """Potentially generates an event given a year"""

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

    elif any("bad-cult" in row for row in site_map) and \
         current_year > 3000 and die <.5:
        event = "cult-dig"

    return event, event_year

def get_knowledge_of_past(visibility, respectability, likability,
                      understandability):
    '''returns 3 for precise knowledge, 2 for location only, 1 for myth,
    0 for none'''
    #note: usability does not come into this calculation
    #this is a deterministic calculation - no dice!

    kop = 0
    if understandability > 5:
        kop = 3
    elif visibility > 4:
        kop = 2
    elif likability > 3 or respectability > 3:
        kop = 1
    #else 0
    return kop



def get_value_of_materials(current_year):
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


def get_stats(site_map, global_buffs, current_year,sot): #pylint: disable=too-many-branches
    """gives the 5 stats given your equipment, year, and state of tech"""

    usability = 1
    visibility = 0
    likability = 0
    respectability = 0
    understandability = 0

    for buff in global_buffs:
        values_list = get_stats_for_marker(buff, current_year, sot)

        usability += values_list[0]
        visibility += values_list[1]
        respectability += values_list[2]
        likability += values_list[3]
        understandability += values_list[4]

    for row in site_map:
        for entry in row:
            values_list = get_stats_for_marker(entry, current_year, sot)

            usability += values_list[0]
            visibility += values_list[1]
            respectability += values_list[2]
            likability += values_list[3]
            understandability += values_list[4]

    #some stats are dependent on visibility
    if visibility < .1:
        respectability *= .1
        likability *= .1
        understandability *= .1
    elif visibility <1:
        respectability *= .8
        likability *= .8
        understandability *= .8

    return usability, visibility, respectability, likability,  understandability

def get_stats_for_marker(marker_id, current_year, sot):
    """Gets the stats for a particular marker, adjusted for decay and state of technology"""
    inits_list = [markers[marker_id].usability_init, markers[marker_id].visibility_init,
                  markers[marker_id].respectability_init, markers[marker_id].likability_init,
                  markers[marker_id].understandability_init]
    decays_list =[markers[marker_id].usability_decay, markers[marker_id].visibility_decay,
                  markers[marker_id].respectability_decay, markers[marker_id].likability_decay,
                  markers[marker_id].understandability_decay]
    values_list = []

    for j in range(len(inits_list)): #pylint: disable=consider-using-enumerate
        init_val = inits_list[j][sot]

        if decays_list[j] == "constant":
            values_list.append(init_val)
        elif decays_list[j] == "slow_lin_0":
            values_list.append(-.0008*(current_year-2000) + init_val)
        elif decays_list[j] == "lin_0":
            values_list.append(-.002*(current_year-2000) + init_val)
        elif decays_list[j] == "fast_lin_0":
            values_list.append(-.005*(current_year-2000) + init_val)
        elif decays_list[j] == "slow_lin_inc_8":
            values_list.append(.0002*(current_year-2000) + init_val)
        elif decays_list[j] == "slow_lin_inc_3":
            values_list.append(.0003*(current_year-2000) + init_val)
        elif decays_list[j] == "exp_0":
            values_list.append(init_val*math.exp(-.001*(current_year-2000)))
        elif decays_list[j] == "exp_neg_10":
            values_list.append((init_val+10)*math.exp(-.001*(current_year-2000))-10)
        elif decays_list[j] == "tech_curve":
            if sot == 0:
                values_list.append((init_val+5)*math.exp(-.005*(current_year-2000))-5)
            else:
                values_list.append(.0005*(current_year-2000) + init_val)

    return values_list

def get_adjacency_bonus(site_map,usability, visibility, respectability, likability, #pylint: disable=too-many-arguments, too-many-branches
        understandability):
    """checks if anything on the map gets adjacency bonus and modifies stats directly"""
    #right now, just checking for a vis bonus tag and giving bonus to vis
    vis_neighbors = 0
    for row_num in range(len(site_map)): #pylint: disable=consider-using-enumerate
        for tile_num in range(len(site_map[row_num])):
            tile_tags = markers[site_map[row_num][tile_num]].tags
            if "adj-bonus" in tile_tags:
                #left neighbor
                if tile_num>0:
                    if "vis-adj-bonus" in markers[site_map[row_num][tile_num-1]].tags:
                        neighbors += 1
                #right neighbor
                if tile_num < len(site_map[row_num]) -1:
                    if "vis-adj-bonus" in markers[site_map[row_num][tile_num+1]].tags:
                        neighbors += 1
                #top neighbor
                if row_num > 0:
                    if "vis-adj-bonus" in markers[site_map[row_num-1][tile_num]].tags:
                        neighbors += 1
                #bottom neighbor
                if row_num < len(site_map) -1:
                    if "vis-adj-bonus" in markers[site_map[row_num+1][tile_num]].tags:
                        neighbors += 1
                #top left
                if tile_num>0 and row_num>0:
                    if "vis-adj-bonus" in markers[site_map[row_num-1][tile_num-1]].tags:
                        neighbors += 1
                #top right
                if tile_num < len(site_map[row_num]) -1 and row_num>0:
                    if "vis-adj-bonus" in markers[site_map[row_num-1][tile_num+1]].tags:
                        neighbors += 1
                # bottom left
                if tile_num>0 and row_num < len(site_map) -1:
                    if "vis-adj-bonus" in markers[site_map[row_num+1][tile_num-1]].tags:
                        neighbors += 1
                #bottom right
                if len(site_map[row_num]) -1 and row_num < len(site_map) -1:
                    if "vis-adj-bonus" in markers[site_map[row_num+1][tile_num+1]].tags:
                        neighbors += 1

    vis_neighbors = vis_neighbors/2
    visibility += vis_neighbors
    return usability, visibility, respectability, likability, understandability

def miner_prob(knowledge_of_past, value_of_materials, years): #pylint: disable=too-many-branches
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
            prob = .2
        else:
            prob = .3
    else:
        if start_year < 2300:
            prob = .01
        elif start_year < 5000:
            prob = .05
        else:
            prob = .01

    return prob

def dam_prob(knowledge_of_past, usability, start_year):
    """gives total prob of at least one dam construction over 200 years"""
    if knowledge_of_past == 3:
        prob = 0
    elif start_year < 2300:
        if usability > 1:
            prob = .02
        elif usability > 0:
            prob = .01
        else:
            prob= .005
    elif start_year < 5000:
        if usability > 1:
            prob = .03
        elif usability > 0:
            prob = .02
        else:
            prob = .01
    else:
        if usability > 1:
            prob = .05
        elif usability > 0:
            prob = .04
        else:
            prob = .03
    return prob

def teen_prob(visibility, respectability):
    """gives total prob of random teen violence breaching the site"""
    if visibility < 3 or respectability > 8:
        prob = 0
    elif respectability > 6:
        prob = .001
    elif respectability > 3:
        prob = .01
    else:
        prob = .03
    return prob

def transit_tunnel_prob(state_of_technology, understandability, visibility):
    """gives the probability of a transit tunnel being built through the site in a 200 year period"""
    awareness_of_danger = understandability*visibility
    base_probability = 0
    if state_of_technology == LOW_TECH:
        base_probability = 0
    elif state_of_technology == MEDIUM_TECH:
        base_probability = .001
    else:
        base_probability = .1
    return base_probability*(1-(awareness_of_danger/100))
