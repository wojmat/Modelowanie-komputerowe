#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>

int main() {
    int plansza[40] = { 0 }; 
    int pozycja_gracza = 0; 

    srand(time(NULL)); 
    int n_rz; // Liczba rzutów kostkami.
    std::cout << "Ile rzutow koscmi?" << std::endl;
    std::cin >> n_rz; 

    for (int i = 0; i < n_rz; i++) {
        int kostka1 = rand() % 6 + 1; 
        int kostka2 = rand() % 6 + 1; 
        int suma = kostka1 + kostka2; 

        if ((pozycja_gracza + suma) < 40) {
            pozycja_gracza += suma; // Aktualizacja pozycji gracza, jeśli nie przekroczył końca planszy.
        } else {
            pozycja_gracza = (pozycja_gracza + suma) % 40; // Powrót na początek planszy po przekroczeniu 40 pól.
        }
        // Sprawdzenie, czy gracz trafił na pole "Idziesz do więzienia". Zaczynamy liczenie od pola 0.
        if (pozycja_gracza == 29) { // Sprawdzenie, czy gracz trafił na pole "Idziesz do więzienia".
            plansza[pozycja_gracza] += 1; // Zwiększenie licznika wizyt na polu "Idziesz do więzienia".
            pozycja_gracza = 9; // Przesunięcie gracza do więzienia.
            plansza[pozycja_gracza] += 1; // Zwiększenie licznika wizyt na polu "Więzienie".
        } else {
            plansza[pozycja_gracza] += 1; 
        }
    }

    std::ofstream outfile("output_with_jail.txt"); 

    for (int j = 0; j < 40; j++) {
        double procent = (double)plansza[j] / n_rz * 100; // Obliczenie procentowej szansy wizyty na polu.
        outfile << "Pole " << j + 1 << ": " << plansza[j] << " (" << procent << "%)" << std::endl; 
    }

    outfile.close(); 

    return 0;
}
