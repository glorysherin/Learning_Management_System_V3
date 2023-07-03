a = [	
    '00011111',
	'00010001',
	'00010011',
	'00010110',
	'00011100',
	'00010000',
	'00011111',
	'00000000']


b = [ int(i) for i in "1,2,8,16,32,64,128".split(',')[::-1] ]

print(b)

sum = 0

out = []

for i in a: 
    for k,j in enumerate(i):
        if int(j) == 1:
            print(sum,k)
            sum = sum + b[k-1]
    out.append(sum)

print(out)



# import requests
# from bs4 import BeautifulSoup


# def google_search(query):
#     url = f"https://www.google.com/search?q={query}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, "lxml")
#     search_results = []
#     for result in soup.find_all("div", class_="g"):
#         link = result.find("a").get("href")
#         title = result.find("h3").text
#         description = result.find("span", class_="aCOpRe").text
#         search_results.append((title, link, description))
#     return search_results


# google_search("cat")


