void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;

    float zoom = 2.0;
    
    //Zoom al centro
    //uv = (uv - 0.5) / zoom + 0.5;
    
    //Zoom abajo a la derecha
    //uv = (uv - 1.0) / zoom + 1.0;
    
    //Zoom arriba a la izquierda
    uv = (uv - 0.0) / zoom + 0.0;
    
    //El unico numero que cambia representa la posicion en la pantalla
    //0 representa la esquina superior izquierda que se mueve diagonalmente hasta el 1 
    //que representa la esquina inferior derecha
    
    fragColor = texture(iChannel0, uv);
}