from bs4 import BeautifulSoup
from dateutil.parser import parser

def top_chart_extraction(response):

    try: 
        soup = BeautifulSoup(response.text, 'html.parser')
        list_items = soup.find_all('li', class_ = 'ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent')
        top_movies = []

        for each_li in list_items:
            each_movie = {}
            movie_poster = each_li.find('img',class_ ='ipc-image')['src'] # movie poster url
            
            # getting Movie's Ranking and Name
            details_ranking_name = each_li.find('h3', class_ = 'ipc-title__text').text.split(" ",1)
            movie_ranking = details_ranking_name[0].replace(".","")
            movie_name = details_ranking_name[1]
            
            # getting Movie's Year, length and Certification
            div_year_lenght_certification = each_li.find('div', class_ = 'sc-b189961a-7 feoqjK cli-title-metadata') # length of movie
            div_details = [span.text for span in div_year_lenght_certification.find_all('span', class_='sc-b189961a-8 kLaxqf cli-title-metadata-item')]
            movie_release_year = div_details[0]
            movie_length = div_details[1]
            movie_certification = div_details[2]

            # getting IMDb rating and voters count
            movie_imdb_rating = each_li.find('span',class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text.split('(')[0].strip()
            movie_star_vote_counts = each_li.find('span', class_ = 'ipc-rating-star--voteCount').text.replace("(","").replace(")","") # total number of rating on imdb
            # print(type(movie_star_vote_counts))
            each_movie = {
                "movie_ranking": movie_ranking,
                "movie_name":movie_name,
                "movie_poster_url":movie_poster,
                "release_year": movie_release_year,
                "movie_length": movie_length,
                "movie_certification": movie_certification,
                "imdb_rating": movie_imdb_rating,
                "people_voted": movie_star_vote_counts.replace('\xa0', '')
            }
            top_movies.append(each_movie)

        return top_movies
    
    except Exception as e:
        print(f"Exception occured: {e}")
        return None
    

def upcoming_releases_extract(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        date_blocks = soup.find_all('article', class_ = 'sc-48add019-1 hSuRMl') # get date block for movies
        upcoming_releases = []
        for one_date_block in date_blocks:

            date = one_date_block.find('h3').text
            each_movie_block = one_date_block.find_all('li', class_ = 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 eWVqBf')
            for each in each_movie_block:
                each_movie = {}
                movie_poster_tag = each.find('img', class_ ='ipc-image')
                if movie_poster_tag:
                    movie_poster = movie_poster_tag.get('src') 
                each_movie_detail = each.find('div', class_ = 'ipc-metadata-list-summary-item__tc')
                # name
                movie_name = each_movie_detail.find('a', class_ = 'ipc-metadata-list-summary-item__t' ).text
                # genres
                movie_genres_block = each_movie_detail.find('ul', class_ = 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base')
                movie_genres = []
                movie_genres_all_li = movie_genres_block.find_all('li', class_ = 'ipc-inline-list__item') if movie_genres_block is not None else None
                if movie_genres_all_li is not None:
                    for each_li in movie_genres_all_li:
                        if each_li is not None:
                            movie_genres.append(each_li.find('span', class_ = 'ipc-metadata-list-summary-item__li').text)

                # actors
                movie_actors_block = each_movie_detail.find('ul', class_ = 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base')
                movie_actors = []
                movie_actors_all_li = movie_actors_block.find_all('li', class_ = 'ipc-inline-list__item') if movie_actors_block is not None else None
                if movie_actors_all_li is not None:
                    for each_li in movie_actors_all_li:
                        if each_li is not None:
                            movie_actors.append(each_li.find('span', class_ = 'ipc-metadata-list-summary-item__li').text)

                # make each movie info
                each_movie = {       
                    "movie_name": movie_name,
                    "release_date": date,
                    "movie_poster": movie_poster,
                    "movie_genres": movie_genres,
                    "movie_actors" : movie_actors,
                }
                upcoming_releases.append(each_movie)
            return upcoming_releases

    except Exception as e:
        print(f"Exception occured: {e}")
        return None