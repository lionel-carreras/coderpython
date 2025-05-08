import pandas as pd

#clase padre 
class Usuarios:
    def __init__(self, usuario, password,rol,usuario_id):
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.id = usuario_id

    def __str__(self):
        return (
            f"Usuario ID: {self.id}\n"
            f"Usuario:   {self.usuario}\n"
            f"Rol:       {self.rol}"
            
        )

    def login(self):
            intentos=0
            while True:   
                print('------LOGIN-----')
                if intentos <= 3:
                    intentos += 1
                else :
                    print('Demasiados intentos, cuenta bloqueada')    
                    break
                nombre_ingresado= input('ingrese su nombre: ')
                contraseña_ingresada = input('ingrese su contraseña: ')
                data = pd.read_csv('base.csv')
                encontrado=False
                for i, filas in data.iterrows():
                    if filas['usuario'] == nombre_ingresado and filas['password'] == contraseña_ingresada:
                        encontrado = True
                        rol=filas['rol'] 
                        usuario_id=filas['id']
                        nombre=filas['nombre']
                        apellido=filas['apellido']
                        edad=filas['edad']
                        direccion=filas['direccion']
                        telefono=filas['telefono']
                        limite_credito=filas['limite_credito']
             
                        instancia = Web(nombre_ingresado,contraseña_ingresada,rol,usuario_id,nombre,apellido,edad,direccion,telefono,limite_credito)
                        instancia.web()
                        
                if not encontrado:
                        print('usuario o contraseña incorrecto')

                        
    def registrarse(self):
            nombre=input('ingrese su nombre: ')
            apellido=input('ingrese su apellido: ')
            edad=int(input('ingrese su edad: '))
            direccion=input('ingrese su direccion: ')
            telefono=int(input('ingrese su telefono: '))
            usuario=input('ingrese su nombre de usuario: ')
            password=input('ingrese su contraseña: ')
            rol='cliente'
            limite_credito=200000
             
            
            data=pd.read_csv('base.csv')
            id=data['id'].max()+1
            nuevo_usuario=[id,usuario,password,rol,nombre,apellido,edad,direccion,telefono,limite_credito]
            data.loc[len(data)]=nuevo_usuario
            data.to_csv('base.csv', index=False)
            return Usuarios.login(self)

