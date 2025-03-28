import pymysql
import os
import json

def lambda_handler(event, context):
    try:
        conn = pymysql.connect(
        host=os.environ['DB_ENDPOINT'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Get building distribution
            cursor.execute("""
                SELECT building_name, COUNT(*) as device_count
                FROM devices
                GROUP BY building_name
            """)
            buildings = cursor.fetchall()
            
            # Get floor distribution
            cursor.execute("""
                SELECT floor, COUNT(*) as device_count
                FROM devices
                GROUP BY floor
            """)
            floors = cursor.fetchall()
            
            # Get device types
            cursor.execute("""
                SELECT room_type, COUNT(*) as device_count
                FROM devices
                GROUP BY room_type
            """)
            types = cursor.fetchall()
            
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'buildings': buildings,
                'floors': floors,
                'room_types': types
            })
        }
        
    except Exception as e:
        return {
        "statusCode": 500,
        'headers': {'Access-Control-Allow-Origin': '*'},
        "body": json.dumps({"error": str(e)})
    }