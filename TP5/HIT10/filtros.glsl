// Estados globales para los filtros
bool grisFilter = false;
bool sobelFilter = false;

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    vec4 color = texture(iChannel1, uv); //Video

    //Detecto teclas presionadas tomando la fila y columna que representan estas acciones de las teclas y tomando el color rojo
    float keyG = texture(iChannel0, vec2(71.0 / 256.0, 1.0)).r; // Detecto el toggle de la tecla G (1.0 es la primera fila)
    float keyS = texture(iChannel0, vec2(83.0 / 256.0, 0.0)).r; // Detecto el mantener presionada la tecla S (0.0 es la ultima fila)

    //Gris mientras g este presionada
    grisFilter = (keyG > 0.0);

    //Sobel mientras s este presionada
    sobelFilter = (keyS > 0.0);

    //Aplicar filtro de escala de grises
    if (grisFilter) {
        float gris = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b;
        color = vec4(vec3(gris), color.a);
    }

    //Aplicar filtro de Sobel
    if (sobelFilter) {
        vec2 texelSize = 1.0 / iResolution.xy;
        vec3 originalColor = color.rgb;
        
        mat3 Gx = mat3( -1.0,  0.0,  1.0, 
                        -2.0,  0.0,  2.0, 
                        -1.0,  0.0,  1.0 );

        mat3 Gy = mat3( -1.0, -2.0, -1.0,
                         0.0,  0.0,  0.0,
                         1.0,  2.0,  1.0 );

        float sobelX = 0.0;
        float sobelY = 0.0;

        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                vec2 offset = vec2(float(i), float(j)) * texelSize;
                vec3 sampl = texture(iChannel1, uv + offset).rgb;
                float graySample = 0.299 * sampl.r + 0.587 * sampl.g + 0.114 * sampl.b; // Convertir a escala de grises
                sobelX += graySample * Gx[i + 1][j + 1];
                sobelY += graySample * Gy[i + 1][j + 1];
            }
        }
      
        float edge = sqrt(sobelX * sobelX + sobelY * sobelY);
        
        color = vec4(vec3(edge), 1.0);
   
    }
    
    fragColor = color;
}