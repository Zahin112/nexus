from django.shortcuts import render,redirect
from django.db import connection
import datetime


import hashlib

def home(request):
    if 'LogIn_Id' in request.session:
        return redirect('currentuser')
    else:
        return render(request, 'identification/home.html')

#ROLE_ID
#AGENT-1
#Customer-0

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'identification/signupuser.html')
    else:
        cursor = connection.cursor()
        name = request.POST['username']
        sql = "SELECT * FROM LOGIN WHERE LogIn_Username = %s"
        cursor.execute(sql,[name])
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            return render(request, 'identification/signupuser.html', {'error':'Username already exist! Try another one.'})
        else:
            cursor = connection.cursor()
            num = request.POST['mobile']
            sql = "SELECT * FROM eUSER WHERE User_MobileNo = %s "
            cursor.execute(sql,[num])
            res = cursor.fetchone()
            cursor.close()
            if res is not None:
                return render(request, 'identification/signupuser.html', {'error':'Mobile number already exist! Try another one.'})
            else:
                if request.POST['password1'] == request.POST['password2']:
                    s = request.POST['username']
                    a = abs(hash(s)) % (10 ** 5)
                    if request.POST['role'].upper() == 'AGENT' or request.POST['role'].upper() == 'CUSTOMER':
                        cursor = connection.cursor()
                        sql = "INSERT INTO LOGIN VALUES(%s,%s,%s)"
                        cursor.execute(sql,[a,request.POST['username'],request.POST['password1']])
                        connection.commit()
                        cursor.close()
                    else:
                        return render(request, 'identification/signupuser.html', {'error':'Role must be Agent or Customer'})


                    cursor = connection.cursor()
                    sql = "INSERT INTO ACCOUNT VALUES(%s,%s,%s)"
                    if request.POST['role'].upper() == 'AGENT':
                        cursor.execute(sql,[request.POST['mobile'],'100000',''])
                    else:
                        cursor.execute(sql,[request.POST['mobile'],'0.0',''])
                    connection.commit()
                    cursor.close()


                    cursor = connection.cursor()
                    sql = "INSERT INTO eUSER VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                    if request.POST['role'].upper() == 'AGENT':
                        cursor.execute(sql, [a,request.POST['name'], request.POST['mobile'], request.POST['email'], request.POST['address'], a, request.POST['mobile'], 'Agent'])
                    else:
                         cursor.execute(sql, [a,request.POST['name'], request.POST['mobile'], request.POST['email'], request.POST['address'], a, request.POST['mobile'], 'Customer'])
                    connection.commit()
                    cursor.close()

                    request.session['LogIn_Id'] = str(a)
                    request.session['LogIn_Username'] = request.POST['username']
                    return redirect('currentuser')
                else:
                    return render(request, 'identification/signupuser.html', {'error':'Password did not match'})




def loginuser(request):
    if 'LogIn_Id' in request.session:
        return redirect('currentuser')
    else:
        if request.method == 'GET':
            return render(request, 'identification/loginuser.html')
        else:
            cursor = connection.cursor()
            name = request.POST['username']
            password = request.POST['password']
            sql = "SELECT * FROM LOGIN WHERE LogIn_Username = %s"
            cursor.execute(sql,[name])
            result = cursor.fetchone()
            cursor.close()

            if result is not None:
                id = result[0]
                name = result[1]
                r = result[2]
                if password == r:
                    request.session['LogIn_Id'] = str(id)
                    request.session['LogIn_Username'] = name
                    return redirect('currentuser')
                else:
                    return render(request, 'identification/loginuser.html' , {'error':'Username or password did not match'})
            else:
                return render(request, 'identification/loginuser.html' , {'error':'Username or password did not match'})

def logoutuser(request):
    try:
        del request.session['LogIn_Id']
        del request.session['LogIn_Username']
    except KeyError:
        return render(request, 'identification/loginuser.html' , {'error':'Not Logged In!!'})
    return redirect('loginuser')


