from AddressManager import *
from Customer import *
from Address import *
from DatabaseManager import *
from CustomerManager import *

#customer1 = Customer("eren","uzun", 20,5533967919,"metineren0061@gmail.com",1,1)
#customer4 = Customer("Ahmet", "Yılmaz", 30, "05551234567", "ahmet@example.com",2,2)
#customer2 = Customer("Ayşe", "Demir", 25, "05559876543", "ayse@example.com",3,3)
#customer3 = Customer("Mehmet", "Kara", 40, "05551230000", "mehmet@example.com",4,4)




#CustomerManager.delete_customer_by_id(5)

#address1 = Address("Trabzon","Akçabat","Dürbinar", "Okullar", 3,13,61547)





db = DatabaseManager()
db.create_all_tables()
#AddressManager.add_address(address1)




#customers = CustomerManager.get_all_customers()
#for c in customers:
   # print(c.get_name(), c.get_surname())

#CustomerManager.add_customer(customer1)
#CustomerManager.add_customer(customer4)
#CustomerManager.add_customer(customer2)
#CustomerManager.add_customer(customer3)
#CustomerManager.remove_customer_address(1)