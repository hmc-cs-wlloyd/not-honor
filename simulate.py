"""Contains simulation code to test whether a nuclear waste site with a given set of markers remains undisturbed"""

import copy
import random
import math
from marker import markers

LOW_TECH = 0
MEDIUM_TECH = 1
HIGH_TECH = 2

def simulate(years, site_map, global_buffs): #pylint: disable=too-many-locals,too-many-statements,too-many-return-statements
    """Runs the simulation"""

    dead = False
    event_list = [(0, "null")]
    map_list = [site_map]
    stats_list = []
    time_period_map = copy.deepcopy(site_map)
    #set default stats
    usability, visibility, respectability, likability, \
        understandability = (10,0,0,0,0)

    #initial values for "close to death-ness"
    mining_margin = 1
    archaeology_margin = 1
    dam_margin = 1
    teen_margin = 1
    tunnel_margin = 1


    for i in range(int(years/200)):

        current_year = 2000+(200*(i+1))
        print("Simulating to " + str(current_year))

        sot = state_of_tech(current_year)
        print("state of tech is " + str(sot))

        usability, visibility, respectability, likability, \
        understandability = get_stats(time_period_map, global_buffs, current_year, sot, event_list)
        if len(event_list) > len(stats_list):
            stats_list.append((usability, visibility, respectability, likability, understandability))

        event, event_year = get_random_event(current_year, sot, site_map,usability,
                                             visibility, respectability, likability, understandability,
                                             global_buffs)
        if event != "":
            print ("In the year " + str(event_year) + ", " + str(event) +
                    " happened!")
            event_list.append((event_year, event))
            stats_list.append((usability, visibility, respectability, likability, understandability))
            vikings = (event =="vikings")
            earthquake = (event == "earthquake")
            faultline = (event == "faultline")
            if vikings or earthquake or faultline:
                time_period_map = get_modified_map(time_period_map, vikings, earthquake, faultline)
            map_list.append(time_period_map)

        #handle instakill events
        if any("aliens" in tup for tup in event_list) or any("cult-dig" in tup for tup in event_list):
            dead = True
            margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}
            map_list.append(time_period_map)
            return dead, event_list, map_list, margins_dict, stats_list

        #handle events that change the map


        print("usability, visibility, respectability, likability, understandability:")
        print(usability, visibility,respectability,  likability,
              understandability)

        kop = get_knowledge_of_past(visibility, respectability, likability,
                      understandability)
        print("knowledge of past is " + str(kop))

        vom = get_value_of_materials(current_year)
        print ("value of materials is " + str(vom))

        miners = miner_prob(kop, vom, understandability, 200)
        print("200 year probability of mining is " + str(miners))
        mine_die = random.random()
        if mine_die < miners:
            mine_year = random.randint(event_year+1,current_year)
            print("I rolled " + str(mine_die) +
                  ", so mining did happen in year " +
                  str(mine_year))
            event_list.append((mine_year, "miners"))
            stats_list.append((usability, visibility, respectability, likability, understandability))
            dead = True
            mining_margin = 0
            margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}
            map_list.append(time_period_map)
            return dead, event_list, map_list, margins_dict, stats_list
        print("I rolled " + str(mine_die) +
              ", so no mining happened by year " + str(current_year))
        mining_margin = min(mining_margin, mine_die-miners)

        archaeologists = arch_prob(kop, current_year-200, understandability)
        print("200 year probability of archaeologists is " +
              str(archaeologists))
        arch_die = random.random()
        if arch_die < archaeologists:
            arch_year = random.randint(event_year+1,current_year)
            print("I rolled " + str(arch_die) +
                  ", so archaeology did happen in year " +
                  str(arch_year))
            event_list.append((arch_year, "archaeologists"))
            stats_list.append((usability, visibility, respectability, likability, understandability))
            dead = True
            archaeology_margin = 0
            margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}
            map_list.append(time_period_map)
            return dead, event_list, map_list, margins_dict, stats_list
        print("I rolled " + str(arch_die) +
              ", so no archaeology happened by year " + str(current_year))
        archaeology_margin = min(archaeology_margin, arch_die-archaeologists)

        dams = dam_prob(kop, usability, current_year-200, understandability)
        print("200 year probability of dam builders is " +
              str(dams))
        dam_die = random.random()
        if dam_die < dams:
            dam_year = random.randint(event_year+1,current_year)
            print("I rolled " + str(dam_die) +
                  ", so dam bulidng did happen in year " +
                  str(dam_year))
            dead = True
            event_list.append((dam_year, "dams"))
            stats_list.append((usability, visibility, respectability, likability, understandability))
            dam_margin = 0
            margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}
            map_list.append(time_period_map)
            return dead, event_list, map_list, margins_dict, stats_list
        print("I rolled " + str(dam_die) +
              ", so no dam building happened by year " + str(current_year))
        dam_margin = min(dam_margin, dam_die-dams)

        teens = teen_prob(visibility, respectability, understandability)
        print("200 year probability of teens is " +
              str(teens))
        teen_die = random.random()
        if teen_die < teens:
            teen_year = random.randint(event_year+1,current_year)
            print("I rolled " + str(teen_die) +
                  ", so teens did happen in year " +
                  str(teen_year))
            dead = True
            teen_margin = 0
            event_list.append((teen_year, "teens"))
            stats_list.append((usability, visibility, respectability, likability, understandability))
            margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}
            map_list.append(time_period_map)
            return dead, event_list, map_list, margins_dict, stats_list
        print("I rolled " + str(teen_die) +
              ", so no teens happened by year " + str(current_year))
        teen_margin = min(teen_margin, teen_die-teens)

        transit_tunnel = transit_tunnel_prob(sot, understandability, visibility)
        print("200 year probability of transit tunnel is " + str(transit_tunnel))
        transit_tunnel_die = random.random()
        if transit_tunnel_die < transit_tunnel:
            transit_tunnel_year = random.randint(event_year+1,current_year)
            print("I rolled " + str(transit_tunnel_die) + ", so a transit tunnel breached the site in year " +str(
                transit_tunnel_year))
            dead = True
            event_list.append((transit_tunnel_year, "tunnel"))
            stats_list.append((usability, visibility, respectability, likability, understandability))
            tunnel_margin = 0
            margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}
            map_list.append(time_period_map)
            return dead, event_list, map_list, margins_dict, stats_list
        print("I rolled " + str(transit_tunnel_die) + ", so no transit tunnel disrupted the site by year " + str(
            current_year))
        tunnel_margin = min(tunnel_margin, transit_tunnel_die - transit_tunnel)

    margins_dict = {"mining": mining_margin,
                            "archaeology": archaeology_margin,
                            "dams":  dam_margin,
                            "teens": teen_margin,
                            "tunnels": tunnel_margin}

    return dead, event_list, map_list, margins_dict, stats_list

