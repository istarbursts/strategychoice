from random import randint

# ----- Operators for actual addition strategies and test routines.

'''
There are the following systems herein:

   1. The experimenter chooses problems, presents them, handles
      cycling the world, and gives feedback on results of addition.

   2. ASCM (more correctly, the LMT module) knows the specific high
      level structure of each strategy, and carries with each a memory
      strength value.  Each time the memory system is referenced (by
      the cognitive system), the referred-to elements get their
      strengths increased.  This principle gives us an account of the
      basic memory effects: (a) whenever a strategy is used (whether
      it works or not) its strenght is increased.  (b) when a strategy
      gets the right answer, it is increased again (by viture of the
      cognitivie system getting rewarded and so sort of patting the
      strategy on the head), and (c) when a new strategy is entered,
      it gets very high strength points (because there's a lot of
      memory interaction involved in entering it into the memory).

   3. The performance system knows how to do the specific things that
      come with goals (as stored in the memory to describe a
      strategy).

   4. The cognitive system gets the problem, computes its features,
      probes ASCM for a strategy, gets the goals for the selected
      strategy from the memory, sets the peripheral system off on the
      first of these and then monitors performance as the process
      takes place.  When the answer appears (in an echoic buffer at
      the end of the run) the cognitive system reports this to the
      experimenter, gets the right or wrong feedback, and then, if the
      answer was correct, pats ASCM on the head.  The cognitive system
      also permanently knows the general structure of a good addition
      strategy.  This is coded into the cognitive system and never
      changes.
'''


# General utilities for reporting, etc.

def trp(tl,text):
    if TL>tl:
        print text

# The peripheral system.This is a very simple representation of the
# stuff needed for the addition domains: ten "fingers", a focus of
# attention, and an echoic memory into which numbers are stored.
# Operations on these constitute the basic operations of the
# domain.

class Hand(object):
    
    def __init__(self):
        
        # The fingers memory structure; five on each of two hands, 
        # each of which my be up or down.
        
        self.s = {'left':['']*5,'right':['']*5}
        
        #| The focus of attention may point at a particular finger, or may be nil. |#
        
        self.foa = {'hand':'','finger':0}
        self.hand = ''
    
    def clear(self):
        self.s['left'] = ['d']*5
        self.s['right'] = ['d']*5
    
    # Basic operations; most of which operate on what's in foa.
    
    def increment_focus(self):
        if not((self.foa['hand']=='right') and (self.foa['finger']==4)):
        
            # If we're done the left hand, move on to the rigt.
            
            if (self.foa['hand']=='left') and (self.foa['finger']==4):
                self.foa['hand']='right'
                self.foa['finger']=0
                
            # Else shift to the next finger.
            
            else:
                self.foa['finger']+=1
        self.report()
    
    # This is just a reporting function (and helpers).  The fingers are
    # shown up (u) or down (d) for each hand, and the one begin attended to
    # is capitalized.
    
    def report(self):
        text=''
        for i in ['left','right']:
            for j in range(5):
                if (i==self.foa['hand'] and j ==self.foa['finger']):
                    text+=self.s[i][j].upper()
                else:
                    text+=self.s[i][j]   
        text=text[:5]+'|'+text[5:]
        trp(4,text)
    
    # Finger raising; always does the focussed finger.
    
    def put_up(self):
        self.s[self.foa['hand']][self.foa['finger']] = 'u'

    # The hands are external components as well, so 
    # that all you need to do is select a hand and switch hands.

    def choose(self):
        if randint(0,1)==0:
            self.hand='left'
        else:
            self.hand='right' 
        trp(3,'Looking to the %s hand.' % self.hand)
        self.foa['hand'] = self.hand
        self.foa['finger'] = 0
        self.report()
    
    def swap(self):
        if self.hand == 'left':
            self.hand='right'
            #mempush(swap-hands, from left to right)
        else:
            self.hand='left'
            #mempush(swap-hands, from right to left)
        trp(3,'Looking to the %s hand.' % self.hand)
        self.foa['hand'] = self.hand
        self.foa['finger'] = 0
        self.report()


# Maipulation in the echoic buffer where number facts live.  We
# assume perfect knowledge of the number sequence.  That way incr
# and decr can be used.  This is where all possible errors come into
# the picture.  There is a probability (*perr*) of say-next
# reporting the WRONG number; this always takes place by simply
# failing to count.  Note that there are really a number of ways
# that one can get errors in addition, but the basic effect of
# correlating errors with the number of step in the procedure is
# accomplished by this method.

def say(n):
    trp(2,'<%s>' % n)
    global EB
    EB = n
    #mempush(say, list n) 

