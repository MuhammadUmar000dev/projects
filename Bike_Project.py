#A Bike Rental System
#Phle ye k total bike stock batana hai
#user bike rent pr le skta hai
#to total no of quantity wo add karega to hum uske according price dikhaenge
# 1 quantity of price 100 rup set karke logic lagaenge
#Agr wo 50 bike rents pr leta hai to hum usko 50 into 100 set karke display karnge
#Agrwo 50 bike leta hai to usko available stock b dikhana hai

#1-Display available bikes
#2-Request a bike for rent(100 ->1 qty)
#3-Exit

class BikeShop:

    def __init__(self,stock):
        self.stock=stock #self.stock me jitne hum add karnge utne honge
    def displayBike(self): #displaybike me jitna available stock hoga utna show hoga
        print("Total Bikes ",self.stock)
    def rentForBike(self,q): #q means quantity kitni chaiye
        if q<=0:
            print("Enter the Quantity number, greater than 0...")
        elif q>self.stock:
            print('''Limited stock
            please write according to the stock we have.''')
        else:
            self.stock=self.stock-q
            print("Total Price ",q*100)
            print("Total Stock ",self.stock)
while True:
    obj=BikeShop(100) #ye bike ka stock hai
    uc=int(input('''
    1- Display Stock
    2- Wanna rent bike/bikes
    3- Exit
    Enter the choice No...'''))
    if uc==1:
        obj.displayBike()
    elif uc==2:
        n=int(input("Enter the Quantity...")) #user quantity bataega
        obj.rentForBike(n)
    else:
        break

