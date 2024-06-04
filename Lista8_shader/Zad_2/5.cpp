void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 p = fragCoord.xy / iResolution.xy; 
    vec2 uv = p * 0.1;
    vec3 col = texture(iChannel0, uv).rgb;
    fragColor = vec4(col, 1.0);
}
