#FastAPI app

from fastapi import FastAPI
import pandas as pd
from typing import Optional

app = FastAPI()

df = pd.read_csv("datasets/movies_titles.csv")

@app.get("/")
def read_root():
    return {"Hola!": "Bienvenido!"}

#Consigna 1: Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
@app.get("/get_max_duration")
async def get_max_duration(year: Optional[int] = None, platform: Optional[str] = None, duration_type: Optional[str] = 'min'):

    if duration_type is not None and duration_type not in ['min', 'season']:
        return("La duración debe ser una de las siguientes: min, season")
    
    # Filtramos por solo peliculas (NOTA: Según una consulta de sli.do este paso no debe de ser realizado)
    # df_movies = df[df.type == 'movie']

    df_movies = df

    # Aplicar los filtros OPCIONALES
    if year:
         df_movies = df_movies[df_movies.release_year == year]

    if platform:
        # Pasamos platform a minusculas por si un usuario lo escribe en mayusculas
        platform = platform.lower()
        # Controlamos que la plataforma ingresada sea correcta
        platforms = ["amazon", "disney", "hulu", "netflix"]
        if platform not in platforms:
            return ("Plataforma incorrecta! Debe ingresar una de las siguientes: amazon, disney, hulu, netflix")
        df_movies = df_movies[df_movies.platform == platform]

    if duration_type:
        # Controlamos que el duration_type sea valido
        duration_type = duration_type.lower()
        df_movies = df_movies[df_movies.duration_type == duration_type]

    if not df_movies.empty:
        max_duration_movie = df_movies.sort_values('duration_int', ascending=False).iloc[0]['title']
    else:
        return("No se encontró ninguna pelicula con los parametros dados.")    

    return {"max_duration_movie": max_duration_movie}


# Consigna 2: Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año.
@app.get("/get_score_count/{platform}/{year}/{scored}")
def get_score_count(platform: str, scored: float, year: int):
    # Controlamos que la plataforma ingresada sea correcta
    platform = platform.lower()

    platforms = ["amazon", "disney", "hulu", "netflix"]
    if platform not in platforms:
        return ("Plataforma incorrecta! Debe ingresar una de las siguientes: amazon, disney, hulu, netflix")
    
    # Verificar que el rango de scored sea valido. No deberia ser menor que 0 ni mayor que 5
    if scored is not None and (scored < 0 or scored > 5):
        return("El score promedio no puede ser menor que 0 o mayor que 5.")
    
    # Filtrar las películas para la plataforma, año y puntaje especificados
    df_filtered_movies = df[(df.platform == platform) & (df.score > scored) & (df.date_added.str.contains(str(year)))] 
    # & (df.type == 'movie')] Segun sli.do no hay que filtrar por movies

    # Verificar que hay al menos una película que cumpla con los filtros
    if not df_filtered_movies.empty:
        count = df_filtered_movies.groupby('platform').size()
        return count.to_dict()
    else:
        return("No se encontró ninguna pelicula con los parametros dados.")
    


# Consigna 3: Cantidad de películas por plataforma con filtro de PLATAFORMA.
@app.get("/get_count_platform/{platform}")
def get_count_platform(platform):
    # Controlamos que la plataforma ingresada sea correcta
    platform = platform.lower()

    platforms = ["amazon", "disney", "hulu", "netflix"]
    if platform not in platforms:
        return ("Plataforma incorrecta! Debe ingresar una de las siguientes: amazon, disney, hulu, netflix")
    
    # Filtrar las películas para la plataforma especificada
    df_filtered_movies = df[(df.platform == platform)] # & (df.type == 'movie')] Segun sli.do no hay que filtrar por movies

    # Agrupar por plataforma y contar el número de filas resultantes
    count = df_filtered_movies.groupby('platform').size()
    
    # Verificar que hay al menos una película que cumpla con los filtros
    if df_filtered_movies.empty:
        return("No hay peliculas para esa plataforma")
    return count.to_dict()


# Consigna 4: Actor que más se repite según plataforma y año.
@app.get("/get_actor/{platform}/{year}")
def get_actor(platform: str, year: int):
    # Controlamos que la plataforma ingresada sea correcta
    platform = platform.lower()

    platforms = ["amazon", "disney", "hulu", "netflix"]
    if platform not in platforms:
        return ("Plataforma incorrecta! Debe ingresar una de las siguientes: amazon, disney, hulu, netflix")
    

    # Verificar que el año esté dentro del rango válido
    if year is not None and year < 1920:
        raise ValueError("El año debe de ser mayor a 1920")
    
    # Filtrar las películas para la plataforma y año especificado
    df_filtered = df[(df.platform == platform) & (df.release_year == year)]
         
    # Poner el cast en un array para poder hacer el recorrido
    df_cast_filtered= df_filtered.assign(actor=df_filtered.cast.str.split(',')).explode('cast')
    
    # Contar la cantidad de apariciones de cada actor
    actor_count = df_cast_filtered.cast.value_counts()
    
    # Obtener el actor que más se repite y su cantidad de apariciones
    max_actor = actor_count.index[0]
    max_count = int(actor_count.iloc[0])
    actor = dict({'actor': max_actor, 'count': max_count})

    return actor