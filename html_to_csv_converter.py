import os
from bs4 import BeautifulSoup
import pandas as pd

def html_table_to_csv(directory_path):
    # Get all HTML files in the directory
    html_files = [f for f in os.listdir(directory_path) if f.endswith('.html')]

    for html_file in html_files:
        file_path = os.path.join(directory_path, html_file)

        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all tables in the HTML
        tables = soup.find_all('table')

        # Check if the file contains any tables
        if not tables:
            print(f'No tables found in {html_file}')
            continue

        # Loop through each table and process it
        for idx, table in enumerate(tables):
            rows = table.find_all('tr')

            # Extract headers (if any)
            headers = [header.text.strip() for header in rows[0].find_all('th')] if rows[0].find_all('th') else None

            # Extract the table data
            data = []
            for row in rows[1:]:
                cells = row.find_all('td')
                data.append([cell.text.strip() for cell in cells])

            # Create a DataFrame from the extracted data
            if headers:
                df = pd.DataFrame(data, columns=headers)
            else:
                df = pd.DataFrame(data)

            # Create output file path
            output_csv_file = os.path.join(directory_path + '/csv', html_file.replace('.html', '.csv'))

            # Save the DataFrame to a CSV file
            df.to_csv(output_csv_file, index=False)
            print(f'Table from {html_file} saved to {output_csv_file}')

if __name__ == '__main__':
    # Change the path to whatever the relative source of the html files is
    directory_path = 'evaluate_roles'
    html_table_to_csv(directory_path)
