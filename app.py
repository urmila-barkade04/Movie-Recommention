from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd
import json

from patsy import dmatrices
movies=pd.read_pickle(open('model/movies_list.pkl','rb'))
similarity=pd.read_pickle(open('model/similarity.pkl','rb'))
app = Flask(__name__)





def fetch_poster(movie_id):
   url="https://api.themoviedb.org/3/movie/{}?api_key=f46725f553407715e2e70aa16281ee92".format(movie_id)
   data =requests.get(url)
   data=data.json()
   poster_path=data['poster_path']
   full_path="https://image.tmdb.org/t/p/w500"+poster_path
   return full_path

def recommend(movie):
   index=movies[movies['title']==movie].index[0]
   

   distances=sorted(list(enumerate(similarity[index])), reverse=True,key=lambda x: x[1])  
   recommended_movies_name=[]
   recommended_movies_poster=[]
   for i in distances[1:6]:
      movie_id=movies.iloc[i[0]].movie_id
      recommended_movies_poster.append(fetch_poster(movie_id))
      recommended_movies_name.append(movies.iloc[i[0]].title)
      
   return recommended_movies_name,recommended_movies_poster


    

@app.route('/')
def home():
   return render_template("index1.html")

@app.route('/about')
def about():
   return render_template("about.html")

@app.route('/contact')
def contact():
   return render_template("contact.html")

@app.route('/recommendation',methods=['GET','POST'])
def recommendation():
   movies_list=movies['title'].values
   
   status=False
    0
   if request.method=="POST":
      try:
         if request.form:
            movies_name=request.form['movies']
            print(movies_name)
            recommended_movies_name, recommended_movies_poster=recommend(movies_name) 
            recommended_movies_name, recommended_movies_poster=recommend(movies_name) 
            print(recommended_movies_name)
            print(recommended_movies_poster)
            status=True

            return render_template("prediction.html", movies_name=recommended_movies_name, poster=recommended_movies_poster,movie_list=movies_list,status=status)

      except Exception as e:
         error={'error':e}
         return render_template("prediction.html",error=error, movie_list=movies_list,status=status)
   else:
      return render_template("prediction.html", movie_list=movies_list,status=status)





if __name__ == '__main__':
   app.debug= True
   app.run()    