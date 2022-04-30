import requests
import csv


def request_posts(domain: str) -> list:
    token = "aaaa4beaaaaa4beaaaaa4bea26aaddd276aaaaaaaaa4beaca2c9dc224e26a0308da8ba7"
    version = 5.131
    offset = 0
    count = 200
    filter = 'all'

    response = requests.get("http://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': count,
                                'filter': filter
                            })

    data = response.json()['response']['items']
    data_list = list()
    data_list.extend(data)
    print(data_list)
    return data_list


def output(data_list: list):
    with open('Analyze.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['likes', 'reposts', 'body', 'url'])
        img_url = ""
        for post in data_list:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'pass'
            except:
                pass
            try:
                writer.writerow([post['likes']['count'], post['reposts']['count'], post['text'], img_url])
            except:
                pass


def counter(data_list: list):
    i = 0
    likes_sum = 0
    reposts_sum = 0

    for post in data_list:
        if i == 0:
            last_post = post['text']
        else:
            continue
        likes_sum += post['likes']['count']
        reposts_sum += post['reposts']['count']
        i += 1

    if last_post != '':
        pass
    else:
        last_post = "contains no text."

    print("Amount of likes for 300 posts = " + str(likes_sum) + ";" +
          "\nAmount of reposts for 300 posts = " + str(reposts_sum) + ";" +
          "\nAVG likes per post = " + str(likes_sum / i) + ";" +
          "\nAVG reposts per post = " + str(reposts_sum / i) + "."
                                                               "\n***************************\n" +
          '\nLast post:''\n\t"' + str(last_post) + '"'
          )


while True:
    print("\n***************************")
    print("Hello, input VK public URL: ")
    domain = str(input())
    try:
        data_list = request_posts(domain)
        output(data_list)
        counter(data_list)
    except:
        print("ERROR:\tOops an incorrect domain name \n")
