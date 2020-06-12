

def pop_and_select(dictionary, organized_times_list, tally_organized_times_sum, prescribed_time):
    """
    dictionary = dict of ordered tally
    organized_times_list = list of times organized high to low
    tally_organized_times_sum = int sum of organized times list
    prescribed time = time alloted by  def get_all_warmup_times
    return: selected list
    """
    x = tally_organized_times_sum

    pop_dict = dictionary.copy()
    pop_organized_time_list = organized_times_list.copy()

    while x > prescribed_time:
        pop_dict.popitem()
        pop_organized_time_list.pop()
        x = sum(pop_organized_time_list)
    return list(pop_dict.keys())