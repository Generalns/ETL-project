## Setup Process

* First of all make sure you have docker and docker compose installed on your computer.
* Download the .zip file of the project source code and extract it or clone the repository with the following command:
```python
git clone [url]
```
* Run the following command:
```python
docker-compose up --build
```

## PostgreSQL and Redis Access
### PostgreSQL Access
* In order to access the PostgreSQL ssh into postgresql service and in the terminal and enter the following commands:
```python
* psql -U postgres
* psql \c jobs_project
* SELECT COUNT(title) FROM raw_table;
```
This will give you the number of records. After entering the first two commands you can query and sql statement you want.

### Redis Access

* In order to access the Redis ssh into redis service and in the terminal and enter the following commands:
```python
* redis-cli
* KEYS *
```
This will give you all the keys of the cached elements.


## Pipeline Process

The pipeline process in this project is designed to extract, transform, and load (ETL) data from a JSON file into a PostgreSQL database, allowing for further analysis and retrieval. The pipeline consists of multiple components that work together to ensure efficient data processing.

#### 1. **Data Extraction**

-   The first step of the pipeline involves extracting data from a JSON file. This is handled by a Scrapy spider, specifically `json_spider.py`, which is responsible for reading the JSON data and extracting relevant fields.
-   The spider is configured to parse the JSON structure, identify the required data points, and yield items that represent structured data records.

#### 2. **Data Caching with Redis**

-   To prevent duplicate processing of items that have already been scraped, Redis is used as an in-memory caching layer.
-   Before inserting a newly scraped item into the PostgreSQL database, the spider checks Redis to see if the item (or a unique identifier associated with it) already exists in the cache.
-   If the item is found in Redis, it is skipped, thus avoiding unnecessary database writes and ensuring that only new or updated items are processed.

#### 3. **Data Transformation**

-   After extraction, the data may require transformation to ensure it fits the schema of the target PostgreSQL database. This includes formatting date fields, and ensuring data types match the database requirements.

#### 4. **Data Loading**

-   Once the data is transformed, it is loaded into a PostgreSQL database. This is done using the `psycopg2` library, which allows Python to interact with the PostgreSQL database.
-   The data loading process involves establishing a connection to the database, creating the necessary tables (if they do not exist), and inserting the extracted records into the appropriate table.

#### 5. **Data Retrieval and Storage**

-   The processed data can be retrieved from the PostgreSQL database for further analysis or reporting. The `query.py` script includes functionality to fetch data from specified tables and save it as a CSV file.
-   This output file can be used for external reporting or as input for other data processing tasks.

#### 6. **Dockerization and Deployment**

-   The entire pipeline process is containerized using Docker. This ensures that the application runs consistently across different environments. The Dockerfile specifies the necessary dependencies, including Python libraries and PostgreSQL drivers.

#### 7. **Execution Flow**

-   The pipeline is initiated by running the Scrapy spider, which extracts data from the JSON file.
-   Upon successful extraction, the spider triggers the data loading process into the PostgreSQL database.
-   Finally, the `query.py` script can be executed to retrieve the data and save it to a CSV file, ensuring the processed data is readily available for analysis.