def get_random_event(current_year, sot, site_map,usability, visibility, respectability, likability, #pylint: disable=too-many-arguments,too-many-branches
        understandability, global_buffs):
    """Potentially generates an event given a year"""

    event = ""
    #generate a year for the thing to have happened i
    event_year = current_year - random.randint(0,199)

    
    die = random.random()
    print("bad cult? " + str(("bad-cult" in global_buffs)))
    print("current year: " + str(current_year))
    print(die)
    print('met dig conditions: ' + str(("bad-cult" in global_buffs) and current_year > 3000 and die <.5))
    num_monoliths =0
    for row in site_map:
        for tile in row:
            if "monolith" in markers[tile].tags:
                num_monoliths += 1

    if current_year > 5000 and sot == 2 and die < .000005:
            event = "aliens"

    elif current_year > 2400 and die < .01:
            event = "goths"

    elif current_year > 2600 and sot == 0 and die < .01:
            event = "vikings"

    elif die < .009:
        event = "earthquake"

    elif ("bad-cult" in global_buffs) and current_year > 3000 and die <.5:
        print("cult dig!!!")
        event = "cult-dig"

    elif die < .013:
        event = "faultline"

    elif ("bad-cult" in global_buffs) and ("ray-cats" in global_buffs)and \
         current_year > 3000 and die <.6:
        event = "cat-holics"

    elif num_monoliths > 5 and die <.04:
        event = "stonehenge"

    elif die < .019:
        event = "flood"


    elif sot == 1 and current_year < 3000 and die < .047:
        event = "klingon"

    elif sot == 2 and die < .03:
        event = "turtle"

    elif sot == 1 and die < .18:
        event = "smog"
        
    elif sot > 0 and current_year >2500 and respectability>3 and die <.4:
        event = "park"

    return event, event_year

