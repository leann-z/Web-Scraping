from amazon_scrape import AmazonScraper

def main():
    # MUST download chromedriver for your device and insert path to it below.
    scraper = AmazonScraper('/Users/leannhashishi/Downloads/chromedriver-mac-arm64/chromedriver')
    search_query = input("Enter the product you want to search for: ")
    product_details = scraper.scrape(search_query)
    
    if product_details:
        for i, details in enumerate(product_details):
            print(f"details for item number {i}: {details}\n")
    else:
        print("no details found or error occurred.")

    scraper.close()

if __name__ == "__main__":
    main()
