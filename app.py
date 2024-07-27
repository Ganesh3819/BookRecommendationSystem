from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

popular_df = pd.read_pickle('popular.pkl')

pt = pd.read_pickle('pt.pkl')

similarity_score = pd.read_pickle('similarity_score.pkl')

books = pd.read_pickle('books.pkl')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input:
        # Convert the user input to lower case
        user_input_lower = user_input.lower()

        # Convert the book titles in the pivot table to lower case
        pt_lower = pt.index.str.lower()

        # Find the index of the matching book title (case insensitive)
        try:
            index = np.where(pt_lower == user_input_lower)[0][0]
        except IndexError:
            # Handle the case where the book is not found
            return render_template('recommend.html', data=[], message="Book not found")

        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'].str.lower() == pt_lower[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

            data.append(item)

        print(data)
        return render_template('recommend.html', data=data)
    else:
        return render_template('recommend.html', data=[], message="No input provided")


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
