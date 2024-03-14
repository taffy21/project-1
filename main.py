from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.pickers.datepicker import MDDatePicker

from mydb import *

class MyManager(ScreenManager):
    pass


class LoadingPage(MDScreen):
    '''This class is the loading page.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.switch_screen, 2)

    def switch_screen(self, dt):
        self.manager.current = 'landing'

class LandingPage(MDScreen):
    pass

class PaymentsLandingPage(MDScreen):
    PaymentDate = ObjectProperty()
    CycleNumber = NumericProperty()
    MembersList = ListProperty()

    def to_home(self):
        self.manager.current = 'landing'
        self.ids.datefield.text = ""
        self.ids.cycle.text = ""

    def nextPage(self):
        self.PaymentDate = self.ids.datefield
        try:
            self.CycleNumber = self.ids.cycle.text
            # run database
            query2 = "SELECT FirstName, Surname, MemberID FROM members"
            f = execute_sql_query(query2)
            self.MembersList = f.fetchall()
            # move to next page
            self.manager.current = 'entryPayments'
        except ValueError:
            failure = MDDialog(title='Entry Failure', text='Enter the Cycle Field!', size_hint=(0.5, 0.5),
                               auto_dismiss=True, elevation=0)
            failure.open()


class PaymentsEntryPage(MDScreen):
    my_text = StringProperty()
    my_list = ListProperty()
    my_date = ObjectProperty()
    my_cycle = NumericProperty()

    def to_home(self):
        self.manager.current = 'landing'
        self.clear()


    def membersName(self):
        self.name_dropdown = []
        self.my_list = self.manager.get_screen('landPayments').MembersList

        for name in self.my_list:
            modified_name = name[0] + " " + name[1] + " " + str(name[2])
            self.name_dropdown.append({
                "viewclass": "OneLineListItem",
                "text": f"{modified_name}",
                "on_release": lambda x=f"{modified_name}": self.call_back_names(x)
            })

        self.name_type = MDDropdownMenu(
            caller=self.ids.drop_item2,
            items=self.name_dropdown,
            width_mult=4
        )
        self.name_type.open()

    def call_back_names(self, text):
        self.ids.person_name.text = text

    def paymentTypeMenu(self):
        self.payment_type_dropdown = [
            {
                "viewclass": "OneLineListItem",
                "text": "Routine Contribution",
                "on_release": lambda x="Routine Contribution": self.call_back_payment(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Loan Repayment",
                "on_release": lambda x="Loan Repayment": self.call_back_payment(x)
            }

        ]
        self.menu_payment_type = MDDropdownMenu(
            caller=self.ids.drop_item2,
            items=self.payment_type_dropdown,
            width_mult=4
        )
        self.menu_payment_type.open()

    def call_back_payment(self, text):
        self.ids.payment_type.text = text

    def clear(self):
        self.ids.payment_type.text = ""
        self.ids.person_name.text = ""
        self.ids.pay_amount.text = ""

    def addPayment(self):
        # date and cycle from previous page
        my_date = self.manager.get_screen('landPayments').PaymentDate
        my_cycle = self.manager.get_screen('landPayments').CycleNumber

        # entry into database
        try:
            g = add_payment(self.ids.person_name, my_date, self.ids.payment_type, self.ids.pay_amount, my_cycle)
            self.my_text = g
        except ValueError:
            failure = MDDialog(title='Entry Failure', text='Enter Valid Number!', size_hint=(0.5, 0.5),
                               auto_dismiss=True, elevation=0)
            failure.open()
        self.manager.get_screen('register').my_dialogue(self.my_text)



class LoansPage(MDScreen):
    my_list = ListProperty()

    def to_home(self):
        self.manager.current = 'landing'
        self.ids.date_loan.text = ""
        self.clear()

    def membersName(self):
        self.name_dropdown = []

        query2 = "SELECT FirstName, Surname, MemberID FROM members"
        f = execute_sql_query(query2)
        self.my_list = f.fetchall()

        for name in self.my_list:
            modified_name = name[0] + " " + name[1] + " " + str(name[2])
            self.name_dropdown.append({
                "viewclass": "OneLineListItem",
                "text": f"{modified_name}",
                "on_release": lambda x=f"{modified_name}": self.call_back_names(x)
            })

        self.name_type = MDDropdownMenu(
            caller=self.ids.drop_item_loans,
            items=self.name_dropdown,
            width_mult=4
        )
        self.name_type.open()

    def call_back_names(self, text):
        self.ids.loanee_name.text = text


    def addLoan(self):
        # section on loans
        # entry into database
        h = add_loan(self.ids.loanee_name, self.ids.date_loan, self.ids.loan_amount)
        self.my_text = h
        self.manager.get_screen('register').my_dialogue(self.my_text)


    def clear(self):
        self.ids.loanee_name.text = ""
        self.ids.loan_amount.text = ""

    def on_save(self, instance, value, date_range):
        """Saves the Date"""
        self.ids.date_loan.text = str(value)

    def on_cancel(self, instance, value):
        """Cancels the Date"""
        self.ids.date_loan.text = ""

    def show_date_picker(self):
        """Opens Date Picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


class RegisterMemberPage(MDScreen):
    """Registers a new member to the Organisation"""
    my_text = StringProperty()

    def to_home(self):
        """Returns Home"""
        self.manager.current = 'landing'

    def on_save(self, instance, value, date_range):
        """Saves the Date"""
        self.ids.birthday.text = str(value)

    def on_cancel(self, instance, value):
        """Cancels the Date"""
        self.ids.birthday.text = ""

    def show_date_picker(self):
        """Opens Date Picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def show_gender(self):
        """Opens Gender Picker"""
        self.gender_dropdown = [
            {
                "viewclass": "OneLineListItem",
                "text": "Male",
                "on_release": lambda x="Male": self.call_back_gender(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Female",
                "on_release": lambda x="Female": self.call_back_gender(x)
            }

        ]
        self.gender_type = MDDropdownMenu(
            caller=self.ids.gender,
            items=self.gender_dropdown,
            width_mult=4
        )
        self.gender_type.open()

    def call_back_gender(self, text):
        self.ids.gender.text = text

    def clear(self):
        """Clears Entry"""
        self.ids.name.text = ""
        self.ids.surname.text = ""
        self.ids.gender.text = ""
        self.ids.birthday.text = ""
        self.ids.address.text = ""
        self.ids.number.text = ""

    def addMember(self):
        """Adds New Member to DB"""
        f = add_entry(self.ids.name, self.ids.surname, self.ids.gender, self.ids.birthday, self.ids.address, self.ids.number)
        self.my_text = f
        self.my_dialogue(self.my_text)

    def my_dialogue(self, context):
        """Opens Dialogue Box"""
        if context == "success":
            successful = MDDialog(title="Member Entry", text="Success!", size_hint=(0.5, 0.5),
                                  auto_dismiss=True, elevation=0)
            successful.open()


        elif context == "name_exists":
            unsuccessful = MDDialog(title="Member Entry Failure", text="Already in the database",
                                    size_hint=(0.5, 0.5),
                                    auto_dismiss=True, elevation=0)
            unsuccessful.open()
        else:
            failure = MDDialog(title='Member Entry Failure', text='There are missing fields!', size_hint=(0.5, 0.5),
                               auto_dismiss=True, elevation=0)
            failure.open()


# ALL THE VIEWS OCCUR AFTER THIS LINE
class ViewMembersPage(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDBoxLayout(orientation='vertical')
        self.bar = MDTopAppBar(title="Membership", left_action_items=[['menu']],
                               right_action_items=[["home", lambda x: self.home()],
                                                   ["refresh", lambda x: self.refresh()]])
        self.space = MDLabel(text='', size_hint_y=0.05)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("ID", dp(25)), ("FirstName", dp(25)), ("Surname", dp(25)), ("Gender", dp(25))],
            row_data=self.view_data(),
            size_hint=(0.90, 0.80),
            pos_hint={"center_x": 0.5, 'center_y': 0.43},
            sorted_on="Word",
            sorted_order='ASC',
            elevation=2,
            background_color_header="lightblue")

        self.data_tables.bind(on_check_press=self.select_row)
        self.box.add_widget(self.bar)
        self.box.add_widget(self.space)
        self.box.add_widget(self.data_tables)
        self.add_widget(self.box)

    def view_data(self):
        contact_list = view_member_data()
        my_list = []
        for item in contact_list:
            my_list.append(item)
        return my_list

    def select_row(self, instance_table, instance_row):
        pkey = instance_row[0]
        query = f'DELETE FROM members WHERE MemberID = ?'
        self.deletion_dialogue(query, pkey)

    def deletion_dialogue(self, query, pkey):

        self.successful_del = MDDialog(title="Item Deletion",
                                       text=f"Are you you want to delete {pkey} from the records?",
                                       size_hint=(0.5, 0.5),
                                       auto_dismiss=False, elevation=0, buttons=[
                MDRaisedButton(text="Yes", on_press=lambda x: execute_sql_query(query, (pkey,)),
                               on_release=self.close_dialog),
                MDRaisedButton(text="No", on_release=self.close_dialog)])
        self.successful_del.open()

    def close_dialog(self, instance):
        if self.successful_del:
            self.successful_del.dismiss()
            self.data_tables.row_data = self.view_data()

    def home(self):
        self.manager.current = 'landing'

    def refresh(self):
        self.data_tables.row_data = self.view_data()

class ViewPaymentsPage(MDScreen):
    # Only for Viewing
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDBoxLayout(orientation='vertical')
        self.bar = MDTopAppBar(title="Payments", left_action_items=[['menu']],
                               right_action_items=[["home", lambda x: self.home()],
                                                   ["printer",],
                                                   ["refresh", lambda x: self.refresh()]])
        self.space = MDLabel(text='', size_hint_y=0.05)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("Date", dp(25)), ("FirstName", dp(25)), ("Surname", dp(25)), ("CycleNo.", dp(25)),
                         ("PayType", dp(25)), ("Amount", dp(25))],
            row_data=self.view_data(),
            size_hint=(0.90, 0.80),
            pos_hint={"center_x": 0.5, 'center_y': 0.43},
            sorted_on="Date",
            sorted_order='DSC',
            elevation=2,
            background_color_header="lightblue")


        self.box.add_widget(self.bar)
        self.box.add_widget(self.space)
        self.box.add_widget(self.data_tables)
        self.add_widget(self.box)

    def view_data(self):
        contact_list = view_payments_data()
        my_list = []
        for item in contact_list:
            my_list.append(item)
        return my_list
    def home(self):
        self.manager.current = 'landing'

    def refresh(self):
        self.data_tables.row_data = self.view_data()

class ViewLoansPage(MDScreen):
    # Only for Viewing
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDBoxLayout(orientation='vertical')
        self.bar = MDTopAppBar(title="Loans", left_action_items=[['menu']],
                               right_action_items=[["home", lambda x: self.home()],
                                                   ["printer",],
                                                   ["refresh", lambda x: self.refresh()]])
        self.space = MDLabel(text='', size_hint_y=0.05)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("Date", dp(25)), ("FirstName", dp(25)), ("Surname", dp(25)),("LoanAmt", dp(25))],
            row_data=self.view_data(),
            size_hint=(0.90, 0.80),
            pos_hint={"center_x": 0.5, 'center_y': 0.43},
            sorted_on="Date",
            sorted_order='ASC',
            elevation=2,
            background_color_header="lightblue")


        self.box.add_widget(self.bar)
        self.box.add_widget(self.space)
        self.box.add_widget(self.data_tables)
        self.add_widget(self.box)

    def view_data(self):
        contact_list = view_loans_data()
        my_list = []
        for item in contact_list:
            my_list.append(item)
        return my_list
    def home(self):
        self.manager.current = 'landing'

    def refresh(self):
        self.data_tables.row_data = self.view_data()

class ViewContributionsPage(MDScreen):
    # Only for Viewing
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDBoxLayout(orientation='vertical')
        self.bar = MDTopAppBar(title="Total Contribution", left_action_items=[['menu']],
                               right_action_items=[["home", lambda x: self.home()],
                                                   ["printer", ],
                                                   ["refresh", lambda x: self.refresh()]])
        self.space = MDLabel(text='', size_hint_y=0.05)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("ID", dp(25)), ("FirstName", dp(25)), ("Surname", dp(25)),("Amount", dp(25))],
            row_data=self.view_data(),
            size_hint=(0.90, 0.80),
            pos_hint={"center_x": 0.5, 'center_y': 0.43},
            sorted_on="Date",
            sorted_order='ASC',
            elevation=2,
            background_color_header="lightblue")


        self.box.add_widget(self.bar)
        self.box.add_widget(self.space)
        self.box.add_widget(self.data_tables)
        self.add_widget(self.box)

    def view_data(self):
        contact_list = view_contributions_data()
        my_list = []
        for item in contact_list:
            my_list.append(item)
        return my_list
    def home(self):
        self.manager.current = 'landing'

    def refresh(self):
        self.data_tables.row_data = self.view_data()


class ViewAmountDuePage(MDScreen):
    # Only for Viewing
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDBoxLayout(orientation='vertical')
        self.bar = MDTopAppBar(title="Amount Due", left_action_items=[['menu']],
                               right_action_items=[["home", lambda x: self.home()],
                                                   ["printer", ],
                                                   ["refresh", lambda x: self.refresh()]])
        self.space = MDLabel(text='', size_hint_y=0.05)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[("ID", dp(25)), ("FirstName", dp(25)), ("Surname", dp(25)),("AmountDue", dp(25))],
            row_data=self.view_data(),
            size_hint=(0.90, 0.80),
            pos_hint={"center_x": 0.5, 'center_y': 0.43},
            sorted_on="Date",
            sorted_order='ASC',
            elevation=2,
            background_color_header="lightblue")


        self.box.add_widget(self.bar)
        self.box.add_widget(self.space)
        self.box.add_widget(self.data_tables)
        self.add_widget(self.box)

    def view_data(self):
        contact_list = view_amount_due()
        my_list = []
        for item in contact_list:
            my_list.append(item)
        return my_list
    def home(self):
        self.manager.current = 'landing'

    def refresh(self):
        self.data_tables.row_data = self.view_data()



class MainApp(MDApp):
    def build(self):
        pass

    def on_save(self, instance, value, date_range):
        self.root.children[0].ids.datefield.text = str(value)

    def on_cancel(self, instance, value):
        self.root.children[0].ids.datefield.text = ""


    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel = self.on_cancel)
        date_dialog.open()

if __name__ == "__main__":
    MainApp().run()





