#define S 0.2

// surface - distance function
float plane(vec3 r)
{
	//return (r.y-0.25*( sin(r.x*12.2+iTime*1.2)+sin(r.z*0.2+iTime*0.2)));
	return r.y;
}
// sphere - distance function
float sphere(vec3 r, float R)
{ return length(r) - R; }

// cube - distance function
float aabb(vec3 c, vec3 s)
{
	vec3 d = abs(c)-s;
	return max(d.x,max(d.y,d.z));
}

// 3d rotations
vec3 rotx(vec3 r, float fi) {
    mat3 R = mat3(	1,0,0, 0,cos(fi),-sin(fi), 0,sin(fi),cos(fi) );
	return R*r;
}
vec3 roty(vec3 r, float fi) {
	mat3 R = mat3(	cos(fi),0,sin(fi), 0,1,0, -sin(fi),0,cos(fi) );
	return R*r;
}
vec3 rotz(vec3 r, float fi) {
	mat3 R = mat3(	cos(fi),-sin(fi),0, sin(fi),cos(fi),0, 0,0,1 );
	return R*r;
}

float sdTriPrism(vec3 p, vec2 h)
{
    const vec3 k = vec3(-0.8660254, 0.5, 0.57735);
    p = abs(p);
    p.xy -= 2.0 * min(dot(k.xy, p.xy), 0.0) * k.xy;
    vec2 d = vec2(
        length(p.xy - vec2(clamp(p.x, -k.z * h.x, k.z * h.x), h.x)) * sign(p.y - h.x),
        p.z - h.y);
    return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}

//  distance from the scene
float dist(vec3 r)
{
    float d = 1e10;
    
    // d = min(d, aabb(roty(r + vec3(-1.0, -0.9, 3.9), 0.2 * iTime), vec3(0.7)));
    d = min(d, sdTriPrism(rotx(roty(r + vec3(-1.0, -1.0, 5.0), iTime * 0.75 * S), iTime * S * 2.5), vec2(0.5, 0.5)));
    
    d = min(d, plane(r));
    
    return d;
}


// shadow is just sum of distances from the scene while marching towards light (l)
float shadow(vec3 p, vec3 l, float d)
{
	float o=0.0;
	for (int i=12; i > 0; i--) 
	{
		o += dist( p+l*float(i)*d );
	}

	return clamp(o, 0.0, 1.0);
}

// normal vector (needed for lighting)
// http://www.pouet.net/topic.php?which=7920&page=10
// rar
vec3 normal(vec3 p)
{
	#define dr 1e-4
	vec3 drx = vec3(dr,0,0);
	vec3 dry = vec3(0,dr,0);
	vec3 drz = vec3(0,0,dr);
	return ( vec3( dist(p+drx), dist(p+dry), dist(p+drz) ) - dist(p)) / dr;
}

#define ITER 90	
#define EPS 0.0001
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	vec2 r = fragCoord.xy / iResolution.xy;
	r.x*=(iResolution.x/iResolution.y);
	
	vec4 color=vec4(0,0,0,1);

	vec3 camera = vec3(1.0,2.0,1.0);
	vec3 p = vec3(r.x, r.y+1.0, -1.0);
	vec3 dir = normalize(p-camera);
	
	for(int i=0; i<ITER; i++)
	{
		float d = dist( p );
		if(d < EPS)
		{
		    break;
		}
		p = p + dir * d;
	}

	vec3 n = normal(p);
	
	vec3 light_pos = vec3(1.2,4.2,-0.5);
	float light = 15.0 + 1.2*(dot(n,light_pos));
	vec3 lightdir = normalize(light_pos-p);
	light /= 0.2*pow(length(light_pos-p),3.4);
	
    // uncomment for shadows
	light *= shadow(p, lightdir, 0.01);
	
	//vec4 color2 = vec4(texture(iChannel0,r.xy ).xyz,1.0);//,light*0.891,light*0.998,1.0);
	color = vec4(light*0.89,light*0.891,light*0.998,1.0)*2.0;
	fragColor = color;
}
