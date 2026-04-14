import os
import json
import asyncio
from datetime import datetime
from typing import Optional
from fetch_pric3 import fetchPrices

class Bot:

    def __init__(self, Data_File: str = 'gold_prices.json', threshold: float = 1.0) -> None:
        
        self.Data_File = Data_File
        self.threshold = threshold
        self.previous = None

        def loadPrice():
            if os.path.exists(Data_File):
                try:

                    with open(Data_File, 'r') as rf:
                        data = json.load(rf)

                        return data.get('previous_price')
                    
                except (json.JSONDecodeError, IOError) as e:
                        print(f"Error loading price: {e}")
                        
                        return None
            
            return None
        

        def savePrice(price) -> None:
            data = {
                'previous_price': price,
                'time': str(datetime.now())
            }

            try:
                with open(Data_File, 'w') as wf:
                    json.dump(data, wf)

            except IOError as e:
                print(f"Error saving price: {e}")