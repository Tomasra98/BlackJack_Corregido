import random

class Carta:
    def __init__(self, pinta: str, valor: str):
        self.pinta = pinta
        self.valor = valor
        self.tapada = False

    def __str__(self):
        if self.tapada:
            return "Carta tapada"
        else:
            return f'{self.valor} de {self.pinta}'

class Baraja:
    def __init__(self):
        self.cartas = []
        self.revolver()

    def revolver(self):
        pintas = ['CORAZÓN', 'TRÉBOL', 'DIAMANTE', 'ESPADA']
        valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cartas = [Carta(pinta, valor) for pinta in pintas for valor in valores]
        random.shuffle(self.cartas)

    def repartir_carta(self, tapada: bool) -> Carta:
        carta = self.cartas.pop()
        carta.tapada = tapada
        return carta

class Mano:
    def __init__(self):
        self.cartas = []

    def recibir_carta(self, carta):
        self.cartas.append(carta)

    def calcular_valor(self):
        valor = sum([10 if carta.valor in ['J', 'Q', 'K'] else int(carta.valor) for carta in self.cartas])
        ases = [carta for carta in self.cartas if carta.valor == 'A']
        for _ in ases:
            if valor > 21:
                valor -= 10
        return valor

class Blackjack:
    def __init__(self):
        self.jugador = None
        self.fichas = 0
        self.baraja = None

    def registrar_jugador(self, nombre):
        self.jugador = nombre
        self.fichas = 100
        self.baraja = Baraja()
        print(f'Bienvenido, {self.jugador}!')
        self.menu()

    def iniciar_juego(self, apuesta):
        self.fichas -= apuesta
        self.baraja.revolver()

        mano_jugador = Mano()
        mano_casa = Mano()

        mano_jugador.recibir_carta(self.baraja.repartir_carta(False))
        mano_jugador.recibir_carta(self.baraja.repartir_carta(False))

        mano_casa.recibir_carta(self.baraja.repartir_carta(False))
        mano_casa.recibir_carta(self.baraja.repartir_carta(True))

        self.mostrar_mano('Tu mano', mano_jugador.cartas)
        self.mostrar_mano('Mano de la casa', [mano_casa.cartas[0], Carta("DESCONOCIDO", "DESCONOCIDO")])

        if mano_jugador.calcular_valor() == 21:
            print('¡Blackjack! Ganaste la mano.')
            self.fichas += apuesta * 2
            self.menu()
        else:
            self.hacer_jugada_jugador(mano_jugador, mano_casa, apuesta)

    def hacer_jugada_jugador(self, mano_jugador, mano_casa, apuesta):
        while True:
            print('Opciones:')
            print('1. Pedir carta')
            print('2. Plantarse')
            opcion = input('Selecciona una opción: ')

            if opcion == '1':
                carta_nueva = self.baraja.repartir_carta(False)
                mano_jugador.recibir_carta(carta_nueva)
                self.mostrar_mano('Tu mano', mano_jugador.cartas)

                if mano_jugador.calcular_valor() > 21:
                    print('Te has pasado de 21. Pierdes la mano.')
                    self.menu()
            elif opcion == '2':
                break
            else:
                print('Opción no válida. Selecciona 1 para pedir carta o 2 para plantarse.')

        self.hacer_jugada_casa(mano_jugador, mano_casa, apuesta)

    def hacer_jugada_casa(self, mano_jugador, mano_casa, apuesta):
        mano_casa.cartas[1].tapada = False
        self.mostrar_mano('Mano de la casa', mano_casa.cartas)

        while mano_casa.calcular_valor() <= 16:
            carta_nueva = self.baraja.repartir_carta(False)
            mano_casa.recibir_carta(carta_nueva)
            self.mostrar_mano('Mano de la casa', mano_casa.cartas)

        if mano_casa.calcular_valor() > 21:
            print('La casa se ha pasado de 21. ¡Ganas la mano!')
            self.fichas += apuesta * 2
        elif mano_casa.calcular_valor() >= mano_jugador.calcular_valor():
            print('La casa gana. Pierdes la mano.')
        else:
            print('¡Ganas la mano!')
            self.fichas += apuesta * 2

        self.menu()

    def mostrar_mano(self, nombre, cartas):
        print(f'{nombre}:')
        for carta in cartas:
            print(carta)
        print(f'Valor total: {Mano().calcular_valor()}')