void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 p = fragCoord.xy / iResolution.xy;
    vec2 mouse = iMouse.xy / iResolution.xy;
    float d = length(p - 0.5) * 10.0 + 0.5;
    vec2 uv = p / d + mouse;
    vec3 col = texture(iChannel0, uv).rgb;
    fragColor = vec4(col, 1.0);
}
