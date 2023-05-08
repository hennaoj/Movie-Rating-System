'''
The movie rating system client script that provides a program runnable
on the command line. Includes functionalities for viewing movies and genres.
'''

import os
import sys
import requests

DEFAULT_API_KEY = "ea4bfdbe683994744fd665f90ac1f393"
API_KEY = DEFAULT_API_KEY
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
    "1": ["Return to Movies list", list_movies, []], 
    "2": ["Return to Main Menu", print_main_menu, []], 
    }
    ask_for_inputs(inputdict, "\nMake your choice (0, 1, 2)?")

def print_reviews(body):
    '''
    Prints the reviews of a movie.
    '''
    decorate_title("Reviews")
    resp = s.get(API_URL + body["@controls"]["reviews"]["href"])
    body_ = resp.json()
    reviews = body_["items"]
    if len(reviews) > 0:
        for review in reviews:
            print(review["rating"] + ".0 / 5.0")
            if review["comment"]:
                print(review["comment"])
            print(f'by {review["user"]}\n')
    else:
        print("No reviews yet.\n")
    inputdict = {
    "0": ["Add a Review", add_a_review, [API_URL + body["@controls"]["reviews"]["href"], body]], 
    "m": ["Return to Movies list", list_movies, []], 
    "n": ["Return to Main Menu", print_main_menu, []], 
    }
    ask_for_inputs(inputdict, "\nMake your choice (0, 1, 2)?")

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
    review =  {"rating":int(rating), "comment":comment, "apikey":API_KEY}
    resp = s.post(url, json=review, headers={"API-Key":API_KEY})
    print_reviews(body)
    print(resp)

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

def check_api_file():
    '''
    Check api file folder for {username}.txt files.
    '''
    p = os.path.dirname(os.path.abspath(__file__))
    apifiles = os.listdir(p + "/apikeys/")
    global API_KEY
    global ASK_LOGIN
    if len(apifiles) == 0:
        return()
    txtfiles = filter(lambda x: x[-4:] == '.txt', apifiles)
    for i in txtfiles:
        try:
            with open(p+"/apikeys/"+i, "r", encoding='UTF-8') as f:
                line = f.readline()
                name = i.split(".")[0]
                choice = input("Log in as " + name + "? (y/n)")
                if choice == "y":
                    API_KEY = line
                    ASK_LOGIN = False
                    break
                if choice == "n":
                    pass
                else:
                    print("Invalid input.")
        except:
            pass
    return()

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
        with open(p+"/apikeys/"+ username + ".txt", "w", encoding='UTF-8') as f:
            f.write(resp.headers["API-key"])
    print_main_menu()

def print_main_menu():
    '''
    Prints the main menu with different functionality options.
    '''
    decorate_title("Movie Rating System Client", "View movie information and reviews")
    if ASK_LOGIN:
        check_api_file()
    inputdict = {
    "1": ["List of movies in the database", list_movies, []], 
    "2": ["List of the genres in the database", list_genres, []], 
    "3": ["Search for a movie by title", search_for_movie, []], 
    "n": ["Exit", sys.exit, []]
    }
    if API_KEY == DEFAULT_API_KEY:
        inputdict["4"] = ["Create user", create_user, []]
    ask_for_inputs(inputdict, "\nWhat do you want to do?", False)

if __name__ == "__main__":
    API_URL = "http://localhost:5000"
    CURRENT_URL = "movies/"
    with requests.Session() as s:
        s.headers.update({"Accept": "application/vnd.mason+json"})
        response = s.get(API_URL + "/api/movies/")
        if response.status_code != 200:
            print("Unable to access API.")
        else:
            print_main_menu()
