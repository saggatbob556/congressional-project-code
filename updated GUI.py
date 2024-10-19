import PySimpleGUI as sg   
from dataParser import *
sg.theme('Dark Amber')

# contains the String of the searched product
searchedItem = ''

# variables that are currently not used:
# these will contain whatever the database / barcode scanner returns (add more as needed)
# eventually add them to the window titled windowProduct
foundItem = ''
score = ''
reasoning = ''




""" controls which window is shown 
0 = home
1 = scan barcode
2 = database search
3 = product confirm
4 = product info
5 = try again
6 = submit a product for review
7 = thank you for submitting a product
"""
windowActive = 0


# home screen layout: maybe put some images in the 2nd row for icons
cameraIcon_base64 = b'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'
searchIcon_base64 = b'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'
exitIcon_base64 = b'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAAvFJREFUeF7tnEFSg0AQRSHH0fu4z8ozucre+8TjxNRUalKoJMww3f1/W99tYLr7PT5QYDJP+oMSmKHVVXySAPBBIAESACYALq8ESACYALi8EiABYALg8kqABIAJgMsrARIAJgAurwRIAJgAuLwSIAFgAuDySoAEgAmAy4ck4Hh8fzmdPr7As3aVj+rZXUAZ5HI4fB4ul7csEiJ7dhVQB5mm79dpms8ZJET37Cbg5yA1/dwSED27CFgfhFsCqmdzAc8H4ZSA7NlUQNsgXBLQPZsKKGjRA/XcazL0ai4giwQG+IWViwB2CSzwXQWwSmCC7y6ATQIb/BABLBIY4YcJQEtghR8qACWBGX64gGgJ7PAhAqIkZIAPE+AtIQt8qAAvCZngwwVYS8gGn0KAlYSM8GkEjErICp9KwF4JZb/y0v/23nnrj++VqNvT0C0Ujz7vPZpv6+SET5eAKqVPQotqviO/dk2XAHsJvPBpE2AngRs+vYD+C/PydMQPP4WAfRJywJeAluu38za0F+Hx60COFFALGL8d5ZdAK2Ac/v1Om/q/sikF2MHnl0AnoA/+fNajCMO7hF745QsfehhnJGAP/PqVp5F9jdrfvQzFKcgCoMUauykO7AgXYAnOcq0Bpl27QgV4APNYs4to58YwAZ6gPNfu5Lu5OURABKCIGpt0GzYIFxAJJrJWA+vVTUIFIIAgavbICBOABIGsvSUjRAADAIYe1mS4C2AanKmX+2PCrYiMfM44MFtPbglgG3R5IDH15iKAacBHCWbp0VwAy2Atp06GXk0FMAzUAp7pdGQqoAzWJoHrZTmyZ3MB2xK44Nc0PJfg17OLgMcS/AbpPfWsbb8uwbdnNwF/JfgOYiEA0bOrgOVAGX4x8ffpKKJndwFVQpbfDF1KiOg5RIDV6eE/riMBYKsSIAFgAuDySoAEgAmAyysBEgAmAC6vBEgAmAC4vBIgAWAC4PJKgASACYDLKwESACYALq8ESACYALi8EgAWcAWtkeyOXk4U5wAAAABJRU5ErkJggg=='

layoutHome = [[sg.Text("Is your product sustainable?", p = (100, 10), font = (15))],
              [sg.Button("", key = "Scan barcode", image_data = cameraIcon_base64, p = 26, border_width = 5), 
               sg.Button("", key = "Search our database", image_data = searchIcon_base64, p = 26, border_width = 5), 
               sg.Button("", key = "Exit", image_data = exitIcon_base64, p = 26, border_width = 5)],
               [sg.Text("Scan barcode", p = (35, 5)), sg.Text("Search our database", p = (30, 5)), sg.Text("Exit", p = (50, 5))]]

