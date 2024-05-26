void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Coordenadas de textura normalizadas
    vec2 uv = fragCoord.xy / iResolution.xy;
    
    // Asigno los canales
    vec4 textura = texture(iChannel0, uv);
    vec4 video = texture(iChannel1, uv);

    // Defino el color verde
    vec4 chromaColor = vec4(0.0, 1.0, 0.0, 1.0);
   
    // Definir un umbral de chroma como un float
    float umbral = 0.75;
    
    // Calculo la distancia entre el color del video y el color de chroma
    // Usando el teorema de distancia pitagórica en n dimensiones (n=3)
    float chromaDif = sqrt(
        pow(video.r - chromaColor.r, 2.0) +
        pow(video.g - chromaColor.g, 2.0) +
        pow(video.b - chromaColor.b, 2.0)
    );
    
    // Variable para almacenar el color de salida
    vec4 salida;

    // Muestro la textura o el video si la distancia supera o no el umbral
    if (chromaDif < umbral) {
        salida = textura;
    } else {
        salida = video;
    }

    // Aplico el filtro de escala de grises usando la fórmula
    float gris = 0.299 * salida.r + 0.587 * salida.g + 0.114 * salida.b;

    // Asigno el valor de escala de grises a fragColor, manteniendo el canal alfa
    fragColor = vec4(vec3(gris), salida.a);
}