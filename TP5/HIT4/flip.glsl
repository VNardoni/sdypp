void mainImage( out vec4 fragColor, in vec2 fragCoord ) {

    vec2 uv = (fragCoord.xy / iResolution.xy);
    uv.y = -uv.y;
    uv.x = -uv.x;
    fragColor = texture(iChannel0, uv);
    
}