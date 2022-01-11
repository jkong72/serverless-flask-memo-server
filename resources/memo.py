from dns.rdatatype import HTTPS
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from mysql.connector.errors import Error
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from MySQL_connection import get_cnx

class MemoListResource(Resource):
    @jwt_required(optional=False) 
    def get(self):
        user_id = get_jwt_identity()
        try:
            cnx = get_cnx()

            # MySQL
            query = '''select * from memos
                        where user_id = %s;'''

            param = (user_id,)
            cursor = cnx.cursor(dictionary = True)
            cursor.execute(query, param)
            record_list = cursor.fetchall()

            # 요청에는 항상 JSON 형식을 통해 응답해야 하며
            # 시간 형식이 JSON 파일과 맞지 않으므로 문자열로 바꾸어주었다.
            i = 0
            for record in record_list:
                record_list[i]['date'] = record['date'].isoformat()
                record_list[i]['created_at'] = record['created_at'].isoformat()
                record_list[i]['updated_at'] = record['updated_at'].isoformat()
                i=i+1

        except Error as e:
            print('Error while connecting to MySQL\n',e) #DB 통신 에러/터미널
            return {'error':str(e)}, HTTPStatus.BAD_REQUEST #DB 통신 에러/응답

        finally :
            cursor.close()
            if cnx.is_connected():
                cnx.close()
                print('MySQL connection is closed')
            else:
                print('connection does not exist')

        # 반환받은 정보를 클라이언트에 응답.
        if len(record_list) == 0:
            return {'result':'현재 작성된 메모가 없습니다.'}, HTTPStatus.OK
        return {'data':record_list}, HTTPStatus.OK

    @jwt_required(optional=False) 
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        try:
            cnx = get_cnx()
                
            #MySQL
            query = '''insert into memos
                    (title, contents, date, user_id)
                    values
                    (%s, %s, %s, %s);'''
        

            record = (
                data['title'],
                data['contents'],
                data['date'],
                user_id)
        

            cursor = cnx.cursor()
            cursor.execute(query, record)
            cnx.commit()

        except Error as e:
            print('Error ', e)
            return {'error':str(e)}, HTTPStatus.BAD_REQUEST
        finally :
            if cnx.is_connected():
                cursor.close()  # 커서 닫음
                cnx.close()     # 연결 닫음

        return {'result': '메모가 작성되었습니다.'}, HTTPStatus.OK