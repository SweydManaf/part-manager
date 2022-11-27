from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from DBAdmin import BancoDeDados


class MainWindow:
    def __init__(self, root):
        self.bancoDeDados = BancoDeDados()
        self.order = 1

        # DATA INFORMATION FRAME
        self.dataFrame = ttk.Frame(root)
        self.dataFrame.configure(width=int(640 / 2), height=int(500 / 2))

        self.partNameVar = StringVar()
        self.partNameLabel = ttk.Label(self.dataFrame, text='Part Name')
        self.patternName = self.dataFrame.register(self.verify_name_is_empty)
        self.partNameEntry = ttk.Entry(self.dataFrame, textvariable=self.partNameVar,
                                       validate='focusout',
                                       validatecommand=self.patternName)
        self.partNameEntry.bind('<Return>', self.bind_change_name_to_customer)

        self.customerVar = StringVar()
        self.customerLabel = ttk.Label(self.dataFrame, text='Customer')
        self.patternCustomer = self.dataFrame.register(self.verify_customer_is_empty)
        self.customerEntry = ttk.Entry(self.dataFrame, textvariable=self.customerVar,
                                       validate='focusout',
                                       validatecommand=self.patternCustomer)
        self.customerEntry.bind('<Return>', self.bind_change_customer_to_retailer)

        self.retailerVar = StringVar()
        self.retailerLabel = ttk.Label(self.dataFrame, text='Retailer')
        self.patternRetailer = self.dataFrame.register(self.verify_retailer_is_empty)
        self.retailerEntry = ttk.Entry(self.dataFrame, textvariable=self.retailerVar,
                                       validate='focusout',
                                       validatecommand=self.patternRetailer)
        self.retailerEntry.bind('<Return>', self.bind_change_retailer_to_price)

        self.priceVar = StringVar()
        self.priceLabel = ttk.Label(self.dataFrame, text='Price')
        self.patternPrice = self.dataFrame.register(self.verify_pattern_price)
        self.priceEntry = ttk.Entry(self.dataFrame, textvariable=self.priceVar,
                                    validate='focusout',
                                    validatecommand=self.patternPrice)
        self.priceEntry.bind('<Return>', self.bind_change_price_to_addpart)

        self.lineDivisorLabel = ttk.Separator(self.dataFrame, orient='horizontal')

        self.addButton = ttk.Button(self.dataFrame, text='Add Part', style='Accent.TButton',
                                    command=self.verify_data_input)
        self.addButton.bind('<Return>', self.bind_add_part)
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
        self.dataList.heading('Id', text='ID', anchor='w', command=self.sort_list_by_id)
        self.dataList.heading('Part Name', text='Part Name', anchor='w', command=self.sort_list_by_partname)
        self.dataList.heading('Customer', text='Customer', anchor='w', command=self.sort_list_by_customer)
        self.dataList.heading('Retailer', text='Retailer', anchor='w', command=self.sort_list_by_retailer)
        self.dataList.heading('Price', text='Price', anchor='w', command=self.sort_list_by_price)

        self.dataList.bind('<Double-1>', self.complete_fields_with_select_item)

        # ROLL SCROL TO LISTBOX
        self.scrollBarList = ttk.Scrollbar(self.viewDataFrame, orient=VERTICAL, command=self.dataList.yview)
        self.dataList.configure(yscrollcommand=self.scrollBarList)

        # FIRST ACTIONS
        self.draw_widgets()
        self.call_load_data()

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

    def bind_change_name_to_customer(self, *args):
        self.customerEntry.focus()

    def bind_change_customer_to_retailer(self, *args):
        self.retailerEntry.focus()

    def bind_change_retailer_to_price(self, *args):
        self.priceEntry.focus()

    def bind_change_price_to_addpart(self, *args):
        self.add_data_input()

    def call_load_data(self):
        self.load_data(self.bancoDeDados.list_parts())

    def sort_list_by_id(self, *args):
        self.clear_data_fields()
        if self.order:
            self.load_data(self.bancoDeDados.list_parts_by_id(self.order))
            self.order = 0
        else:
            self.load_data(self.bancoDeDados.list_parts_by_id(self.order))
            self.order = 1
    def sort_list_by_partname(self, *args):
        self.clear_data_fields()
        if self.order:
            self.load_data(self.bancoDeDados.list_parts_by_partname(self.order))
            self.order = 0
        else:
            self.load_data(self.bancoDeDados.list_parts_by_partname(self.order))
            self.order = 1

    def sort_list_by_customer(self, *args):
        self.clear_data_fields()
        if self.order:
            self.load_data(self.bancoDeDados.list_parts_by_customer(self.order))
            self.order = 0
        else:
            self.load_data(self.bancoDeDados.list_parts_by_customer(self.order))
            self.order = 1

    def sort_list_by_retailer(self, *args):
        self.clear_data_fields()
        if self.order:
            self.load_data(self.bancoDeDados.list_parts_by_retailer(self.order))
            self.order = 0
        else:
            self.load_data(self.bancoDeDados.list_parts_by_retailer(self.order))
            self.order = 1

    def sort_list_by_price(self, *args):
        self.clear_data_fields()
        if self.order:
            self.load_data(self.bancoDeDados.list_parts_by_price(self.order))
            self.order = 0
        else:
            self.load_data(self.bancoDeDados.list_parts_by_price(self.order))
            self.order = 1

    def load_data(self, data):
        # CLEAN THE TREEVIEW
        for item in self.dataList.get_children():
            self.dataList.delete(item)

        # LOAD DATA ON FILE
        print(data)
        try:
            for item in data:
                print(item)
                self.dataList.insert('', END, values=(item[0], item[1], item[2], item[3], item[4]))
        except Exception as e:
            print(e)
            messagebox.showwarning('SEVERAL ERRO', 'A CRITICAL ERROR OCURRED. PLEASE REPORT')


    def verify_data_input(self):
        name = self.partNameVar.get()
        customer = self.customerVar.get()
        retailer = self.retailerVar.get()
        price = self.priceVar.get()

        if name == '' or customer == '' or retailer == '' or price == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
        else:
            if not price.isdigit():
                messagebox.showwarning('Field Erro', 'Price must be a integer number')
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
        name = self.partNameVar.get().upper()
        customer = self.customerVar.get().title()
        retailer = self.retailerVar.get().capitalize()
        price = self.priceVar.get()

        if not self.bancoDeDados.insert_new_part(name, customer, retailer, price):
            messagebox.showwarning('Part Repeated', 'This part already add')

        self.call_load_data()

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

    def bind_add_part(self, *args):
        self.add_data_input()

    def complete_fields_with_select_item(self, *args):
        id, name, customer, retailer, price = self.catch_select_item()
        self.partNameVar.set(name)
        self.customerVar.set(customer)
        self.retailerVar.set(retailer)
        self.priceVar.set(price)
        self.partNameEntry.focus()
        self.partNameEntry.icursor(END)

    def update_data_input(self):
        selected_datas = self.catch_select_item()

        name = self.partNameVar.get().upper()
        customer = self.customerVar.get().title()
        retailer = self.retailerVar.get().capitalize()
        price = self.priceVar.get()

        self.bancoDeDados.update_part(selected_datas[0], name, customer, retailer, price)

        self.call_load_data()
        self.clear_data_fields()
        self.partNameEntry.focus()

    def remove_selected_item(self):
        index = self.dataList.selection()[0]
        item = self.dataList.item(index)['values']

        self.bancoDeDados.delete_part(str(item[0]))

        self.call_load_data()
        self.partNameEntry.focus()