def say_next():
    if EB==0:
        say(1)
    elif PERR>randint(1,100):
        say(EB)
    else:
        say(EB+1)

# Clear EB each time you're about to start a count off.  If you
# don't do this, the last number counted will be left in the echoic
# buffer and you'll count on from it, which is actually right, of
# course, for shortcut-sum.

def clear_eb():
    global EB
    EB = 0

# This tells the driver to stop.

def end():
    global SOLUTION_COMPLETED
    SOLUTION_COMPLETED = True
            
# Raise is an important heart of this process.  The question is how
# to do the test-for-done.  That is, when putting up fingers, how
# does the child know when he's got the right number up?  In this
# version, he uses the echoic buffer trace, but that can't be right
# for shortcut sum because the echoic buffer contains the SUM, not
# just the single hand's count, so the right hand won't work.
# Somehow the child can SAY one thing while covertly counting
# another.  This suggests a dissociation of the echoic number
# sequence from counting, which can be done covertly.  Instead of
# relying upon the echoic trace for the count, We uses a new buffer
# (*cb*) to maintain the count of fingers up on a particular hand.
# This buffer is cleared by raise2 itself, and is used for the done
# test.

def exec_op(op):
    trp(2,'Doing:(%s)' % op)
    #mempush (exect_op, lisp op)
    #funcall (car op)

# This version of raise assumes that hand control is done by the caller.

def raise_hand():
    global CB
    CB = 0
    while True:
        say_next()
        HAND.put_up()
        HAND.increment_focus()
        CB+=1
        if CB == ADDEND.addend:
            break
        
def count_fingers():
    for i in range(5):
        look_n_count()

def look_n_count():
    if HAND.s[HAND.foa['hand']][HAND.foa['finger']] == 'u':
        say_next()
    HAND.increment_focus()

# Finally we need to replace the n1 and n2 with echoic buffers so
# that they aren't arguments to a lisp function. This also requires
# putting the addends into external stores which, like the hands,
# can be attended.  Instead of doing all that I just assume here
# that the problem is written on an external board, and that there
# is a sort of second set of eyes that can look at one or the other
# addend, and swap them, just like with the hands.  We ought to
# organize all the different buffers.  I wonder if kids ever get
# these mixed up, and if not, why not?

class Addend(object):
    
    def __init__(self,ad1,ad2):
        self.ad1 = ad1
        self.ad2 = ad2
        self.addend = 0
        self.cla = ''

    def choose(self):
        if randint(0,1) == 0:
            self.addend = self.ad1
        else:
            self.addend = self.ad2
            
        # Indicate which addend we've chosen for min discovery.
        
        if self.ad1==self.ad2:
            self.cla = 'equal'
        elif ((self.addend==self.ad1) and (self.ad1>self.ad2)) or ((self.addend==self.ad2) and (self.ad1<self.ad2)):
            self.cla = 'larger'
        else:
            self.cla = 'smaller'
        trp(3, 'Choose addend %s.' % self.addend)

    def swap(self):
        if self.addend == self.ad1:
            self.addend = self.ad2
            #mempush (swap_addends, from 1 to 2)
        else:
            self.addend = self.ad1
            #mempush (swap_addeds, from 2 to 1)
        trp(3, 'Looking to the other addend %s.' % self.addend)
    
    def say(self):
        say(self.addend)
    
    def choose_larger(self):
        if self.ad1>self.ad2:
            self.addend = self.ad1
        else:
            self.addend = self.ad2
        
        if self.ad1 == self.ad2:
            self.cla = 'equal'
        else:
            self.cla = 'larger'
        trp(3, 'Choose addend %s.' % self.addend)



''' leaving space for line 1697-2304'''


#Here's are the actual strategies.

def count_from_one_twice():
    
    # First addend on first hand.
    
    HAND.clear()
    HAND.choose()
    ADDEND.choose()
    ADDEND.say()
    clear_eb()
    raise_hand()
    
    # Second addend on the other hand.
    
    HAND.swap()
    ADDEND.swap()
    ADDEND.say()
    clear_eb()
    raise_hand()
    
    #Final count out.
    
    HAND.choose()
    clear_eb()
    count_fingers()
    HAND.swap()
    count_fingers()
    
    end()

def test():
    global HAND, CB, EB, PERR, ADDEND
    
    PERR = 0
    HAND = Hand()
    ADDEND = Addend(3,4)
    count_from_one_twice()

def main():
    
    global TL, HAND, CB, EB, PERR, SOLUTION_COMPLETED, ADDEND, AD1, AD2, CLA
    TL=5 #trace level -- 0 means off
    
    test()
    

if __name__ == "__main__":
    main()
