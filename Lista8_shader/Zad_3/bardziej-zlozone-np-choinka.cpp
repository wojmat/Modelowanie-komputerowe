#define S 0.2

// surface - distance function
float plane(vec3 r)
{
    //return (r.y-0.25*( sin(r.x*12.2+iTime*1.2)+sin(r.z*0.2+iTime*0.2)));
    return r.y;
}

// sphere - distance function
float sphere(vec3 r, float R)
{ 
    return length(r) - R; 
}

// cube - distance function
float aabb(vec3 c, vec3 s)
{
    vec3 d = abs(c) - s;
    return max(d.x, max(d.y, d.z));
}

// 3d rotations
vec3 rotx(vec3 r, float fi) {
    mat3 R = mat3(1, 0, 0, 0, cos(fi), -sin(fi), 0, sin(fi), cos(fi));
    return R * r;
}

vec3 roty(vec3 r, float fi) {
    mat3 R = mat3(cos(fi), 0, sin(fi), 0, 1, 0, -sin(fi), 0, cos(fi));
    return R * r;
}

vec3 rotz(vec3 r, float fi) {
    mat3 R = mat3(cos(fi), -sin(fi), 0, sin(fi), cos(fi), 0, 0, 0, 1);
    return R * r;
}

// Torus distance function
float sdTorus(vec3 p, vec2 t)
{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// distance from the scene
float dist(vec3 r)
{
    float d = 1e10;
    
    // Dodajemy rotację wokół każdej osi
    vec3 rotated_r = rotz(roty(rotx(r + vec3(-1.0, -1.0, 5.0), iTime * 0.5 * S), iTime * 0.75 * S), iTime * S * 2.5);
    d = min(d, sdTorus(rotated_r, vec2(0.5, 0.2)));
    
    d = min(d, plane(r));
    
    return d;
}

// shadow function
float shadow(vec3 p, vec3 l, float d)
{
    float o = 0.0;
    for (int i = 12; i > 0; i--) 
    {
        o += dist(p + l * float(i) * d);
    }

    return clamp(o, 0.0, 1.0);
}

// normal vector function
vec3 normal(vec3 p)
{
    #define dr 1e-4
    vec3 drx = vec3(dr, 0, 0);
    vec3 dry = vec3(0, dr, 0);
    vec3 drz = vec3(0, 0, dr);
    return (vec3(dist(p + drx), dist(p + dry), dist(p + drz)) - dist(p)) / dr;
}

#define ITER 90
#define EPS 0.0001
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 r = fragCoord.xy / iResolution.xy;
    r.x *= (iResolution.x / iResolution.y);
    
    vec4 color = vec4(0, 0, 0, 1);
    vec3 camera = vec3(1.0, 2.0, 1.0);
    vec3 p = vec3(r.x, r.y + 1.0, -1.0);
    vec3 dir = normalize(p - camera);
    
    for (int i = 0; i < ITER; i++)
    {
        float d = dist(p);
        if (d < EPS)
        {
            break;
        }
        p = p + dir * d;
    }

    vec3 n = normal(p);
    
    vec3 light_pos = vec3(1.2, 4.2, -0.5);
    float light = 15.0 + 1.2 * (dot(n, light_pos));
    vec3 lightdir = normalize(light_pos - p);
    light /= 0.2 * pow(length(light_pos - p), 3.4);
    
    // Dodajemy cień
    light *= shadow(p, lightdir, 0.01);
    
    // Definiowanie kolorów brązowego i zielonego
    //vec3 brown = vec3(0.6, 0.3, 0.1);
    vec3 green = vec3(0.0, 1.0, 0.0);
    
    // Ustawienie koloru obiektu na brązowy
    color = vec4(light * green, 0.6) * 2.0;
    
    // Ustawienie koloru tła na zielony
    vec3 background = green;
    fragColor = mix(vec4(background, 1.0), color, color.a);
}
