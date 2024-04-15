from bs4 import BeautifulSoup


def top_chart_extraction(response):

    try: 
        soup = BeautifulSoup(response.text, 'html')
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