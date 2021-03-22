from flask import Flask, jsonify, request, abort

from flaskr.db import setup_db, db, Todo, TodoList


def create_app(test_config=None):
  # Create and Config the app
  app = Flask(__name__)
  setup_db(app)

  # Root
  @app.route('/')
  def index():
    return 'developed by hos'


  '''
  GET POST PATCH DELETE >>lists<<
  '''

  # GET LISTS and All Todos
  @app.route('/lists')
  def get_list():
    lists = TodoList.query.order_by('id').all()
    formated_lists = [li.format() for li in lists]
    todos = Todo.query.order_by('id').all()
    formated_todos = [todo.format() for todo in todos]

    return jsonify({
      "success": True,
      "lists": formated_lists,
      "allTodos": formated_todos
    })     

  # CREATE LISTS
  @app.route('/lists', methods=['POST'])
  def create_list():
    error = False
    li = request.get_json()
    if not li.get('name'):
      abort(400, 'name expected in req body')
    try:
      new_list = TodoList(name=li['name'])
      new_list.insert()
    except:
      db.session.rollback()
      error = True
    finally:
      body = new_list.format()
      db.session.close()

    if error:
      abort(422)
    else:
      return jsonify({
        'success': True,
        "created": body
      })

  # DELETE A LIST
  @app.route('/lists/<int:list_id>', methods=['DELETE'])
  def delete_list(list_id):
    error = False
    li = TodoList.query.get_or_404(list_id)
    try:
      li.delete()
    except:
      db.session.rollback()
      error = True
    finally:
      db.session.close()
    if error:
      abort(422)
    else:
      return jsonify({
        "success": True,
        "deleted": list_id,
        "total_lists": len(TodoList.query.all())
      })       

  return app


app = create_app()

if __name__ == '__main__':
  app.run()