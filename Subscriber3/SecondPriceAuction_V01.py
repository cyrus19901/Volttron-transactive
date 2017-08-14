# This code emulates the sealed second price bid auction, proposed by Derek.

import numpy as np
import os
os.system('cls')

Sellers = ['WSU','UofW','Macys',
          'AvistaBuilding','House01','House02','House03']
N=len(Sellers)   # Number of Sellers

# Creating Random Bid Prices and Ramdom Bid MW Quantities
# np.random.seed(seed=0)
BidPrice=np.random.randint(90,120,len(Sellers))
BidQuant=np.round(np.random.randint(500,3000,len(Sellers))/1000,1)

# Creating the MW that the PV requires to purchase
Qreq=np.sum(BidQuant)/2


# -------------- BEGIN: Second Price auction Algorithm -----------------
pos=np.argsort(BidPrice)    # Sorting the Bids by price (cheapest to highest)
BidPriceSorted=BidPrice[pos]    # Bid prices sorted (cheapest to highest)
BidQuantSorted=BidQuant[pos]    # MW quantities sorted by price

Qreq_aux=Qreq
Seller_i=0
Str='The winners are: '
QuantBuyed=np.zeros(N)          # Results of the Auction Winners 

while Seller_i <= N and Qreq_aux>0:     # Stack Algorithm.
    # Taking into account the price ordered bids,
    # If the Quantity offered by the Seller is lower thant the 
    # remaining PV required quantity, then, the energy offered by the seller 
    # is purchased (QuantBuyed vector). Remaining Quantity is updated
    if BidQuantSorted[Seller_i] <= Qreq_aux:
        QuantBuyed[Seller_i] = BidQuantSorted[ Seller_i ]
        Qreq_aux = Qreq_aux - BidQuantSorted[ Seller_i ]
        Str = Str + Sellers[pos[Seller_i]] +"; "
    elif BidQuantSorted[Seller_i] > Qreq_aux:
        QuantBuyed[Seller_i]=Qreq_aux
        Str = Str + Sellers[pos[Seller_i]]
        Qreq_aux=0
    Seller_i=Seller_i+1
    SecondPriceRes=BidPriceSorted[min(Seller_i,N-1)]    # Next bid Price 
# -------------- END: Second Price auction Algorithm -----------------

# -------------- BEGIN: Showing Results  -----------------
print('The Quantity required by the PV is: ', Qreq," [MW]" )
print('The MW offered are: ', BidQuantSorted ," [MW]")
print('The bid prices are: ', BidPriceSorted, " [USD]" )
print(Str)
print('The Quantities buyed are: ', QuantBuyed," [MW]" )
print('The closing price of the "Second price Auction" is: ', SecondPriceRes, " [USD]")

# -------------- END: Showing Results  -----------------
