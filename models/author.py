from database.connection import get_db_connection

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name,str):
            raise Exception("Name must be a string")
        
        if len(name) == 0:
            raise Exception ("Name must be longer than 0 characters")
        self._name = name
        self._id =id
        if id is None :
            CONN = get_db_connection()
            CURSOR = CONN.cursor()
            CURSOR.execute("INSERT INTO authors (name)VALUES(?)", (name,))
            self._id = CURSOR.lastrowid
            CONN.close()

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def author_id(self):
        return self._id
      
    @property
    def author_name(self):
        return self._name
    
    @author_name.setter
    def set_author_name(self,new_name):
        if hasattr(self,"_name"):
            raise Exception("Name cannot be changed after the author is instantiated.")
        
        if not isinstance(new_name,str):
            raise Exception("Name must be a string")
        
        if len(new_name) == 0:
            raise Exception ("Name must be longer than 0 characters")
        
        self._name = new_name

    def articles(self):
        CONN = get_db_connection()   
        CURSOR = CONN.cursor() 
        CURSOR.execute("""
            SELECT articles.id,articles.title,articles.content 
            FROM articles 
            WHERE articles.author_id = ? 
        """,(self._id,))

        author_articles = CURSOR.fetchall()
        CONN.close()
        return author_articles
    
    def magazines(self):
        CONN = get_db_connection()   
        CURSOR = CONN.cursor() 
        CURSOR.execute("""
            SELECT magazines.name, magazines.category
            FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?  
        """, (self._id,))

        author_magazine = CURSOR.fetchall()
        CONN.close()
        return author_magazine

