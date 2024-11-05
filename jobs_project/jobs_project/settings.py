BOT_NAME = "jobs_project"

SPIDER_MODULES = ["jobs_project.spiders"]
NEWSPIDER_MODULE = "jobs_project.spiders"



ROBOTSTXT_OBEY = True


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
