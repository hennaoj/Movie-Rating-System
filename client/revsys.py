'''
The movie rating system client script that provides a program runnable
on the command line. Includes functionalities for viewing movies and genres.
'''

import os
import sys
import requests

DEFAULT_API_KEY = "ea4bfdbe683994744fd665f90ac1f393"
USER_DICT = {"username": "", "apikey": ""}
ASK_LOGIN = True


def decorate_title(text, subtext=None):
    '''
    Decorate text for the command line interface
    '''
    print("\n########################################")
    lengthoftitle = len(text)
    numberofsigns = int((40 - lengthoftitle - 2) / 2)
    string = ""
    for _ in range(numberofsigns):
        string += "#"
    string += " " + text + " "
    for _ in range(numberofsigns):
        string += "#"
    print(string)
    if not subtext:
        print("########################################\n")
    else:
        lengthofsubtext = len(subtext)
        numberofsigns = int((40 - lengthofsubtext - 2) / 2)
        string = ""
        for _ in range(numberofsigns):
            string += "#"
        string += " " + subtext + " "
        for _ in range(numberofsigns):
            string += "#"
        print(string)
        print("########################################\n")
def ask_for_inputs(inputdict, prompt, toggleseparator=True):
    '''
    print input options
    '''
    if toggleseparator:
        print("\n########################################\n")
    for key in sorted(inputdict.keys()):
        print(key + " = " + inputdict[key][0])
    choice = input(prompt + " ")
    if choice in inputdict.keys():
        if len(inputdict[choice][2]) > 0:
            inputdict[choice][1](*inputdict[choice][2])
        else:
            inputdict[choice][1]()
    else:
        print("Invalid input.")
        ask_for_inputs(inputdict, prompt)

def list_movies():
    '''
    Prints the full list of database movies in alphabetical order.
    Offers an option to view more information on a selected movie.
    '''
    decorate_title("List of All Movies")
    resp = s.get(API_URL + "/api/movies/")
    body = resp.json()
    sorted_movies = sorted(body["items"], key=lambda d: d['title'])
    inputdict = {}
    i = 0
    for movie in sorted_movies:
        inputdict[str(i)] = [movie["title"], view_movie_info, [movie]]
        i+=1
    inputdict["n"] = ["Return to main menu", print_main_menu, []]
    ask_for_inputs(inputdict, "\nLook at specific movie or return? ", False)

def list_genres():
    '''
    Lists all the genres in the database in alphabetical order.
    Offers an option to view all movies in a selected genre.
    '''

    decorate_title("List of All Genres")
    resp = s.get(API_URL + "/api/movies/")
    body = resp.json()

    genreresp = s.get(API_URL + body["@controls"]["genres"]["href"])
    genrebody = genreresp.json()

    sorted_genres = sorted(genrebody["items"], key=lambda d: d['name'])

    inputdict = {}
    i = 0
    for genre in sorted_genres:
        inputdict[str(i)] = [genre["name"], view_movies_in_genre, [genre]]
        i+=1
    inputdict["n"] = ["Return to main menu", print_main_menu, []]
    ask_for_inputs(inputdict, "\nLook at movies in specific genre or return? ", False)

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
    decorate_title("Movie Information")
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

    inputdict = {
    "0": ["View Reviews", print_reviews, [body]], 
    "m": ["Return to Movies list", list_movies, []], 
    "n": ["Return to Main Menu", print_main_menu, []], 
    }
    ask_for_inputs(inputdict, "\nMake your choice (0, m, n)?")

def print_reviews(body):
    '''
    Prints the reviews of a movie.
    '''
    decorate_title("Reviews")
    resp = s.get(API_URL + body["@controls"]["reviews"]["href"])
    body_ = resp.json()
    reviews = body_["items"]
    inputdict = {
    "0": ["Add a Review", add_a_review, [API_URL + body["@controls"]["reviews"]["href"], body]], 
    "m": ["Return to Movies list", list_movies, []], 
    "n": ["Return to Main Menu", print_main_menu, []], 
    }
    if len(reviews) > 0:
        for review in reviews:
            print(review["rating"] + ".0 / 5.0")
            if review["comment"]:
                print(review["comment"])
            print(f'by {review["user"]}\n')
            if review["user"] == USER_DICT["username"]:
                inputdict["1"] = ["Edit your review", edit_a_review, [API_URL + review["@controls"]["self"]["href"], review, body]]
                inputdict["2"] = ["Delete your review", delete_a_review, [API_URL + review["@controls"]["self"]["href"], body]]

    else:
        print("No reviews yet.\n")
    ask_for_inputs(inputdict, "\nMake your choice")


def edit_a_review(url, review, body):
    '''
    Edit a review you made.
    '''
    rating = None
    while rating not in [1, 2, 3, 4, 5]:
        try:
            print("Previous rating: " + review["rating"] + "\n")
            rating = int(input("Rating for movie? (1, 2, 3, 4, 5) "))
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError
        except ValueError:
            print("Invalid input. Give integer between 1-5")
    print("Previous comment: " + review["comment"] + "\n")
    comment = str(input("Write a comment.\n\n"))
    review =  {"rating":int(rating), "comment":comment, "apikey":USER_DICT["api_key"]}
    resp = s.put(url, json=review, headers={"API-Key":USER_DICT["api_key"]})
    print_reviews(body)


