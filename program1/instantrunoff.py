import goody

def read_voter_preferences(file : open):
    dictionary, pref_list = dict(), list()
    for dictitems in file:
        dictitems = list(dictitems.rstrip().split(';'))
        pref_list.append(list(pref for pref in dictitems[1:]))
        dictionary[dictitems[0]] = pref_list[0]
        pref_list = []
    return dictionary

def dict_as_str(d : {None:None}, key : callable=None, reverse : bool=False) -> str:
    return ''.join(f'  {k} -> {str(d[k])}\n' for k in sorted(d.keys(), key=key, reverse=reverse))

def evaluate_ballot(vp : {str:[str]}, cie : {str}) -> {str:int}:
    votes = dict((candidate, 0) for candidate in cie)
    for voter in vp :
        for candidate in vp[voter]:
            if candidate in cie: 
                votes[candidate] += 1 
                break
            else: continue
    return votes


def remaining_candidates(vd : {str:int}) -> {str}:
    return{k for k,y in vd.items() if y != min(vd.values())}


def run_election(vp_file : open) -> {str}:
    ballot = read_voter_preferences(vp_file)
    print(f'\nPreferences: voter -> [candidates in order]\n{dict_as_str(ballot)}')
    cie, ballot_count = set(), 0
    for candidateS in ballot.values():
        for candidate in candidateS:
            cie.add(candidate)
    while (len(cie) not in (1,0)) :
        ballot_count+= 1
        print(f'Vote count on ballot #{str(ballot_count)}: candidates (sorted alphabetically) using only candidates in set {cie}\n{dict_as_str(evaluate_ballot(ballot, cie))}')
        print(f'\nVote count on ballot #{str(ballot_count)}: candidates (sorted numerically) using only candidates in set {cie}\n{dict_as_str(evaluate_ballot(ballot, cie), key=(lambda x : -evaluate_ballot(ballot, cie)[x]))}')
        cie = remaining_candidates(evaluate_ballot(ballot, cie))
    print(f'Election winner is {cie}')
    return cie

  
  
  
  
    
if __name__ == '__main__':
    # Write script here
    file = goody.safe_open('Enter the name of the file of voter preferences', 'r', 'Illegal File Name')
    run_election(file)
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#   #  driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
