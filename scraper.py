import requests
from bs4 import BeautifulSoup
import json


#product_code = input("Please enter the product code: ")
product_code = "129910940"
print(product_code)

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"


#def get(dom, sel):
#    return dom.select_one(sel)

#def get_stripped_element_checked(dom, sel):
#    el = get_element(dom, sel)
#    return el.text.strip() if el else None

#def get_stripped_element(dom, sel):
#    return get_element(dom, sel).text.strip()

def get_element(dom, sel = None, attribute = None):
    try:
        if attribute:
            if sel:
                return dom.select_one(sel)[attribute].strip()
            
            return dom[attribute]
        
        return dom.select_one(sel).text.strip()
    except (AttributeError, TypeError):
        return None


all_opinions = []

while url:
    response = requests.get(url)
    print("2222")
    print(url)
    if response.status_code == requests.codes.ok:   
        page_dom = BeautifulSoup(response.text, "html.parser")
        opinions = page_dom.select("div.js_product-review")
    
        if len(opinions)>0:
            print(f"There are opinions about procudt with {product_code} code.")
            

            for opinion in opinions:
                opinion_id = opinion["data-entry-id"]
                author = get_element(opinion, "span.user-post__author-name")
                
                recommendation = get_element(opinion, "span.user-post__author-recomendation > em")
                
                
                score = get_element(opinion, "span.user-post__score-count")
                description = get_element(opinion, "div.user-post__text")
            
                pros = opinion.select("div.review-feature__col:has( > div.review-feature__title--positives)> div.review-feature__item")
                pros = [p.text.strip() for p in pros]
                cons = opinion.select("div.review-feature__col:has( > div.review-feature__title--negatives)> div.review-feature__item")
                cons = [c.text.strip() for c in cons]

                like = get_element(opinion, "span[id^=votes-yes]")

                dislike = get_element(opinion, "span[id^=votes-no]")

                publish_date = get_element(opinion, "span.user-post__published > time:nth-child(1)", "datetime")
              
                purchase_date = get_element(opinion, "span.user-post__published > time:nth-child(2)", "datetime")
                
                single_opinion = {
                    "opinion_id" : opinion_id,
                    "author" : author,
                    "recommendation": recommendation,
                    "score": score,
                    "description": description,
                    "pros": pros,
                    "cons": cons,
                    "like": like,
                    "dislike": dislike,
                    "publish_date": publish_date,
                    "purchase_date": purchase_date


                }

                all_opinions.append(single_opinion)
            
            next_page = get_element(page_dom, "a.pagination__next", "href")
            url = f"https://ceneo.pl/{next_page}"

            print(url)

        else:
            print(f"There are no opinions about procudt with {product_code} code.")
            url = None

    else:
        print("The product does not exist")

if len(all_opinions) > 0:
    with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions,jf, indent=4, ensure_ascii=False)