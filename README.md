# Individual1_Henry

## Sistema de Recomendación de peliculas

Link para render: https://individual1-henry.onrender.com/docs

# 🎥 Sistema de Recomendación de Películas - Proyecto Individual

Este repositorio contiene el desarrollo de un sistema de recomendación de películas.
## 📖 Contexto y Rol a Desarrollar

### Contexto

En este proyecto, el objetivo principal es desarrollar un **MVP** que permita implementar un modelo de recomendación para una start-up que provee servicios de agregación de plataformas de streaming. El reto radica en que los datos iniciales están desordenados, anidados y carecen de procesos automatizados, lo que requiere comenzar desde cero.

Para esta actividad, contamos con dos bases de datos que deben pasar por un proceso de limpieza, las cuales son: movies (contienen la información relacionada con la producción de las peliculas) y credits (que contiene la información sobre el elenco y la dirección de las peliculas encontradas en la base anterior)

## ⚙️ Procesos Implementados

A continuación explicaré el ETL desarrollado (archivo: ETL_completo): 

1. Doy inicio a la desagregación y limpieza del dataset "credits" dado que este es más grande. La idea es extraer unicamente el nombre del director de las peliculas y posteriormente el actor principal, junto con el nombre de su respectivo personaje. Debido a que las peliculas tienen varios directores y varios actores, he optado por tomar solo el principal para reducir al maximo el tamaño del dataset. En este data set toda la información esta anidada, por lo tanto necesité normalizarla para poder extraer la información mencionada. Hice la extracción creando nuevos datasets con la información que queria: primero con el actor pincipal, luego con el director. En ambos caos elimine todas las columnas innecesarias.

2. Luego inicio con la limpieza del dataset "movies"; es un archivo igualmente pesado, voy a eliminar las columnas que se solicita que se eliminen y tambien las que considero no aportan información que yo vaya a utilizar. Tambien agregué en este la información resultante de "credits"

3. El proyecto pide que se desaniden unas columnas especificas: "belongs_to_collection", "genres", "production_companies" y "production_countries". Este proceso fue bastante dispendioso. Para empezar confirme que no hayan datos nulos en estas columnas y los reemplacé con listas vacias, posteriormente convertí los strings en diccionarios y finalmente se normalizaron los datos con la función normalize_entry para posteriormente concatenar los df en uno solo. El proceso fue el mismo con cada una de las columnas mencionadas. 

4. Seguido, hice las transformaciones sugeridas para el proyecto:
   - Desanidado y limpieza de datos iniciales.
   - Rellenado de valores nulos en `budget` y `revenue` con 0.
   - Conversión de fechas a formato `AAAA-MM-DD` y creación de la columna `release_year`.
   - Cálculo de la columna `return` (revenue/budget) para medir el retorno de inversión.
   - Eliminación de columnas innecesarias como `video`, `imdb_id`, `poster_path`, entre otras.
   - Adicionalmente, agregué una columna con el dia de la semana de estreno para cada pelicula. 

5. Con ambos dataset limpios y organizados, creo un nuevo dataset llamado movies, con el cual procedo a hacer la EDA. 


**Análisis Exploratorio de Datos (EDA)**:

Para realizar este análisis (archivo: EDA_completo), he utilizado la base de datos completamente depurada, la cual se llama igual que la original "movies". Saco la información de las columnas con las que cuento en el dataset, se observa que las variables numericas no tienen datos nulos; la información nula no aporta mucho a este analisis por lo tanto no la tendré en cuenta. Me quedo con las cuatro variables numericas: promedio, desviación, minimos y máximos. 

Utilizo histogramas de las cuatro variables seleccionadas, para entender el comportamiento; alguna conclusiones: 

1. *Budget:* esta grafica del presupuesto no es muy explicativa, creo que vale la pena explorarla mejor de otra manera. 
2. *Revenue:* esta grafica del presupuesto no es muy explicativa, creo que vale la pena explorarla mejor de otra manera. 
3. *vote_average*: lo que veo en esta grafica es que el promedio de votos de la mayoria de las peliculas esta entre 5 y 7.5 
4. *vote_count*: no considero que esta variable sea muy representativa, creo que puedo descartarla o explorarla de otra manera. 
5. *release_year*: veo que la mayoria de peliculas fueron estrenadas desde la decada de 1990. Voy a revisar si elimino las anteriores para que la información pueda ser más ilustrativa. 
6. *Return*: esta grafica del presupuesto no es muy explicativa, creo que vale la pena explorarla mejor de otra manera. 

Posteriormente elimino todas las peliculas que tienen una fecha de estreno anterior a 1990, y reviso la información de las nuevas columnas resultantes. La conclusión más significativa es que eliminar las peliculas estrenadads antes de 1990, no genera un cambio significativo. 

Busco los valores atipicos de  las variables 'budget', 'revenue' y 'return'. 

