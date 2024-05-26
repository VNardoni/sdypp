# Por que no podría aplicar el operador de sobel sobre el código anterior donde aplicaba el chroma pero si puedo aplicar el de escala de grises?

Es un problema de incompatibilidad, ya que el filtro Sobel necesita primero en convertir en escala de grises para aplicar el filtro, que se basa en detectar cambios de intensidad
en los colores. Por otro lado aplicarlo sobre un croma no tendria sentido porque tiene ciertos lugares donde el color es trasnparente, y no se podria calcular
un cambio de intensidad.
Pero podria aplicarlo en una escala de grises ya que requiero solo unas conversiones de los colores, y ademas necesita la conversion a gris para aplicarse.
