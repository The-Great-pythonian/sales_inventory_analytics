import streamlit
import pandas as pd
import numpy
from matplotlib import pyplot

streamlit.markdown(
    """
    <style>
    textinput {
        font-size: 3rem !important;
    }
    input {
        font-size: 3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



def salesRecords(sales_details):
    # try:
        if sales_details[0] == 0:
            return 'Enter Sales ID.  '
        elif sales_details[1] == '':
            return 'Enter Sales item '
        elif sales_details[2] == 0:
            return 'Enter stock id '
        # elif sales_details[3] == '':
        #     return 'Enter  item description '
        elif sales_details[4] == 0.00:
            return 'Enter unit price '
        elif sales_details[5] == 0:
            return 'Enter quantity '
        # elif sales_details[6] == 0.00: zero value is allowed as no dsicount
        #     return 'Enter Discount'
        elif sales_details[7] == 0 : #automatically calclated
             return 'Enter price'
        elif sales_details:
            # check for double sales id
            df_sale = pd.read_csv('SalesRecord.csv')
            check_salesid = df_sale['SALES_ID'].values.tolist()  # if does work with pandas convert to list
            if sales_details[0] in check_salesid:
                return 'This sales has been registered. choose another sales id!!!'
            else:
                Input_array = numpy.asarray(sales_details)
                Input_array_reshaped = Input_array.reshape(1, -1)  # one row ,as many cols
                df= pd.DataFrame(Input_array_reshaped)
                df.to_csv('SalesRecord.csv',mode='a',index= False,header=False)
                # for backup
                df.to_csv('SalesRecord_bk.csv', mode='a', index=False, header=False)
                #for stock taking
                df.to_csv('SalestempRecord.csv',mode= 'a',index= False,header=False)
                return 'Sales entry was sucessful'
        else: # if everrything failed
            return 'Sales entry  failed '
    # except:  # capture bug and error
    #     return 'error in sales recording '

#get all sales rcord
def fetchSale():
    df_fetch = pd.read_csv('SalesRecord.csv')
    streamlit.write(df_fetch)
    count = len(df_fetch) -1
    total_sales = df_fetch['PRICE'].sum()
    return f'You have made a total sales  of {total_sales}  naira. Number of sales is {count}'

#delete sales record
def deleteSalesRecords(sales_delete):
    if sales_delete[0]:
        df_fetch2 = pd.read_csv('SalesRecord.csv')
        if sales_delete[0] < len(df_fetch2.index) :
            df_update_sales = df_fetch2.drop(df_fetch2.index[sales_delete[0]])
            df_update_sales.to_csv('SalesRecord.csv',index =False)  #do not add new index to update file
            return f'Row {sales_delete[0]} sales record is succesfully deleted '
        else:
            return 'Row of record doesnt exist. Enter proper row number  '
    else:
        return ' you have not entered row number to delete'


def deleteAllSalesRecords():
    df_fetch3 = pd.read_csv('SalesRecord.csv')
                #drop all row df.index[-1]
    df_update_all_sales = df_fetch3.drop(df_fetch3.index[1:])
    df_update_all_sales.to_csv('SalesRecord.csv',index =False)  #do not add new index to update file
    streamlit.write(df_update_all_sales)
    return f' all sales record is succesfully deleted '


#fetch backuo sales record
def fetchSale_bk():
    df_fetch = pd.read_csv('SalesRecord_bk.csv')
        # dispay the file to user
    streamlit.write(df_fetch)
    count = len(df_fetch) -1
        # calculate the sum  to user
    total_sales = df_fetch['PRICE'].sum()
    return f'You have made a total sales  of {total_sales}  naira. Number of sales is {count}'

#data visualisation
def hot():
    df_fetch_hot = pd.read_csv('SalesRecord.csv')
    data= df_fetch_hot['ITEMS'].value_counts()
    streamlit.bar_chart(data)

def vol_sales():
    df_fetch_vol = pd.read_csv('SalesRecord.csv')
    data = df_fetch_vol['QTY']
    streamlit.line_chart(data)

def stock_qty():
    df_fetch_vis = pd.read_csv('Stock.csv')
    y = df_fetch_vis['QTY_IN_STOCK']
    x = df_fetch_vis['DESC']
    fig, ax = pyplot.subplots()
    ax.bar(x, y, width=0.25)
    pyplot.xticks(rotation='vertical')
    streamlit.pyplot(fig)

def profit_track():
    df_fetch_vis = pd.read_csv('Stock.csv')
    a = df_fetch_vis['BULK_PRICE'].values.tolist()
    b = df_fetch_vis['TOTAL_SALES_AMOUNT'].values.tolist()
    r = numpy.arange(len(df_fetch_vis['BULK_PRICE']))
    width = 0.25
    fig, ax = pyplot.subplots()
    ax.bar(r, a, width=width, label='Total cost price')
    ax.bar(r + width, b, width=width, label='gross sales')
    pyplot.xlabel('items')
    pyplot.ylabel('Amount in Naira')
    pyplot.title('Tracking gross sale vs cospt price for Profit')
    c = df_fetch_vis['DESC'].values.tolist()
    pyplot.xticks(r + width / 2, c, rotation=90)
    pyplot.legend()
    streamlit.pyplot(fig)


def storepix ():
    df_fetch_store = pd.read_csv('Stock.csv')
    data= df_fetch_store['QTY_IN_STOCK']
    mylabel = df_fetch_store['DESC']
    fig, ax = pyplot.subplots()
    ax.pie(data,labels= mylabel)
    streamlit.pyplot(fig)



#fetchStock
def fetchStock():
    df_fetchstk = pd.read_csv('Stock.csv')
    streamlit.write(df_fetchstk)
    count = len(df_fetchstk)
        # calculate the sum  to user
    total_stock_price = df_fetchstk['BULK_PRICE'].sum()
    Sales_made = df_fetchstk['TOTAL_SALES_AMOUNT'].sum()
    return f'Sales made so far is {Sales_made}. Total Investement sum is {total_stock_price} Naira for  {count} stock records'

######## edit a stock file
def editing(usersupdate):
        if usersupdate[0] == 0:  #2
            return ' enter index or row  number to edit '
        elif usersupdate[1] == '': #desc
            return ' enter column name to edit'
        elif usersupdate[2] == '':
            return ' enter new values '
        elif usersupdate:
            df_update = pd.read_csv('Stock.csv')
            df_update.at[usersupdate[0], usersupdate[1]] = usersupdate[2]
            df_update.to_csv('Stock.csv',index = False)
            df_update.to_csv('Stock_main.csv', index = False) #backup
            return ' file has been update '
        else:
            return 'no entry found'

def deleteStockRecords(stock_delete):
    if stock_delete[0]: # if entry for row is not empty
        df_fetchstk = pd.read_csv('Stock.csv')
        if stock_delete[0] < len(df_fetchstk.index) :
            df_update_stock = df_fetchstk.drop(df_fetchstk.index[stock_delete[0]])
            df_update_stock.to_csv('Stock.csv',index =False)  #do not add new index to update file
            return f'Row {stock_delete[0]} sales record is succesfully deleted '
        else:
            return 'Row of record doesnt exist. Enter proper row number  '
    else:
         return ' you have not entered row number to delete'


#deleteAllstockRecords
def deleteAllstockRecords():
        df_fetch3 = pd.read_csv('Stock.csv')
        df_update_all_stk = df_fetch3.drop(df_fetch3.index[1:])
        df_update_all_stk.to_csv('Stock.csv',index =False)  #do not add new index to update file
        streamlit.write(df_update_all_stk)
        return f' all sales record is succesfully deleted '

def fetchliveStock():
    df_fetchtempsales = pd.read_csv('SalestempRecord.csv')
    df_fetchstock = pd.read_csv('Stock.csv')
    for j in range(len(df_fetchtempsales)):  #use df.at it uses index and col label to pick a cell
        for i in range(len(df_fetchstock)):
            if  df_fetchtempsales.at[j,'STOCK_ID'] ==df_fetchstock.at[i,'STOCK_ID']:
                diff_in_qty = df_fetchstock.at[i,'QTY_IN_STOCK'] - df_fetchtempsales.at[j, 'QTY']
                    # UPdate stock record qty
                df_fetchstock.at[i,'QTY_IN_STOCK'] = diff_in_qty

                #calculate amount sold
                amount_sold = df_fetchstock.at[i,'TOTAL_SALES_AMOUNT'] + df_fetchtempsales.at[j,'PRICE']
                df_fetchstock.at[i, 'TOTAL_SALES_AMOUNT'] = amount_sold
                profit_made = df_fetchstock.at[i, 'TOTAL_SALES_AMOUNT'] -df_fetchstock.at[i, 'BULK_PRICE']
                #update record
                df_fetchstock.at[i, 'PROFIT'] = profit_made
                #update the stock file
                df_fetchstock.to_csv('Stock.csv', index=False)
                #go to necxt row in df_fetchtempsales until finished

        # print out the live stocking when for lopp finishes
    df_fetchstocklive = pd.read_csv('Stock.csv')
    streamlit.write(df_fetchstocklive)  # it holds THE LIVE STOCK after the for loop
        #drop the row in SalestempRecord.csv where the qty has been update in stock
    df_fetchtempsales_update = df_fetchtempsales.drop(df_fetchtempsales.index[:])                    #evry time index =1 is drop, the next item becomes index 1 in temp file
    df_fetchtempsales_update.to_csv('SalestempRecord.csv', index =False)
        # streamlit.write(df_fetchtempsales_update)

#stock entry stckRecords
def stckRecords(stock_details):
    # try:
        if stock_details[0] == 0:
            return 'Enter stock ID.  '
        elif stock_details[1] == '':
            return 'Enter stock item generic name'
        elif stock_details[2] == '':
            return 'Enter  stock description '
        elif stock_details[3] == 0:
            return 'Enter stock qty '
        elif stock_details[4] == 0.00:
            return 'Enter stock price.Pleae dont add comma '
        # elif stock_details[5] == 0.00:
        #     return 'Enter amount made '
        # elif stock_details[6] == 0.00:
        #     return 'Enter profit_ made '
        elif stock_details[7] == 0.00:
            return 'Enter unit selling price.Pleae dont add comma '
        elif stock_details:
            # check for double stock entry
            df_sale = pd.read_csv('Stock.csv')
            check_stkid = df_sale['STOCK_ID'].values.tolist()  # if does work with pandas convert to list
            if stock_details[0] in check_stkid:
                return 'This stock has been entered. choose another stock id for new stock!'
            else:
                Input_array = numpy.asarray(stock_details)
                Input_array_reshaped = Input_array.reshape(1, -1)  # one row ,as many cols
                df= pd.DataFrame(Input_array_reshaped)
                df.to_csv('Stock.csv',mode='a',index= False,header=False)
                df.to_csv('Stock_main.csv', mode='a', index=False, header=False)
                return 'Stock was added sucessfully'
        else: # if everrything failed
            return 'Stock  entry  failed '
    # except:  # capture bug and error
    #     return 'error in Stock  recording '

##### build interface
def main():
    # # sales inteface
    # # give a title
    streamlit.title('MY BUSINESS-')
    streamlit.subheader('Sales, Inventory & Data Analytics')
    streamlit.image('blogo.png', caption='Shop Logo')  # copy image to pain resize 100 pixel
    #business location
    streamlit.header('business location')
    data ={'lat':[6.55281,6.55531,6.56278],'lon':[3.21897,3.30915,3.28306],'location':['shop1','shop2','shop3']}
    df = pd.DataFrame(data)
    streamlit.map(df)

    streamlit.title('Enter Sales')

    # fect last sales id for tracking
    dflast_sales_id= pd.read_csv('SalesRecord.csv')
    last_sales_id = dflast_sales_id['SALES_ID'].iloc[-1]
    Next_sales_ID = last_sales_id + 1
    streamlit.write('sales id is:',Next_sales_ID)
    #sales number
    # Enter_sale_id = streamlit.number_input('enter sales id', min_value=0, max_value=1000000,
    #                                        value=Next_sales_ID, step=1, key='sid')
    Enter_sale_id = Next_sales_ID
    Enter_sale_id = int(Enter_sale_id) # convert data type  when fetching from file or user

    #select items
    dfs = pd.read_csv('Stock.csv')
    selected_item = streamlit.selectbox("SELECT ITEMS",dfs['ITEMS'] + "  " + "  " + dfs['DESC'] , key='salcategory')
    Enter_items_cl = str(selected_item)  # convert data type  when fetching from file or user

    #find the stock id of selected item
    filtered_df = dfs[dfs['ITEMS'] + "  " + "  " + dfs['DESC'] == selected_item]
    # #from the filtered row bring values of stock id
    select_stck_id = filtered_df['STOCK_ID']
    select_stck_id1 = int(select_stck_id)  # convert data type when fetching from file or user
    # streamlit.write('STOCK id is:', select_stck_id1)
    Enter_stck_id  =select_stck_id1

    #GET Item description
    fetch_Desc = filtered_df['DESC']
    Enter_Desc2 = str(fetch_Desc)  # convert data type when fetching from file or user
    # streamlit.write('Item Desc is:', Enter_Desc2)
    Enter_Desc_cl = Enter_Desc2

    ##enter unit price for 1 item
    fetch_unitprice = filtered_df['UNIT_PRICE']
    fetch_unitprice2 = float(fetch_unitprice) # convert data type when fetching from file or user
    Enter_unit_price = streamlit.number_input('UNIT PRICE', min_value=0.00, max_value=1000000.00,value=fetch_unitprice2, step=1.00, key='uprice')
    Enter_unit_price = float(Enter_unit_price)  # convert when fetching from file or user

    #enter qty
    Enter_qty = streamlit.number_input('ENTER QUANTITY', min_value=0, max_value=1000000, value=1, step=1,key='uqty')
    Enter_qty = int(Enter_qty)  # convert when fetching from file or user

    Enter_Discount = streamlit.number_input('DISCOUNT ANY?', min_value=0.00, max_value=1000000.00, value=0.00,step=1.00, key='dis')
    Enter_Discount = float(Enter_Discount)  # convert when fetching from file or user


    #AMOUNT SOLD
    Enter_price2 = (Enter_unit_price * Enter_qty) - Enter_Discount
    Enter_price1 = float(Enter_price2)  # convert when fetching from file or user
    Enter_price = streamlit.number_input('PRICE IS:', min_value=0.00, max_value=1000000000.00, value=Enter_price1,step=1.00, key='price')

    Enter_notes = streamlit.text_input('enter sales observation  if any', value="", key='ob')

    current_time = pd.Timestamp.now()
    streamlit.write('TIMER:', current_time)
    time = current_time

    # time = streamlit.text_input('date and Time of sales', value=current_time, key='tim')

    salesrecords = ""  # declare this variable to hold result like empty list
    if streamlit.button('Upload Sales',key = 'upsal'):  # Call a function salesRecords to handle user inputs
        salesrecords = salesRecords([Enter_sale_id,Enter_items_cl,Enter_stck_id,Enter_Desc_cl,Enter_unit_price,Enter_qty ,Enter_Discount,Enter_price,Enter_notes,time])
    streamlit.success(salesrecords)

    #  ----- fetch all sales records interface
    # give a title
    streamlit.title('MY Sales RECORDS ')
    # sub section
    streamlit.subheader('Admins only')

    fetchsale = ""  # declare this variable to hold result like empty list

    if streamlit.button('SEE ALL SALES', key='fetsale'):
        # fetchRecords ...call the function to process input
        fetchsale = fetchSale()
    streamlit.success(fetchsale)


    # DELeTING wrong sales RECORDS

    admin_del = streamlit.number_input('enter row number of record to delete', min_value=0, max_value=1000000, value=0,
                                       step=1, key='delrows')
    # admin_del_upper = admin_del.upper().strip()
    delectesal = ""
    if streamlit.button('DELETE SALES ROW', key='delsal'):
        delectesal = deleteSalesRecords([int(admin_del)])
    streamlit.success(delectesal)  # return the result

    # DELeTING all sales RECORDS for new business day or week or month
    #a bacup file salesrecord2 in case of loss of sales record

    delecteallsal = ""
    if streamlit.button('DELETE ALL SALES', key='delallsal'):
        delecteallsal = deleteAllSalesRecords()
    streamlit.success(delecteallsal)  # return the result


    # fetch backup interface

    fetchbksale = ""  # declare this variable to hold result like empty list

    if streamlit.button('Recover Sales Records', key='fetbksale'):
        # fetchRecords ...call the function to process input
        fetchbksale = fetchSale_bk()
    streamlit.success(fetchbksale)
### data analytic
    streamlit.header('Data Analytic - visualisation')
    col1, col2, col3, col4,col5 = streamlit.columns((1, 1, 1,1,1))  # layout element
    with col1:
        hotsales = ""
        if streamlit.button('HOT SELLING', key='hotsal'):
            hotsales = hot()
        streamlit.success(hotsales)  # return the result
    with col2:
        # qty sold per time
        selltimes = ""
        if streamlit.button('SALES VOLUME', key='timesal'):
            selltimes = vol_sales()
        streamlit.success(selltimes)  # return the result
    with col3:
        # qty in stock left
        stkoty = ""
        if streamlit.button('TAKE STOCK', key='stkoty'):
            stkoty = stock_qty()
        streamlit.success(stkoty)  # return the result
    with col4:
        # track gros sales v cost price  for profit
        profitstk = ""
        if streamlit.button('PROFIT TRACKER', key='stkpro'):
            profitstk = profit_track()
        streamlit.success(profitstk)  # return the result
    with col5:
        # distribution of goods in stor
        stkgoods = ""
        if streamlit.button('% GOODS IN STORE', key='stkgoods'):
            stkgoods = storepix()
        streamlit.success(stkgoods)  # return the result


    #  ----- fetch all stock records
    # give a title
    streamlit.title('Check Inventory & stock taking ')

    fetchstk = ""  # declare this variable to hold result like empty list

    if streamlit.button('CHECK STORE', key='fetstck'):
        # fetchRecords ...call the function to process input
        fetchstk = fetchStock()
    streamlit.success(fetchstk)

    # admin
    #### edit button of a file
    streamlit.subheader('Edit Stock --- ---  ---')
    col1, col2, col3 = streamlit.columns((1, 1, 1))  # layout element
    with col1:
        Enter_row_number = streamlit.number_input('INPUT ROW ', min_value=0, max_value=10000, value=0, step=1,
                                                  key='rowno')
        Enter_row_number = int(Enter_row_number)
    with col2:
        df_col = pd.read_csv('Stock_col.csv')
        selected_item = streamlit.selectbox("SELECT COLUMN", df_col['COL_TITLE'], key='colabel')
        Enter_col_title_cl = str(selected_item)
        # Enter_col_title = streamlit.text_input('Enter_col_title', value="", key='colabel')
        # Enter_col_title_cl = Enter_col_title.upper().strip()  # col must match the document
    with col3:
        Enter_new_value = streamlit.text_input('INPUT_NEW VALUE', value="", key='newval')
        Enter_new_value_cl = Enter_new_value.strip()

    edit = ""  # declare this variable to hold result like empty list

    if streamlit.button('EDIT FILE', key='ed'):
        # Reg ...call the function to process input
        edit = editing([Enter_row_number, Enter_col_title_cl, Enter_new_value_cl])

    streamlit.success(edit)

    # DELeTING wrong stock RECORDS
    streamlit.subheader( 'Delete Stock ----          ----           ----       ----')
    col1, col2 = streamlit.columns((1, 1))  # layout element
    with col1:
        row_del = streamlit.number_input('INPUT ROW TO DELETE', min_value=0, max_value=1000000, value=0,
                                           step=1, key='delstkrows')

        delectestk = ""
        if streamlit.button('DELETE STOCK RECORD', key='delstk'):
            delectestk = deleteStockRecords([int(row_del)])
        streamlit.success(delectestk)  # return the result

        # DELeTING all stock  RECORDS

    delecteallstk = ""
    if streamlit.button('Delete All STOCK', key='delallstk'):
        delecteallstk = deleteAllstockRecords()
    streamlit.success(delecteallstk)  # return the result

    #### getting live inventory
    streamlit.subheader(' latest inventory')
    fetchstklive = ""  # declare this variable to hold result like empty list

    if streamlit.button('TAKE STOCK', key='fetlivstck'):
        # fetchRecords ...call the function to process input
        fetchstklive = fetchliveStock()
    streamlit.success(fetchstklive)

    # upload stock
    streamlit.title(' upload new stock')

    dflast_stcok_id = pd.read_csv('Stock.csv')
    dflast_stcok_id = dflast_stcok_id['STOCK_ID'].iloc[-1]
    Next_stcok_id = dflast_stcok_id + 1
    streamlit.write('the next stock id is:', Next_stcok_id)

    with streamlit.form("myform", clear_on_submit=True):
        # # Enter_stk_id = streamlit.number_input('enter stock category id', min_value=0, max_value=1000000, value=0,
        # #                                       step=1, key='sitemid')
        # Enter_stk_id = int(Enter_stk_id)
        # fect curent stock id
        Enter_stk_id = Next_stcok_id
        Enter_stk_id = int(Enter_stk_id)


        Enter_stk_items = streamlit.text_input('ITEM CATEGORY', value="", key='stckitems')
        Enter_stk_items_cl = Enter_stk_items.upper().strip()  # pass an upper

        Enter_stk_Desc = streamlit.text_input('ITEM DESCRIPTION', value="", key='stkdesc')
        Enter_stk_Desc_cl = Enter_stk_Desc.upper().strip()  # pass an upper

        Enter_stk_oty = streamlit.number_input('QUANTITY ', min_value=0, max_value=1000000, value=0, step=1,
                                               key='stkqty')
        Enter_stk_oty = int(Enter_stk_oty)

        Enter_stk_price = streamlit.number_input('TOTAL COST PRICE', min_value=0.00, max_value=1000000000.00,
                                                 value=0.00, step=1.00, key='stkprice')
        Enter_stk_price = int(Enter_stk_price)
        Enter_amount_made = 0
        Enter_profit_made = 0
        Enter_stk_uprice = streamlit.number_input('ENTER UNIT PRICE', min_value=0.00,
                                                  max_value=1000000000.00,
                                                  value=0.00, step=1.00, key='unstkprice')
        Enter_stk_uprice = int(Enter_stk_uprice)

        Enter_stk_notes = streamlit.text_input('OBSERVATION', value="", key='stkob')

        current_time = pd.Timestamp.now()
        streamlit.write('TIMER:', current_time)
        time_stk = current_time

        submit = streamlit.form_submit_button(label="Upload stock")
    stockrecords = ""  # declare this variable to hold result like empty list

    if submit:  # streamlit.button('Upload stock',key = 'upstck'):
        # Reg ...call the function to process input
        stockrecords = stckRecords(
            [Enter_stk_id, Enter_stk_items_cl, Enter_stk_Desc_cl, Enter_stk_oty, Enter_stk_price, Enter_amount_made,
             Enter_profit_made, Enter_stk_uprice, Enter_stk_notes, time_stk])

    streamlit.success(stockrecords)


    streamlit.subheader('aPP for every shop developers')



if __name__ == '__main__':
    main()

# web app  on your desktop local host
#run  on your pycharm terminal ' streamlit run Sales.py '



