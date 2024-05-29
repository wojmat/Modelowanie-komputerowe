void mainImage( out vec4 fragColor, in vec2 fragCoord )
{   
    vec2 q = fragCoord.xy / iResolution.xy;
    
    vec2 p = (-1.0 + 2.0 * q) * vec2(iResolution.x / iResolution.y, 1.0);
    
    float d = length(p - vec2(0.0, 0.0));
    
    d = smoothstep(0.55, 0.6, 1.0 - d);

    // Time varying pixel color
    vec3 col = vec3(d, d, d);
    
    // Output to screen
    fragColor = vec4(col,1.0);
}