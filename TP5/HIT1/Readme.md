# Informe

## Tipos de Shaders

### 2D

Los shaders 2D tambien son conocidos como texturas y son usados para renderizar geometria 3D.
El unico tipo de Shader 2D es el **Pixel Shader**, que se conocen como fragmentos de shaders. Los mas simples de este tipo son
los que se encargan de producir un pixel como un solo color, y es capaz de aplicarle a ese color un valor de iluminacion, y otros efectos como
Bump Mapping (Mapeado topologico), aplicar sombras, transparencia, etc. Ademas puede alterar la profundidad (Eje Z) del fragmento.
En graficos 3D, un fragmento solo no puede producir estos efectos complejos porque opera en singular, sin conocimiento de la geometria que lo rodea.
Sin embargo, en conjunto pueden acceder a las coordenadas de la pantalla que están siendo dibujadas y pueden muestrear la pantalla y los píxeles cercanos
si se pasa el contenido de toda la pantalla como una textura al shader. Esta técnica permite una amplia variedad de efectos de postprocesamiento en 2D.

### 3D

Los shaders en 3D actúan sobre modelos tridimensionales y pueden acceder a los colores y texturas que se usan para dibujar el modelo o mesh.

Los **Vertex Shaders** se ejecutan una vez por cada vértice enviado a la GPU.
Los vertex shaders transforman la posición 3D de cada vértice en el espacio virtual en coordenada 2D de la pantalla.
Pueden manipular propiedades como la posición, el color y las coordenadas de la textura, pero no pueden crear nuevos vértices.

Los **Geometry Shaders** pueden generar nuevos primitivas gráficas, es decir formas geometricas simples como puntos, líneas o triángulos,
a partir de las primitivas enviadas al pipeline grafico. Se ejecutan después de los vertex shaders y toman como entrada una primitiva, como un triángulo.
Luego, el shader puede emitir cero o más primitivas, la cual son convertidos en pixeles y sus fragmentos pasan al pixel shader.

Los **Tessellation Shaders** agregan dos etapas al proceso: tessellation control shaders y los tessellation evaluation shaders.
Estos permiten subdividir meshes simples en meshes más finas en tiempo real con una función matemática.
Permite que mientras mas cerca estes de un objeto mas detalle tiene, mientras que los más alejados pueden tener meshes más gruesas sin perder calidad.
También reducen el ancho de banda requerido para las meshes.

Los **Primitive Shaders**, similares a los compute shaders pero con acceso a los datos necesarios para procesar geometría.
Nvidia introdujo los **mesh** y task shaders permitiendo al GPU manejar algoritmos más complejos y aliviando la carga del CPU.

Los **Compute Shaders**  pueden integrarse en pipelines de renderizado para etapas adicionales en algoritmos de animación o iluminación.

Para renderizar graficos en 3D, se utiliza una secuencia llamada Pipeline de renderizado utilizando una API llamada WebGL,
la cual es usada para crear estos graficos en un navegador. El pipeline de renderizado es una secuencia de pasos que hace WebGL al renderizar usando 
unidades de procesamiento de nuestra GPU.

![Pipeline de renderizado]("rendering_pipeline.png")
