import pymysql
import os
import json

def lambda_handler(event, context):
    print(event)
    try:
        # page = int(event.get('queryStringParameters', {}).get('page', 1))
        # page_size = int(event.get('queryStringParameters', {}).get('page_size', 10))
        
        conn = pymysql.connect(
        host=os.environ['DB_ENDPOINT'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Get paginated results
            query = """
            SELECT device_id, building_name, floor, zone, room_name, user_notes, room_type
            FROM devices
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Get total count for pagination metadata
            cursor.execute("SELECT COUNT(*) FROM devices")
            total_count = cursor.fetchone()['COUNT(*)']
            

            
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