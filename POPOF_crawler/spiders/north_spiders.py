from scrapy.spider import Spider
from scrapy.selector import Selector

from POPOF_crawler.items import PopofItem

class NorthSpider(Spider):

    name = "north"

    start_urls = [
        "http://www.fnpn.gov.tw/ct/CFT.php?page=CFTBidInfo&area=N000&CFT_ID=1038"
    ]

    def __init__(self,*args, **kwargs):
        super(NorthSpider, self).__init__(*args, **kwargs)

        pass

    def parse(self, response):

        def extract_div_data(td):
            return td.xpath("div/text()").extract()[0].encode('utf-8')

        def extract_span_data(td):
            return td.xpath("span/text()").extract()[0].encode('utf-8')

        def extract_div_span_data(td):
            return td.xpath("div/span/text()").extract()[0].encode('utf-8')

        sel = Selector(response)

        # catch all tr tag of this table
        tr_list = sel.xpath("//table[@class='table-border-yellow']/tr")

        tr_list_len = len(tr_list)

        items = []

        for index in range(1, tr_list_len):
            item = PopofItem()

            tds = tr_list[index].xpath('td')

            td_count = len(tds)

            # need to pass some fiels if it's rowspan
            if td_count == 3:
                item['addr'] = extract_div_data(tds[0])
                item['area'] = extract_div_data(tds[1])
                item['category'] = extract_span_data(tds[2])

                prev_item = items[-1]

                item['security_deposits'] = prev_item['security_deposits']
                item['notes'] = prev_item['notes']
                item['stop'] = prev_item['stop']
            else:
                item['addr'] = extract_div_data(tds[1])
                item['area'] = extract_div_data(tds[2])
                item['category'] = extract_span_data(tds[3])
                item['price'] = extract_span_data(tds[4])
                item['security_deposits']  = extract_span_data(tds[5])
                item['notes'] = extract_span_data(tds[7])
                item['stop'] = extract_div_span_data(tds[8])

            items.append(item)
            pass

        return items
        pass
