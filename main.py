from requests import get
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

def fetch(url, headers):
    resp = get(url, headers=headers)
    while resp.status_code != 200:
        print(resp.status_code)
        resp = get(url, headers=headers)
    
    return resp.text

def scrape(html, data):
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all(data["products"][0], data["products"][1])
    
    results = []
    
    for product in products:
        name = product.find(data["name"][0], data["name"][1])
        price = product.find(data["price"][0], data["price"][1])
        link = product.find("a", href=True)
        
        if not (name and price and link):
            continue
        
        results.append({
            "name": name.text,
            "price": price.text,
            "link": link["href"],
            "source": data["source"]
        })
    
    return results

def get_results(url_prefix, query, data):

    url = url_prefix + query
    html = fetch(url, headers)
    
    results = scrape(html, data)
    
    return results

def get_amazon_results(query):
    url_prefix = "https://www.amazon.in/s?k="
    data = {
        "products": [
            "div",
            {"class": "s-result-item"}
        ],
        "name": [
            "span",
            "a-text-normal"
        ],
        "price": [
            "span",
            "a-offscreen"
        ],
        "source": "Amazon"
    }
    
    return get_results(url_prefix, query, data)

def get_snapdeal_results(query):
    url_prefix = "https://www.snapdeal.com/search?keyword="
    data = {
        "products": [
            "div",
            {"class": "product-tuple-listing"}
        ],
        "name": [
            "p",
            "product-title"
        ],
        "price": [
            "span",
            "product-price"
        ],
        "source": "Snapdeal"
    }
    
    return get_results(url_prefix, query, data)

def int_extractor(string):
    int_string = ""
    
    for ch in string:
        if ch == "." and len(int_string):
            break
        
        if ch.isdigit():
            int_string += ch

    return int(int_string)

def main():
    query = input("Please enter the product you want to purchase: ")
    results = []
    
    results.extend(get_amazon_results(query))
    results.extend(get_snapdeal_results(query))
    
    results.sort(key=lambda p: int_extractor(p["price"]))
    
    for product in results:
        name = product["name"][:30]
        price = int_extractor(product["price"])
        source = product["source"]
        print(f"{name:<30} - Rs. {price:,} ({source})")

main()

