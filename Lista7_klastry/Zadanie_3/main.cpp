#define OLC_PGE_APPLICATION
#include "olcPixelGameEngine.h"

const int W = 1280;
const int H = 720;
int stan[2][W][H];

class Platek : public olc::PixelGameEngine
{
public:
    Platek()
    {
        sAppName = "Wzrost płatka śniegu";
        t = 0;
        c = 0;
        init(c);
        pause = 0;
        rule = 0;
    }

    bool OnUserCreate() override
    {
        return true;
    }

    void init(int _c)
    {
        // Resetowanie stanu
        for (int i = 0; i < W; i++)
            for (int j = 0; j < H; j++)
            {
                stan[_c][i][j] = stan[1 - _c][i][j] = 0;
            }

        // Inicjalizacja początkowego płatka w centrum
        stan[_c][W / 2][H / 2] = stan[1 - _c][W / 2][H / 2] = 1;
    }

    void platek(int _c, int rule)
    {
        // Zmienne pomocnicze dla indeksów sąsiadów
        int ip, im, jp, jm;

        for (int i = 0; i < W; i++)
        {
            for (int j = 0; j < H; j++)
            {
                ip = (i + 1) % W;
                im = (i - 1 + W) % W;
                jp = (j + 1) % H;
                jm = (j - 1 + H) % H;

                int s1, s2, s3, s4, s5, s6;
                int p = j % 2; // parzysty wiersz
                if (p == 0)
                {
                    s1 = stan[_c][ip][j];
                    s2 = stan[_c][ip][jp];
                    s3 = stan[_c][i][jp];
                    s4 = stan[_c][im][j];
                    s5 = stan[_c][i][jm];
                    s6 = stan[_c][ip][jm];
                }
                else
                {
                    s1 = stan[_c][ip][j];
                    s2 = stan[_c][i][jp];
                    s3 = stan[_c][im][jp];
                    s4 = stan[_c][im][j];
                    s5 = stan[_c][im][jm];
                    s6 = stan[_c][i][jm];
                }

                int sum = s1 + s2 + s3 + s4 + s5 + s6;

                bool grow = false;
                switch (rule)
                {
                    case 0:
                        grow = (sum == 1);
                        break;
                    case 1:
                        grow = (sum == 2);
                        break;
                    case 2:
                        grow = (sum > 0);
                        break;
                    case 3:
                        grow = (sum % 3 == 0 && sum > 0); // Dodatkowa zasada: wzrost dla sumy sąsiadów podzielnej przez 3, ale większej od 0
                        break;
                }

                if (!stan[_c][i][j] && grow)
                {
                    if (i <= 0 || i >= W - 1 || j <= 0 || j >= H - 1)
                        pause = 1;

                    stan[1 - _c][i][j] = 1;
                }
                else if (stan[_c][i][j])
                {
                    stan[1 - _c][i][j] = 1;
                }
            }
        }
    }

    bool OnUserUpdate(float fElapsedTime) override
    {
        t += fElapsedTime;

        Clear(olc::Pixel(0, 0, 0));

        if (GetKey(olc::Key::ESCAPE).bPressed)
            exit(0);

        if (GetKey(olc::Key::SPACE).bPressed)
        {
            init(c);
            pause = 0;
        }

        if (GetKey(olc::Key::K1).bPressed)
            rule = 0;
        if (GetKey(olc::Key::K2).bPressed)
            rule = 1;
        if (GetKey(olc::Key::K3).bPressed)
            rule = 2;
        if (GetKey(olc::Key::K4).bPressed)
            rule = 3; // Dodatkowa zasada

        // Rysowanie stanu automatu komórkowego
        for (int j = 0; j < H; j++)
            for (int i = 0; i < W; i++)
            {
                int r, g, b;

                r = g = b = stan[c][i][j] * 255;
                Draw(i, j, olc::Pixel(r, g, b));
            }

        if (!pause)
        {
            platek(c, rule);
            c = 1 - c;
        }
        return true;
    }

private:
    float t;
    int c;
    int pause;
    int rule;
};

int main()
{
    Platek demo;
    if (demo.Construct(W, H, 1, 1))
        demo.Start();

    return 0;
}
