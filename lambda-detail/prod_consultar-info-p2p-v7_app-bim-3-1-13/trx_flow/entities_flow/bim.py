
import ewp as ew
from errores_ewp import *
from operacion import *
import config as cfg
import errores

class Bim:

    def __init__(self, origin_msisdn, destination_msisdn, firstname, surname):
        self.origin_msisdn = origin_msisdn
     
        self.destination_msisdn = destination_msisdn
        self.firstname = firstname
        self.surname = surname

        self.fullname = self.format_fullname(self.firstname +' '+ self.surname)
        self.comision = cfg.default_comision

        self.op = Operacion()
        self.ewp = ew.EWP_APIS()
        

    def format_fullname(self, fullname):
        fullname = fullname.replace(' / ', ' ')
        fullname = fullname.replace('/', ' ')
        fullname = fullname.title()
        return fullname