def delete_a_review(url, body):
    '''
    Delete your review to a movie.
    '''
    resp = s.delete(url, headers={"API-Key":USER_DICT["api_key"]})
    print_reviews(body)


def add_a_review(url, body):
    '''
    Add a review to a movie.
    '''
    rating = None
    while rating not in [1, 2, 3, 4, 5]:
        try:
            rating = int(input("Rating for movie? (1, 2, 3, 4, 5) "))
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError
        except ValueError:
            print("Invalid input. Give integer between 1-5")
    comment = str(input("Write a comment.\n\n"))
    review =  {"rating":int(rating), "comment":comment, "apikey":USER_DICT["api_key"]}
    resp = s.post(url, json=review, headers={"API-Key":USER_DICT["api_key"]})
    print_reviews(body)

def view_movies_in_genre(genre):
    '''
    Prints the full list of movies belonging to a given genre in alphabetical order.
    Offers an option to view more information on a selected movie.
    '''

    decorate_title("Movies in the genre")

    resp = s.get(API_URL + genre["@controls"]["self"]["href"])
    body = resp.json()

    sorted_movies = sorted(body["movies"], key=lambda d: d['title'])
    inputdict = {}
    i = 0
    for movie in sorted_movies:
        inputdict[str(i)] = [movie["title"], view_movie_info, [movie]]
        i+=1
    inputdict["m"] = ["Return to genres", list_genres, []]
    inputdict["n"] = ["Return to main menu", print_main_menu, []]
    ask_for_inputs(inputdict, "\nLook at specific movie or return: ", False)


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
    inputdict = {}
    i = 0
    for movie in sorted_movies:
        if keyword.lower() in movie["title"].lower():
            inputdict[str(i)] = [movie["title"], view_movie_info, [movie]]
            i+=1
    inputdict["n"] = ["Return to main menu", print_main_menu, []]
    ask_for_inputs(inputdict, "\nLook at specific movie or return: ", False)

def validate_input(prompt, inputtype, validlist=False):
    '''
    Validate given input
    '''
    for _ in range(100):
        try:
            value = inputtype(input(prompt))
        except:
            print("Input needs to be of type ", inputtype)
            continue
        if validlist:
            if value in validlist:
                return(value)
            print("Input needs to be one of given choices ", inputtype)
            continue
        return(value)


def create_user():
    '''
    Create a new user for api usage
    '''
    decorate_title("Create user")
    username = validate_input("Give username.\n", str)
    age = validate_input("Give age.\n", int)
    gender = validate_input("Give gender (1:male, 2:female, 3:other)\n", int, [1, 2, 3])

    user =  {"username":username, "age":age, "gender":gender}
    resp = s.post(API_URL+"/api/users/", json=user)
    if resp.status_code == 500:
        print("\nUsername already exists")
    if resp.status_code == 201:
        p = os.path.dirname(os.path.abspath(__file__))
        with open(p+"/apikeys/apikey.txt", "w", encoding='UTF-8') as f:
            f.write(resp.headers["API-key"])
    log_in()

def print_main_menu():
    '''
    Prints the main menu with different functionality options.
    '''
    decorate_title("Movie Rating System Client", "View movie information and reviews")
    inputdict = {
    "1": ["List of movies in the database", list_movies, []], 
    "2": ["List of the genres in the database", list_genres, []], 
    "3": ["Search for a movie by title", search_for_movie, []], 
    "n": ["Exit", sys.exit, []]
    }
    if USER_DICT["api_key"] == DEFAULT_API_KEY:
        inputdict["4"] = ["Create user", create_user, []]
    ask_for_inputs(inputdict, "\nWhat do you want to do?", False)


def log_in():
    global USER_DICT
    p = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(p+"/apikeys/apikey.txt", "r", encoding='UTF-8') as f:
            line = f.readline()
            resp = s.get(API_URL+"/api/users/", headers={"API-key":line})
            if resp.status_code == 200:
                name = resp.json()["username"]
            else:
                raise Exception
            choice = input("Log in as " + name + "? (y/n)")
            if choice == "y":
                USER_DICT["username"] = name
                USER_DICT["api_key"] = line
                ASK_LOGIN = False
            elif choice == "n":
                print("Logging in to default test user 123bob321\n")
                USER_DICT["username"] = "123bob321"
                USER_DICT["api_key"] = DEFAULT_API_KEY
            else:
                print("Invalid input.")
    except Exception as e:
        print("No valid API-keys in apikeys folder\n")
        print("Logging in to default test user 123bob321\n")
        USER_DICT["username"] = "123bob321"
        USER_DICT["api_key"] = DEFAULT_API_KEY
    print_main_menu()



if __name__ == "__main__":
    API_URL = "http://localhost:5000"
    CURRENT_URL = "movies/"
    with requests.Session() as s:
        s.headers.update({"Accept": "application/vnd.mason+json"})
        response = s.get(API_URL + "/api/movies/")
        if response.status_code != 200:
            print("Unable to access API.")
        else:
            log_in()
