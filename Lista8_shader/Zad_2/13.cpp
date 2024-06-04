void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Normalizowanie współrzędnych pikseli do zakresu [0,1]
    vec2 p = fragCoord.xy / iResolution.xy;
    
    // Normalizowanie współrzędnych myszki do zakresu [0,1]
    vec2 mouse = iMouse.xy / iResolution.xy;
    
    // Obliczenie odległości od środka ekranu, przemnożenie przez 10 i dodanie 0.5
    float d = length(p - 0.5) * 10.0 + 0.5;
    
    // Obliczenie kąta (phi) od środka ekranu
    float phi = atan(p.y - 0.5, p.x - 0.5);
    
    // Modyfikacja odległości na podstawie kąta, tworzenie falowego efektu
    float dp = 2.0 + 1.0 * sin(phi * 6.0);
    d = d + dp;
    
    // Przesunięcie współrzędnych tak, aby środek (0,0) był w środku, skalowanie względem d, dodanie przesunięcia myszki
    vec2 uv = (p - 0.5) / d + mouse;
    
    // Pobranie koloru z tekstury na podstawie nowych współrzędnych i skalowanie koloru względem d
    vec3 col = texture(iChannel0, uv).rgb * 2.0 / d;
    
    // Ustawienie koloru fragmentu
    fragColor = vec4(col, 1.0);
}