def get_knowledge_of_past(visibility, respectability, likability,
                      understandability):
    '''returns 3 for precise knowledge, 2 for location only, 1 for myth,
    0 for none'''
    #note: usability does not come into this calculation
    #this is a deterministic calculation - no dice!

    kop = 0
    if understandability > .5:
        kop = 3
    elif visibility > .4:
        kop = 2
    elif visibility > .2 and (likability > .3 or respectability > .3):
        kop = 1
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


def get_stats(site_map, global_buffs, current_year,sot, event_list): #pylint: disable=too-many-branches,too-many-locals
    """gives the 5 stats given your equipment, year, and state of tech"""

    usability = 100
    visibility = 0
    likability = 0
    respectability = 0
    understandability = 0

    #stat changes for events
    catholics = any("cat-holics" in tup for tup in event_list)
    stonehenge = any("stonehenge" in tup for tup in event_list)
    flood = any("flood" in tup for tup in event_list)
    smog = any("somg" in tup for tup in event_list)
    klingon = any("cat-holics" in tup for tup in event_list)
    turtle = any("cat-holics" in tup for tup in event_list)
    goths = any("goths" in tup for tup in event_list)
    faultline = any("faultline" in tup for tup in event_list)
    park = any("park" in tup for tup in event_list)

    for buff in global_buffs:
        values_list = get_stats_for_marker(buff, current_year, sot,klingon, turtle,goths, faultline)

        usability += values_list[0]
        visibility += values_list[1]
        respectability += values_list[2]
        likability += values_list[3]
        understandability += values_list[4]

    for row in site_map:
        for entry in row:
            values_list = get_stats_for_marker(entry, current_year, sot,klingon, turtle,goths, faultline)

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


    usability, visibility, respectability, likability, understandability = get_adjacency_bonus(site_map,
                                                                                               usability,
                                                                                               visibility,
                                                                                               respectability,
                                                                                               likability,
                                                                                               understandability,
                                                                                               current_year,
                                                                                               sot,
                                                                                               klingon,
                                                                                               turtle,
                                                                                               goths,
                                                                                               faultline)

    if catholics:
        likability += 10
    if stonehenge:
        likability += 7
    if flood:
        usability += 20
    if smog:
        visibility = min(visibility, 20)
    if park:
        usability -= 20
        likability += 15

    visibility = max(0, visibility)
    
    print("Pre-normalization understandability: ", understandability, " visibility: ", visibility, " respectability: ", respectability, " likability: ", likability, " usability: ", usability)
    return normalize_stat(usability), normalize_stat(visibility), normalize_stat(respectability),\
        normalize_stat(likability), normalize_stat(understandability)

def normalize_stat(stat_value):
    """Maps stat to a value on [-1, 1]"""
    stat_value = min(stat_value, 100)
    stat_value = max(stat_value, -100)
    return stat_value / 100

def get_stats_for_marker(marker_id, current_year, sot, klingon, turtle, goths, faultline): #pylint: disable=too-many-arguments,too-many-branches
    """Gets the stats for a particular marker, adjusted for decay and state of technology"""
    inits_list = [list(markers[marker_id].usability_init),
                  list(markers[marker_id].visibility_init),
                  list(markers[marker_id].respectability_init),
                  list(markers[marker_id].likability_init),
                  list(markers[marker_id].understandability_init)]

    #very special case for goth event - flip likability for spoopy stuff
    if goths:
        if "spooky" in markers[marker_id].tags:
            inits_list[3][0] = -1* inits_list[3][0]
            inits_list[3][1] = -1* inits_list[3][1]
            inits_list[3][2] = -1* inits_list[3][2]
    #special case for klingon event: understandability down
    if klingon:
        if "linguistic" in markers[marker_id].tags:
            inits_list[4][0] = .5* inits_list[4][0]
            inits_list[4][1] = .5* inits_list[4][1]
            inits_list[4][2] = .5* inits_list[4][2]
    #special case for turtles! understandability down for more stuff
    if turtle:
        if "linguistic" in markers[marker_id].tags or "pictoral" in markers[marker_id].tags:
            inits_list[4][0] = .7* inits_list[4][0]
            inits_list[4][1] = .7* inits_list[4][1]
            inits_list[4][2] = .7* inits_list[4][2]
    #faultline: vis up for buried markers
    if faultline:
        if "buried" in markers[marker_id].tags:
            inits_list[1][0] = 2* inits_list[1][0]
            inits_list[1][1] = 2* inits_list[1][1]
            inits_list[1][2] = 2* inits_list[1][2]



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