def updateprofile(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            cursor = connection.cursor()
            sql = "SELECT * FROM eUSER WHERE LogIn_Id = %s"
            cursor.execute(sql,[request.session['LogIn_Id']])
            result = cursor.fetchone()
            cursor.close()

            dict_result = {'name':result[1], 'mail':result[3], 'address':result[4]}

            return render(request, 'identification/updateprofile.html', {'dict_result':dict_result})

        else:
            name = request.POST['name']
            mail = request.POST['email']
            address = request.POST['address']

            cursor = connection.cursor()
            sql = "UPDATE eUSER SET User_Name = '"
            sql += name
            sql += "', User_Email = '"
            sql += mail
            sql += "', User_Address = ' "
            sql += address
            sql += "'"
            sql += "WHERE LogIn_Id = %s"
            cursor.execute(sql,[request.session['LogIn_Id']])

            return redirect('currentuser')


    else:
        return redirect('loginuser')

def currentuser(request):
    if 'LogIn_Id' in request.session:
        name = request.session['LogIn_Username']
        id = request.session['LogIn_Id']

        cursor = connection.cursor()
        sql = "SELECT Role_Name FROM eUSER WHERE LogIn_Id = %s"
        cursor.execute(sql,[id])
        result = cursor.fetchone()
        cursor.close()
        r = result[0]

        if r == 'Agent':
            return render(request, 'identification/currentagent.html',{'name':name})
        else:
            return render(request, 'identification/current.html',{'name':name})
    else:
        return redirect('loginuser')
def agent(request):
    if 'LogIn_Id' in request.session:
        name = request.session['LogIn_Username']
        return render(request, 'identification/current.html', {'name':name})
    else:
        return redirect('loginuser')


def accountinfo(request):
    if 'LogIn_Id' in request.session:
        id = request.session['LogIn_Id']
        name = request.session['LogIn_Username']

        cursor = connection.cursor()
        sql = "SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s"
        cursor.execute(sql,[id])
        result = cursor.fetchone()
        cursor.close()
        r = result[0]

        cursor = connection.cursor()
        sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s"
        cursor.execute(sql,[r])
        result = cursor.fetchone()
        cursor.close()
        balance = result[0]

        cursor = connection.cursor()
        sql = "SELECT * FROM eUSER WHERE Account_Id = %s"
        cursor.execute(sql,[r])
        result = cursor.fetchone()
        cursor.close()
        username = result[1]
        mobileno = result[2]
        mail = result[3]
        address = result[4]



        return render(request, 'identification/accountinfo.html', {'balance':balance , 'acc_id':r , 'name':name, 'username':username, 'mobileno':mobileno, 'mail':mail, 'address':address})
    else:
        return redirect('loginuser')

def billpayment(request):
    if 'LogIn_Id' in request.session:
        return render(request, 'identification/billpayment.html')
    else:
        return redirect('loginuser')


def moneysending(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/moneysending.html')
        else:
            RID = int(request.POST.get('transaction_receiver'))
            Amount = request.POST.get('transaction_amount')
            TDATE = datetime.datetime.now()

            cursor = connection.cursor()
            sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s "
            cursor.execute(sql,[RID])
            result = cursor.fetchone()
            cursor.close()

            if result is not None:
                oldbalance = float(result[0])

                cursor = connection.cursor()
                sql = "SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s"
                cursor.execute(sql,[request.session['LogIn_Id']])
                result = cursor.fetchone()
                cursor.close()
                SID = int(result[0])

                cursor = connection.cursor()
                sql = """
                        DECLARE
                        BEGIN
                        	MONEYSENDING(%s, %s, %s);
                        END COMMIT ; """ ;
                cursor.execute(sql, [SID,Amount, RID])
                cursor.close()

                return redirect('showreceipts')
                # cursor = connection.cursor()
                # sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s"
                # cursor.execute(sql,[r])
                # result = cursor.fetchone()
                # cursor.close()
                # old_balance = float(result[0])
                #
                # if old_balance > float(amount):
                #     new_balance = old_balance - float(amount)
                #
                #     cursor = connection.cursor()
                #     sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                #     sql += str(new_balance)
                #     sql += "' WHERE Account_Id =  "
                #     sql += str(r)
                #     cursor.execute(sql)
                #
                #
                #
                #
                #     newbalance = oldbalance + float(amount)
                #
                #     cursor = connection.cursor()
                #     sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                #     sql += str(newbalance)
                #     sql += "' WHERE Account_Id =  "
                #     sql += str(id)
                #     cursor.execute(sql)
                #
                #     cursor = connection.cursor()
                #     sql = "INSERT INTO TRANSACTION VALUES(%s,%s,%s,%s,%s,%s)"
                #     cursor.execute(sql,['',amount,id,date,'',r])
                #     cursor.close()
                #
                #     cursor = connection.cursor()
                #     sql = "INSERT INTO RECEIPT VALUES(%s,%s,%s,%s,%s,%s)"
                #     cursor.execute(sql,['',amount,'','','Sent Money',date])
                #     cursor.close()
                #
                #
                #
                #
            else:
                return render(request, 'identification/moneysending.html' , {'error': 'No account found'})



        return redirect('moneysending')
    else:
        return redirect('loginuser')


def pulloutmoney(request):
    if 'LogIn_Id' in request.session:
        if (request.method == 'GET'):
            return render(request, 'identification/pulloutmoney.html')
        else:

            date = datetime.datetime.now()
            cursor = connection.cursor()
            id = request.POST.get('agent_id')
            amount = request.POST.get('ammount2')
            sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s "
            cursor.execute(sql,[id])
            result = cursor.fetchone()
            cursor.close()


            if result is not None:
                oldbalance = float(result[0])

                cursor = connection.cursor()
                sql = "SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s"
                cursor.execute(sql,[request.session['LogIn_Id']])
                result = cursor.fetchone()
                cursor.close()
                r = result[0]

                cursor = connection.cursor()
                sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s"
                cursor.execute(sql,[r])
                result = cursor.fetchone()
                cursor.close()
                old_balance = float(result[0])

                if old_balance > float(amount):
                    new_balance = old_balance - float(amount)

                    cursor = connection.cursor()
                    sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                    sql += str(new_balance)
                    sql += "' WHERE Account_Id =  "
                    sql += str(r)
                    cursor.execute(sql)




                    newbalance = oldbalance + float(amount)

                    cursor = connection.cursor()
                    sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                    sql += str(newbalance)
                    sql += "' WHERE Account_Id =  "
                    sql += str(id)
                    cursor.execute(sql)

                    cursor = connection.cursor()
                    sql = "INSERT INTO TRANSACTION VALUES(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,['',amount,id,date,'',r])
                    cursor.close()

                    cursor = connection.cursor()
                    sql = "INSERT INTO RECEIPT VALUES(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,['',amount,'','','Cash Out',date])
                    cursor.close()


                else:
                    return render(request, 'identification/pulloutmoney.html' , {'error':'Not enough Money'})


                return redirect('showreceipts')
            else:
                return render(request, 'identification/pulloutmoney.html' , {'error':'Account does not exist'})
    else:
        return redirect('loginuser')


def showreceipts(request):
    if 'LogIn_Id' in request.session:


        cursor = connection.cursor()
        sql = "SELECT Transaction_Id FROM TRANSACTION WHERE Account_Id  IN(SELECT Account_Id FROM eUSER WHERE LogIn_Id = "
        sql += str(request.session['LogIn_Id'])
        sql += " )"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()



        dict_result = []

        for r in result:
            cursor = connection.cursor()
            sql = "SELECT User_Name FROM eUSER WHERE Account_Id  = (SELECT Receiver_Id FROM TRANSACTION WHERE Transaction_Id = "
            sql += str(r[0])
            sql += " )"
            cursor.execute(sql)
            a = cursor.fetchone()
            cursor.close()

            name = a[0]


            cursor = connection.cursor()
            sql = "SELECT Receipt_Id FROM RECEIPT WHERE Transaction_Id = %s"
            cursor.execute(sql,[r[0]])
            receipts = cursor.fetchone()
            cursor.close()

            r_id = receipts[0]

            cursor = connection.cursor()
            sql = "SELECT * FROM RECEIPT WHERE Receipt_Id = %s"
            cursor.execute(sql,[r_id])
            info = cursor.fetchone()
            cursor.close()

            receipt_id = info[0]
            amount = info[1]
            description = info[2]
            tran_id = info[3]
            type = info[4]
            date = info[5]
            row = {'receipt_id':receipt_id , 'amount':amount, 'description':description, 'tran_id':tran_id, 'type':type, 'date':date, 'name':name}
            dict_result.append(row)


        cursor = connection.cursor()
        sql = "SELECT Transaction_Id FROM TRANSACTION WHERE Receiver_Id  IN(SELECT Account_Id FROM eUSER WHERE LogIn_Id = "
        sql += str(request.session['LogIn_Id'])
        sql += " )"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()


        for r in result:
            cursor = connection.cursor()
            sql = "SELECT User_Name FROM eUSER WHERE Account_Id  = (SELECT Account_Id FROM TRANSACTION WHERE Transaction_Id = "
            sql += str(r[0])
            sql += " )"
            cursor.execute(sql)
            a = cursor.fetchone()
            cursor.close()

            name = a[0]


            cursor = connection.cursor()
            sql = "SELECT Receipt_Id FROM RECEIPT WHERE Transaction_Id = %s"
            cursor.execute(sql,[r[0]])
            receipts = cursor.fetchone()
            cursor.close()

            r_id = receipts[0]

            cursor = connection.cursor()
            sql = "SELECT * FROM RECEIPT WHERE Receipt_Id = %s"
            cursor.execute(sql,[r_id])
            info = cursor.fetchone()
            cursor.close()

            receipt_id = info[0]
            amount = info[1]
            description = info[2]
            tran_id = info[3]
            type = info[4]
            date = info[5]
            row = {'receipt_id':receipt_id , 'amount':amount, 'description':description, 'tran_id':tran_id, 'type':type, 'date':date, 'name':name}
            dict_result.append(row)


        #for bills
        cursor = connection.cursor()
        sql = "SELECT Bill_Id FROM BILL WHERE Account_Id  IN(SELECT Account_Id FROM eUSER WHERE LogIn_Id = "
        sql += str(request.session['LogIn_Id'])
        sql += " )"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()

        dict_result2 = []
        for r in result2:

            cursor = connection.cursor()
            sql = "SELECT Receipt_Id FROM BILL_RECEIPT WHERE Bill_Id = %s"
            cursor.execute(sql,[r[0]])
            receipt = cursor.fetchone()
            cursor.close()

            r_id = receipt[0]

            cursor = connection.cursor()
            sql = "SELECT * FROM BILL_RECEIPT WHERE Receipt_Id = %s"
            cursor.execute(sql,[r_id])
            info = cursor.fetchone()
            cursor.close()

            receipt_id = info[0]
            type = info[1]
            amount = info[2]
            description = info[3]
            bill_id = info[4]
            date = info[5]
            customer = info[6]
            row = {'receipt_id':receipt_id , 'amount':amount, 'name':description, 'bill_id':bill_id, 'type':type, 'date':date, 'customer':customer}
            dict_result2.append(row)




        return render(request, 'identification/showreceipts.html' ,{'receipts':dict_result, 'bill_receipts':dict_result2})


    else:
        return redirect('loginuser')

def cashin(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/cashin.html')
        else:


            date = datetime.datetime.now()
            cursor = connection.cursor()
            id = request.POST.get('account_id')
            amount = request.POST.get('ammount')
            sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s "
            cursor.execute(sql,[id])
            result = cursor.fetchone()
            cursor.close()

            if result is not None:
                oldbalance = result[0]
                newbalance = float(oldbalance) + float(amount)

                cursor = connection.cursor()
                sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                sql += str(newbalance)
                sql += "' WHERE Account_Id =  "
                sql += str(id)
                cursor.execute(sql)

                cursor = connection.cursor()
                sql = "SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s"
                cursor.execute(sql,[request.session['LogIn_Id']])
                result = cursor.fetchone()
                cursor.close()
                r = result[0]

                cursor = connection.cursor()
                sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = %s"
                cursor.execute(sql,[r])
                result = cursor.fetchone()
                cursor.close()
                old_balance = result[0]

                new_balance = float(old_balance) - float(amount)

                cursor = connection.cursor()
                sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                sql += str(new_balance)
                sql += "' WHERE Account_Id =  "
                sql += str(r)
                cursor.execute(sql)

                cursor = connection.cursor()
                sql = "INSERT INTO TRANSACTION VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,['',amount,id,date,'',r])
                cursor.close()

                cursor = connection.cursor()
                sql = "INSERT INTO RECEIPT VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,['',amount,'','','Cash In',date])
                cursor.close()



                return redirect('showreceipts')
            else:
                return render(request, 'identification/cashin.html' , {'error':'Account does not exist'})
    else:
        return redirect('loginuser')



def electricitybill(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/electricity.html')
        else:
            pass
    else:
        return redirect('loginuser')

def gasbill(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/gas.html')
        else:
            pass
    else:
        return redirect('loginuser')


def waterbill(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/water.html')
        else:
            pass
    else:
        return redirect('loginuser')

def phonebill(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/phone.html')
        else:
            pass
    else:
        return redirect('loginuser')

def internetbill(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/internet.html')
        else:
            pass
    else:
        return redirect('loginuser')

def billform(request,bill_pk):
    if 'LogIn_Id' in request.session:

        date = datetime.datetime.now()
        cursor = connection.cursor()
        sql = "SELECT * FROM BILL_INFO WHERE BILL_PK = %s"
        cursor.execute(sql,[bill_pk])
        result = cursor.fetchone()
        cursor.close()

        name = result[2]
        number = result[1]
        type = result[3]

        if request.method == 'GET':
            return render(request, 'identification/billform.html', {'name':name, 'number':number, 'type':type})
        else:
            amount = request.POST['bill_amount']
            desc = request.POST['bill_desc']
            customer = request.POST['customer_num']

            cursor = connection.cursor()
            sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = (SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s)"
            cursor.execute(sql,[request.session['LogIn_Id']])
            result = cursor.fetchone()
            cursor.close()

            oldbalance = float(result[0])

            if oldbalance > float(amount):
                newbalance = oldbalance - float(amount)



                cursor = connection.cursor()
                sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                sql += str(newbalance)
                sql += "' WHERE Account_Id = (SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s) "
                cursor.execute(sql, [request.session['LogIn_Id']])
                cursor.close()

                cursor = connection.cursor()
                sql = "SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s"
                cursor.execute(sql,[request.session['LogIn_Id']])
                r = cursor.fetchone()
                cursor.close()

                cursor = connection.cursor()
                sql = "INSERT INTO BILL VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,['',number,date,amount,type,name,r[0],customer])
                cursor.close()

                cursor = connection.cursor()
                sql = "INSERT INTO BILL_RECEIPT VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,['',type,amount,name,'',date,customer])
                cursor.close()

                return redirect('showreceipts')

            else:
                return render(request, 'identification/billform.html', {'error':'Not enough money'})


    else:
        return redirect('loginuser')



def addmoney(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/add.html')
        else:
            return render(request, 'identification/add.html')
    else:
        return redirect('loginuser')


def card(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/card.html')
        else:
            id = request.session['LogIn_Id']
            amount = request.POST['amount']
            month = request.POST['mm']
            year = request.POST['yy']
            invalid = 0

            cdate = datetime.date.today()
            cmonth = cdate.month
            cyear = cdate.year

            if (cyear < year) or ((cyear == year) and (cmonth < month)):
                return render(request, 'identification/card.html', {'error':'Credit Card Expired'})
            else:
                cursor = connection.cursor()
                sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = (SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s)"
                cursor.execute(sql, [id])
                result = cursor.fetchone()
                cursor.close()

                newbalance = float(result[0]) + float(amount)

                cursor = connection.cursor()
                sql = "UPDATE ACCOUNT SET Account_Balance = ' "
                sql += str(newbalance)
                sql += "' WHERE Account_Id = (SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s)"
                cursor.execute(sql, [request.session['LogIn_Id']])
                cursor.close()
                return redirect('accountinfo')



    else:
        return redirect('loginuser')

def netbank(request):
    if 'LogIn_Id' in request.session:
        if request.method == 'GET':
            return render(request, 'identification/netbank.html')
        else:
            id = request.session['LogIn_Id']
            amount = request.POST['amount']

            cursor = connection.cursor()
            sql = "SELECT Account_Balance FROM ACCOUNT WHERE Account_Id = (SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s)"
            cursor.execute(sql,[id])
            result = cursor.fetchone()
            cursor.close()

            newbalance = float(result[0]) + float(amount)

            cursor = connection.cursor()
            sql = "UPDATE ACCOUNT SET Account_Balance = ' "
            sql += str(newbalance)
            sql += "' WHERE Account_Id = (SELECT Account_Id FROM eUSER WHERE LogIn_Id = %s)"
            cursor.execute(sql,[request.session['LogIn_Id']])
            cursor.close()
            return redirect('accountinfo')
    else:
        return redirect('loginuser')
