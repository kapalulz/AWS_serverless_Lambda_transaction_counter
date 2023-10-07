import boto3
import csv
import io
import json
import logging
from collections import defaultdict

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Categories and keywords
categories_and_keywords = {
    "Stores": ["COSTCO", "TARGET", "MARKET BASKET", "CVS", "PHARMACY", "WAL-MART", "CONVENIENCE", "STORE", "WINE"],
    "Gas": ["GAS", "PRESTIGE", "CAR", "GULF", "EXXON", "HOLBROOK", "VIOC AB1137 BROCKTON MA", "PRESTIGE"],
    "FastFood": ["MCDONALDS","APPLESEED", "SWEET", "BURGER KING", "STEAK", "STARBUCKS", "DUNKIN", "JAPAN", "WOK", "UNOCHICAGOGRILL#227", "KAM", "STEAK", "POPEYES", "DOMINO", "SIP", "SWEET", "SUSHI", "THAI", "SteakSalem", "TOKYO", "HIBACHI", "PIZZERIA"],
    "Makeup": ["ULTA", "SEPHORA", "LUSH"],
    "IKEA": ["IKEA", "PRIMARK"],
    "FUN": ["ZOO", "EXAM", "SMOKER", "BARBERING", "TRAINING", "ARCADE", "BABY", "VAEP"]
}

def process_csv_file(file_content):
    # Initialize category totals
    category_totals = defaultdict(float)

    try:
        decoded_content = file_content.decode('utf-8')
        file_data = io.StringIO(decoded_content)
        reader = csv.reader(file_data)
        next(reader)  # Skip the header if present
        for row in reader:
            if len(row) >= 6:
                description = row[2]
                amount = row[3]

                matched_category = "Other"  # Default category if no match is found

                # Check if any keyword in the file matches a category
                for category, keywords in categories_and_keywords.items():
                    for keyword in keywords:
                        if keyword in description.upper():
                            matched_category = category
                            break

                try:
                    amount = float(amount)
                    category_totals[matched_category] += amount
                except ValueError:
                    logger.error(f"Invalid amount format for record: {description}")

        return category_totals
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return None

def get_word_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        word_content = response['Body'].read()
        return word_content.decode('utf-8')
    except Exception as e:
        logger.error(f"Error reading word.txt from S3: {str(e)}")
        return ""

def count_occurrences(file_content, word_to_search):
    word_count = 0
    transactions_total_amount = 0
    try:
        decoded_content = file_content.decode('utf-8')
        sentences = decoded_content.split('.')  # Assume sentences are separated by periods

        for sentence in sentences:
            if word_to_search in sentence.upper():  # Search for the keyword in uppercase
                word_count += 1

        file_data = io.StringIO(decoded_content)
        reader = csv.reader(file_data)
        next(reader)  # Skip the header if present
        for row in reader:
            if len(row) >= 6:
                description = row[2]
                amount = row[3]

                if word_to_search in description.upper():  # Search for the keyword in transaction description
                    try:
                        amount = float(amount)
                        transactions_total_amount += amount
                    except ValueError:
                        logger.error(f"Invalid amount format for record: {description}")

        return word_count, transactions_total_amount
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return 0, 0

def calculate_category_percentages(category_totals):
    total_amount = sum(category_totals.values())
    category_percentages = {}

    for category, amount in category_totals.items():
        percentage = (amount / total_amount) * 100
        category_percentages[category] = percentage

    return category_percentages

def lambda_handler(event, context):
    try:
        s3_bucket = 'game-saves-kapalulz'  # Replace with your S3 bucket name
        s3_key_word = 'word.txt'  # Replace with your S3 file name
        s3_key_transactions = 'Yeartodate.CSV'  # Replace with your S3 transaction file name

        # Read the word from the file in S3
        search_word = get_word_from_s3(s3_bucket, s3_key_word)

        # Read transactions from the file in S3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=s3_bucket, Key=s3_key_transactions)
        transactions_content = response['Body'].read()

        # Count occurrences of the keyword and transactions in the file
        word_count, transactions_total_amount = count_occurrences(transactions_content, search_word)

        # Process the CSV file considering categories
        category_totals = process_csv_file(transactions_content)

        if category_totals is not None:
            category_percentages = calculate_category_percentages(category_totals)
            response_body = {
                "word_content": search_word,
                "transactions_count": word_count,
                "transactions_total_amount": transactions_total_amount,
                "category_totals": category_totals,
                "category_percentages": category_percentages  # Add category percentages to the response
            }
        else:
            response_body = {
                "word_content": search_word,
                "transactions_count": word_count,
                "transactions_total_amount": transactions_total_amount,
                "category_totals": {},
                "category_percentages": {}
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Allow CORS
            },
            "body": json.dumps(response_body)
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Allow CORS
            },
            "body": json.dumps({"error": str(e)})
        }

        return response
