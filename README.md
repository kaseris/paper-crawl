# How to install

Clone the repo

```bash
git clone https://github.com/kaseris/paper-crawl.git
```

Make sure you create a Python virtual environment.

```bash
pip install bs4
pip install scrapy
```

# How to run

_Note_: Variable NAME_OF_CRAWLER can either be Arxiv, IEEE, MDPI
_Note 2_: Variable OUTPUT_FILE_NAME can be a name of your choice.

```bash
cd paper-crawl/arxiv
scrapy crawl NAME_OF__CRAWLER -o OUTPUT_FILE_NAME.json
```