def get_adjacency_bonus(site_map,usability, visibility, respectability, likability, #pylint: disable=too-many-arguments, too-many-locals
        understandability, current_year, sot, klingon, turtle, goths, faultline):
    """checks if anything on the map gets adjacency bonus and modifies stats directly"""
    #right now, just checking for a vis bonus tag and giving bonus to vis
    visibility += get_visibility_adjacency_bonus(site_map)

    understandability += get_synergy_partnership_bonus(site_map)

    spooky_respectability_modifier, spooky_likability_modifier = get_spooky_adjacency_bonus(site_map, goths)
    respectability += spooky_respectability_modifier
    likability += spooky_likability_modifier

    understandability += get_pro_educational_adjacency_bonus(site_map)

    terraforming_usability_modifier, terraforming_visibility_modifier, terraforming_respectability_modifier,\
            terraforming_likability_modifier, terraforming_understandability_modifier = \
            get_massive_terraforming_bonus(site_map, current_year, sot,klingon, turtle,goths, faultline)
    usability += terraforming_usability_modifier
    visibility += terraforming_visibility_modifier
    respectability += terraforming_respectability_modifier
    likability += terraforming_likability_modifier
    understandability += terraforming_understandability_modifier

    monolith_usability_penalty, monolith_respectability_bonus = get_standing_stones_bonus(site_map)
    usability += monolith_usability_penalty
    respectability += monolith_respectability_bonus

    return usability, visibility, respectability, likability, understandability

def get_neighbors(site_map, row_num, col_num):
    """Given a site map and a pair of coordinates, returns the neighbors of those coordinates"""
    neighbors = []
    if row_num-1 >= 0:
        neighbors.append(site_map[row_num-1][col_num])
        if col_num-1 >=0:
            neighbors.append(site_map[row_num-1][col_num-1])
        if col_num+1 < len(site_map[row_num]):
            neighbors.append(site_map[row_num-1][col_num+1])

    if row_num+1 < len(site_map):
        neighbors.append(site_map[row_num+1][col_num])
        if col_num-1 >=0:
            neighbors.append(site_map[row_num+1][col_num-1])
        if col_num+1 < len(site_map[row_num]):
            neighbors.append(site_map[row_num+1][col_num+1])

    if col_num-1 >= 0:
        neighbors.append(site_map[row_num][col_num-1])
    if col_num+1 < len(site_map[row_num]):
        neighbors.append(site_map[row_num][col_num+1])

    return neighbors

def get_neighbor_coords(site_map, row_num, col_num):
    """Given a site map and a pair of coordinates, returns the neighboring coordinates of those coordinates"""
    neighbors = []
    if row_num-1 >= 0:
        neighbors.append((row_num-1, col_num))
        if col_num-1 >=0:
            neighbors.append((row_num-1, col_num-1))
        if col_num+1 < len(site_map[row_num]):
            neighbors.append((row_num-1, col_num+1))

    if row_num+1 < len(site_map):
        neighbors.append((row_num+1, col_num))
        if col_num-1 >=0:
            neighbors.append((row_num+1, col_num-1))
        if col_num+1 < len(site_map[row_num]):
            neighbors.append((row_num+1, col_num+1))

    if col_num-1 >= 0:
        neighbors.append((row_num, col_num-1))
    if col_num+1 < len(site_map[row_num]):
        neighbors.append((row_num, col_num+1))

    return neighbors

def get_like_contiguous_markers(site_map, row_num, col_num):
    """Returns the number of markers in the block of contiguous markers of which (row_num, col_num) is a part,
    which all share a type with the marker at (row_num, col_num)"""
    num_contiguous_markers = 0
    coords_visited = []
    coords_to_visit = [(row_num, col_num)]
    marker_type = site_map[row_num][col_num]
    while coords_to_visit:
        current_coords = coords_to_visit.pop()
        coords_visited.append(current_coords)
        this_marker = site_map[current_coords[0]][current_coords[1]]
        if this_marker == marker_type:
            num_contiguous_markers += 1
            neighbor_coords = get_neighbor_coords(site_map, current_coords[0], current_coords[1])
            like_neighbor_coords = [coords for coords in neighbor_coords if site_map[coords[0]][coords[1]] == this_marker]
            unvisited_like_neighbor_coords = [coords for coords in like_neighbor_coords if coords not in coords_visited]
            unvisited_unscheduled_like_neighbor_coords = [coords for coords in unvisited_like_neighbor_coords if coords not in coords_to_visit]
            coords_to_visit[:0] = unvisited_unscheduled_like_neighbor_coords

    print(num_contiguous_markers)
    return num_contiguous_markers