# barcode scan layout
layoutScan = [[sg.Text("Please hold your barcode up to the camera")],
              [sg.Button("Home", border_width=5), sg.Button("Search our database", border_width=5)]]

# database search layout
layoutSearch = [[sg.Text("Type your product here: "),sg.Input(key = '-INPUT-'),sg.Button("Search", border_width=5)],
                [sg.Button("Home", border_width=5), sg.Button("Scan barcode", border_width=5)]]

# is-this-your-product layout
confirmColumnLayout1 = [[sg.Text("Is this your product?", font = (15))],
                 [sg.Text(key = '-OUTPUT-')]] #large empty space reserved for product name and/or picture

confirmColumnLayout2 = [[sg.Button("Yes", size = (10,2), p = 20, border_width = 5)],
                 [sg.Button("No", size = (10,2), p = 20, border_width = 5)],
                 [sg.Button("Home", size = (10,2), p = 20, border_width = 5)]]

layoutConfirm = [[sg.vtop(sg.Column(confirmColumnLayout1)), sg.Push(), sg.Column(confirmColumnLayout2, element_justification = "right")]]

# product information layout
# ADD MORE INFO AS NEEDED
layoutProduct = [[sg.Text("Your product: "), sg.Text(key='-OUTPUT1-')],
          [sg.Text("Score: "), sg.Text(key='-OUTPUT2-')],
          [sg.Text("Reasoning: ")], 
          [sg.Multiline(key='-OUTPUT3-', disabled = True, size = (100,5), wrap_lines=True)],
          [sg.VPush()],
          [sg.Button("Home", border_width=5)]]

# layout for if the scan and database aren't working
sadFace_base64 = b'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'

layoutTryAgain = [[sg.Text("Sorry!", font = (10))],
                  [sg.Image(sadFace_base64)],
                  [sg.Text("We couldn't find your product.", font = (10))], 
                  [sg.Button("Scan", size = (5,1), p = (20, 10), border_width=5), 
                   sg.Button("Search database", size = (17, 1), p = (20, 10), border_width=5), 
                   sg.Button("Home", size = (5,1), p = (20, 10), border_width=5)]]

# submit product for review layout (does nothing)
layoutReview = [[sg.Text("Name of product"),sg.Input(key = '-INPUT1-'),sg.Button("Home")],
          [sg.Text("Name of company"),sg.Input(key = '-INPUT2-')],[sg.Button("Enter")]]

# your request has been recorded layout (does nothing)
layoutRecorded = [[sg.Text("Your response has been recorded. Thank you for making our app better.")],[sg.Button("Home")]]


# creates the windows for home, barcode scan, search database, etc.
windowHome = sg.Window('Sustainable product app', layoutHome,  size=(500, 250), finalize=True)
windowScan = sg.Window('Scanning object', layoutScan, element_justification='center', finalize=True)
windowSearch = sg.Window('Search database', layoutSearch, finalize=True)

windowConfirm = sg.Window('Confirm your product', layoutConfirm, size=(600,300), finalize=True)
windowProduct = sg.Window('Product info', layoutProduct, size = (500, 250), finalize=True)

windowTry = sg.Window('Oops', layoutTryAgain, size = (500, 250), element_justification= 'center',finalize=True)
windowSubmit = sg.Window('Submit a product for review', layoutReview, finalize=True)
windowThanks = sg.Window('Thank you', layoutRecorded, finalize=True)


def hideWindows():
  windowHome.hide()
  windowScan.hide()
  windowSearch.hide()
  windowConfirm.hide()
  windowProduct.hide()
  windowTry.hide()
  windowSubmit.hide()
  windowThanks.hide()


def closeAll():
  windowHome.close()
  windowScan.close()
  windowSearch.close()
  windowConfirm.close()
  windowProduct.close()
  windowTry.close()
  windowSubmit.close()
  windowThanks.close()

stay = True

