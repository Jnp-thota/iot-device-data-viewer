from __future__ import print_function
import json
import pymysql
import os


def lambda_handler(event, context):
    try:
        filters = json.loads(event.get('queryStringParameters', '{}'))
        
        conn = pymysql.connect(
        host=os.environ['DB_ENDPOINT'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor
        )
        
        with conn.cursor() as cursor:
            base_query = """
                SELECT device_id, building_name, floor, zone, room_name, user_notes, room_type
                FROM devices WHERE 1=1
            """
            params = []
            
            # Dynamic filter building
            if filters.get('building'):
                base_query += " AND building_name = %s"
                params.append(filters['building'])
                
            if filters.get('floor'):
                base_query += " AND floor = %s"
                params.append(filters['floor'])
                
            cursor.execute(base_query, params)
            results = cursor.fetchall()
            
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(results)
        }
        
    except Exception as e:
        return {
        "statusCode": 500,
        'headers': {'Access-Control-Allow-Origin': '*'},
        "body": json.dumps({"error": str(e)})
    }