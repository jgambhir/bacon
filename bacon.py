if __name__ == '__main__':
    from bacon_functions import *
    actor_data = open('large_actor_data.txt')
    actor_dict = parse_actor_data(actor_data)
    movie_dict = invert_actor_dict(actor_dict)
    largest = 0
    
    actor = raw_input("Please enter an actor (or press return to exit: ")
    while actor.rstrip():
        # rstrip is needed to remove "\r" or any other backslash characters
        # that were supposed to be removed by Python but weren't (it's a known
        # bug). [Source: Dan Zingaro on CSC108 forum]
        actor = actor.title().rstrip()
        connection = find_connection(actor, actor_dict, movie_dict)
        if actor == 'Kevin Bacon':
            print actor + " has a Bacon Number of %s." % len(connection)
        elif connection != []:
            print actor + " has a Bacon Number of %s." % len(connection)
            act1 = actor
            for tup in connection:
                print "%s was in %s with %s." % (actor, tup[0], tup[1])
                actor = tup[1]
            if len(connection) > largest:
                largest = len(connection)
        else:
            print actor + " has a Bacon Number of Infinity."
            
        actor = raw_input("\nPlease enter an actor (or press return to exit: ")
            
    print "Thank you for playing! The largest Bacon Number you found was %s." \
          % largest
        
        