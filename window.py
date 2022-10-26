from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class MainWindow:
    def __init__(self, root):
        # DATA INFORMATION FRAME
        self.dataFrame = ttk.Frame(root)
        self.dataFrame.configure(width=int(640/2), height=int(500/2))

        self.partNameVar = StringVar()
        self.partNameLabel = ttk.Label(self.dataFrame, text='Part Name')
        self.patternName = self.dataFrame.register(self.verify_name_is_empty)
        self.partNameEntry = ttk.Entry(self.dataFrame, textvariable=self.partNameVar,
                                       validate='focusout',
                                       validatecommand=self.patternName)

        self.customerVar = StringVar()
        self.customerLabel = ttk.Label(self.dataFrame, text='Customer')
        self.patternCustomer = self.dataFrame.register(self.verify_customer_is_empty)
        self.customerEntry = ttk.Entry(self.dataFrame, textvariable=self.customerVar,
                                       validate='focusout',
                                       validatecommand=self.patternCustomer)

        self.retailerVar = StringVar()
        self.retailerLabel = ttk.Label(self.dataFrame, text='Retailer')
        self.patternRetailer = self.dataFrame.register(self.verify_retailer_is_empty)
        self.retailerEntry = ttk.Entry(self.dataFrame, textvariable=self.retailerVar,
                                       validate='focusout',
                                       validatecommand=self.patternRetailer)

        self.priceVar = StringVar()
        self.priceLabel = ttk.Label(self.dataFrame, text='Price')
        self.patternPrice = self.dataFrame.register(self.verify_pattern_price)
        self.priceEntry = ttk.Entry(self.dataFrame, textvariable=self.priceVar,
                                    validate='focusout',
                                    validatecommand=self.patternPrice)

        self.lineDivisorLabel = ttk.Separator(self.dataFrame, orient='horizontal')

        self.addButton = ttk.Button(self.dataFrame, text='Add Part', style='Accent.TButton',
                                    command=self.verify_data_input)
        self.removeButton = ttk.Button(self.dataFrame, text='Remove Part', style='Accent.TButton',
                                       command=self.remove_selected_item)
        self.updateButton = ttk.Button(self.dataFrame, text='Update Part', style='Accent.TButton',
                                       command=self.update_data_input)
        self.clearButton = ttk.Button(self.dataFrame, text='Clear Input', style='Accent.TButton',
                                      command=self.clear_data_fields)

        # VIEW DATA INFORMATION FRAME
        self.viewDataFrame = ttk.Frame(root)
        self.viewDataFrame.configure(width=int(640 / 2), height=int(500 / 2))

        # LIST BOX OF INFORMATION
        self.dataList = ttk.Treeview(self.viewDataFrame,
                                    columns=('Id', 'Part Name', 'Customer', 'Retailer', 'Price'),
                                     show='headings')

        self.dataList.column('Id', width=40, minwidth=20)
        self.dataList.column('Part Name', width=140, minwidth=80)
        self.dataList.column('Customer', width=120, minwidth=75)
        self.dataList.column('Retailer', width=120, minwidth=70)
        self.dataList.column('Price', width=120, minwidth=70)
        self.dataList.heading('Id', text='ID', anchor='w')
        self.dataList.heading('Part Name', text='Part Name', anchor='w')
        self.dataList.heading('Customer', text='Customer', anchor='w')
        self.dataList.heading('Retailer', text='Retailer', anchor='w')
        self.dataList.heading('Price', text='Price', anchor='w')

        self.dataList.bind('<Double-1>', self.complete_fields_with_select_item)

        # ROLL SCROL TO LISTBOX
        self.scrollBarList = ttk.Scrollbar(self.viewDataFrame, orient=VERTICAL, command=self.dataList.yview)
        self.dataList.configure(yscrollcommand=self.scrollBarList)

        # FIRST ACTIONS
        self.draw_widgets()
        self.load_data()

        self.partNameEntry.focus_force()

    def draw_widgets(self):
        # DATA INFORMATION FRAME
        self.dataFrame.grid(row=0, column=0, pady=(10, 0))

        self.partNameLabel.grid(row=0, column=0, padx=(20, 30), pady=(20, 15), sticky='w')
        self.partNameEntry.grid(row=0, column=1, pady=(20, 15), padx=(0, 25), sticky='w')

        self.customerLabel.grid(row=0, column=2, padx=(10, 30), pady=(20, 15), sticky='w')
        self.customerEntry.grid(row=0, column=3, pady=(20, 15), sticky='w')

        self.retailerLabel.grid(row=1, column=0, padx=(20, 30), pady=(0, 15), sticky='w')
        self.retailerEntry.grid(row=1, column=1, padx=(0, 25), pady=(0, 15), sticky='w')

        self.priceLabel.grid(row=1, column=2, padx=(10, 30), pady=(0, 15), sticky='w')
        self.priceEntry.grid(row=1, column=3, pady=(0, 20), sticky='w')

        self.lineDivisorLabel.grid(row=2, columnspan=5, padx=(10, 0), pady=(5, 5), sticky='we')

        self.addButton.grid(row=3, column=0, padx=(20, 0), pady=(10, 0))
        self.removeButton.grid(row=3, column=1, padx=(10, 0), pady=(10, 0))
        self.updateButton.grid(row=3, column=2, padx=(10, 0), pady=(10, 0))
        self.clearButton.grid(row=3, column=3, padx=(10, 0), pady=(10, 0))

        # VIEW DATA INFORMATION FRAME
        self.viewDataFrame.grid(row=1, column=0, padx=(20, 0))

        self.dataList.grid(row=1, column=0, pady=(20, 10), sticky='sw')
        self.scrollBarList.grid(row=1, column=1, columnspan=1, pady=(45, 15), sticky='ns')

    def load_data(self):
        # LOAD DATA ON FILE
        try:
            with open('dataBase.txt', 'r', encoding='utf-8') as db:
                for item in db.readlines():
                    item = item.split(',')
                    self.dataList.insert('', END, values=(item[0], item[1], item[2], item[3], item[4]))
                db.close()
        except:
            pass

    def count_lines_to_id(self):
        # RETURN THE ID OR INFO IF THERE ARE NO INFORMATION
        id = 1
        try:
            with open('dataBase.txt', 'r', encoding='utf-8') as db:
                for lines in db.readlines():
                    id += 1
                db.close()
            return id
        except:
            return id

    def verify_data_input(self):
        name = self.partNameVar.get()
        customer = self.customerVar.get()
        retailer = self.retailerVar.get()
        price = self.priceVar.get()

        if name == '' or customer == '' or retailer == '' or price == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
        else:
            if price.isdigit() == False:
                messagebox.showwarning('Field Erro', 'Price must be a number')
            else:
                self.add_data_input()

    def verify_name_is_empty(self):
        name = self.partNameVar.get()
        if name == '':
            return False
        else:
            return True
    def verify_customer_is_empty(self):
        customer = self.customerVar.get()
        if customer == '':
            return False
        else:
            return True
    def verify_retailer_is_empty(self):
        retailer = self.retailerVar.get()
        if retailer == '':
            return False
        else:
            return True
    def verify_pattern_price(self):
        price = self.priceVar.get()
        if price.isdigit():
            return True
        else:
            return False

    def add_data_input(self):
        # LOAD DATA INFORMATION TO NEWS VARIABLES
        id = self.count_lines_to_id()
        name = self.partNameVar.get().upper()
        customer = self.customerVar.get().title()
        retailer = self.retailerVar.get().capitalize()
        price = self.priceVar.get()

        if id == 1:
            with open('dataBase.txt', 'w', encoding='utf-8') as db:
                db.write(f'{id},'
                         f'{name},'
                         f'{customer},'
                         f'{retailer},'
                         f'{price}\n')
                db.close()
            self.dataList.insert('', END, values=(id, name, customer, retailer, price))
        else:
            with open('dataBase.txt', 'a', encoding='utf-8') as db:
                db.write(f'{id},'
                         f'{name},'
                         f'{customer},'
                         f'{retailer},'
                         f'{price}\n')
                db.close()
            self.dataList.insert('', END, values=(id, name, customer, retailer, price))

        self.clear_data_fields()

    def clear_data_fields(self):
        self.partNameVar.set('')
        self.customerVar.set('')
        self.retailerVar.set('')
        self.priceVar.set('')
        self.partNameEntry.focus()

    def catch_select_item(self, *args):
        index = self.dataList.selection()[0]
        item = self.dataList.item(index)['values']
        return item

    def complete_fields_with_select_item(self, *args):
        id, name, customer, retailer, price = self.catch_select_item()
        self.partNameVar.set(name)
        self.customerVar.set(customer)
        self.retailerVar.set(retailer)
        self.priceVar.set(price)
        self.partNameEntry.focus()
        self.partNameEntry.icursor(END)

    def update_data_input(self):
        try:
            oldId = str(self.catch_select_item()[0])

            readDB = open('dataBase.txt', 'r')
            for x, line in enumerate(readDB.readlines()):
                line = line.split(',')
                if line[0] == oldId:
                    pass
        except:
            pass

        # doing

    def remove_selected_item(self):
        pass

        # doing


