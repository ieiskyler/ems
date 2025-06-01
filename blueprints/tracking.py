from flask import Blueprint, send_file
import csv
import io

tracking_bp = Blueprint('tracking', __name__)


# Old
"""@tracking_bp.route('/tracking/<tracking_id>')
def track(tracking_id):
    # Log the open event (update CSV or database)
    # For CSV, you might append a new row or update status
    with open("tracking.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([tracking_id, "OPENED"])
    # Return a 1x1 transparent GIF
    gif_bytes = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')"""

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
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')