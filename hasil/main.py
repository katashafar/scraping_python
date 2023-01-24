import requests
import json
import pandas as pd
  
cari = "cardfight"
url = "https://gql.tokopedia.com/graphql/searchFeedbackQuery"
def get_params():
    params = []
    for i in range(1, 19):
      param = "device=desktop&ob=23&page={}&q={}%20vanguard%20deck&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&st=product&start={}&topads_bucket=true&unique_id=0ed1fcf4c09246b8da2e8be3edf28d8f&user_addressId=24923390&user_cityId=151&user_districtId=1732&user_id=17828771&user_lat=&user_long=&user_postCode=16810&user_warehouseId=0&variants=". format(i, cari, (i -1)*60)      
      params.append(param)
    return params

def scrap_data(param):
    payload = [{
        "operationName": "SearchProductQueryV4",
        "variables": {
            "params": param
        },
        "query": "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      banner {\n        position\n        text\n        imageUrl\n        url\n        componentId\n        trackingOption\n        __typename\n      }\n      backendFilters\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        customVideoURL\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}]

    req = requests.post(url, json=payload).json()
    rows = req[0]["data"]["ace_search_product_v4"]["data"]["products"]
    scrap_data =[]
    for i in range(0, len(rows)):
        no = i
        nama_produk = rows[i]["name"]
        harga = rows[i]["price"]
        rating = rows[i]["ratingAverage"]
        toko = rows[i]["shop"]["name"]
        lokasi = rows[i]["shop"]["city"]
        link_toko = rows[i]["shop"]["url"]
        scrap_data.append(
            (no, nama_produk, harga, rating, toko, lokasi, link_toko)
        )
    return scrap_data

if __name__ == "__main__":
    params = get_params()
    all_data=[]
    for i in range(0, len(params)):
        param = params[i]
        data = scrap_data(param)
        all_data.extend(data)
    
    df = pd.DataFrame(all_data, columns=["no", "nama_produk","harga", "rating", "toko", "lokasi", "link_toko"])
    df.to_excel("Tokped_VG_Catalog.xlsx", index=False)
    print ("Data Telah Tersimpan")