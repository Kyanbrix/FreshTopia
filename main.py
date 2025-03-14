import db_connection.connection as connection
from db_connection.connection import ConnectionPool
from pathlib import Path
from controller.barcode_logic import BarcodeController as BC
import utils.utilities as utilities
import utils.expiration_check as ex


from gpiozero import LED
from db_connection.database import Database
import ttkbootstrap as ttk
import traceback
from datetime import datetime
from ttkbootstrap.constants import*
from ttkbootstrap.dialogs.dialogs import Messagebox
from controller.date_logic import DateFormatter as df

is_scanning = False

image = None
dateofexpiration = ''
dateadded = ''
barcode_id = ''


led1 = LED(17)

expired_products_list = []

def change_frame_content(): # <--------------------------- INVENTORY BUTTON IN MENU

    global is_scanning

    is_scanning = False


    for widget in target_frame.winfo_children():
        widget.destroy()

    
    db = Database('mydatabase.db')

    try:
        data = db.fetch_all_query('SELECT * FROM storage')

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        table = ttk.Treeview(target_frame, style="Treeview",
                         columns=["Barcode ID", "Item Name", "Date Added", "Date Expiration"], show="headings",
                         height=20,
                         padding=20)
        table.heading("Barcode ID", text="Barcode ID")
        table.heading("Item Name", text="Item Name")
        table.heading("Date Added", text="Date Added")
        table.heading("Date Expiration", text="Date Expiration")
        table.column("Barcode ID", width=50, anchor=CENTER)
        table.column("Item Name", width=50, anchor=CENTER)
        table.column("Date Added", width=50, anchor=CENTER)
        table.column("Date Expiration", width=50, anchor=CENTER)
        table.pack(fill=BOTH, expand=YES, padx=50, pady=100)

        for row in data:
             table.insert("", "end", values=row)

    except Exception as e:
        print(f"Error on when getting inventory table {e}")

    finally:
        db.disconnect()

def addItemBtn():   # <-------------------------------- BUTTON ADD ITEM IN MENU
    for widget in target_frame.winfo_children():
        widget.destroy()

    global itemname_entry, barcode_image,day_combobox,month_combobox,year_combobox

    value = utilities.Util()

    days = value.generate_days()

    month = value.generate_months()

    itemname_label = ttk.Label(target_frame, text="Product Name", font=("Arial", 30, "bold"))
    itemname_label.place(x=100, y=50)

    itemname_entry = ttk.Entry(target_frame, width=30, font=("Arial", 30, "bold"))
    itemname_entry.place(x=380, y=50)

    itemname_entry.focus_set()

    expiration_date_label = ttk.Label(target_frame,text='Expiration Date (Days/Month/Year)', font=('Arial',30,'bold'))
    expiration_date_label.place(x=100, y= 150)

    day_combobox = ttk.Combobox(target_frame, values=days,width= 5,font=('Arial',30,'bold'))
    day_combobox.place(x=300,y=220)

    month_combobox = ttk.Combobox(target_frame,values=month, width=5, font= ('Arial',30,'bold'))
    month_combobox.place(x=450, y= 220)

    year_combobox = ttk.Combobox(target_frame,values=value.generate_years(),width=5,font=('Arial',30,'bold'))
    year_combobox.place(x=600,y=220)

    

    generate_btn = ttk.Button(target_frame,text="Register Item",width = 15,command=generateBtn)
    generate_btn.place(x=100, y=500)

    empty_image = ttk.PhotoImage(width=1, height=1)

    barcode_image = ttk.Label(target_frame, image=empty_image)
    barcode_image.place(x=300, y=400)




def getbarcode_value(event):
    global scanner_entry, info_label,dateofexpiration,dateadded,barcode_id

    value = str(scanner_entry.get)

    db = Database('mydatabase.db')

    try:
        

        data = db.fetch_all_query('SELECT * FROM inventory WHERE barcode_id = ?',(value))
        
        if len(data) == 0:
            print('Barcode ID Not Found!')
        else:
            info_label.pack_forget()
            
            scanner_entry = ttk.Entry(target_frame,width=0)
            scanner_entry.place(x=-100,y=-200)
            scanner_entry.focus_set()

            file_path = Path(f"C:/Users/Admin/Documents/freshtopia/barcde_images/{value}.png") ## <----------------------------- CHANGE
            img = ttk.PhotoImage(file=file_path)
            b_img = ttk.Label(target_frame,image=img)
            b_img.image = img
            b_img.place(x=500,y=200)

            product_information_label = ttk.Label(target_frame,text="Product Information",font=('Helvetica',25,'bold'))
            product_information_label.place(x=10,y=90)
            barcode_id_label = ttk.Label(target_frame,text=f"Barcode ID: \t\t{data[0][0]}",font=('Arial',20,'bold'))
            barcode_id_label.place(x=300,y=400)
            date_added_label = ttk.Label(target_frame,text=f"Date Added: \t\t{data[0][2]}",font=('Arial',20,'bold'))
            date_added_label.place(x=300,y=450)
            date_expiration_label = ttk.Label(target_frame,text=f"Date Expiration: \t\t{data[0][3]}",font=('Arial',20,'bold'))
            date_expiration_label.place(x=300,y=500)

            dateofexpiration = data[0][3]
            dateadded = data[0][2]
            barcode_id = data[0][0]
            

            pull_out_button = ttk.Button(target_frame,text='Pull Out Item',width=20,command=pull_out_cmnd_btn)
            pull_out_button.place(x=550,y=600)


        scanner_entry = ttk.Entry(target_frame,width=0)
        scanner_entry.place(x=-100,y=-200)
        scanner_entry.focus_set()
        scanner_entry.bind('<Return>',getbarcode_value)


    except Exception as e:
        print(e)
        traceback.print_exception()
    finally:
        db.disconnect()


