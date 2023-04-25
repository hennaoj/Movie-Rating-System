'''Miscellaneous utilities'''
from flask import url_for
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from review_system.models import Movie, Genre, Review

# MasonBuilder provided in the PWP Exercise 3
class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    
    Note that child classes should set the *DELETE_RELATION* to the application
    specific relation name from the application namespace. The IANA standard
    does not define a link relation for deleting something.
    """

    DELETE_RELATION = ""

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

class ReviewSystemBuilder(MasonBuilder):
    """ReviewSystem specific MasonBuilder"""
    def add_control_add_review(self, movie):
        self.add_control(
            "revsys:add-review",
            url_for("reviewcollection", movie=movie),
            method = "post",
            encoding = "json",
            title = "Add a new review for this movie",
            schema = Review.json_schema()
        )

    def add_control_delete_review(self, movie, review):
        self.add_control(
            "revsys:delete-review",
            url_for("reviewitem", movie=movie, review=review),
            method="delete",
            title= "Delete this review from the database"
        )

    def add_control_add_movie(self):
        self.add_control(
            "revsys:add-movie",
            url_for("moviecollection"),
            method="post",
            encoding="json",
            title="Add a new movie to the movie collection",
            schema = Movie.json_schema()
        )

    def add_control_delete_movie(self, movie):
        self.add_control(
            "revsys:delete-movie",
            url_for("movieitem", movie=movie),
            method="delete",
            title= "Delete this movie from the database"
        )

    def add_control_edit_movie(self, movie):
        self.add_control(
            "revsys:edit-movie",
            url_for("movieitem", movie=movie),
            method="put",
            encoding="json",
            title= "Edit the movie's information in the database",
            schema = Movie.json_schema()
        )

    def add_control_add_genre(self):
        self.add_control(
            "revsys:add-genre",
            url_for("genrecollection"),
            method="post",
            encoding="json",
            title="Add a new genre to the database",
            schema = Genre.json_schema()
        )

class MovieConverter(BaseConverter):
    '''Converter for movies'''
    def to_python(self, value):
        db_movie = Movie.query.filter_by(uri_id=value).first()
        if db_movie is None:
            raise NotFound
        return db_movie

    def to_url(self, value):
        return str(value.uri_id)

class GenreConverter(BaseConverter):
    '''Converter for genres'''
    def to_python(self, value):
        db_genre = Genre.query.filter_by(name=value).first()
        if db_genre is None:
            raise NotFound
        return db_genre

    def to_url(self, value):
        return str(value.name)
