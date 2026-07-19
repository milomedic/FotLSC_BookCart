"# FOTLSC_BookCart" 


**This repo contains the web files for the South Central Friends of the Library Book Cart**

### Included Files
**README.md** - *this file*
**index.html** - *the html file that dictates how the shopping cart page is displayed on the web*
**server.py** - *the python file that takes the shopping cart data and configures it as an API request to Stripe*
**scrlibrary_friends_pythonanywhere_com_wsgi.py** - *the wsgi file required to work with pythonanywhere*


### Now I will explain the sections of each file. This is geared towards someone already familiar with the basics of syntax in a programming environment.

## Index.html

<head> section:
Useful features:
    <script>
        function updateTotal
            Contains the **prices** list. Each item in the list is defined as a variable with a specific price value. Note capitalization.
            example:
                hardback: 2.00,
        function attachListeners
            Sets up the Javascript for listening for user inputs in each section
    <style>
        sets the style for how the page looks. Defines the margins, the colors, the fonts, the button sizes, etc.

<body> section:
Useful features:
    <div> class="logo"
        contains the link to the Friends of the Library Logo
    <h1>
        contains the title that appears on the checkout page
    <form>
        contains the formatting and the text that appears for each item for sale.
        NOTE:
        basic format for an item for sale:
        <tr>
                    <td>NAME OF ITEM HERE (NAME IN SPANISH)</td>
                    <td class="price">$PRICEHERE</td>
                    <td class="quantity"><input type="number" name="VARIABLENAME" min="0" value="0"></td>
        </tr>
            where PRICEHERE is the list price (e.g. $2.00)
            VARIABLENAME must match one of the items in the list of prices, as shown above in the <script> section
        
        Also, there is a section for a tip/donation.
            Note that the input has an element step="0.25" in it. This means that clicking the up or down arrow on the tip function will increase/decrease it by $0.25.
            Also note that min="0". This prevents people from entering negative tips/donations.




## server.py

**this is using several python libraries: flask and stripe.**

I will not bother going through the entire 