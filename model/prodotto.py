from dataclasses import dataclass

@dataclass
class Prodotto:
    id:int
    product_name:str
    brand_id:int
    category_id:int
    model_year:int
    list_price:float

    def __str__(self):
        return f"{self.product_name} {self.brand_id} "

    def __repr__(self):
        return f"{self.product_name} {self.brand_id} "

    def __hash__(self):
        return hash(self.id)