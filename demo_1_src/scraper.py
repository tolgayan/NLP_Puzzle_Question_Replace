from selenium import webdriver
import time

def listToString(s):
    str1 = " "
    return(str1.join(s))

# set up options for selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", chrome_options=options)

# load the page
driver.get("https://www.nytimes.com/crosswords/game/mini")

# do necessary operations to display the puzzle
time.sleep(3)
initial_ok_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div[2]/div[2]/article/div[2]/button')
initial_ok_button.click()
time.sleep(0.1)
reveal_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button')
reveal_button.click()
time.sleep(0.1)
reveal_puzzle_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div[1]/ul/div[2]/li[2]/ul/li[3]')
reveal_puzzle_button.click()
time.sleep(0.1)
final_reveal_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/article/div[2]/button[2]')
final_reveal_button.click()
time.sleep(0.1)
popup_window_close_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/span')
popup_window_close_button.click()

time.sleep(1)

# scrape cells with answers from page content
cells_table =  driver.find_element_by_xpath('//*[@data-group="cells"]')
cells_table_cells = cells_table.find_elements_by_tag_name("g")

cells = []

for index, cell in enumerate(cells_table_cells):
    texts = None
    try:
        texts = [text.text for text in cell.find_elements_by_tag_name('text')]
            
    except:
        pass
    cell_info = {
        "cell_index": index,
        "texts": texts
    }

    cells.append(cell_info)

# display the scraped cell content
print("number of cells: ", len(cells))
for cell in cells:
    print(cell)    
# scrape clues
across = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/article/section[2]/div[1]/ol')
across_clues = [clue.text.replace("\n", ".") for clue in across.find_elements_by_tag_name('li')]
down = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/article/section[2]/div[2]/ol')
down_clues = [clue.text.replace("\n", ".") for clue in down.find_elements_by_tag_name('li')]

# display the scraped clues
print("across clues: \n", across_clues)
print("down clues: \n", down_clues)

with open("PuzzleInfo.txt", "w") as f:
    for cell in cells:
        if(len(cell["texts"]) != 0):
            for i in range(len(cell["texts"])):
                if(cell["texts"][i].isdigit()):
                    f.write('%s' % (cell["texts"][i]))
                    f.write(' ')
                else:
                    f.write('%s' % (cell["texts"][i]))
                    f.write('\n')
        else:
            f.write('%s' % ('-1\n'))
    f.write('\n')
    for text in across_clues:
        f.write("%s\n" % text)
    f.write('\n')
    for text in down_clues:
        f.write("%s\n" % text)