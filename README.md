## Project Overview

This project analyzes user engagement across 24 Armenian news YouTube channels, focusing on metrics such as views, ratings, and upload frequency. The goal is to understand how audiences consume news content on YouTube and identify trends in engagement patterns. The analysis was conducted using data scraped from YouTube channels, stored in an SQL database, and processed with Python.

## Repository Structure

- **`Armenian News YouTube Channel Activity Analysis.pdf`**: The final report detailing the analysis, findings, and visualizations.
- **`youtube_scraping.py`**: Script for scraping data from YouTube channels.
- **`database_insertion.py`**: Script for inserting scraped data into the SQL database.
- **`data_vizualization.py`**: Script for generating visualizations from the analyzed data.
- **`youtube_database.sql`**: SQL file containing the database schema and queries used for analysis.
- **`XML Files/`**: Directory containing scraped data in XML format.
- **`README.md`**: This file, providing an overview of the project.

## Key Features

- **Data Collection**: Custom scripts scrape publicly available data from YouTube channels, including views, ratings, and publication dates.
- **Database Management**: Data is stored in an SQL database with two main tables:
  - `youtube_channels`: Metadata about each channel.
  - `videos`: Detailed records of each video, including engagement metrics.
- **Analysis**: SQL and Python are used to analyze trends in views, ratings, and upload frequency.
- **Visualizations**: Graphs and charts illustrate key findings, such as average views per channel, correlation between views and ratings, and view growth over time.


## How to Use This Repository

1. **Data Scraping**:
   - Run `youtube_scraping.py` to collect data from YouTube channels. Ensure you update the script with your individual paths as noted in the comments.

2. **Database Setup**:
   - Use `youtube_database.sql` to set up the database schema. The script includes all necessary tables and queries for analysis. Create the tables first by running the appropriate query, then use Python code for insertion.

3. **Data Insertion**:
   - Run `database_insertion.py` to insert scraped data into the database. Update the script with your database connection details.

4. **Data Visualization**:
   - Execute `data_vizualization.py` to generate visualizations. Customize the script to reflect your data paths and preferences.

## Dependencies

Here’s the updated **Dependencies** section for your `README.md` with the full list of libraries. I’ve organized them by purpose and removed duplicates (like `matplotlib.pyplot` and `ElementTree` listed twice):

---

- Python 3.x
- Libraries: `psycopg2` (for PostgreSQL), `pandas`, `matplotlib`, `sqlalchemy`, `os`, `pathlib`, `datetime`, `numpy`, `re`, `requests`,  `BeautifulSoup` (from `bs4`), `xml.etree.ElementTree`  
- PostgreSQL database


## Conclusion

This project provides valuable insights into how Armenian news content performs on YouTube, highlighting successful strategies and areas for improvement. The repository includes all necessary scripts and documentation to replicate or extend the analysis.

For questions or further details, refer to the full report in `Armenian News YouTube Channel Activity Analysis.pdf`.
