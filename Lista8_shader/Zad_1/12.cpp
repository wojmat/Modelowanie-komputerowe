void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 q = fragCoord.xy / iResolution.xy;
    vec2 p = (-1.0 + 2.0 * q) * vec2(iResolution.x / iResolution.y, 1.0);
    float d = length(p - vec2(0.0, 0.0));
    d = smoothstep(0.55, 0.6, d);
    float phi = atan(p.y, p.x);
    d += sin(phi * 10.0 + iTime * 0.55) * 0.1;
    vec3 col = vec3(d, d, d);
    fragColor = vec4( col, 1.0 );
}
