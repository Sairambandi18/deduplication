import json
from datetime import datetime
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['leads']  # Extract the array from under "leads" key

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def deduplicate_records(records):
    by_id = {}  # Track records by _id
    by_email = {}  # Track records by email
    change_log = []  # Log changes during deduplication

    for index, record in enumerate(records):
        # Parse entryDate into a datetime object
        entry_date = datetime.strptime(record['entryDate'], '%Y-%m-%dT%H:%M:%S+00:00')

        current_id = record['_id']
        current_email = record['email']

        # Check for conflicts by _id and email
        existing_by_id = by_id.get(current_id)
        existing_by_email = by_email.get(current_email)

        # Determine which existing record to compare with
        existing = None
        conflict_type = None

        if existing_by_id and existing_by_email:
            # If both _id and email conflict, prefer the one with the newer date
            if existing_by_id['entryDate'] >= existing_by_email['entryDate']:
                existing = existing_by_id
                conflict_type = '_id'
            else:
                existing = existing_by_email
                conflict_type = 'email'
        elif existing_by_id:
            existing = existing_by_id
            conflict_type = '_id'
        elif existing_by_email:
            existing = existing_by_email
            conflict_type = 'email'

        if existing:
            # Compare dates
            existing_date = datetime.strptime(existing['entryDate'], '%Y-%m-%dT%H:%M:%S+00:00')

            if entry_date > existing_date or (entry_date == existing_date and index > records.index(existing)):
                # Log changes
                log_changes(change_log, existing, record, conflict_type)

                # Remove old mappings
                if by_id.get(existing['_id']) == existing:
                    del by_id[existing['_id']]
                if by_email.get(existing['email']) == existing:
                    del by_email[existing['email']]

                # Add new mappings
                by_id[current_id] = record
                by_email[current_email] = record
        else:
            # No conflict, add to both mappings
            by_id[current_id] = record
            by_email[current_email] = record

    # Deduplicated records are the values in by_id (or by_email)
    deduped = list(by_id.values())
    return deduped, change_log

def log_changes(log, old_record, new_record, conflict_type):
    changes = defaultdict(dict)
    for key in new_record:
        if key == 'entryDate':
            old_time = old_record['entryDate']
            new_time = new_record['entryDate']
            if old_time != new_time:
                changes['entryDate'] = {'from': old_time, 'to': new_time}
        elif old_record.get(key) != new_record.get(key):
            changes[key] = {'from': old_record.get(key), 'to': new_record.get(key)}
    
    if changes:
        log.append({
            'conflict_type': conflict_type,
            'source_record': old_record,
            'output_record': new_record,
            'changes': dict(changes)
        })

def main(input_file, output_file, log_file):
    records = load_json(input_file)
    deduped, changes = deduplicate_records(records)
    save_json(deduped, output_file)
    save_json(changes, log_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python deduplicate.py <input_file> <output_file> <log_file>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
