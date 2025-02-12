import streamlit as st
import pickle

# Загрузка данных
final_books = pickle.load(open('artifacts/final_books.pkl', 'rb'))  
cosine_sim_df = pickle.load(open('artifacts/cosine_sim_df.pkl', 'rb'))  
book = pickle.load(open('artifacts/book.pkl', 'rb'))  


# Функция для получения обложек книг

def fetch_poster(book_titles):
    poster_urls = []
    for title in book_titles:
        try:
            matches = book.loc[book['Book-Title'] == title, 'Image-URL-L']
           
            if not matches.empty:
                poster_urls.append(matches.values[0])
            else:
                poster_urls.append('https://sun1-26.userapi.com/s/v1/ig2/KfaMsfWodHqriH91_R4kU-DFPn8NshitwxjZC2JmBVHftG9h6cf1b0ERU7Nw9B_RsyJMe1rsyLMuHRMtunE7cmhs.jpg?size=400x400&quality=96&crop=2,2,1077,1077&ava=1')  # По желанию, можно добавить заглушку
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            poster_urls.append('Ошибка при извлечении')  
    return poster_urls

# Рекомендация книг

def recommend_book(book_name):
    if book_name not in cosine_sim_df.index:
        return [], []
    similar_books = cosine_sim_df[book_name].sort_values(ascending=False)[1:6]
    recommended_books = similar_books.index.tolist()
    poster_urls = fetch_poster(recommended_books)
    return recommended_books, poster_urls


st.header('Рекомендация книг с помощью коллаборативной фильтрации')

book_names = final_books['Book-Title'].unique()
selected_book = st.selectbox("Выберите книгу", book_names)

if st.button('Показать рекомендации'):
    recommended_books, poster_urls = recommend_book(selected_book)
    
    if not recommended_books:
        st.error("Нет рекомендаций.")
    else:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(recommended_books):
                with col:
                    st.text(recommended_books[i])
                    st.image(poster_urls[i])