while stay:

  # user is currently on home window
  while windowActive == 0:
    hideWindows()
    windowHome.un_hide()
    event0, values0 = windowHome.read()

    # close the entire app
    if event0 == sg.WIN_CLOSED or event0 == 'Exit':
      stay = False
      break

    # open barcode window
    if event0 == "Scan barcode":
      windowActive = 1
      break

    # open database window
    if event0 == "Search our database":
      windowActive = 2
      break


  # barcode scanner UI
  while windowActive == 1:
    hideWindows()
    windowScan.un_hide()
    event1, values1 = windowScan.read()

    # if the window is closed, close the entire application
    if event1 == sg.WIN_CLOSED:
      stay = False
      break 

    # exit to home window 
    if event1 == 'Home':
      windowActive = 0
      break

    # close current window and open database search window
    if event1 == "Search our database":
      windowActive = 2
      break

    # if product is found:
    #   windowActive = 3
    #   the variables at the top get assigned to the info gathered from the barcode scanner and webscraper
    # break
    
      
  
  # database search UI
  while windowActive == 2:
    hideWindows()
    windowSearch.un_hide()
    event2, values2 = windowSearch.read()

    if event2 == sg.WIN_CLOSED:
      stay = False
      break

    # exit to home window
    if event2 == 'Home':
      windowActive = 0
      break
      
    # close current window and open barcode window
    if event2 == "Scan barcode":
      windowActive = 1
      break

    # if the user types something into the box and presses 'search'
    if event2 == "Search":
      searchedItem = values2['-INPUT-']
      
      # in app, search through the database and return the product (should go into foundItem)
      # also update the variables at the top (add more as needed)

      # PLACEHOLDER CODE FOR TESTING
      foundItem = getData(searchedItem)
      score = getRatingOfSpecific(searchedItem)
      reasoning = str(getPraiseOf(searchedItem)) + " " + str(getCriticismOf(searchedItem))
      windowActive = 3
      windowConfirm["-OUTPUT-"].update(foundItem)
      break
  

  # confirm product window
  while windowActive == 3:
    hideWindows()
    windowConfirm.un_hide()
    event3, values3 = windowConfirm.read()

    if event3 == sg.WIN_CLOSED:
      stay = False
      break

    if event3 == "Home":
      windowActive = 0
      break

    if event3 == "Yes":
      windowActive = 4
      windowProduct["-OUTPUT1-"].update(foundItem)
      windowProduct["-OUTPUT2-"].update(score)
      windowProduct["-OUTPUT3-"].update(reasoning)
      break

    if event3 == "No":
      windowActive = 5
      break

  
  # displays product information
  while windowActive == 4:
    hideWindows()
    windowProduct.un_hide()
    event4, values4 = windowProduct.read()

    if event4 == sg.WIN_CLOSED:
      stay = False
      break

    if event4 == "Home": 
      windowActive = 0
      break


  # window if product isn't found
  while windowActive == 5:
    hideWindows()
    windowTry.un_hide()
    event5, values5 = windowTry.read()

    if event5 == sg.WIN_CLOSED:
      stay = False
      break

    if event5 == "Home":
      windowActive = 0
      break

    if event5 == "Scan":
      windowActive = 1
      break

    if event5 == "Search database":
      windowActive = 2
      break

    if event5 == "Submit a product for review":
      windowActive = 6
      break

  
  # submit a product for review
  while windowActive == 6:
    hideWindows()
    windowSubmit.un_hide()
    event6, values6 = windowSubmit.read()

    if event6 == sg.WIN_CLOSED:
      stay = False
      break

    if event6 == "Home":
      windowActive = 0
      break

    # can do something if you want it to
    if event6 == "Enter":
      windowActive = 7
      break



  # thanks the user
  while windowActive == 7:
    hideWindows()
    windowThanks.un_hide()
    event7, values7 = windowThanks.read()

    if event7 == sg.WIN_CLOSED:
      stay = False
      break

    if event7 == "Home":
      windowActive = 0
      break


closeAll()
