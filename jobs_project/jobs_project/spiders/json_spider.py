import json
import scrapy
from jobs_project.items import JobsProjectItem


class JobSpider(scrapy.Spider):
    name = "job_spider"
    custom_settings = {
        "ITEM_PIPELINES": {
            "jobs_project.pipelines.PostgreSQLPipeline": 300,
            "jobs_project.pipelines.RedisPipeline": 400,
        },
    }

    def __init__(self, **kwargs):
        self.json_paths = ["app/data_source/s01.json", "app/data_source/s02.json"]
        pass
        super().__init__(**kwargs)

    def start_requests(self):
        for json_path in self.json_paths:
            url = f'file:///{json_path}'
            yield scrapy.Request( url=url, callback=self.parse_page)

    def parse_page(self, response):
        """
        Parse json response and yield items
        """
        data = json.loads(response.text)
        jobs = data["jobs"]

        for job in jobs:
            job_data = job.get("data")
            item = JobsProjectItem()
            create_item(item, job_data)
            yield item


def create_item(item, job_data):
    """
    Create item from job_data by
    - copying the key value pair from job_data to item
    - inspecting data type and converting to string
    - cleaning the string
    - marking NULL values with NA
    """
    for key in job_data:
        value = job_data.get(key)
        if isinstance(value, str):
            item[key] = clean_string(value)
        elif isinstance(value, list):
            if len(value) == 0:
                item[key] = "NA"
            else:
                convert_with_type_check = lambda item: (
                    ", ".join(list(item.values()))
                    if isinstance(item, (dict))
                    else clean_string(str(item))
                )
                str_value = ", ".join(convert_with_type_check(item) for item in value)
                item[key] = str_value
        elif isinstance(value, dict):
            item[key] = ", ".join(list(item.values()))
        else:
            item[key] = str(value)


def clean_string(value):
    """
    - Remove special characters from string
    - Remove - from string
    - Remove leading and trailing whites
    - remove all special character not accepted by sql
    """
    return value.replace("'", "").replace('"', "").replace("-", "").strip()