#clase cliente hereda de Usuarios                             
class Cliente(Usuarios):
    def __init__(self,usuario,password,rol,id,nombre,apellido,edad,direccion,telefono,limite_credito):
        Usuarios.__init__(self,usuario,password,rol,id)
        self.nombre=nombre
        self.apellido=apellido
        self.edad=edad
        self.direccion=direccion
        self.telefono=telefono
        self.limite_credito=limite_credito

    def editar_perfil(self):
        usuario=self.usuario
        contreseña=self.password
        rol=self.rol
        id=self.id
        data=pd.read_csv('base.csv')

        cliente_id= data['id']==self.id
        if cliente_id.any():
            for campos in ['nombre','apellido','edad','direccion','telefono']:
                valor_actual = data.loc[cliente_id, campos].values[0]
                if pd.isna(valor_actual) or valor_actual == '':
                    entrada = input(f'ingrese el {campos} = ')
                    data.loc[cliente_id, campos] = entrada
            else :
                edad=data.loc[cliente_id, 'edad'].values[0]
                edad=int(edad)
                telefono=data.loc[cliente_id, 'telefono'].values[0]
                telefono=int(telefono)
                print(f'nombre: {data.loc[cliente_id, "nombre"].values[0]} \n apellido: {data.loc[cliente_id, "apellido"].values[0]} \n edad: {edad} \n direccion: {data.loc[cliente_id, "direccion"].values[0]} \n telefono: {telefono}')
        else :
            print('el usuario no existe')   

        data.to_csv('base.csv', index=False)

        return Web.web(self)
        
    def comprar(self):

        print('------Bienvenido a la tienda-----')
        print('--------------------------------')
        print('Estos son los productos disponibles:')
        productos_df = pd.read_csv('productos.csv')
        print(productos_df)
        while True:
            try:
                seleccion = int(input('Ingrese el ID del producto que desea comprar (0 para salir): '))
                if seleccion == 0:
                    print("Volviendo al menú principal...")
                    return Web.web(self)
                elif seleccion in productos_df['id'].values:
                    cantidad = int(input('Ingrese la cantidad que desea comprar: '))
                    producto = productos_df[productos_df['id'] == seleccion].iloc[0]
                    precio_total = producto['precio'] * cantidad
                    print(f'El precio total de su compra es: {precio_total}')
                    confirmacion = input('¿Desea confirmar la compra? (s/n): ')
                    if confirmacion.lower() == 's':
                        usuarios_df =pd.read_csv('base.csv')
                        cliente_id= usuarios_df['id']==self.id
                        if usuarios_df.loc[cliente_id, 'limite_credito'].values[0] < precio_total:
                            print('saldo insuficiente')
                        else:
                            usuarios_df.loc[cliente_id, 'limite_credito'] -= precio_total
                            usuarios_df.to_csv('base.csv', index=False)
                            productos_df = pd.read_csv('productos.csv')
                            productos_df.loc[productos_df['id'] == seleccion, 'cantidad'] -= cantidad
                            productos_df.to_csv('productos.csv', index=False)
                            estadisticas_df = pd.read_csv('estadisticas.csv')
                            estadisticas_df.loc[estadisticas_df['id'] == seleccion, 'cantidad'] -= cantidad
                            estadisticas_df.loc[estadisticas_df['id'] == seleccion, 'vendidos'] += cantidad
                            estadisticas_df.to_csv('estadisticas.csv', index=False)
                            print('¡Compra realizada con éxito!')
                    else:
                        print('Compra cancelada.')
                else:
                    print('ID de producto no válido. Intente nuevamente.')
            except ValueError:
                print('Entrada no válida. Ingrese un número.')
                
    def estadisticas(self):
        print(f'Bienvenido {self.nombre} rol-> {self.rol}')
        print('--------------------------------')
        estadistica_df = pd.read_csv('estadisticas.csv')
        print(estadistica_df)
        return Web.web(self)
        
        
        

        
# clase web emulando pagina web heredando de Cliente

class Web(Cliente):
    def __init__(self, usuario, password,rol,usuario_id,nombre,apellido,edad,direccion,telefono,limite_credito):
        super().__init__(usuario, password,rol,usuario_id,nombre,apellido,edad,direccion,telefono,limite_credito)
        
    def web(self):
        
        if self.rol == "admin":
            print('------Bienvenido Administrador-----')
            print('--------------------------------')
            seleccion=input('escriba "es" para ver estadisticas = \n presione s para salir = \n =>')
        
            if seleccion.lower() == 'es':
                return Cliente.estadisticas(self)
            elif seleccion == 's':
                print("Saliendo de la web...")
            
                
               
            
        elif self.rol == "cliente":
            print(f'------Bienvenido Sr. Cliente -----')
            
            print('--------------------------------')
            seleccion=input('presione e para editar su perfil = \n presione c para comprar = \n presione s para salir = \n => ')
        
            if seleccion.lower() == 'e':
                return Cliente.editar_perfil(self)
            elif seleccion.lower() == 'c':
                return Cliente.comprar(self)
            elif seleccion.lower() == 's':
                print("Saliendo de la web...")
                return self.login()
                 
                

                

            
user=Usuarios('usuario','password','rol','id')
cliente=Cliente('usuario','password','rol','id','nombre','apellido','edad','direccion','telefono','limite_credito')
pagina = Web('usuario','password','rol','usuario_id','nombre','apellido','edad','direccion','telefono','limite_credito')
pagina.web()

                