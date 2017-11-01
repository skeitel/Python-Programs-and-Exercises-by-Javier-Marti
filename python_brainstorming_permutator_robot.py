#BRAINSTORMING robot by JavierMarti.co.uk
#Generates business ideas by mixing elements from different fields
#This robot can also be used to combine a mix of elements for scientific research, or for investment purposes, diversifying an investment portfolio
#During a brainstorming session participants input random words into the list and at the same time eliminate or punctuate the formed ideas that appear on screen in real time, as a game. At the end of the session only the highest vote ideas remain int the outcome file

import random
import itertools

do_what = ['deliver', 'monitor','transport']
with_what = ['books','people','animals','gadgets','robots']
transport = ['by ecoship','by electric bycicle','by drone']
where = ['in India', 'in Germany', 'in the US']
platform = ['using a mobile app', 'through crowdsourcing', 'using robots to do it']
promotion = ['promoting via Reddit', 'promoting via Facebook','promoting via email', 'promoting via VR']
sum_all_elements = len(do_what) +len(with_what)+len(transport)+len(where)+len(platform)+len(promotion)

print('\n')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n')
print('Starting BRAINSTORMING robot by JavierMarti.co.uk...\n')

#give 10 random combinations
print('10 RANDOM IDEAS')
print('Here are 10 ideas, randomly chosen: ')
print('----------------------------')

counter = 1
for i in range(10):
    print(counter, random.choice(do_what).title(),random.choice(with_what),random.choice(transport), random.choice(where),random.choice(platform),'and',random.choice(promotion))
    counter += 1


#Show ALL possible combinations of all elements
print('\n')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n')
print('ALL POSSIBLE COMBINATIONS')
print('----------------------------')

outcome = ["{a} {b} {c} {d} {e} and {f}".format(a=a.title(), b=b, c=c, d=d, e=e, f=f) for a,b,c,d,e,f in itertools.product(do_what, with_what, transport, where, platform, promotion)]

print('There are ', len(outcome), 'possible combinations of all these',sum_all_elements,'elements. Here they are:\n')

for number, el in enumerate(outcome):
    print(number, el)






#END OF PROGRAM ##########################################################################################
#To do:
#Generate random idea every time key is pressed
#Eliminate idea if key is pressed, or add to dictionary of "to review" the idea, if another key is pressed

'''Another way to do it is:
list1 = ['The girl', 'The boy']
list2 = ['wears', 'touches', 'tries']
list3 = ['a red sweater', 'a blue sweater', 'a yellow sweater', 'a white sweater']

for x in list3:
    for y in list2:
        for z in list1:
            print (z,y,x)
'''