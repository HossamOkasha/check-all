from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flaskr.db import setup_db, db, Todo, TodoList

def create_app(test_config=None):
  # Create and Config the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

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


  '''
  GET POST PATCH DELETE >>todos<<
  '''

  # GET TODOS FROM LIST
  @app.route('/lists/<int:list_id>/todos')
  def get_todos_from_list(list_id):
    current_list = TodoList.query.get_or_404(list_id)
    todos = current_list.todos

    formated_todo = [todo.format() for todo in todos]
    formated_list = current_list.format()
    return jsonify({"success": True, "currentTodos": formated_todo, "currentList": formated_list})

  # POST TODOS
  @app.route('/lists/<int:list_id>/todos', methods=['POST'])
  def create_todo(list_id):
    error = False
    todo = request.get_json()
    if not todo.get('description'):
      abort(400, 'description expected in req body')
    try:
      new_todo = Todo(description=todo["description"], list_id=list_id)
      new_todo.insert()
    except:
      db.session.rollback()
      error = True
    finally:
      if not error:
        body = new_todo.format()
      db.session.close()
    if error:
      abort(422)
    else:
      return jsonify({
        'success': True,
        'created': body
      })

  # UPDATE A Todo
  @app.route('/todos/<int:todo_id>', methods=["PATCH"])
  def update_todo_completed(todo_id):
    error = False
    todo = Todo.query.get_or_404(todo_id)
    complete = request.get_json().get('complete')
    if complete is None:
      abort(400, 'complete expected in req body')
    try:
      todo.complete = bool(complete)
      todo.update()
    except:
      db.session.rollback()
      error = True
    finally:
      db.session.close()

    if error:
      abort(400)

    else:
      return jsonify({
        "success": True,
        "todoId": todo_id
      })

  # DELETE a ToDo
  @app.route("/todos/<int:todo_id>", methods=["DELETE"])
  def delete_todo(todo_id):
    error = False
    todo = Todo.query.get_or_404(todo_id)
    try:
      todo.delete()
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
        "deleted": todo_id,
        "total_todos": len(Todo.query.all())
      })

  # CHECK ALL TODOS
  @app.route('/lists/<int:list_id>', methods=['PATCH'])
  def set_completed_list(list_id):
    error = False
    selected_list = TodoList.query.get_or_404(list_id)
    complete_value = request.get_json().get('complete')
    if complete_value is None:
      abort(400, 'complete expected in req body')
    
    try:
      for todo in selected_list.todos:
        todo.complete = complete_value
      selected_list.update()
    except:
      db.session.rollback()

      error = True
    finally:
      db.session.close()

    if error:
      abort(500)
    else:
      return jsonify({
        "success": True,
        "listId": list_id
      })
  
  # ERROR HANDLERS
  
  # 404 NOT FOUND
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found!'
    }), 404

  # 405 NOT ALLOWED
  @app.errorhandler(405)
  def not_alllowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Method Not Allowed!'
    }), 405

  # 400 BAD REQUEST
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request!'
    }), 400

  # 422 UNPROCESSABLE
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422    
  
  return app


app = create_app()

if __name__ == '__main__':
  app.run()