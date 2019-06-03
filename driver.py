from fboscraper import FedBizOpps


def main():
    scope='both'
    naics_codes = ['54151', '541511', '541512', '541519', '518']
    posted_range_start = '2013-03-01'
    posted_range_end = '2014-03-01'
    procurement_type=['combined_synopsis_solicitation', 'fair_opportunity_limited', 'presolicitation', 'modification_amendment_cancel', 'sources_sought']

    biz_ops = FedBizOpps(scope=scope,
                         naics_codes=naics_codes,
                         posted_range_start=posted_range_start,
                         posted_range_end=posted_range_end,
                         procurement_type=procurement_type)

    biz_ops.scrape_opportunities()
    biz_ops.export_to_csv()


if __name__ == '__main__':
    main()
