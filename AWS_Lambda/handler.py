from __future__ import print_function
import json
import pymysql
import os
import traceback


endpoint = os.environ['DB_ENDPOINT']
username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
database_name = os.environ['DB_NAME']

conn = pymysql.connect(host=endpoint,user=username,password=password,db=database_name,cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor() 

def lambda_handler(event, context):
    print(event)
    cursor = conn.cursor()
    try:
        http_method = event.get('httpMethod')
        path = event.get('resource')


        if http_method == 'GET' and path == '/devices':
            cursor.execute("""
                SELECT device_id, building_name, floor, zone, room_name, user_notes, room_type
                FROM devices
            """)
            result = cursor.fetchall()
            if result:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(result)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'message': 'Zero Devices found'})
                }

        elif http_method == 'GET' and path == '/devices/{device_id+}':
            device_id = event.get("pathParameters", {}).get("device_id")
            cursor.execute("""
                SELECT device_id, building_name, floor, zone, room_name, user_notes, room_type
                FROM devices
                WHERE device_id = %s
            """, (device_id,))
            result = cursor.fetchone()
            if result:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(result)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'message': 'Device not found'})
                }

        elif http_method == 'GET' and path == '/devices/time-series-data/{device_id+}':
            # Fetch time-series data
            device_id = event.get("pathParameters", {}).get("device_id")
            # print(event.get("queryStringParameters",{}))
            # print("Data")
            # print(event.get("queryStringParameters"))
            # print(event.get("queryStringParameters", {})!=None)
            if(event.get("queryStringParameters", {})!=None):
                start_time = event.get("queryStringParameters", {}).get("start_time")
                end_time = event.get("queryStringParameters", {}).get("end_time")
                cursor.execute("""
                    SELECT timestamp, metric_value
                    FROM time_series_data
                    WHERE device_id = %s AND timestamp BETWEEN %s AND %s
                    ORDER BY timestamp
                """, (device_id, start_time, end_time))
            else:
                cursor.execute("""
                    SELECT timestamp, metric_value
                    FROM time_series_data
                    WHERE device_id = %s
                    ORDER BY timestamp
                """, (device_id,))
            results = cursor.fetchall()
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(results, default=str)
            }
        elif http_method == 'POST' and path == '/devices':
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

        elif http_method == 'PUT' and path == '/devices/{device_id+}':
            # Update device attributes
            device_id = event.get("pathParameters", {}).get("device_id")
            updates = json.loads(event.get('body'))
            print(updates)
            set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
            values = list(updates.values())
            values.append(device_id)
            sql = f"""
                UPDATE devices
                SET {set_clause}
                WHERE device_id = %s
            """
            cursor.execute(sql, values)
            conn.commit()
            return {
                'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
                'body': json.dumps({'message': 'Device updated successfully'})
            }

        else:
            return {
                'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
                'body': json.dumps({'message': 'Invalid operation none of previous conditions satisfied {http_method}, {path}'})
            }

    except Exception as e:
        # Log the full exception details
        error_message = f"An error occurred: {str(e)}"
        print("Error:", error_message)
        print("Traceback:", traceback.format_exc())  # Log the full traceback
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': error_message, 'traceback': traceback.format_exc()})  
        }
