import unittest
import json
from flaskr import create_app
from flaskr.db import setup_db, db, Todo, TodoList 

from os import environ


class checkAllTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(True)
    self.client = self.app.test_client
    setup_db(self.app, environ.get("TEST_DATABASE_URI"), True)
    self.new_list = {"name": 'new list20'}

    self.new_todo = {"description": 'new todo'}
    self.headersConf = {'Content-type': 'application/json','Access-Control-Allow-Origin': '*'}
  
    
  def test_add_new_list(self):
    res = self.client().post(
      '/lists', headers=self.headersConf,
      json=self.new_list)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['created'])
    self.assertTrue(data['totalLists'])

  def test_add_new_todo(self):
    res = self.client().post(
      '/lists/25/todos', headers=self.headersConf,
      json=self.new_todo)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['created'])
    
  def test_get_lists(self):
    res = self.client().get('/lists', headers=self.headersConf)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['totalLists'])
    self.assertTrue(data['allTodos'])

  def test_404_get_no_existing_endpoint(self):
    res = self.client().get('/listssss', headers=self.headersConf)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Not Found!')  

  def test_get_todos_from_list(self):
    res = self.client().get('/lists/25/todos', headers=self.headersConf)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(data['currentTodos'])
    self.assertTrue(data['currentList'])

  def test_404_get_todos_from_list(self):
    res = self.client().get('/lists/1000/todos', headers=self.headersConf)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Not Found!')

   
  