Se elaboran graficas de la distribución del presupuesto, la distribución del ingreso, la distribución de retornos. Estas graficas muestran que efectivamente hay valores atipicos dentro del periodo estudiado. 

Generé las graficas de estas tres variables agrupadas por año, de cada variable se generó una gráfica del total y una del promedio. Con esta información saco un top 5 de las peliculas que en promedio tuvieron una mayor inversión: 2017, 1999, 2000, 2004 y 1997. Asi mismo saco un top 5 de las peliculas con mayor presupuesto: 	Pirates of the Caribbean: On Stranger Tides (2011), Pirates of the Caribbean: At World's End	(2007), Avengers: Age of Ultron (2015), Superman Returns	(2006) y Tangled (2010). No se ve una relación de el top 5 por promedio y top cinco por mayor presupuesto. 

Generé tambien las graficas teniendo en cuenta el total y el promedio de ingresos y saco igualmente el top 5 de estas peliculas. Las peliculas con mayores ingresos fue Avatar (2009), Star Wars: The Force Awakens (2015), Titanic	(1997), The Avengers (2012) y Jurassic World (2015); los promedios de peliculas con mayores ingresos fueron en los años: 2017, 2016, 2003, 2004 y 1997. 	

Finalmente hice el mismo ejercicio con el retorno del ingreso total e ingreso promedio por año. Las peliculas con mejor retorno son: 웰컴 투 동막골/Bienvenido a Dongmakgol (2005), Aquí Entre Nos (2012), Nurse 3-D (2013), From Prada to Nada (2011)	y Paranormal Activity (2007). Los cinco años con mayor retorno promedio son: 2005, 2012, 2013, 2011 y 2007.

**CONCLUSIÓN:** He visto que en mi dataset original hay muchas peliculas de las decadas anteriores a 1990 que no son muy representativas por lo tanto las elimino, tambien despues de todo este analisis exploratorio veo que si hay valores atipicos que vale la pena exploar por eso no los voy a borrar.

Me parece muy importante tener en cuenta que así como no hay mucha correlación entre si una pelicula tuvo un gran presupuesto porque veo que esto no implica que haya tenido tambien un gran ingreso, me voy a centrar en la columna de retorno de la inversión como variable representativa y voy a crear un nuevo df de movies solo con las peliculas desde 1990 (este ya está) y luego de este voy a eliminar todas las peliculas con un return igual o menor que cero, considerando que no fueron peliculas rentables. 

La información resultante quedp en el archivo Exitosas_1990.

4. **Despliegue de la API**:

Se propone el uso de una API (arhivo: main) para que la empresa tenga disponibles los resultados de las siguientes funciones: 

1. Cantidad de filmaciones por mes: Se ingresa un mes en españpl y devuelve la cantidad de peliculas que fueron estrenadas en el mes, consultando en todo el dataset. 
2. Cantidad de filmaciones por día: Se ingresa un dia de la semana en español y arroja la cantidad de peliculas estrenadas ese día. 
3. Score por titulo: se ingresa el titulo de una filmación y se arroja el año de estreno y el score de la pelicula. El nombre debe coincidir exactamente. Ejemplo: Toy Story
4. Votos por titulo: se ingresa el titulo exacto de una pelicula y la API arroja la cantidad de votos y el promedio de votaciones de esa pelicula. La pelicula debe tener al menos 2000 valoraciones. 
5. Actor: se ingresa el nombre del actor y arroja el exito del actor a traves del retorno, la cantidad de peliculas en las que ha participado y el retorno promedio. 
6. Director: se ingresa el nombre del director y arroja el exito medido a traves del retorno, devuelve en orden de exito las peliculas, incluyendo la fecha de lanzamiento, retorno individual, costo y ganancia. 

3. **Desarrollo del Sistema de Recomendación**:

Dentro de la misma API (arhivo: main) se incluye una función de recomendación, el cual busca recomendar peliculas a los usuarios basandose en los nombres similares de las peliculas utilizando TF-IDF y la similitud del coseno. Las peliculas recomendadas se ordenan segun el score de similaridad y devolverá uan lista con las peliculas de mayor puntaje. 

- Mediante TF-IDF se crea un vectorizador que elimina las palabras comunes en ingles. 
- Luego se ajusta y transforma la columna "original_title" del dataframe en una matriz con caracteristicas TF-IDF. 
- Posteriormente, se limpia el titulo ingresado, eliminando los caracteres no alfabeticos y convirtiendolo a minusculas. 
- Luego se transforma el titulo limpio en un vector TF-IDF
- Se calcula la similitud del coseno entre el vector del titulo dado y la matriz TF-IDF de todas las peliculas. 
- Finalmente obtiene los indices de las peliculas similares ordenadas de esa forma. 
- Arroja las peliculas con esta caracteristica. 

## 🚀 Funcionalidades de la API


### Cómo Usar la API

Link para render: https://individual1-henry.onrender.com/docs

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Anavig14/Individual1_Henry.git
   cd Individual1_Henry
