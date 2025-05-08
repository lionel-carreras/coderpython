from login import Usuarios


class Index:
    def __init__(self):
        self.inicio()

    def inicio(self):
        print('BIENVENIDO A MARKET-PLUS')
        print ("debe iniciar sesión o registrarse para comprar : \n")
        print('------------------------------')

        while True:
            try:      
                entrada=int(input('ingrese 1 para loguearse\n ingrese 2 para registrarse :'))
                if entrada == 1:
                    return Usuarios.login(self)
                elif entrada == 2:
                    return Usuarios.registrarse(self)
                else:
                    print('intentelo nuevamente')
                    return self.inicio()
            except ValueError:
                print('Ingrese la opción correcta')
iniciar = Index()  
          
iniciar.inicio()