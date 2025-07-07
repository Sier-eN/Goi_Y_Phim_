import streamlit as st
import pickle
import requests

# Hàm để lấy poster của phim từ API The Movie Database (TMDB)
def fetch_poster(phim_id):
    api_key = 'd8e72da2e901ad82afbc71d5c65d6eca' 
    url = f'https://api.themoviedb.org/3/movie/{phim_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

# Tải dữ liệu phim và ma trận tương đồng từ file pickle
phim = pickle.load(open("phim_list.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
phim_list = phim['title'].values

st.header("Gợi Ý Phim")
selectvalues = st.selectbox("Chọn Phim", phim_list)

# Hàm để gợi ý phim dựa trên phim đã chọn
def recommend(phim1):
    index = phim[phim['title']==phim1].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True, key=lambda vector:vector[1])
    recommend_phim=[]
    recommend_poster=[]
    for i in distance[1:6]:
        phim_id = phim.iloc[i[0]].id
        recommend_phim.append(phim.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(phim_id))
    return recommend_phim,recommend_poster

if st.button("Đưa Ra Gợi Ý"):
    st.write("Dựa theo phim bạn chọn, đây là 5 gợi ý cho dành cho bạn:")
    ten_phim, phim_poster = recommend(selectvalues)
    # Hiển thị tên phim và poster trong 5 cột
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(ten_phim[0])
        st.image(phim_poster[0])
    with col2:
        st.text(ten_phim[1])
        st.image(phim_poster[1])
    with col3:
        st.text(ten_phim[2])
        st.image(phim_poster[2])
    with col4:
        st.text(ten_phim[3])
        st.image(phim_poster[3])
    with col5:
        st.text(ten_phim[4])
        st.image(phim_poster[4])