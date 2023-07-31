import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_movie_img(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=81c67b61e84cde33f9aa31ad914d0a0c&language=en-US'.format(movie_id))
    data= response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']
    

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movie_posters=[]
    
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetching poster from api
        recommended_movie_posters.append(fetch_movie_img(movie_id))
        
    return recommended_movies,recommended_movie_posters
        

movies_dict_path='movies_dict.pkl'
similarity_path='similarity.pkl'

with open(movies_dict_path,'rb') as file:
    movies_dict=pickle.load(file)
    
with open(similarity_path,'rb') as file:
    similarity=pickle.load(file)
    
    
movies=pd.DataFrame(movies_dict)


st.title('Movie Recommender system')
selected_movie_name = st.selectbox(
'Please select movies you watched for similar movie recommendations',
movies['title'].values)
st.write('You selected:', selected_movie_name)


if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[2])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])