preferred_ranking_men={
'ray': ['liz','sar','zoe','dan'],
'jos': ['sar','liz','dan','zoe'],
'bla': ['sar','dan','zoe','liz'],
'jam': ['liz','sar','zoe','dan']
}

preferred_ranking_women={
'liz': ['ray','bla','jos','jam'],
'sar': ['ray','jos','bla','jam'],
'zoe': ['bla','ray','jos','jam'],
'dan': ['jos','bla','ray','jam']
}

male={'Male:','ray', 'jos','bla','jam'}
female={'female:', 'liz','sar','zoe','dan'}

#keeps track of the peeple that "may: end up together
tentative_engagement=[]

#men who still need to get someone to dance
free_man=[]

def init_free_man():
    for man in preferred_ranking_men.iterkeys():
        free_man.append(man)
def stable_matching():
    while(len(free_man)>0):
        for man in free_man:
            begin_matching(man)
def begin_matching(man):
    print('dealing with %s'%(man))
    for woman in preferred_ranking_men[man]:
     
      taken_match=[couple for couple in tentative_engagement if woman in couple]
      
      if(len(taken_match)==0):
        tentative_engagement.append([man,woman])
        free_man.remove(man)
        print('%s is no longer a free man and is now tentatively engaged to %s'%(man,woman))
        break
      elif(len(taken_match)>0):
          print('%s is taken already..'%(woman))
          
          current_guy=preferred_ranking_women[woman].index(taken_match[0][0])
          potential_guy=preferred_ranking_women[woman].index(man)
          
          if(current_guy<potential_guy):
             print('she is satisifed with%s..'%(taken_match[0][0]))
          else:
             print('%s is better than %s '%(man,taken_match[0][0]))
             print('making %s free again.. and hen tentatively accept dance between %s and %s'%(taken_match[0][0],man,woman))
             
             free_man.remove(man)
             free_man.append(taken_match[0][0])
             
             taken_match[0][0]=man
             break
def main():
    init_free_man()
    print(male)
    print(female)
    stable_matching()
    
    print('complet list of couple\n')
    print(tentative_engagement)

if __name__ == '__main__':
    main()
