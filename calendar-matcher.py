
def get_time_on_mins(time):
    h, m = time.split(":")
    if int(h) != 0 or int(h) != 00:
        return (int(h)*60) + int(m)
    else:
        return int(m)

def get_time_on_mins_on_gap(time_gap):
    start = get_time_on_mins(time_gap[0])
    end = get_time_on_mins(time_gap[1])
    return end - start

def get_hour(time):
    return int(time.split(":")[0])

def compare_times(time1, time2):
    print("Comparing {} to {}".format(time1, time2))
    h1, m1 = time1.split(":")
    h2, m2 = time2.split(":")

    t1 = (int(h1) * 60) + int(m1);
    t2 = (int(h2) * 60) + int(m2);

    return 1 if t1 > t2 else -1 if t1 < t2 else 0

def get_max_time_possible(time1,time2):
    p1_min_hours, p1_min_mins = time1[0].split(":")
    p2_min_hours, p2_min_mins = time2[0].split(":")

    p1_max_hours, p1_max_mins = time1[1].split(":")
    p2_max_hours, p2_max_mins = time2[1].split(":")

    min = "{}:{}".format(p1_min_hours, p1_min_mins) if int(p1_min_hours) > int(p2_min_hours) else "{}:{}".format(p2_min_hours, p2_min_mins) if int(p1_min_hours) < int(p2_min_hours) else "{}:{}".format(p1_min_hours, p1_min_mins if int(p1_min_mins) > int(p2_min_mins) else p2_min_mins)
    max = "{}:{}".format(p1_max_hours, p1_max_mins) if int(p1_max_hours) < int(p2_max_hours) else "{}:{}".format(p2_max_hours, p2_max_mins) if int(p1_max_hours) > int(p2_min_hours) else "{}:{}".format(p1_max_hours, p1_max_mins if int(p1_max_mins) < int(p2_max_mins) else p2_max_mins)

    return [min, max]

def get_time_between(time1, time2):
    comparassion = compare_times(time1, time2)
    if comparassion == -1:
        return [time1, time2]
    else:
        return None

def get_recursive_free_time_between_hours(person_time, office_min_max, list, aux):
    if len(person_time) != 0:
        popped = person_time.pop(0)
        if len(list) == 0:
            list.append(get_time_between(office_min_max[0],popped[0]))
        else:
            list.append(get_time_between(aux, popped[0]))
        return get_recursive_free_time_between_hours(person_time, office_min_max, list, popped[1])
    else:
        list.append(get_time_between(aux, office_min_max[1]))

def filter_enought_time_for_meeting(time_tuple, time_needed):
    if time_tuple == None:
        return False
    time_start = time_tuple[0]
    time_finish = time_tuple[1]
    time_gap = get_time_on_mins(time_finish) - get_time_on_mins(time_start)

    return time_gap >= get_time_on_mins(time_needed)

def find_time_gaps(time_l1, time_l2):
    gaps = []
    for time_g1 in time_l1:
        for time_g2 in time_l2:
            if get_hour(time_g1[1]) > get_hour(time_g2[0]) and get_hour(time_g1[0]) < get_hour(time_g2[1]):
                time_gap = get_max_time_possible(time_g1, time_g2)
                gaps.append(time_gap)
    return gaps

def find_best_possible_meetinf(time_gaps):
    res = ['00:00', '00:00']
    for gap in time_gaps:
        if get_time_on_mins_on_gap(gap) > get_time_on_mins_on_gap(res):
            res = gap

    return res

def get_meetings_brackets(p1_tuple, p2_tuple, time_needed):
    max_time_both_at_office = get_max_time_possible(p1_tuple[0],p2_tuple[0])
    print("Person1 and Person2 would be booth at office from {} to {}".format(max_time_both_at_office[0],max_time_both_at_office[1]))

    p1_free_time = []
    p2_free_time = []
    get_recursive_free_time_between_hours(p1_tuple[1], max_time_both_at_office, p1_free_time, None)
    get_recursive_free_time_between_hours(p2_tuple[1], max_time_both_at_office, p2_free_time, None)

    p1_free_time = list(filter(lambda x: x is not None, p1_free_time))
    p2_free_time = list(filter(lambda x: x is not None, p2_free_time))

    print("Person1 free time is {}".format(p1_free_time))
    print("Person2 free time is {}".format(p2_free_time))

    time_gaps = find_time_gaps(p1_free_time, p2_free_time)
    print("Common time gaps {}".format(time_gaps))
    res = list(filter(lambda x: filter_enought_time_for_meeting(x, time_needed), time_gaps))

    if len(res) != 0:
        return res, None
    else:
        best_match = find_best_possible_meetinf(time_gaps)
        if len(best_match) != 0:
            return None, [best_match, get_time_on_mins_on_gap(best_match)]
        else:
            return None, None


if __name__ == "__main__":
    p1_ocupped_time = [['10:00', '11:30'], ['14:00', '16:00'], ['16:30', '18:00']]
    p2_ocupped_time = [['09:30', '10:30'], ['13:30', '15:00']]
    p1_at_office_time = ['09:20', '18:00']
    p2_at_office_time = ['09:00', '18:00']
    p1 = (p1_at_office_time, p1_ocupped_time)
    p2 = (p2_at_office_time, p2_ocupped_time)
    meeting_time = '00:30'

    print("Find free times between 2 people")
    print("[Person1] Would be at the office from {} to {}".format(p1_at_office_time[0], p1_at_office_time[1]))
    print("[Person1] Is already taken at these time periods {}".format(p1_ocupped_time))
    print("[Person2] Would be at the office from {} to {}".format(p1_at_office_time[0], p1_at_office_time[1]))
    print("[Person2] Is already taken at these time periods {}".format(p2_ocupped_time))
    print("Doing some magic?")

    some_match, best_aproach = get_meetings_brackets(p1, p2, meeting_time)

    if some_match != None:
        print("Person1 and Person2 can meet at one of these time periods {}".format(some_match))
    elif best_aproach != None:
        print("Im Sorry but Person1 and Person2 dont have time for a {} hour meeting, fortunately we found time for a "
              "{} minutes meeting from {} to {} ".format(meeting_time, best_aproach[1], best_aproach[0][0], best_aproach[0][1]))
    else:
        print("Person1 and Person2 have no time today!")
