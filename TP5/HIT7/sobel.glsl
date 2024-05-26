void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord.xy / iResolution.xy;
    
    // Obtener el tamaño del paso para las derivadas
    vec2 texelSize = 1.0 / iResolution.xy;

    vec3 color = texture(iChannel0, uv).rgb;

    // Matrices de Sobel
    mat3 Gx = mat3( -1.0,  0.0,  1.0, 
                    -2.0,  0.0,  2.0, 
                    -1.0,  0.0,  1.0 );

    mat3 Gy = mat3( -1.0, -2.0, -1.0,
                     0.0,  0.0,  0.0,
                     1.0,  2.0,  1.0 );

    // Calcular las derivadas
    float sobelX = 0.0;
    float sobelY = 0.0;

    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            vec2 offset = vec2(float(i), float(j)) * texelSize;
            vec3 salida = texture(iChannel0, uv + offset).rgb;
            float gris = 0.299 * salida.r + 0.587 * salida.g + 0.114 * salida.b; // Convertir a escala de grises
            sobelX += gris * Gx[i + 1][j + 1];
            sobelY += gris * Gy[i + 1][j + 1];
        }
    }

    // Calcular la magnitud del gradiente
    float edge = sqrt(sobelX * sobelX + sobelY * sobelY);

    fragColor = vec4(vec3(edge), 1.0);
}
