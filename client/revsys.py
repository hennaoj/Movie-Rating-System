'''
The movie rating system client script that provides a program runnable
on the command line. Includes functionalities for viewing movies and genres.
'''

import sys
import requests

def list_movies(body):
    '''
    Prints the full list of database movies in alphabetical order.
    Offers an option to view more information on a selected movie.
    '''
    print()

    sorted_movies = sorted(body["items"], key=lambda d: d['title'])

    i = 0
    for movie in sorted_movies:
        print(i, movie["title"])
        i+=1
    print()

    choice = input("Do you want view more information on one of the movies? (y/n) ")

    if choice == "y":
        print_movie_selection_menu(sorted_movies)

    print_main_menu(body)

def list_genres(body):
    '''
    Lists all the genres in the database in alphabetical order.
    Offers an option to view all movies in a selected genre.
    '''
    print()

    genreresp = s.get(API_URL + body["@controls"]["genres"]["href"])
    genrebody = genreresp.json()

    sorted_genres = sorted(genrebody["items"], key=lambda d: d['name'])

    i = 0
    for genre in sorted_genres:
        print(i, genre["name"])
        i+=1
    print()

    choice = input("Do you want view all movies in a given genre? (y/n) ")

    if choice == "y":
        print_genre_selection_menu(sorted_genres)

    print_main_menu(body)

def print_movie_selection_menu(sorted_movies):
    '''
    Prints the menu for selecting a movie to show more information
    about and handles incorrect inputs.
    '''
    print()
    index = input("Enter the number of the movie: ")
    try:
        movie = sorted_movies[int(index)]
        view_movie_info(movie)
    except ValueError:
        print("Please input an integer value!")
        print_movie_selection_menu(sorted_movies)
    except IndexError:
        print("The number you gave does not match a movie!")
        print_movie_selection_menu(sorted_movies)

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
        if body["rating"]:
            print("Description: ", body["rating"])
    except KeyError:
        pass

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

    choice = input("Do you want view more information on one of the movies? (y/n) ")

    if choice == "n":
        print_main_menu(body)
    elif choice == "y":
        print_movie_selection_menu(sorted_movies)

def search_for_movie(body):
    '''
    Searches for a movie title based on the keyword given by the user.
    '''
    print()
    keyword = input("Enter keyword to be searched from movie titles: ")
    print(keyword)

def print_main_menu(body):
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
        list_movies(body)
    if choice == "2":
        list_genres(body)
    if choice == "3":
        search_for_movie(body)
    elif choice == "0":
        print()
        print("See you later!")
        sys.exit(0)

if __name__ == "__main__":
    API_URL = "http://localhost:5000"
    with requests.Session() as s:
        s.headers.update({"Accept": "application/vnd.mason+json"})
        init_resp = s.get(API_URL + "/api/movies/")
        if init_resp.status_code != 200:
            print("Unable to access API.")
        else:
            print()
            print("Welcome to the Movie Rating System! \n")
            print("Here you can view movie information and reviews left by others.")
            init_body = init_resp.json()
            print_main_menu(init_body)