def pull_out_cmnd_btn(): # <--------------------- PULL OUT BUTTON COMMAND

    
    db = Database('mydatabase.db')

    try:

        db.executeQuery('DELETE FROM storage WHERE barcode_id = ?',(barcode_id))

        Messagebox.show_info(target_frame,title='Item Removed',message=f"Barcode ID {barcode_id} has been removed from the database")

    except Exception as e:

        print(f"Error on pulling out an item \n{e}")

    finally:
        db.disconnect()


def scan_item_btn():

    for widget in target_frame.winfo_children():
        widget.destroy()

    global scanner_entry, info_label

    info_label = ttk.Label(target_frame,text="Scan a Barcode ID to check its Information",font=('Arial',50,'bold'))
    info_label.pack(padx=100,pady=200)


    scanner_entry = ttk.Entry(target_frame,width=0)
    scanner_entry.place(x=-100,y=-200)
    scanner_entry.focus_set()

    scanner_entry.bind('<Return>',getbarcode_value)



def generateBtn():
    
    if itemname_entry.get().strip() == '' or day_combobox.get().strip() == '' or month_combobox.get().strip() == '' or year_combobox.get().strip() == '':
        Messagebox.show_error(parent=target_frame,title='Input Field Missing',message='Please complete filling up the fields!',alert=True)
        return

    day = day_combobox.get()
    month = month_combobox.get()
    year = year_combobox.get()


    date_of_expiration = '-'.join([day,month,year])


    date_expired_obj = datetime.strptime(date_of_expiration,"%d-%m-%Y").date()


    db = Database('mydatabase.db')

    con = ConnectionPool().sql_connection()

    
    try:

        path = BC.generate_barcode_image()

        
        file = Path(f"./{path}.png") # need ilisan ang directory para sa linux

        Messagebox.show_info(title="Barcode Image Created!", message="Item added to the database", alert=True)

        img = ttk.PhotoImage(file=file)
        
        barcode_image.config(image=img)
        barcode_image.image = img
        
        cursor = con.cursor()

        query = """INSERT INTO inventory (barcode_id, item_name, date_added, date_expiration) VALUES(%s,%s,%s,%s)"""

        data = (str(path), itemname_entry.get(), df.format_datetime_to_fullname(datetime.now().date()), str(date_expired_obj))

        # data = db.executeQuery('INSERT INTO inventory (barcode_id, item_name, date_added, date_expiration) VALUES (?,?,?,?)',(path, itemname_entry.get(),str(current_date.strftime('%d-%m-%Y'))))

        


        itemname_entry.delete(0,ttk.END)
        day_combobox.delete(0,ttk.END)
        month_combobox.delete(0,ttk.END)
        year_combobox.delete(0,ttk.END)
        
    except Exception as e:
        print(f"Error in generated button {e}")
        traceback.print_exc()
    
    finally:
        db.disconnect()


def check_item_expiration():
    conn = connection.ConnectionPool().sql_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM storage")

    rows = cursor.fetchall()

    for row in rows:
        if row[0] in expired_products_list:
            continue
        if ex.is_expired(row[3]):
            
            led1.on()
        



def exitBtn():
    root.quit()
    SystemExit(0)



root = ttk.Window(themename="solar", title="Dynamic Frame Content", size=(1100, 600))
root.resizable(False, False)

control_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="ridge")
control_frame.pack(side=LEFT, fill=Y)

target_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="ridge")
target_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)

entry = ttk.Entry(width=15, font=('arial', 12, 'bold'))
entry.place_forget()

freshtopia_label = ttk.Label(target_frame, text="FRESHTOPIA: HARMONIZING FOOD STORAGE AND FRESHNESS",
                             font=("Arial", 35, "bold"))
freshtopia_label.pack(padx=30, pady=80)

control_label = ttk.Label(control_frame, text="Menu", font=("Arial", 14))
control_label.pack(pady=10)

chect_item = ttk.Button(control_frame, text="Inventory", command=change_frame_content, width=12)
chect_item.pack(pady=50, padx=20)

exit_btn = ttk.Button(control_frame, text='Exit', command=exitBtn, width=12)
exit_btn.place(x=20, y=600)

scan_item = ttk.Button(control_frame, text="Scan Item", width=12, command=scan_item_btn)
scan_item.place(x=20, y=150)

reg_item = ttk.Button(control_frame, text="Register Item", width=12, command=addItemBtn)
reg_item.place(x=20, y=210)

additem = ttk.Entry(width=12, font="arial")
additem.place_forget()

itemname_entry = ttk.Entry(width=30, font=("Arial", 12, "bold"))

day_combobox = ttk.Combobox()
month_combobox = ttk.Combobox()
year_combobox = ttk.Combobox()

scanner_entry = ttk.Entry()
info_label = ttk.Label(text='Scan a Barcode ID to check its Information')


if __name__ == '__main__':

    root.mainloop()
    
