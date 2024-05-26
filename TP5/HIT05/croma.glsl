void mainImage( out vec4 fragColor, in vec2 fragCoord ) {

    vec2 uv = fragCoord.xy / iResolution.xy;
    
    //asigno los canales
    vec4 textura = texture(iChannel0, uv);

    vec4 video = texture(iChannel1, uv);

    //Defino el color verde
    vec4 chromaColor = vec4(0.0, 1.0, 0.0, 1.0);
   
    float umbral = 0.75;
    
    //Calculo la distancia entre el color del video y el color de chroma
    //Usando el teorema de distancia pitagórica en n dimensiones (n=3)
    float chromaDif = sqrt(
        pow(video.r - chromaColor.r, 2.0) +
        pow(video.g - chromaColor.g, 2.0) +
        pow(video.b - chromaColor.b, 2.0)
    );
    
    //Muestro la textura o el video si la distancia supera o no el umbral
    if (chromaDif < umbral) {
        fragColor = textura;
    } else {
        fragColor = video;
    }

    //Despues de varias pruebas parece que un umbral de 0.75 parece lo mas adecuado
}
