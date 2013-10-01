def parse_actor_data(actor_data):
    '''Return actor_dict, a dictionary mapping actors (strings) to lists of
    movies (each are strings) they've acted in, from open reader actor_data,
    which contains movie and actor information in IMDB's format.'''
    
    actor_dict = {}
        
    line = actor_data.readline().strip()
    # Read past the header
    while line.find('Name') != 0:
        line = actor_data.readline().strip()

    actor_data.readline()    
    line = actor_data.readline().strip()    
    # The beginning of the footer is a line full of dashes (-)
    while line and line.find('------') == -1:
        # Identify actor's name in line
        actor = actor_name(line)
        tab_index = line.find('\t')    
        # Find the last "\t" starting before the opening bracket of the
        # movie year. This is where the first movie title starts.
        movie_index = line.rfind('\t', 0, line.find('(', tab_index)) + 1
        movie = line[movie_index : line.find(')', movie_index) + 1]
        if actor not in actor_dict:
            actor_dict[actor] = [movie]
        else:
            actor_dict[actor] += [movie]
                
        line = actor_data.readline().strip()
                
        # Find and record the rest of the movies actor has been in
        while line != '': 
            movie = line[: line.find(')') + 1]
            if movie not in actor_dict[actor]:
                actor_dict[actor] += [movie]
            line = actor_data.readline().strip()
                        
        line = actor_data.readline().strip()
                          
    return actor_dict

def actor_name(line):
    '''Return actor, a string in title case in the format Firstname Lastname,
    from line (a string), a line from an IMDB-format actor-movie file containing
    an actor name and a movie they've acted in.'''
    
    # There is at least one tab between actor name and movie name
    tab_index = line.find('\t')
    # If the actor has a last name, their name appears as Last, First in line.
    # A comma can be used as a delimiter here.
    comma_index = line.find(',', 0, tab_index)
    bracket_index = line.find('(')

    if comma_index != -1:
        # Avoid roman numerals in actor name
        if tab_index > bracket_index and bracket_index != -1:
            first_name = line[comma_index + 2 : bracket_index - 1]
        # No roman numerals in name; bracket_index is the index of the
        # opening bracket in the movie year
        elif bracket_index > tab_index:
            first_name = line[comma_index + 2 : tab_index]
        last_name = line[: comma_index]
        actor = first_name + ' ' + last_name
    # Actor name is comma-less; example: LL Cool J
    else:
        if tab_index > bracket_index and bracket_index != -1:
            actor = line[: bracket_index - 1]
        else:
            actor = line[: tab_index]
   
    return actor.title()


def invert_actor_dict(actor_dict):
    '''Return movie_dict, a dictionary which is the inverse of actor_dict, 
    mapping movies (string) to lists of actors (string) who have acted in 
    them.''' 
    
    movie_dict = {}
    for (actor, movies) in actor_dict.items():
        for movie in movies:
            if movie in movie_dict:
                movie_dict[movie].append(actor)
            else:
                movie_dict[movie] = [actor]
    return movie_dict
        
    
def find_connection(actor_name, actor_dict, movie_dict):
    '''Return a list of (movie, actor) tuples (both elements of type string)
    that represent a shortest connection between actor_name and Kevin Bacon 
    that can be found in the actor_dict (a dictionary that maps an actors 
    (string) to lists of movies they've acted in (each are strings) and 
    movie_dict (the inverse dictionary of actor_dict). Each tuple in the 
    returned list has a special property: the actor from the previous tuple 
    and the actor from the current tuple both appeared in the stated movie. 
    For the first tuple, the "actor from the previous tuple" is actor_name, and 
    the last tuple must contain Kevin Bacon. If there is no connection between
    actor_name and Kevin Bacon, return an empty list.'''
    
    done = []
    to_do = [actor_name]
    distances = {actor_name: 0}
    movie_list = []
    path = []
    
    if actor_name not in actor_dict or actor_name == 'Kevin Bacon':
        return path
    
    while len(to_do) > 0:
        # actor is the actor currently being investigated
        actor = to_do[0]
        to_do.remove(actor)
        done.append(actor)
        
        for movie in actor_dict[actor]:
            for co_star in movie_dict[movie]:
                # If Kevin Bacon has been found, put together the path
                # from actor_name to him.
                if co_star == 'Kevin Bacon':
                    distance_inv = invert_distances(distances)
                    path += [(movie, "Kevin Bacon")]
                    dist = distances[actor]
                    actor2 = actor
                    while dist - 1 >= 0:
                        # Find an actor with distance 1 less than actor2's that
                        # is connected to actor2 through a movie that has been
                        # investigated.
                        for actor1 in distance_inv[dist - 1]:
                            for M in movie_list:
                                if actor1 in movie_dict[M] and actor2 in \
                                   movie_dict[M]:
                                    path.insert(0, (M, actor2))
                                    actor2 = actor1
                                    dist = distances[actor2]
                                    break
                    return path
                                
                    
                elif co_star not in to_do and co_star not in done:
                    distances[co_star] = distances[actor] + 1
                    to_do.append(co_star)
                    movie_list.append(movie)
    
    return path

def invert_distances(distances):
    '''Return inverse, the inverse of dictionary distances (which maps
    an actor name (a str) to their distance (through movies) from a certain
    actor).'''
    
    inverse = {}
    
    for (actor, distance) in distances.items():
        if distance in inverse:
            inverse[distance].append(actor)
        else:
            inverse[distance] = [actor]
            
    return inverse