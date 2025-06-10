
class Customer:

    def __init__(self, name, surname, age, phone_number, email, address_id=None, contract_id=None):
        self.__name = name
        self.__surname = surname
        self.__age = age
        self.__phone_number = phone_number
        self.__email = email
        self.__address_id = address_id
        self.__contract_id = contract_id




    def get_address_id(self):
        return self.__address_id

    def set_address_id(self, new_id):
        self.__address_id = new_id

    def get_contract_id(self):
        return self.__contract_id

    def set_contract_id(self, new_id):
        self.__contract_id = new_id

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname
    def get_age(self):
        return self.__age
    def get_phone_number(self):
        return self.__phone_number
    def get_email(self):
        return self.__email