def get_standing_stones_bonus(site_map):
    """Calculates the usability and respectability modifiers for adjacent monoliths"""
    usability_penalty = 0
    respectability_bonus = 0
    for row_num in range(len(site_map)): #pylint: disable=consider-using-enumerate, too-many-nested-blocks
        for col_num in range(len(site_map[row_num])):
            this_marker = site_map[row_num][col_num]
            if markers[this_marker].is_monolith():
                neighbors = get_neighbors(site_map, row_num, col_num)
                for neighbor in neighbors:
                    if markers[neighbor].is_monolith():
                        usability_penalty -= .5
                        respectability_bonus += .5

    return usability_penalty, respectability_bonus


def get_massive_terraforming_bonus(site_map, current_year, sot,klingon, turtle,goths, faultline):
    """Calculates the bonus to all stats for multiple contiguous terraforming markers of the same type"""
    usability_bonus = 0
    visibility_bonus = 0
    respectability_bonus = 0
    likability_bonus = 0
    understandability_bonus = 0
    for row_num in range(len(site_map)): #pylint: disable=consider-using-enumerate, too-many-nested-blocks
        for col_num in range(len(site_map[row_num])):
            this_marker = site_map[row_num][col_num]
            this_marker_stats = get_stats_for_marker(this_marker, current_year, sot, klingon, turtle,goths, faultline)
            if markers[this_marker].is_terraforming():
                contiguous_markers_in_block = get_like_contiguous_markers(site_map, row_num, col_num)
                usability_bonus += ((contiguous_markers_in_block-1)*.05)*this_marker_stats[0]
                visibility_bonus += ((contiguous_markers_in_block-1)*.05)*this_marker_stats[1]
                respectability_bonus += ((contiguous_markers_in_block-1)*.05)*this_marker_stats[2]
                likability_bonus += ((contiguous_markers_in_block-1)*.05)*this_marker_stats[3]
                understandability_bonus += ((contiguous_markers_in_block-1)*.05)*this_marker_stats[4]

    return usability_bonus, visibility_bonus, respectability_bonus, likability_bonus, understandability_bonus

def get_pro_educational_adjacency_bonus(site_map):
    """Calculates the site's understandability bonus from markers with pro-educational tag boosting markers with
    the educational tag"""
    understandability_bonus = 0
    for row_num in range(len(site_map)): #pylint: disable=consider-using-enumerate, too-many-nested-blocks
        for col_num in range(len(site_map[row_num])):
            this_marker = site_map[row_num][col_num]
            if markers[this_marker].is_pro_educational():
                neighbors = get_neighbors(site_map, row_num, col_num)
                for neighbor in neighbors:
                    if markers[neighbor].is_educational():
                        understandability_bonus += 1

    return understandability_bonus

def get_spooky_adjacency_bonus(site_map, goths):
    """Calculates the site's respectability bonus and likability penalty for adjacent markers with the spooky tag"""
    respectability_bonus = 0
    likability_penalty = 0
    for row_num in range(len(site_map)): #pylint: disable=consider-using-enumerate, too-many-nested-blocks
        for col_num in range(len(site_map[row_num])):
            this_marker = site_map[row_num][col_num]
            if markers[this_marker].is_spooky():
                neighbors = get_neighbors(site_map, row_num, col_num)
                for neighbor in neighbors:
                    if markers[neighbor].is_spooky():
                        respectability_bonus += .5
                        if goths:
                            likability_penalty += .5
                        else:
                            likability_penalty -= .5

    return respectability_bonus, likability_penalty

def get_synergy_partnership_bonus(site_map):
    """Calculates the site's understandability bonus from synergy partnerships"""
    understandability_bonus = 0
    for row_num in range(len(site_map)): #pylint: disable=consider-using-enumerate, too-many-nested-blocks
        for col_num in range(len(site_map[row_num])):
            this_marker = site_map[row_num][col_num]
            partnerships = markers[this_marker].get_synergy_partnerships()
            if partnerships:
                neighbors = get_neighbors(site_map, row_num, col_num)
                for neighbor in neighbors:
                    neighbor_partnerships = markers[neighbor].get_synergy_partnerships()
                    for partnership in partnerships:
                        if partnership in neighbor_partnerships:
                            understandability_bonus += .5

    return understandability_bonus

