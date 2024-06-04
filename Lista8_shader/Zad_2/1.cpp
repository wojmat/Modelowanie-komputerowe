void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 p = fragCoord.xy / iResolution.xy;
    vec3 col = texture(iChannel0, p).rgb;
    fragColor = vec4(col, 1.0);
}
