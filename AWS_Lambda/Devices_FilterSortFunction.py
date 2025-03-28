import pymysql
import os
import json

def lambda_handler(event, context):
    try:
        filters = event.get('queryStringParameters', {})
        sort_by = filters.get('sort_by')
        
        # Sort processing
        sort_order = 'ASC' if not sort_by.startswith('-') else 'DESC'
        sort_column = sort_by.lstrip('-')
        
        conn = pymysql.connect(
        host=os.environ['DB_ENDPOINT'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Base query
            query = """
                SELECT device_id, building_name, floor, zone, room_name, user_notes, room_type
                FROM devices WHERE 1=1
            """
            params = []
            
            # Add filters
            if filters.get('building'):
                query += " AND building_name = %s"
                params.append(filters['building'])
                
            if filters.get('floor'):
                query += " AND floor = %s"
                params.append(filters['floor'])
                
            # Add sorting
            query += f" ORDER BY {sort_column} {sort_order}"
            
            cursor.execute(query, params)
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