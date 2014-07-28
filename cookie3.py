"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from thinkbayes import Pmf

class Bowl:
  """Helper class to keep the number of cookies and calculate priors"""
  
  mix = {}

  def __init__(self,chocolate,vanilla):
    """Initialize self.

    chocolate and vanilla: count of cookies initially
    """
    self.mix = {'vanilla':vanilla,'chocolate':chocolate}
    print 'Initialized bowl with ',self.mix

  def Eat(self,kind):
    """Consume a kind of cookie"""
    chocolateCount = self.mix['chocolate']
    vanillaCount = self.mix['vanilla']

    if kind=="chocolate" and chocolateCount>0:
      chocolateCount = chocolateCount-1

    if kind=="vanilla" and vanillaCount>0:
      vanillaCount = vanillaCount-1

    self.mix = {'vanilla':vanillaCount,'chocolate':chocolateCount}

  def Prob(self,kind):
    """Return the probability of getting the type of cookie"""
    chocolateCount = self.mix['chocolate']
    vanillaCount = self.mix['vanilla']
    print 'V=',vanillaCount,' C=',chocolateCount
    prob = 0
    if kind=="chocolate":
      prob = (float(chocolateCount))/(chocolateCount+vanillaCount)
    if kind=="vanilla":
      prob = (float(vanillaCount))/(chocolateCount+vanillaCount)
    print 'Prob for ',kind,' = ',prob
    self.Eat(kind)
    return prob

class Cookie(Pmf):
    """A map from string bowl ID to probablity."""

    def __init__(self, hypos):
        """Initialize self.

        hypos: sequence of string bowl IDs
        """
        Pmf.__init__(self)
        for hypo in hypos.keys():
            self.Set(hypo, 1)
            self.bowls[hypo] = Bowl(chocolate=hypos[hypo]['chocolate'],vanilla=hypos[hypo]['vanilla'])
        self.Normalize()        

    def Update(self, data):
        """Updates the PMF with new data.

        data: string cookie type
        """
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()

    bowls = {}

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """
        bowl = self.bowls[hypo]
        like = bowl.Prob(data)
        
        return like

def printPosteriors(pmf):
    for hypo, prob in pmf.Items():
        print hypo, prob


def main():
    hypos = {'Bowl 1':{'chocolate':3,'vanilla':9}, 
        'Bowl 2':{'chocolate':6,'vanilla':6}}

    pmf = Cookie(hypos)

    pmf.Update('vanilla')
    printPosteriors(pmf)
    print '-------'
    pmf.Update('chocolate')
    printPosteriors(pmf)
    print '-------'
    pmf.Update('vanilla')
    printPosteriors(pmf)
    print '-------'



if __name__ == '__main__':
    main()
