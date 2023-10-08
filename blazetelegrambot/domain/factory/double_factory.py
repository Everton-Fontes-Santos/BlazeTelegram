from ..entitys.double import Double

from datetime import datetime

class DoubleFactory:
    
    @staticmethod
    def create(broker:str, roll:int, creation_time:datetime, id:str='')->Double:
        color = 0
        if roll >=1 and roll <=7:
            color =1
        if roll >=8 and roll <=14:
            color =2
        
        if id:
            double = Double(
                id=id,
                broker=broker,
                color=color,
                roll=roll,
                creation_time=creation_time
            )
        else:
            double = Double(
                broker=broker,
                color=color,
                roll=roll,
                creation_time=creation_time
            )
            
        return double
        