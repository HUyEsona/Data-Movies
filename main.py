import urllib.request
import json
import xlwt
from xlwt import Workbook
import csv
from urllib.request import urlopen

# Thay thế bằng API key của bạn
api_key = '8af1401447c4623340a5e45bb0ff20be'

# URL để lấy danh sách các bộ phim phổ biến
movies_url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
# URL để lấy danh sách tất cả thể loại phim
genres_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'

# Hàm lấy dữ liệu JSON từ API
def fetch_data(url):
    try:
        response = urlopen(url)
        return json.loads(response.read())
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None

# Lấy danh sách các thể loại phim
genres_data = fetch_data(genres_url)
genres_dict = {genre['id']: genre['name'] for genre in genres_data['genres']}

# Lấy danh sách các bộ phim phổ biến
movies_data = fetch_data(movies_url)
movies = []
for row in movies_data['results']:
    genre_names = [genres_dict[genre_id] for genre_id in row['genre_ids'] if genre_id in genres_dict]
    movie_data = {
        'id': row['id'],
        'title': row['title'],
        'original_title': row['original_title'],
        'vote_average': row['vote_average'],
        'genres': ', '.join(genre_names)
    }
    movies.append(movie_data)

# Lưu vào CSV
with open('data_the_movie.csv', 'w', newline='', encoding='utf-8') as file:
    header = ['id', 'title', 'original_title', 'vote_average', 'genres']
    csv_writer = csv.writer(file)
    csv_writer.writerow(header)  # Ghi tiêu đề
    for movie in movies:
        csv_writer.writerow([movie['id'], movie['title'], movie['original_title'], movie['vote_average'], movie['genres']])

# Lưu vào Excel (.xls)
wb = Workbook()
sheet = wb.add_sheet('data the movie')

# Ghi tiêu đề
sheet.write(0, 0, 'ID')
sheet.write(0, 1, 'Title')
sheet.write(0, 2, 'Original Title')
sheet.write(0, 3, 'Vote Average')
sheet.write(0, 4, 'Genres')

# Ghi dữ liệu
for i, movie in enumerate(movies, start=1):
    sheet.write(i, 0, movie['id'])
    sheet.write(i, 1, movie['title'])
    sheet.write(i, 2, movie['original_title'])
    sheet.write(i, 3, movie['vote_average'])
    sheet.write(i, 4, movie['genres'])

wb.save('data the movie.xls')
