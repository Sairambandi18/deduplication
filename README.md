# JSON Deduplication Script

This is a command-line Python script designed to clean and process JSON datasets by removing duplicate records based on `_id` and `email`. The script ensures that the most recent record (based on `entryDate`) is retained and generates a log of all changes.

## Installation

Ensure you have **Python 3.x** installed on your system.

To clone this repository, use:
```bash
git clone https://github.com/Sairambandi18/deduplication.git
cd deduplication
```

## Usage

Run the script from the command line:
```bash
python deduplicate.py leads.json deduplicated_leads.json change_log.json
```

### **Parameters:**
- `leads.json` → Input JSON file containing records.
- `deduplicated_leads.json` → Output JSON file with duplicates removed.
- `change_log.json` → Log file showing modifications.

## How It Works
- Loads records from `leads.json` into memory.
- Identifies duplicate records based on `_id` and `email`.
- Retains the latest `entryDate` for duplicate records.
- If multiple records have the same `entryDate`, the last occurrence in the input is retained.
- Outputs a cleaned JSON dataset and logs all modifications.

## Example Output

### **Example Input (`leads.json`):**
```json
{
  "leads": [
    {
      "_id": "123",
      "email": "test@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "entryDate": "2024-01-01T10:00:00+00:00"
    },
    {
      "_id": "123",
      "email": "test@example.com",
      "firstName": "Johnny",
      "lastName": "Doe",
      "entryDate": "2024-01-02T10:00:00+00:00"
    }
  ]
}
```

### **Expected Output (`deduplicated_leads.json`):**
```json
[
  {
    "_id": "123",
    "email": "test@example.com",
    "firstName": "Johnny",
    "lastName": "Doe",
    "entryDate": "2024-01-02T10:00:00+00:00"
  }
]
```

### **Change Log (`change_log.json`):**
```json
[
  {
    "conflict_type": "_id",
    "source_record": { "_id": "123", "email": "test@example.com", "firstName": "John" },
    "output_record": { "_id": "123", "email": "test@example.com", "firstName": "Johnny" },
    "changes": { "firstName": { "from": "John", "to": "Johnny" } }
  }
]
```



