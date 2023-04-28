'''
The movie rating system client script that provides a program runnable
on the command line. Includes functionalities for viewing movies and genres.
'''

import sys
import requests

def list_movies():
    '''
    Prints the full list of database movies in alphabetical order.
    Offers an option to view more information on a selected movie.
    '''
    print()

    resp = s.get(API_URL + "/api/movies/")
    body = resp.json()
    sorted_movies = sorted(body["items"], key=lambda d: d['title'])

    i = 0
    for movie in sorted_movies:
        print(i, movie["title"])
        i+=1
    print()

    choice = input("Do you want to view more information on one of the movies? (y/n) ")

    if choice == "y":
        print_movie_selection_menu(sorted_movies)

    print_main_menu()

def list_genres():
    '''
    Lists all the genres in the database in alphabetical order.
    Offers an option to view all movies in a selected genre.
    '''
    print()

    resp = s.get(API_URL + "/api/movies/")
    body = resp.json()

    genreresp = s.get(API_URL + body["@controls"]["genres"]["href"])
    genrebody = genreresp.json()

    sorted_genres = sorted(genrebody["items"], key=lambda d: d['name'])

    i = 0
    for genre in sorted_genres:
        print(i, genre["name"])
        i+=1
    print()

    choice = input("Do you want to view all movies in a given genre? (y/n) ")

    if choice == "y":
        print_genre_selection_menu(sorted_genres)

    print_main_menu()

def print_movie_selection_menu(movies):
    '''
    Prints the menu for selecting a movie to show more information
    about and handles incorrect inputs.
    '''
    print()
    index = input("Enter the number of the movie: ")
    try:
        movie = movies[int(index)]
        view_movie_info(movie)
    except ValueError:
        print("Please input an integer value!")
        print_movie_selection_menu(movies)
    except IndexError:
        print("The number you gave does not match a movie!")
        print_movie_selection_menu(movies)

def print_genre_selection_menu(sorted_genres):
    '''
    Prints the menu for selecting a genre in order to list all the movies in that genre.
    '''
    print()
    index = input("Enter the number of the genre: ")
    try:
        genre = sorted_genres[int(index)]
        view_movies_in_genre(genre)
    except ValueError:
        print("Please input an integer value!")
        print_genre_selection_menu(sorted_genres)
    except IndexError:
        print("The number you gave does not match a genre!")
        print_genre_selection_menu(sorted_genres)

def view_movie_info(movie):
    '''
    Prints all the basic information of a movie.
    '''
    print()
    resp = s.get(API_URL + movie["@controls"]["self"]["href"])
    body = resp.json()

    print("Title: ", body["title"])
    print("Release year: ", body["release year"])

    try:
        if body["description"]:
            print("Description: ", body["description"])
    except KeyError:
        pass

    try:
        if body["genres"]:
            print("Genres: ", body["genres"])
    except KeyError:
        pass

    try:
        if body["average rating"]:
            print("Average rating: ", body["average rating"])
    except KeyError:
        pass

    if len(body["reviews"]) != 0:
        print()
        choice = input("Do you want to view the reviews of this movies? (y/n) ")
        if choice == "n":
            print_main_menu()
        elif choice == "y":
            print_reviews(body)

def print_reviews(body):
    '''
    Prints the reviews of a movie.
    '''

    print()
    resp = s.get(API_URL + body["@controls"]["reviews"]["href"])
    body = resp.json()
    reviews = body["items"]
    for review in reviews:
        print("Rating:", review["rating"])
        if review["comment"]:
            print("Comment:", review["comment"])
        print()

def view_movies_in_genre(genre):
    '''
    Prints the full list of movies belonging to a given genre in alphabetical order.
    Offers an option to view more information on a selected movie.
    '''
    print()
    resp = s.get(API_URL + genre["@controls"]["self"]["href"])
    body = resp.json()

    print("Movies in the genre", body['name'], ":")
    print()

    sorted_movies = sorted(body["movies"], key=lambda d: d['title'])

    i = 0
    for movie in sorted_movies:
        print(i, movie["title"])
        i+=1
    print()

    choice = input("Do you want to view more information on one of the movies? (y/n) ")

    if choice == "n":
        print_main_menu()
    elif choice == "y":
        print_movie_selection_menu(sorted_movies)

def search_for_movie():
    '''
    Searches for a movie title based on the keyword given by the user.
    '''
    print()
    resp = s.get(API_URL + "/api/movies/")
    body = resp.json()
    keyword = input("Enter keyword to be searched from movie titles: ")
    sorted_movies = sorted(body["items"], key=lambda d: d['title'])

    print()

    filtered_movies = []
    i = 0
    for movie in sorted_movies:
        if keyword.lower() in movie["title"].lower():
            print(i, movie["title"])
            filtered_movies.append(movie)
            i+=1

    print()
    choice = input("Do you want to view more information on one of the movies? (y/n) ")

    if choice == "n":
        print_main_menu()
    elif choice == "y":
        print_movie_selection_menu(filtered_movies)

def print_main_menu():
    '''
    Prints the main menu with different functionality options.
    '''
    print("\nPlease make your choice!\n")
    print("1 = list of the movies in the database")
    print("2 = list of the genres in the database")
    print("3 = search for a movie by title")
    print("0 = exit")
    print()

    choice = input("What do you want to do? ")

    if choice == "1":
        list_movies()
    if choice == "2":
        list_genres()
    if choice == "3":
        search_for_movie()
    elif choice == "0":
        print()
        print("See you later!")
        sys.exit(0)

if __name__ == "__main__":
    API_URL = "http://localhost:5000"
    with requests.Session() as s:
        s.headers.update({"Accept": "application/vnd.mason+json"})
        resp = s.get(API_URL + "/api/movies/")
        if resp.status_code != 200:
            print("Unable to access API.")
        else:
            print()
            print("Welcome to the Movie Rating System! \n")
            print("Here you can view movie information and reviews left by others.")
            print_main_menu()
