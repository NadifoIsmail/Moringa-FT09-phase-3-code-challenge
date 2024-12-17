from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self,title, author,magazine):
        if not isinstance(title,str):
            raise Exception ("Title must be of type string")
        if not(5 <=len(title)<= 50):
            raise Exception("Title must be between 5 and 50 characters")
        
        if not isinstance(author,Author):
            raise Exception("author must be an instance of Author ")
        
        if not isinstance(magazine,Magazine):
            raise Exception("magazine must be an instance of Magazine ")

        self._title = title
        self._author= author
        self._magazine= magazine


        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("INSERT INTO articles (title,author_id,magazine_id)VALUES(?,?,?)",(self._title,self._author.author_id,self._magazine.magazine_id))

        self._id = CURSOR.lastrowid
        CONN.commit()
        CONN.close()

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def set_title(self,new_title):
        if hasattr(self,"_title"):
            raise Exception("Title cannot be changed after the article is instantiated.")
        if not isinstance(new_title,str):
            raise Exception ("Title must be of type string")
        if not(5 <=len(new_title)<= 50):
            raise Exception("Title must be between 5 and 50 characters")
        
        self._title = new_title

    @property
    def author(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("""
            SELECT authors.id,authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?      
        """,(self._id,))

        author_article = CURSOR.fetchone()
        CONN.close()
        return author_article
    
    @property
    def magazine(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute(""" 
            SELECT magazine.id,magazine.name,magazine.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE article.id = ?       
        """,(self._id,))

        author_magazine = CURSOR.fetchone()
        CONN.close()
        return author_magazine
    
    def content(self,article_content):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        CURSOR.execute("UPDATE articles SET content = ? WHERE articles.id = ?",(article_content,self._id))
        CONN.commit()
        CONN.close()
        
     
