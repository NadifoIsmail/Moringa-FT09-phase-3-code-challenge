from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, name, category, id=None):
        if not isinstance(name,str):
            raise Exception("Name must be a string")
        
        if not (2 <= len(name)<= 16) :
            raise Exception("Name must be between 2 and 16 characters")
        
        if not isinstance(category,str):
            raise Exception("Category must be of type string")
        
        if len(category) == 0:
            raise Exception ("Category must be longer than 0 characters")

        self._name = name
        self._category = category
        self._id = id
        if id is None :
            CONN = get_db_connection()
            CURSOR = CONN.cursor()
            CURSOR.execute("INSERT INTO magazines (name,category) VALUES(?,?)", (name,category))
            self._id = CURSOR.lastrowid
            CONN.close()


    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def magazine_id(self):
        return self._id
    
    @property
    def magazine_name(self):
        return self._name
    
    @magazine_name.setter
    def set_magazine_name(self,new_name):
        if not isinstance(new_name,str):
            raise Exception("Name must be a string")
        
        if not (2 <= len(new_name)<= 16) :
            raise Exception("Name must be between 2 and 16 characters")
        
        self._name = new_name

    @property
    def magazine_category(self):
        return self._category
    
    @magazine_category.setter
    def set_magazine_category(self,new_category):
        if not isinstance(new_category,str):
            raise Exception("Category must be of type string")
        
        if len(new_category) == 0:
            raise Exception ("Category must be longer than 0 characters")
        
        self._category = new_category


    def articles(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT articles.title, articles.content, articles.magazine_id
            FROM articles
            WHERE articles.magazine_id = ?
        """,(self._id,))

        magazine_articles = CURSOR.fetchall()
        CONN.close()
        return magazine_articles
    
    def contributors(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT authors.id,authors.name
            FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """,(self._id,))

        magazine_contributors = CURSOR.fetchall()
        CONN.close()
        return magazine_contributors
    
    def article_titles(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT articles.title
            FROM articles           
            JOIN magazines ON magazines.id = articles.magazine_id
            WHERE articles.magazine_id = ?
        """,(self._id,)) 

        title_list = CURSOR.fetchall()
        list = [row[0] for row in title_list]
        CONN.close()
        if list:
            return list
        else:
            return None
        
    def contributing_authors(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT authors.id,authors.name
            FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2 
        """,(self._id,))  

        contributors_list = CURSOR.fetchall()
        contributing_authors = [Author(id = author[0],name = author[1]) for author in contributors_list]

        if contributing_authors:
            return contributing_authors
        else:
            return None
        
              