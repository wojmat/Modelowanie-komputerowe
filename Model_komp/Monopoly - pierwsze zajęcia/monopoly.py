import matplotlib.pyplot as plt
import random

#Rzut dwiema kośćmi
def rzuc_koscmi():
    return random.randint(1, 6) + random.randint(1, 6)

#Ruch definiowany jako reszta z dzielenia przez 40 rozwiązuje problem z powrotem do początku planszy (gdy gracz zrobi pełne okrążenie)
def ruch(pozycja, ileOczek):
    return (pozycja + ileOczek) % 40

#Funkcja gry przyjmuje zadeklarowaną liczbę ruchów

def start(ileRuchow):
    #Tworzenie pustej planszy i warunki początkowe
    plansza = [0] * 40
    pozycja = 0
    wiezienie = False
    licznikWiezienie = 0
    
    #Główna pętla
    for _ in range(ileRuchow):
        #Zmiana pozycji po rzucie kośćmi
        pozycja = ruch(pozycja, rzuc_koscmi())
        #Pole więzienia
        if pozycja == 30:
            #Przyjęcie statusu więźnia i przeniesienie na pole 10
            wiezienie = True
            pozycja = 10
            continue
        #Jeżeli gracz jest w więzieniu sprawdzamy ile już tam siedzi i rzucamy kośćmi (dwa razy taka sama liczba oczek to wyjście z więznienia)
        if pozycja == 10 and wiezienie == True:
            if licznikWiezienie == 3:
                wiezienie = False
                licznikWiezienie = 0
                continue
            if random.randint(1, 6) == random.randint(1, 6):
                wiezienie = False
                licznikWiezienie = 0
                continue
            licznikWiezienie += 1

        #Zapisz pozycję do tablicy
        plansza[pozycja] += 1

    #Zwracamy prawdopodobieństwo
    return [ilosc/ileRuchow for ilosc in plansza]

def prawdopodobienstwo(tytul,wartosci):
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(wartosci)), wartosci)
    plt.title(tytul)
    plt.xlabel('Pole na planszy')
    plt.ylabel('Prawdopodobieństwo')
    plt.show()

ILE_RUCHOW_1 = 100
rozklad1 = start(ILE_RUCHOW_1)
prawdopodobienstwo('Po 100 ruchach', rozklad1)

ILE_RUCHOW_2 = 1000000
rozklad2 = start(ILE_RUCHOW_2)
prawdopodobienstwo('Po 1000000 ruchów', rozklad2)

