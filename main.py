import pickle
import streamlit as st
import requests
import rajimain1 as m
import streamlit as st
def page1():
    m.log_in()
    if st.button("next"):
        return "page2"
def page2():

    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names,recommended_movie_posters

    if st.button("PROFILE"):
        with st.sidebar:
            m.display_users_list()
    st.header('Neural Flix Advisor')
    movies = pickle.load(open('movie.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )


    col1,col2,col3=st.columns([2,8,2])
    with col1:
        if st.button("history"):
            m.his_print()

    with col2:
        if st.button('Show Recommendation'):
            m.create_table()
            recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4, col5= st.columns(5)
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])
                #to insert data into table
                m.insert_search(selected_movie)
    if st.button("go to sign in page"):
        return "page1"

    with col3:
        if st.button("Rating"):
            st.markdown('<a href=" http://192.168.151.183:8501" target="_blank">View Rating</a>', unsafe_allow_html=True)


# Use a session state variable to keep track of the current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "page1"

# Display the current page
if st.session_state.current_page == "page1":
    result = page1()
elif st.session_state.current_page == "page2":
    result = page2()

# Update the current page based on the result
if result:
    st.session_state.current_page = result



