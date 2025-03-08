import csv
from typing import Dict, List


class CSVReader:
    """A utility class to read CSV files into dictionaries."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_to_dict(self) -> List[Dict]:
        """
        Reads a CSV file and returns a list of dictionaries.
        If item_id is unique among rows, question will be empty.
        If item_id appears multiple times, question will be question_content.
        """
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                rows = list(csv_reader)

                # Count occurrences of each item_id
                item_id_counts = {}
                for row in rows:
                    item_id = row['item_id']
                    item_id_counts[item_id] = item_id_counts.get(item_id, 0) + 1

                # Group by item_id and fill data
                item_descriptions = {}
                correct_options = {}
                for row in rows:
                    item_id = row['item_id']
                    if row['item_description'] and item_id not in item_descriptions:
                        item_descriptions[item_id] = row['item_description']
                    if row['correct_option'].upper() == 'TRUE':
                        correct_options[item_id] = row['options']

                # Create final list with processed data
                processed_rows = []
                for row in rows:
                    item_id = row['item_id']
                    if bool(item_id.strip()):
                        processed_rows.append({
                            'question': row['question_content'] if item_id_counts[item_id] > 1 else '',
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
