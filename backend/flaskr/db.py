from os import environ
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=None, test=False):
  if database_path:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  else:
    try:
      DATABASE_URI = environ["DATABASE_URI"]
      app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    except:
      raise ValueError('DATABASE_URI not found')  
    
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)

  if test:
    db.create_all()
  else:
    migrate = Migrate(app, db)



class TodoList(db.Model):
  __tablename__ = "todolists"
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  todos = db.relationship('Todo', backref='list',
                          lazy=True, cascade="all, delete")
  def __init__(self, name):
    self.name = name


  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()        

  def format_all(self):
    todos = self.todos
    formated_todos = [todo.format() for todo in todos]
    return {
      'id': self.id,
      'name': self.name,
      'todos': formated_todos
    }

  def __repr__(self):
    return f'<TodoList ID: {self.id}, name: {self.name}, todos: {self.todos}>'


'''
Todo

'''


class Todo(db.Model):
  __tablename__ = "todos"
  id = Column(Integer, primary_key=True)
  description = Column(String(), nullable=False)
  complete = Column(Boolean, nullable=False,
                    server_default='f', default=False)
  list_id = Column(Integer, ForeignKey(
      'todolists.id'), nullable=False)

  def __init__(self, description, list_id):
    self.description = description

    self.list_id = list_id    

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit() 

  def format(self):
    return {
      'id': self.id,
      'description': self.description,
      'complete': self.complete,
      'list_id': self.list_id
    }

  def __repr__(self):
    return f'<Todo ID: {self.id}, description: {self.description}, complete: {self.complete}>'
