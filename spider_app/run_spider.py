import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from os import getenv
class RunSpider():
    def __init__(self,form) -> None:
        #init value from the input form
        self.form = form
        self.sheet_domains_name = "Domains to scrap"
        self.brand_links_max = self.form['brand_max']
        self.network_links_max = self.form['network_max']
        self.all_links_max = self.form['result_max']
        self.spider_mode = self.form['mode']
        self.start_row = int(self.form['start_row'])
        self.end_row = int(self.form['end_row'])
        self.initials_spider_name = self.form['spider_name']
        self.spider_name = "".join(["peter_parker_external_links" if self.initials_spider_name == "PP" else "mary_jane_emails"])

        #load external .json files with sensitive data
        if os.path.isfile('spider_app/resources/avian-sunlight-332621-74eb679c388d.json'):
            self.spider_list = json.load(open('spider_app/resources/spider_list.json'))
            self.ref_spreadsheets = json.load(open('spider_app/resources/spreadsheets_reference.json'))
        else:
            self.ref_spreadsheets = json.loads(getenv('REF_SPREADSHEETS'))
            self.spider_list = json.loads(getenv('SPIDER_LIST'))

        #get spreadsheet ID and campaign name
        self.spreadsheet_id = self.get_spread_info("id_sheet")
        self.campaign_name = self.get_spread_info("campaign_name")
        #get more info depending on "mode : Test/Prod" and "spider_name : MJ/PP"
        self.project = self.get_spider_info('project')
        self.sheet_links = self.get_spider_info('sheet_links')
        self.sheet_emails = self.get_spider_info('sheet_emails')
        self.apikey = self.get_spider_info('apikey')
        
       #sheet domain is the sheet where the inputs come from
        self.client = self.init_auth_gsheet()
        
        self.sheet_domains = self.client.open_by_key(self.spreadsheet_id).worksheet(self.sheet_domains_name)
        self.header_domains = [column_name for column_name in self.sheet_domains.row_values(2) if column_name]

        self.init_sheet_domain()

    def init_auth_gsheet(self):
         #init gspread authorization
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']

        if os.path.isfile('spider_app/resources/avian-sunlight-332621-74eb679c388d.json'):
            with open('spider_app/resources/avian-sunlight-332621-74eb679c388d.json') as f:
                local_key_file = f.read()
        else:
            local_key_file = ""

        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(getenv('GSPREAD_KEY',local_key_file)), scope)
        return gspread.authorize(creds)

    def get_spider_info(self,info):
        return "".join([str(spider[info]) for spider in self.spider_list if spider['mode'] == self.spider_mode and spider['name'] == self.initials_spider_name])

    def get_spread_info(self, info):
        return "".join([spread[info] for spread in self.ref_spreadsheets if spread["value_html"] == self.form['name_spread']])

    def get_data_from_sheets_domains(self,header_col,row):
        return self.sheet_domains.cell(row,self.header_domains.index(header_col)+1).value

    def init_sheet_domain(self):
        for row in range(self.start_row,self.end_row):
            
            self.data = {
                'project': self.project,
                "raw_domain": self.get_data_from_sheets_domains('domain',row),
                'spider': self.spider_name,
                "dest_spread": self.spreadsheet_id,
                "sheet_domains": self.sheet_domains_name,
                "count_brands": self.brand_links_max,
                "count_networks": self.network_links_max,
                "count_global": self.all_links_max,
                "campaign_name" : self.campaign_name,
            }

            if self.initials_spider_name == "MJ":
                self.data['start_urls'] = self.get_data_from_sheets_domains('start_url',row)
                self.data["sheet_emails"] = self.sheet_emails
            else:
                self.data["sheet_links"] = self.sheet_links

            url = 'https://app.scrapinghub.com/api/run.json?apikey='+ str(self.apikey)
            headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
            }
            response = requests.post(url,data=self.data, headers=headers)
    
if __name__ == '__main__':
    RunSpider()