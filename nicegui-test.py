#imports ui
from nicegui import ui

def getData():
    #opens file that the list of "banned words" is currently in
    bannedFile = open('bannedWords.txt', 'r')
    bannedWords = []

    #copies file to a list
    for line in bannedFile:
        line = line.strip()
        line.upper()
        bannedWords.append(line)

    #closes file
    bannedFile.close()

    #returns list of "banned words"
    return bannedWords


def findBannedWords(bannedWords, prop):
    #capitalizes all words in the users research proposal
    upperProp = prop.upper()

    #makes a copy of the proposal to add in uppercased words
    newProp = prop

    #initializes list of words flagged in the proposal
    flaggedWords = []

    #searches for each item in the "banned words" list
    for word in bannedWords:

        #capitalizes term
        word = word.upper()

        #checks to see if the term has an 'and' operator
        if '&' in word:
            word1, word2 = word.split('&')

            #finds if each term is in proposal
            i1 = upperProp.find(word1)
            i2 = upperProp.find(word2)

            #adds flagged term to the flaggedWords list
            #and capitalizes the term(s) in the proposal
            if i1 != -1 and i2 != -1:
                newProp, count1 = findAll(newProp, word1)
                newProp, count2 = findAll(newProp, word2)
                flaggedWords.append((word1, count1))
                flaggedWords.append((word2, count2))
        elif '+' in word:
            temp = word.strip('+')
            i = upperProp.find(temp)
            if i != -1:
                newProp, count = specFind(newProp, temp)
                if count > 0:
                    flaggedWords.append((temp, count))
        else:
            i = upperProp.find(word)
            if i != -1:
                newProp, count = findAll(newProp, word)
                flaggedWords.append((word, count))

    #returns the list of flagged terms
    #and the proposal with all flagged terms capitalized
    return flaggedWords, newProp

endCharacters = [' ', ',', '.', '?', '!', '(', ')', '[', ']', '/', '"', "'", '<', '>', '=']

def specFind(prop, toFind):
    newProp = prop
    upperProp = prop.upper()
    i = upperProp.find(toFind)
    x = 0

    while i != -1:
        start = upperProp[i-1:i]
        end = upperProp[i+len(toFind):i+len(toFind)+1]
        if start in endCharacters and end in endCharacters:
            x += 1
            newProp = boldSub(newProp, i, i+len(toFind))
         #erases documented instances of toFind temporarily
        upperProp = fillNothing(upperProp, i+len(toFind))
        #next instance of toFind
        i = upperProp.find(toFind)
    return newProp, x
    

def boldSub(full, start, end):
    while full[start] not in endCharacters:
        start -=1
    while full[end] not in endCharacters:
        end += 1

    beginning = full[0:start]
    ending = full[end:len(full)]
    middle = full[start:end]

    #capitalizes term at full[start:end]
    middle = "<c>" + middle + "</c>"
    new = beginning + middle + ending

    #returns full string with capitalized substring
    return new



def findAll(prop, toFind):

    newProp = prop
    upperProp = prop.upper()
    i = upperProp.find(toFind)
    x = 0

    #loops until there are no more instances of toFind in the proposal
    while i != -1:



        x += 1

        #capitalizes toFind
        newProp = boldSub(newProp, i, i+len(toFind))

        #erases documented instances of toFind temporarily
        upperProp = fillNothing(upperProp, i+len(toFind))
        #next instance of toFind
        i = upperProp.find(toFind)

    #returns proposal with all instances of toFind capitalized
    return newProp, x


def fillNothing(fill, end):
    newProp = ''
    for i in range(end+7):
        newProp = newProp + '-'
    newProp = newProp + fill[end:len(fill)]
    return newProp


def save_prop(prop):
    prop = str(prop)
    flaggedWords, prop = findBannedWords(getData(), prop)
    textbox_I.value = prop
    flaggedWords.sort(key=lambda col: col[0])
    flaggedWords.sort(key=lambda col: col[1], reverse=True)
    if len(flaggedWords) > 0:
        for i in range(len(flaggedWords)):
            text = '' + flaggedWords[i][0] + " (" + str(flaggedWords[i][1]) + ")"
            x = ui.button(text, on_click=lambda: scroller.scroll_to(pixels=1194.5)).props('flat unelevated color-none')
            x.move(card)
    else:
        y = ui.label("No words flagged.")
        y.move(card)


def clickActions():
    card.clear()
    save_prop(textbox_I.value)

ui.add_css('''
    .nicegui-editor c {
        font-weight: bold;
        color: red;
        text-decoration: none;
    }
''')


with ui.row(wrap=True):
    with ui.column(align_items='end'):
        scroller = ui.scroll_area().classes('size-128 border')
        with scroller:
            textbox_I = ui.editor(placeholder='Proposal')
            textbox_I._props.update(toolbar=[
                ['left', 'center', 'right', 'justify'],
                ['italic', 'underline', 'strike'],
            ])
        testbutton = ui.button('Test Proposal', icon='check', on_click=lambda: clickActions()).props(f'color={"negative"}')
    #with ui.scroll_area().classes('width-64 height-128'):
    card = ui.card()
ui.run()
