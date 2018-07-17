

scrapy crawl EastMoney
scrapy crawl PSR


python orderfile.py EastMoney.json EastMoney.tmp code
python orderfile.py psr.json psr.tmp code


python PSRprocess.py EastMoney.tmp psr.tmp result.txt


python application.py result.txt 


rem del EastMoney.json 
rem del EastMoney.tmp
rem del psr.json
rem del psr.tmp
