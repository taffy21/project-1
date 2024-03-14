import sqlite3
import datetime
from kivymd.uix.dialog import MDDialog

dbase = 'hundreddc.db'
def execute_sql_query(query, parameters=()):
    with sqlite3.connect(dbase) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute(query, parameters)
        conn.commit()
    return query_result

def validate_entry(ids1, ids2, ids3):
    return len(ids1.text) != 0 and len(ids2.text) != 0 and len(ids3.text) != 0

def add_entry(ids1, ids2, ids3, ids4, ids5, ids6):
    """add member into database"""

    if validate_entry(ids1, ids2, ids3):
        query = "INSERT INTO members (FirstName, Surname, Gender, DateOfBirth, Address, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (ids1.text, ids2.text, ids3.text, ids4.text, ids5.text, ids6.text)
        try:
            execute_sql_query(query, parameters)
            ids1.text = ""
            ids2.text = ""
            ids3.text = ""
            ids4.text = ""
            ids5.text = ""
            ids6.text = ""
            context = 'success'

        except:
            ids1.text = ""
            ids2.text = ""
            ids3.text = ""
            ids4.text = ""
            ids5.text = ""
            ids6.text = ""
            context = "name_exists"
    else:
        context = 'failure'

    return context

def add_payment(ids1, ids2, ids3, ids4, ids5):
    """add payment into database"""

    if validate_entry(ids1, ids2, ids3):
        query = "INSERT INTO payments (MemberID, Date, PaymentType, AmountPaid, CycleNumber) VALUES (?, ?, ?, ?, ?)"
        parameters = (int(ids1.text.split()[2]), ids2.text, ids3.text, float(ids4.text), ids5)

        try:
            execute_sql_query(query, parameters)
            ids1.text = ""
            ids3.text = ""
            ids4.text = ""
            context2 = 'success'

        except:

            ids1.text = ""
            ids3.text = ""
            ids4.text = ""
            context2 = "entry_exists"

    else:
        context2 = 'failure'

    return context2

def add_loan(ids1, ids2, ids3):
    """add loans into database"""

    if validate_entry(ids1, ids2, ids3):
        query = "INSERT INTO loans (MemberID, Date, Amount_Loaned) VALUES (?, ?, ?)"
        try:
            parameters = (int(ids1.text.split()[2]), ids2.text, float(ids3.text))
        except:
            pass

        try:
            execute_sql_query(query, parameters)
            ids1.text = ""
            ids3.text = ""
            context2 = 'success'

        except:

            ids1.text = ""
            ids3.text = ""
            context2 = "entry_exists"

    else:
        context2 = 'failure'

    return context2

def view_member_data():
    query = "SELECT MemberID, FirstName, Surname, Gender FROM members"
    member_list = execute_sql_query(query)
    return member_list

def view_payments_data():
    query = """SELECT payments.Date, members.FirstName, members.Surname, payments.CycleNumber, payments.PaymentType, 
    payments.AmountPaid FROM members INNER JOIN payments ON members.MemberID = payments.MemberID ORDER BY payments.Date DESC;"""
    payment_list = execute_sql_query(query)
    return payment_list

def view_loans_data():
    query = """SELECT loans.Date, members.FirstName, members.Surname, loans.Amount_Loaned
     FROM members INNER JOIN loans ON members.MemberID = loans.MemberID ORDER BY loans.Date DESC;"""
    payment_list = execute_sql_query(query)
    return payment_list

def view_contributions_data():
    query = """SELECT
        members.MemberID,
        members.FirstName,
        members.Surname,
        PaymentSummary.TotalAmountPaid
    FROM
        members
    INNER JOIN (
        SELECT
            MemberID,
            SUM(AmountPaid) AS TotalAmountPaid
        FROM
            payments
        GROUP BY
            MemberID
    ) AS PaymentSummary ON members.MemberID = PaymentSummary.MemberID;"""
    contributions_list = execute_sql_query(query)
    return contributions_list

def view_amount_due():
    query = """SELECT
    members.MemberID,
    members.FirstName,
    members.Surname,
    IFNULL(LoanDetails.AmountLoaned, 0) - IFNULL(PaymentDetails.TotalLoanRepayment, 0) AS OutstandingLoan
    FROM
        members
    LEFT JOIN (
        SELECT
            MemberID,
            SUM(Amount_Loaned) AS AmountLoaned
        FROM
            loans
        GROUP BY
            MemberID
    ) AS LoanDetails ON members.MemberID = LoanDetails.MemberID
    LEFT JOIN (
        SELECT
            MemberID,
            SUM(AmountPaid) AS TotalLoanRepayment
        FROM
            payments
        WHERE
            PaymentType = 'Loan Repayment'
        GROUP BY
            MemberID
    ) AS PaymentDetails ON members.MemberID = PaymentDetails.MemberID;"""
    due_list = execute_sql_query(query)
    return due_list

def day_activities():
    pass