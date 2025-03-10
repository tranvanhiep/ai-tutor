import csv
from typing import Dict, List


class CSVReader:
    """A utility class to read CSV files into dictionaries."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_to_dict(self) -> List[Dict]:
        """
        Reads a CSV file and returns a list of dictionaries.
        Empty item_ids are filled with the previous valid item_id.
        """
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                original_rows = list(csv_reader)

                # Fill empty item_ids into temp_rows
                temp_rows = []
                previous_id = None
                for row in original_rows:
                    # Create a new dict to avoid modifying original row
                    new_row = row.copy()
                    if not new_row['item_id'].strip():
                        if previous_id is None:
                            raise ValueError("First row cannot have empty item_id")
                        new_row['item_id'] = previous_id
                    else:
                        previous_id = new_row['item_id']
                    temp_rows.append(new_row)

                # Count occurrences of each item_id
                item_id_counts = {}
                for row in original_rows:
                    item_id = row['item_id']
                    item_id_counts[item_id] = item_id_counts.get(item_id, 0) + 1

                # Group by item_id and fill data
                item_descriptions = {}
                correct_options = {}
                for row in temp_rows:
                    item_id = row['item_id'].strip()
                    if row['item_description'] and item_id not in item_descriptions:
                        item_descriptions[item_id] = row['item_description']
                    if row['correct_option'].upper() == 'TRUE':
                        correct_options[item_id] = row['options']

                # Create final list with processed data
                processed_rows = []
                for row in original_rows:
                    item_id = row['item_id'].strip()
                    if bool(item_id):
                        processed_rows.append({
                            'question': row['question_content'] if (
                                item_id_counts[item_id] > 1 or
                                not row['item_description'].strip()
                            ) else '',
                            'answer': correct_options.get(item_id),
                            'item_id': item_id,
                            'item_description': (
                                item_descriptions.get(item_id) or
                                row['item_description']
                            ),
                            'explanation': row['explanation']
                        })

                return processed_rows

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {self.filepath}")
        except ValueError as e:
            raise ValueError(f"Error processing CSV data: {str(e)}")
        except IOError as e:
            raise IOError(f"Error reading CSV file: {str(e)}")

    def read_to_dict_with_key(self, key_column: str) -> Dict:
        """
        Reads a CSV file and returns a dictionary where a specified column
        becomes the key for each row dictionary.
        """
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                return {row[key_column]: row for row in csv_reader}
        except KeyError:
            raise KeyError(f"Column '{key_column}' not found in CSV file")
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {self.filepath}")
        except IOError as e:
            raise IOError(f"Error reading CSV file: {str(e)}")
