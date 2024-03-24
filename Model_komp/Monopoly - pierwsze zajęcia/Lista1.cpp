#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>

int main()
{
    int plansza[40] = { 0 };
    int pozycja_gracza = 0;

    srand(time(NULL));

    int n_rz;
    std::cout << "Ile rzutow koscmi?" << std::endl;
    std::cin >> n_rz;

    for (int i = 0; i < n_rz; i++)
    {
        int kostka1 = rand() % 6 + 1;
        int kostka2 = rand() % 6 + 1;

        int suma = kostka1 + kostka2;

        if ((pozycja_gracza + suma) < 40)
        {
            pozycja_gracza += suma;
        }
        else 
        {
            pozycja_gracza = (pozycja_gracza + suma) % 40;
        }

        if (pozycja_gracza == 30)
        {
            plansza[pozycja_gracza] += 1;
            pozycja_gracza = 10;
        }
        else
        {
            plansza[pozycja_gracza] += 1;
        }
    }

    std::ofstream outfile("output.txt");

    for (int j = 0; j < 40; j++) {
        double procent = (double)plansza[j] / n_rz * 100;
        outfile << "Pole " << j + 1 << " " << plansza[j] << " (" << procent << "%)" << std::endl;
    }

    outfile.close();

    return 0;
}
