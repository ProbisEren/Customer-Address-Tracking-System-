class Contract:
    def __init__(self, customer_id, address_id, kira, imza_tarihi, finish_date, fesih_bedeli, notlar=None):
        self.__customer_id = customer_id
        self.__address_id = address_id
        self.__kira = kira
        self.__imza_tarihi = imza_tarihi
        self.__finish_date = finish_date
        self.__fesih_bedeli = fesih_bedeli
        self.__notlar = notlar

    def get_customer_id(self):
        return self.__customer_id

    def get_address_id(self):
        return self.__address_id

    def get_kira(self):
        return self.__kira

    def get_imza_tarihi(self):
        return self.__imza_tarihi

    def get_finish_date(self):
        return self.__finish_date

    def get_fesih_bedeli(self):
        return self.__fesih_bedeli

    def get_notlar(self):
        return self.__notlar