def get_visibility_adjacency_bonus(site_map): #pylint: disable=too-many-branches
    """Calculate visibility bonus from visibility adjacency bonuses"""
    neighbors = 0
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

    return neighbors/2

def miner_prob(knowledge_of_past, value_of_materials, understandability, years): #pylint: disable=too-many-branches
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
    if knowledge_of_past != 0:
        knowledge_multiplier = .001*(1-understandability)/1
    else:
        knowledge_multiplier = 1

    bhr = .001 #magic! was 83 in source, but then you always lose

    #drill rate is the avg # of bores per sq m per 1000 yrs
    drill_rate = bhr * value_multiplier * knowledge_multiplier
    #print("drill rate is " + str(drill_rate))

    area = 16 #sqare milage from doc

    prob_per_year = (drill_rate*area)/1000
    #print("yearly probability is " + str(prob_per_year))

    prob = 1-((1-prob_per_year)**years)
    #print("total probability of mining is " + str(prob))

    return prob


def arch_prob(knowledge_of_past, start_year, understandability):
    """gives total probability of at least one disruptive archaeological
    dig over 200 years, given start year"""
    #should also take state_of_technology?
    if knowledge_of_past == 3:
        prob = 0
    elif knowledge_of_past == 2:
        if start_year < 3000:
            prob = 0
        elif start_year < 5000:
            prob = .01 * (.5 - understandability)/.5
        else:
            prob = .02 * (.5 - understandability)/.5
    elif knowledge_of_past == 1:
        if start_year < 3000:
            prob = .01 * (.5 - understandability)/.5
        elif start_year < 5000:
            prob = .02 * (.5 - understandability)/.5
        else:
            prob = .03 * (.5 - understandability)/.5
    else:
        if start_year < 3000:
            prob = 0
        else:
            prob = .001 * (.5 - understandability)/.5

    return prob

def dam_prob(knowledge_of_past, usability, start_year, understandability):
    """gives total prob of at least one dam construction over 200 years"""
    if knowledge_of_past == 3:
        prob = 0
    elif start_year < 2300:
        if usability > .5:
            prob = .002 * (.5 - understandability)/.5
        elif usability > 0:
            prob = .001 * (.5 - understandability)/.5
        else:
            prob= .0005
    elif start_year < 5000:
        if usability > .51:
            prob = .003 * (.5 - understandability)/.5
        elif usability > 0:
            prob = .002 * (.5 - understandability)/.5
        else:
            prob = .0001 * (.5 - understandability)/.5
    else:
        if usability > .5:
            prob = .005 * (.5 - understandability)/.5
        elif usability > 0:
            prob = .004 * (.5 - understandability)/.5
        else:
            prob = .0003 * (.5 - understandability)/.5
    return prob

def teen_prob(visibility, respectability, understandability):
    """gives total prob of random teen violence breaching the site"""
    if visibility < .3 or respectability > .8:
        prob = 0
    elif respectability > .6:
        prob = .0001 * (1 - understandability)/1
    elif respectability > .3:
        prob = .001 * (1 - understandability)/1
    else:
        prob = .003 * (1 - understandability)/1
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
        base_probability = .001
    return base_probability*(1-awareness_of_danger)

def get_modified_map(time_period_map, vikings, earthquake, faultline):
    """changes map based on 3 events"""
    new_map = copy.deepcopy(time_period_map)
    for row_num in range(len(time_period_map)):
        for col_num in range(len(time_period_map[row_num])):
            if vikings:
                if time_period_map[row_num][col_num] == "attractive-monument":
                    new_map[row_num][col_num] = "ruined-attractive-monument"
                elif time_period_map[row_num][col_num] == "visitor-center":
                    new_map[row_num][col_num] = "ruined-visitor-center"
                elif time_period_map[row_num][col_num] == "atomic-flowers":
                    new_map[row_num][col_num]= "ruined-atomic-flowers"
            if earthquake or faultline:
                if time_period_map[row_num][col_num] == "granite-monolith":
                    new_map[row_num][col_num] = "ruined-granite-monolith"
                elif time_period_map[row_num][col_num] == "metal-monolith":
                    new_map[row_num][col_num] = "ruined-metal-monolith"
                elif time_period_map[row_num][col_num] == "wooden-monolith":
                    new_map[row_num][col_num] = "ruined-wooden-monolith"
    return new_map
