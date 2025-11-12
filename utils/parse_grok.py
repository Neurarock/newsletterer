from bs4 import BeautifulSoup


with open('./grok_convo_scrap/e6c956603d.html') as f:
    content = f.read()


soup = BeautifulSoup(content)

with open('./grok_convo_scrap/beautiful_e6c956603d.html', "w") as f:
    f.write(soup.prettify())


"""
split = content.split('self.__next_f.push([1,')

grok_response = split[34]
print(grok_response)
"""
"""
response = grok_response.split('</script><script nonce="">')
formatted = response[0]

print(formatted)
"""

"""
convo = content.split('\\",\\"message\\":\\"')
"""




"""
for c in convo:
    print(c[:800])
    print("\n")
"""
