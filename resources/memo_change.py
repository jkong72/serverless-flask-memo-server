from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector.errors import Error

from MySQL_connection import get_cnx


class MemoChangeResource(Resource):
    def put(self, memo_id):
        data = request.get_json()

        if data['title'] is '' or data['contents'] is '':
            return {'error':'제목과 내용을 입력해주세요'}

        try:
            cnx = get_cnx()

            query = '''update memos
                    set title = %s, contents = %s, date = %s
                    where id = %s;'''            

            record = (
                data['title'],
                data['contents'],
                data['date'],
                memo_id)

            cursor = cnx.cursor()
            cursor.execute(query, record)
            cnx.commit()

        except Error as e:
            print('Error while connecting to MySQL\n',e)
            return {'error':str(e)}, HTTPStatus.BAD_REQUEST

        finally :
            cursor.close()
            if cnx.is_connected():
                cnx.close()
                print('MySQL connection is closed')
            else:
                print('connection does not exist')

        return {'result':'메모의 내용이 성공적으로 갱신 되었습니다.'}, HTTPStatus.OK
    

    def delete(self, memo_id):
        try:
            cnx = get_cnx()
            query = '''delete from memos
                    where id = %s'''

            record = (memo_id,)

            cursor = cnx.cursor()
            cursor.execute(query, record)
            cnx.commit()

        except Error as e:
            print('Error ', e)
            return {'error' : str(e)} , HTTPStatus.BAD_REQUEST
        finally :
            if cnx.is_connected():
                cursor.close()
                cnx.close()
                print('MySQL connection is closed')
        return {'result' : '메모가 성공적으로 삭제되었습니다.'}, HTTPStatus.OK