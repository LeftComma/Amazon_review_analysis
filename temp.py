import re
import pandas as pd

url = 'https://www.amazon.co.uk/LEGO-42123-Technic-Collectible-Construction/dp/B08G4293BD/ref=sr_1_1?crid=1SDTYPYXM70YV&keywords=lego&qid=1636379951&refinements=p_89%3Alego&rnid=1632651031&s=kids&sprefix=my+li%2Ctoys%2C163&sr=1-1'


def build_review_url(url):  # Turn a regular review into a product review
    # Replace default page with product reviews
    review_url = url.replace('dp', 'product-reviews')

    # Strip everything off the review before a particular expression, and then add on a different ending
    review_url = re.split('/ref=', review_url)[0] + \
        '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber='
    return review_url


url = build_review_url(url)

df = pd.read_excel('product_urls.xlsx', header=0,
                   index_col=0)

product_urls = df['url'].values.tolist()
print(product_urls[0])
