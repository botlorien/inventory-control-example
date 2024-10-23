from typing import List

class Inventory:
    _inventory:List[List[dict]]


    def __init__(self,inventory) -> None:
        self.inventory = inventory

    @property
    def inventory(self):
        return self._inventory
    
    @inventory.setter
    def inventory(self,new):
        template={'product':str,'stock':int}
        if all(isinstance(sublist,list) and all(isinstance(item,dict) and type(item.get('product')) == template.get('product') and type(item.get('stock')== template.get('stock')) for item in sublist) for sublist in new for item in sublist):
            self._inventory=new
        else:
            raise ValueError(
                f"Invalid input value for inventory: {new}. Expected [[{'product':str(value),'stock':int(value)}],...]"
            )

    def __repr__(self) -> str:
        return f'Inventory({self.inventory})'

    def __iadd__(self,add):
        if isinstance(add,int):
            for i,sublist in enumerate(self.inventory):
                for k, item in enumerate(sublist):
                    item['stock'] += add
            return self
        else:
            raise TypeError(
                f"Invalid input type got: {type(add)}. Expected 'int'"
            )


    def __imul__(self,mul):
        if isinstance(mul,int):
            for i,sublist in enumerate(self.inventory):
                for k,item in enumerate(sublist):
                    item['stock'] *= mul
            return self
        else:
            raise TypeError(
                f"Invalid input type got: {type(mul)}. Expected 'int'"
            )
    
    def __getitem__(self,index):
        if isinstance(index, tuple):
            row_index,col_index = self._process_ellipsis(index)
            print(row_index,col_index)
            return self.inventory[row_index][col_index]
        return self.inventory[index]
    
    def _process_ellipsis(self,index):
        if Ellipsis in index:
            ellipsis_pos = index.index(Ellipsis)
            if ellipsis_pos == 0:
                col_index = index[1]
                return slice(None),col_index
            elif ellipsis_pos == 1:
                row_index = index[0]
                return row_index,slice(None)
        else:
            return index

    def execute(self,action,value):
        match action:
            case "aumentar_estoque":
                self += value
            case "multiplicar_estoque":
                self *= value
            case "checar_estoque":
                found_stock =[item for sublist in self.inventory for item in sublist if value in item.values()]
                print(f'Estoque do produto {value}: {list(found_stock)}')
            case _:
                raise ValueError(
                    f"Comando invalido: {action}"
                )

if __name__=='__main__':
        # Criando o inventário
    inventory = Inventory([
        [{"product": "Laptop", "stock": 50}, {"product": "Mouse", "stock": 200}],
        [{"product": "Shirt", "stock": 100}, {"product": "Shoes", "stock": 80}],
    ])
    print(inventory)

    # Aumentando o estoque de todos os produtos em 10
    inventory += 10
    print("Inventario adicionado: ",inventory)

    # Multiplicando o estoque de todos os produtos por 2
    inventory *= 2
    print("Inventario multiplicado: ",inventory)

    # Acessando todos os produtos da primeira categoria
    print("Inventario filtrado: ",inventory[1,0])

    # Acessando o estoque de um produto específico
    print("Inventario filtrado stock: ",inventory[1, 0]["stock"])  # Estoque de Shirt

    # Executando um comando com match/case
    inventory.execute("aumentar_estoque", 5)
    
    print("Inventario adicionado: ",inventory)
    inventory.execute("checar_estoque", "Mouse")
