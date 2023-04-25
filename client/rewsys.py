import json
import requests

def list_movies():
    print()
    resp = s.get(API_URL + "/api/movies/")
    body = resp.json()

    sorted_movies = sorted(body["items"], key=lambda d: d['title'])

    i = 0
    for movie in sorted_movies:
        print(i, movie["title"])
        i+=1
    print()

    choice = input("Do you want view more information on one of the movies? (y/n) ")

    if choice == "n":
        print_main_menu()
    elif choice == "y":
        print_movie_selection_menu(sorted_movies)

def print_movie_selection_menu(sorted_movies):
    print()
    index = input("Enter the number of the movie: ")
    try:
        movie = sorted_movies[int(index)]
    except ValueError:
        print("Please input an integer value!")
        print_movie_selection_menu(sorted_movies)
    except IndexError:
        print("The number you gave does not match a movie!")
        print_movie_selection_menu(sorted_movies)

def print_main_menu():
    print("\nPlease make your choice!\n")
    print("1 = list of the movies in the database")
    print("2 = list of the genres in the database")
    print("3 = search for a movie")
    print("0 = exit")
    print()

    choice = input("What do you want to do? ")

    if choice == "1":
        list_movies()

if __name__ == "__main__":
    API_URL = "http://localhost:5000"
    with requests.Session() as s:
        s.headers.update({"Accept": "application/vnd.mason+json"})
        resp = s.get(API_URL + "/api/movies/")
        if resp.status_code != 200:
            print("Unable to access API.")
        else:
            print()
            print("Welcome to the Movie Rating System! \n \nHere you can view movie information and reviews left by others.")
            print_main_menu()