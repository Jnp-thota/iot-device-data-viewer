from __future__ import print_function
import json
import pymysql
import os
import traceback


endpoint = os.environ['DB_ENDPOINT']
username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
database_name = os.environ['DB_NAME']

def lambda_handler(event, context):
    print(event)
    conn = pymysql.connect(host=endpoint,user=username,password=password,db=database_name,cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor() 
    try:
        http_method = event.get('httpMethod')
        path = event.get('resource')

        if http_method == 'POST' and path == '/devices':
            # Add a new device
            new_device = json.loads(event.get('body'))
            try:
            # Ensure the new device has the required attributes
                required_fields = ['device_id', 'building_name', 'floor', 'zone', 'room_name', 'user_notes', 'room_type']
                for field in required_fields:
                    if field not in new_device:
                        return {
                            'statusCode': 400,
                            'headers': {
                                'Access-Control-Allow-Origin': '*'
                            },
                            'body': json.dumps({'message': f'Missing required field: {field}'})
                    }
            
                cursor.execute("""
                INSERT INTO devices (device_id, building_name, floor, zone, room_name, user_notes, room_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (new_device['device_id'], new_device['building_name'], new_device['floor'], new_device['zone'], new_device['room_name'], new_device['user_notes'], new_device['room_type']))
                conn.commit()

                return {
                'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Device added successfully'})
                }
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                print("Error:", error_message)
                print("Traceback:", traceback.format_exc())
                return {
                'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
                'body': json.dumps({'message': error_message, 'traceback': traceback.format_exc()})
                }
        elif http_method == 'DELETE' and path == '/devices/{device_id+}':
            device_id = event.get("pathParameters", {}).get("device_id")
            cursor.execute("DELETE FROM devices WHERE device_id = %s", (device_id,))
            if cursor.rowcount > 0:  # Check if a row was affected
                conn.commit()
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'message': 'Device deleted successfully'})
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'message': 'Device not found'})
                }
        else:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'message': 'Invalid operation none of previous conditions satisfied {http_method}, {path}'})
            }

    except Exception as e:
        # Log the full exception details
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        print("Traceback:", traceback.format_exc()) 
        return {
            'statusCode': 500,
            'body': json.dumps({'message': error_message, 'traceback': traceback.format_exc()})  
        }
