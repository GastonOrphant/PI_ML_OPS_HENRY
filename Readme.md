# **PROYECTO INDIVIDUAL Nº1**

Alumno: Gastón Alejandro Orphant

## **Arbol del proyecto:**

PI_ML_OPS                       
├───**API**: Carpeta contenedora de la API.            
│   ├───.space            
│   ├───**datasets**: Carpeta que contiene los datasets utilizados por la API.           
│   ├───src         
│   ├───__pycache__  
│   ├───**main.py**: Archivo principal de la API.    
│   ├───requirements.txt    
│   └───Spacefile  
├───**datasets**: Datasets creados por medio del proceso de ETL y apenas modificados en el EDA.                        
├───**MLOpsReviews**: Carpeta que contiene los archivos .csv a los cuales se le realizó el ETL.     
│   └───ratings       
├───**EDA**: Notebook en el que se realizó el analisis exploratorio de datos del proyecto.  
├───**ETL**: Notebook en el que se realizó el proceso de ETL de los .csv crudos.  
├───**Readme.md**: El archivo que usted se encuentra leyendo en estos momentos.
└───**RecommendationSystem.ipynb**: Notebook en la que se realizó el modelo de recomendación de peliculas.

# **ETAPAS DEL PROYECTO:**

## **Proceso de ETL**

En el proceso de ETL se abrieron en total 9 archivos csv de los cuales 8 simplemente se unificaron en uno solo y se cambió el nombre de una columna mientras que en el que resta se realizó lo siguiente:

- Se generó un nuevo campo **'id'** donde cada id se compone de la primera letra del nombre de la plataforma seguida del **show_id** ya presente en el dataset.

- Los **valores nulos** del campo rating fueron reemplazado por el string **"G"** que corresponde para el rating de "General for all audiences".

- Todas las **fechas** fueron transformadas al formato **AAAA-mm-dd**.

- Todos los **campos de texto** fueron pasados a **minúsculas**.

- El campo **'duration'** fue dividido en dos campos: **'duration_int'** y **'duration_type'**. El primero es un integer y el segundo un string indicando la unidad de medición de la duración 'min' para minutos o 'season' para temporadas.

## **API**

Link de la API (Se necesita estar registrado en https://www.deta.space) : [Ir a la API](https://deta.space/discovery/r/fwqgctaqhm5nj923)

## **Consultas de la API**

**IMPORTANTE:**
- A la hora de utilizar el campo de **platform** es necesario ingresar una plataforma correcta, las plataformas son: netflix, hulu, amazon y disney.

- El campo **duration_type** solo puede tomar dos valores: **min** o **season**

La API es capaz de realizar las siguientes consultas:

1. **/get_max_duration** tiene parametros opcionales de AÑO, PLATAFORMA y TIPO DE DURACIÓN y devolverá la Película con mayor duración con esos filtros especificos.         
    **Modo de uso:**
    /get_max_duration?**platform**=PLATAFORMA&**year**=AÑO&**duration_type**=TIPODEDURACION    

    **Ejemplos:**      
    https://pimlops_api-1-h8197706.deta.app/get_max_duration

    https://pimlops_api-1-h8197706.deta.app/get_max_duration?platform=netflix&year=2016&duration_type=min



2. **/get_score_count/{platform}/{year}/{scored}** retorna la cantidad de películas por plataforma con un puntaje mayor a XX(scored) en determinado año (year).  
    **Ejemplos:**     
    https://pimlops_api-1-h8197706.deta.app/get_score_count/netflix/2016/3.6

    https://pimlops_api-1-h8197706.deta.app/get_score_count/hulu/2019/3.7

3. **/get_count_platform/{platform}** retorna la cantidad de películas por plataforma con filtro de PLATAFORMA.   
    **Ejemplos:**    
    https://pimlops_api-1-h8197706.deta.app/get_count_platform/netflix

    https://pimlops_api-1-h8197706.deta.app/get_count_platform/hulu


4. **/get_actor/{platform}/{year}** retorna el actor que más se repite según plataforma y año.    
    **Ejemplos:**      
    https://pimlops_api-1-h8197706.deta.app/get_actor/amazon/2014

    https://pimlops_api-1-h8197706.deta.app/get_actor/netflix/2016


 Puedes entrar al siguiente [link](https://pimlops_api-2-h8197706.deta.app/docs) para ver la documentación de la API.
#

## **EDA**

El analisis exploratorio de datos lo realizamos mediante las siguientes librerias:    
**pandas:** Es la principal libreria de nuestro EDA, se utilizó para visualizar rapidamente los nulos y duplicados de los datasets además del formato de los mismos.  
**ydata_profiling:** Se utiliza para obtener un EDA automatizado del dataset.   
**matplotlib y seaborn:** Ambos se utilizan en conjunto para graficar, por ejemplo, se realizó un histograma de todas las columnas de un dataset para poder observar su dispersión.


## **SISTEMA DE RECOMENDACIÓN DE PELICULAS**

Puedes entrar al sistema de recomendación de peliculas desde el siguiente **[link](https://huggingface.co/spaces/GastonOrphant/movies-recommendations)**

Tambien puedes encontrar en el archivo [RecommendationSystem.ipynb](RecommendationSystem.ipynb) como se dió el proceso creativo para la implementación del sistema de recomendación previo a hacer su deploy.

### **Librerias utilizadas**

**Pandas:** Se utiliza para abrir el archivo .csv con nuestro dataset y elegir solo las columnas que nos interesan.

**matplotlib:** Si bien no utilizamos esta libreria en el modelo en si, en nuestro notebook lo usamos para visualizar los distintos RMSE para los distintos factores del modelo.

**scikit-surprise:** Esta libreria es la encargada de hacer nuestro modelo predictivo.

**gradio:** Se utilizó gradio para crear una interfaz grafica para nuestro modelo.

### **Surprise SVD**

**SVD** es un algoritmo de factorización matricial que utiliza la descomposición en valores singulares para predecir las calificaciones de los usuarios y las peliculas para los elementos faltantes en la matriz de calificaciones.

Se utilizó **SVD** para hacer el entrenamiento del sistema de recomendación, donde al ingresar un id de usuario y un id de pelicula nos dirá si se recomienda o no esa pelicula para ese usuario.

Como extra se añadió el nombre de la pelicula como un output para que el usuario pueda saber cual es la pelicula que corresponde a ese id.


