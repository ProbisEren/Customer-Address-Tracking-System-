class Address:
    def __init__(self,city, district,neighborhood,street,building_no,flat_no,postal_code):
        self.__city = city
        self.__district = district
        self.__neighborhood = neighborhood
        self.__street = street
        self.__building_no = building_no
        self.__flat_no = flat_no
        self.__postal_code = postal_code
        self.__rented = False

    def get_rented(self):
        return self.__rented

    def set_rented(self, rented):
        self.__rented = rented

    def get_city(self):
        return self.__city

    def get_district(self):
        return self.__district

    def get_neighborhood(self):
        return self.__neighborhood
    def get_street(self):
        return self.__street
    def get_building_no(self):
        return self.__building_no
    def get_flat_no(self):
        return self.__flat_no
    def get_postal_code(self):
        return self.__postal_code