from flask import Blueprint, send_file
import io
import psycopg2
import os

tracking_bp = Blueprint('tracking', __name__)

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def update_tracking_db(tracking_id, column, value):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE email_tracking SET {column} = %s WHERE tracking_id = %s",
            (value, tracking_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to update database record: {e}")

@tracking_bp.route('/tracking/<tracking_id>')
def track(tracking_id):
    update_tracking_db(tracking_id, "opened", True)  # Update 'opened' status
    # Return a tracking pixel (1x1 transparent GIF)
    gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!' \
                b'\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00' \
                b'\x00\x02\x02D\x01\x00;'
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')


"""from flask import Blueprint, send_file
import os
import io
import psycopg2

tracking_bp = Blueprint('tracking', __name__)
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}



def update_tracking_db(tracking_id, column, value):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE email_tracking SET {column} = %s WHERE tracking_id = %s",
            (value, tracking_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to update database record: {e}")

# Use update_tracking_db in your tracking route
@tracking_bp.route('/tracking/<tracking_id>')
def track(tracking_id):
    update_tracking_db(tracking_id, "opened", True)
    # Return a 1x1 transparent GIF
    gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!...'  # truncated for brevity
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

# Old
@tracking_bp.route('/tracking/<tracking_id>')
def track(tracking_id):
    # Log the open event (update CSV or database)
    # For CSV, you might append a new row or update status
    with open("tracking.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([tracking_id, "OPENED"])
    # Return a 1x1 transparent GIF
    gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

def update_tracking_csv(tracking_id, column, value):
    rows = []
    updated = False
    with open("tracking.csv", "r", newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        for row in reader:
            # Pad row if it's too short
            while len(row) < len(header):
                row.append("")
            if row[4] == tracking_id:
                col_idx = header.index(column)
                row[col_idx] = value
                updated = True
            rows.append(row)
    if updated:
        with open("tracking.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

@tracking_bp.route('/tracking/<tracking_id>')
def track(tracking_id):
    update_tracking_csv(tracking_id, "opened", "yes")
    # Return a 1x1 transparent GIF
    gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!' \
                b'\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00' \
                b'\x00\x02\x02D\x01\x00;'
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')"""