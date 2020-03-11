# SFCC_ECDN_LOGS_TO_W3C
Tool for converting Salesforce Commerce Cloud CloudFlare eCDN-WAF log to standard W3C log format

SFCC provides multiple ways to generate eCDN-WAF log files. One of the way is to use [OCAPI](https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/Admin/WAF_LogOCAPIReferences.html?) to download these log files.

[W3C log format](https://www.w3.org/TR/WD-logfile.html) is an official standard. These are plain text files.

W3C log format is one of the format which is accepted by SEO log file analyzer like [Screaming Frog](https://www.screamingfrog.co.uk/log-file-analyser/)

## Usage

```python
python3 log_transformer.py -h
usage: log_transformer.py [-h] [-i INPUT] [-o OUTPUT] [-s]

optional arguments:
  -h, --help  show this help message and exit
  -i INPUT    Existing Input directory from which SFCC logs file will be read
  -o OUTPUT   Existing Output directory to which transformed W3C logs will be
              written
  -s          SFCC cache fingerprint will be removed from URL
```

## Screaming Frog Usage

1. Download Screaming Frog Log analyzer from [official site](https://www.screamingfrog.co.uk/log-file-analyser/)
2. Once installed Click "New"
![Create Project](./images/create_project.png)
3. Enter name of the project
![Create Project](./images/project_name.png)
4. Click User-Agent tab & un-check "Filter User Agents"
![Create Project](./images/user_agent_option.png)
5. Once project is created, Click Import > Log File

![Create Project](./images/import_log.png)

6. Select the log files
