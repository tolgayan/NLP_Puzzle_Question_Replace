from selenium import webdriver

def getFromUrban(answer, driver):
    driver.get("https://www.urbandictionary.com/define.php?term=" + answer)
    meanings = []
    gifSources = []
    examples = []

    try:
        definitions = driver.find_elements_by_class_name("def-panel")
    except:
        return (meanings, gifSources, examples)

    for definition in definitions:
        try:
            headerElement = definition.find_element_by_class_name("def-header")
            header = headerElement.text
        except:
            continue

        if (answer.lower() != header.lower()):
            continue

        try: 
            meaningElement = definition.find_element_by_class_name("meaning")
            meanings.append(meaningElement.text)
        except:
            pass

        try:
            exampleElement = definition.find_element_by_class_name("example")
            examples.append(exampleElement.text)
        except:
            pass

        try: 
            gifElement = definition.find_element_by_class_name("gif")
            imageElement = image = gifElement.find_element_by_tag_name("img")
            gifSources.append(imageElement.get_attribute("src"))
        except:
            pass
   
    return (meanings, gifSources, examples)

def getFromMerriam(answer, driver):
    driver.get("https://www.merriam-webster.com/dictionary/" + answer.lower())

    # try:
    #     headers = driver.find_elements_by_class_name("col-12")
    # except:
    #     return []

    definitions = []
    
    count = 1
    condition = True
    while condition:
        try:
            definitions.append(driver.find_element_by_id("dictionary-entry-"+str(count)))
            count += 1
        except:
            condition = False

    meanings = []

    for definition in definitions:
        meaningElements = definition.find_elements_by_class_name("dtText")

        try:
            headerElement = definition.find_element_by_tag_name("em")
            header = headerElement.text
        except:
            continue

        if (header.lower() != answer.lower()):
            continue

        for meaningElement in meaningElements:
            text = str(meaningElement.text)
            index = text.find("\n")
            if (index != -1):
                text = text[:index]
            if (text[0] == ':'):
                text = text[2:]
            meanings.append(text) 

    return meanings

def getFromWordnet(answer, driver):
    driver.get("http://wordnetweb.princeton.edu/perl/webwn?s=" + answer.lower())
   
    definitions = driver.find_elements_by_tag_name("li")

    meanings = []
    for definition in definitions:
        text = str(definition.text)
        indexBegin = text.find(")")
        text = text[indexBegin:]

        indexBegin = text.find("(")
        indexEnd = text.rfind(")")
        text = text[indexBegin + 1 : indexEnd]
        meanings.append(text)

    return meanings

answer = "HAYES"    

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", chrome_options=options)

meanings, gifSources, examples = getFromUrban(answer,driver)

print("Urban:")
print("---------------------------------------")
print("Meanings:")
for meaning in meanings:
    print(meaning)
print()

print("Gifs:")
for gif in gifSources:
    print(gif)
print()

print("Examples:")
for example in examples:
    print(example)

print("---------------------------------------")

meanings = getFromMerriam(answer, driver)

print("Merriam:")
print("---------------------------------------")
print("Meanings:")
for meaning in meanings:
    print(meaning)

print("---------------------------------------")
meanings = getFromWordnet(answer, driver)

print("WordNet:")
print("---------------------------------------")
print("Meanings:")
for meaning in meanings:
    print(meaning)
