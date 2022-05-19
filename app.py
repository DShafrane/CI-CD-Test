# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 22:33:52 2022

@author: Mohammed
"""

import psycopg2
from flask import Flask
from flask import render_template
from flask import request, url_for, flash, redirect

conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')

cursor = conn.cursor() 
    
    
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = "Doctors"
    error = None
    cursor = conn.cursor() 
    try:

     cursor.execute("select p_id, name from patients")
     patients = cursor.fetchall()
     cursor.execute("select * from doctors")
     row1 = cursor.fetchall()
     rows1 = row1
     
    except Exception as e:
        cursor = conn.cursor() 
        print(e)
        rows1 = "None"
        error = "An Error has occured"
        return render_template("doctors.html", **locals())
    
    
    d_id = request.form.get('docid')
    cursor = conn.cursor() 
    with cursor:
        try:
            cursor.execute("select count(*) from patients") 
            total_num_of_patients = cursor.fetchall()
            
            cursor.execute("select d_id, name from doctors where d_id = " + "'" + d_id + "'") 
            doc_name = cursor.fetchall()
            
            cursor.execute("select count(*) from primary_physician where d_id = " 
                           + "'" + d_id + "'") 
            num_of_patients = cursor.fetchall()
            
            cursor.execute("select count(*) from (" 
                            + " select * from patientsanddoctors where d_id = " + "'" + d_id + "'"
                            + " except (select * from primary_physician where d_id = " + "'" + d_id + "'" + ")) as PD ")
            num_of_other_patients = cursor.fetchall()
            
            cursor.execute("select p_id, name from patients where p_id in (SELECT p_id from primary_physician where d_id = " 
                           + "'" + d_id + "'" + ")") 
            patients_name = cursor.fetchall()
            
            cursor.execute("select p_id, name from patients where p_id in " +
                            "(select p_id from patientsanddoctors where d_id = " + "'" + d_id + "'"
                             + " except (SELECT p_id from primary_physician where d_id = " + "'" + d_id + "'" + "))")
            other_patients_name = cursor.fetchall()
            
            cursor.execute("select name from drugs where M_id in (SELECT m_id from prescribe where d_id ="
                           + "'" + d_id + "'" + ")") 
            drugs_presc = cursor.fetchall()
            
            cursor.execute("select name from pharmacy where d_id = " 
                           + "'" + d_id + "'") 
            supervisor = cursor.fetchall()
            
        except Exception as e:
            cursor = conn.cursor()
            print(e)
            numall = "None"
            doct = "None"
            num = "None"
            num2 = "None"
            pat = "None"
            pat2 = "None"
            drugsall = "None"
            pharm = "None"
            return render_template("doctors.html", **locals())
        
        if d_id != None:
            numall = total_num_of_patients[0][0]
            doct = doc_name
            num = num_of_patients[0][0]
            num2 = num_of_other_patients[0][0]
            pat = patients_name
            pat2 = other_patients_name
            drugsall = drugs_presc
            pharm = supervisor
            scroll = 'ifselected'
    
    
    return render_template("doctors.html", **locals())


@app.route("/enterdoctor/", methods=['GET', 'POST'])
def enterdoctor():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cursor = conn.cursor()
    doctorid = request.form.get('doctorid')
    doctorname = request.form.get('doctorname')
    doctorspecialty = request.form.get('doctorspecialty')
    doctoryoe = request.form.get('doctoryoe')
    patient = request.form.get('patients')
    radio = request.form.get('typeofpatient')
    
    
    cursor.execute("select p_id, name from patients")
    patients = cursor.fetchall()
    cursor.execute("select * from doctors")
    row1 = cursor.fetchall()
    rows1 = row1
    
    print(radio)
    
    with cursor:
        
        try:
        
            cursor.execute("insert into doctors values (" + "'" + doctorid + "'" + ", " + 
                                                                    "'" + doctorname + "'" + ", " + 
                                                                    "'" + doctorspecialty + "'" + ", " +
                                                                    "'" + doctoryoe + "'" + ")")
            
            if radio == "Primary":
                cursor.execute("insert into primary_physician values ("
                                   + "'" + patient + "'" + ", "
                                   + "'" + doctorid + "'" + ")")
                
                cursor.execute("insert into patientsanddoctors values ("
                                   + "'" + patient + "'" + ", "
                                   + "'" + doctorid + "'" + ")")
            else:
                cursor.execute("insert into patientsanddoctors values ("
                                   + "'" + patient + "'" + ", "
                                   + "'" + doctorid + "'" + ")")
                
                
        except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = "iferroroccured"
                return render_template("doctors.html", **locals())
            
        
        conn.commit()
    
    return redirect(url_for('main'))

@app.route("/patients/", methods=['GET', 'POST'])
def patients():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = "Patients"
    cursor = conn.cursor() 
    try:
        cursor.execute("select d_id, name from doctors")
        doctors = cursor.fetchall()
        cursor.execute("select * from patients")
        row2 = cursor.fetchall()
        rows2 = row2
     
     
    except Exception as e:
        cursor = conn.cursor() 
        print(e)
        rows2 = ""
        return render_template("patients.html", **locals())
    
    
    p_name = request.form.get('patname')
    cursor = conn.cursor() 
    with cursor:
        try:
            cursor.execute("select p_id from patients where name = " + "'" + p_name + "'") 
            pat_id = cursor.fetchall()
            
            p_id = pat_id[0][0]
            
            cursor.execute("select name from doctors where d_id in (SELECT d_id from primary_physician where p_id = " 
                           + "'" + p_id + "'" + ")") 
            primary_doctors = cursor.fetchall()
            
            cursor.execute("select name from doctors where d_id in ((SELECT d_id from patientsanddoctors where p_id = " 
                           + "'" + p_id + "'" + ") except (SELECT d_id from "
                           + "primary_physician where p_id = "
                           + "'" + p_id + "'" + "))")
            other_doctors = cursor.fetchall()
            
            cursor.execute("select M_id, name, formula from drugs where M_id in (SELECT m_id from prescribe where p_id = "
                           + "'" + p_id + "'" + ")") 
            drugs_presc_taken = cursor.fetchall()
            
        except Exception as e:
            cursor = conn.cursor()
            print(e)
            patid = "None"
            primdoct = "None"
            othdoct = "None"
            drugs = "None"
            return render_template("patients.html", **locals())
        
        if p_name != None:
            patid = p_id
            primdoct = primary_doctors
            othdoct = other_doctors
            drugs = drugs_presc_taken
            scroll = 'ifselected'
        
    
    return render_template("patients.html", **locals())


@app.route("/enterpatient/", methods=['GET', 'POST'])
def enterpatient():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cursor = conn.cursor()
    error = None
    patiid = request.form.get('patientid')
    patname = request.form.get('patnamee')
    pataddr = request.form.get('pataddress')
    patage = request.form.get('patage')
    doctor = request.form.get('doctors')
    
    
    cursor.execute("select d_id, name from doctors")
    doctors = cursor.fetchall()
    cursor.execute("select * from patients")
    row2 = cursor.fetchall()
    rows2 = row2
    
    print(patiid)
    print(patname)
    print(pataddr)
    print(patage)
    print(doctor)
    
    with cursor:
        
        if len(pataddr) != 0:
            if len(doctor) != 0:
                try:
                    
            
                    cursor.execute("insert into patients values (" + "'" + patiid + "'" + ", " + 
                                                                        "'" + patname + "'" + ", " + 
                                                                        "'" + pataddr + "'" + ", " +
                                                                        "'" + patage + "'" + ")")
                    cursor.execute("insert into primary_physician values ("
                                       + "'" + patiid + "'" + ", "
                                       + "'" + doctor + "'" + ")") 
                        
                    cursor.execute("insert into patientsanddoctors values ("
                                       + "'" + patiid + "'" + ", "
                                       + "'" + doctor + "'" + ")")
                    
                    
                except Exception as e:
                    cursor = conn.cursor()
                    print(e)
                    error = "An Error has occured, " + str(e)
                    scroll = 'iferroroccured'
                    return render_template("patients.html", **locals())
                
            else:
                try:
            
                    cursor.execute("insert into patients values (" + "'" + patiid + "'" + ", " + 
                                                                        "'" + patname + "'" + ", " + 
                                                                        "'" + pataddr + "'" + ", " +
                                                                        "'" + patage + "'" + ")")
                    
                    
                except Exception as e:
                    cursor = conn.cursor()
                    print(e)
                    error = "An Error has occured, " + str(e)
                    scroll = 'iferroroccured'
                    return render_template("patients.html", **locals())
                
            
        else:
            if len(doctor) != 0:
                
                try:
            
                    cursor.execute("insert into patients values (" + "'" + patiid + "'" + ", " + 
                                                                        "'" + patname + "'" + ", " + 
                                                                        "NULL" + ", " +
                                                                        "'" + patage + "'" + ")")
                    cursor.execute("insert into primary_physician values ("
                                       + "'" + patiid + "'" + ", "
                                       + "'" + doctor + "'" + ")") 
                        
                    cursor.execute("insert into patientsanddoctors values ("
                                       + "'" + patiid + "'" + ", "
                                       + "'" + doctor + "'" + ")")
                    
                    
                except Exception as e:
                    cursor = conn.cursor()
                    print(e)
                    error = "An Error has occured, " + str(e)
                    scroll = 'iferroroccured'
                    return render_template("patients.html", **locals())
                
            else:
                try:
            
                    cursor.execute("insert into patients values (" + "'" + patiid + "'" + ", " + 
                                                                        "'" + patname + "'" + ", " + 
                                                                        "NULL" + ", " +
                                                                        "'" + patage + "'" + ")")
                    
                    
                except Exception as e:
                    cursor = conn.cursor()
                    print(e)
                    error = "An Error has occured, " + str(e)
                    scroll = 'iferroroccured'
                    return render_template("patients.html", **locals())
        
        conn.commit()
    
    return redirect(url_for('patients'))


@app.route("/enterpharmacy/", methods=['GET', 'POST'])
def enterpharmacy():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cursor = conn.cursor()
    
    cursor.execute("select d_id, name from doctors")
    doctors = cursor.fetchall()
    cursor.execute("select h_id, name, location, d_id from pharmacy")
    row4 = cursor.fetchall() 
    rows4 = row4
    
    pharmacyid = request.form.get('pharmacyid')
    pharmacyname = request.form.get('pharmacyname')
    pharmacyaddress = request.form.get('pharmacyaddress')
    doctor = request.form.get('doctors')
    
    with cursor:
        
        if len(pharmacyaddress) != 0:
            try:
        
                cursor.execute("insert into pharmacy values (" + "'" + pharmacyid + "'" + ", " + 
                                                                    "'" + doctor + "'" + ", " + 
                                                                    "'" + pharmacyname + "'" + ", " +
                                                                    "'" + pharmacyaddress + "'" + ")")     
                
            except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = 'iferroroccured'
                return render_template("pharmacies.html", **locals())
            
        else:
            try:
        
                cursor.execute("insert into pharmacy values (" + "'" + pharmacyid + "'" + ", " + 
                                                                    "'" + doctor + "'" + ", " + 
                                                                    "'" + pharmacyname + "'" + ", " +
                                                                    "NULL" + ")")  
               
                
            except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = 'iferroroccured'
                return render_template("pharmacies.html", **locals())
        
        conn.commit()
    
    return redirect(url_for('pharmacies'))


@app.route("/prescribe/", methods=['GET', 'POST'])
def prescribe():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = "Prescribe Medicine"
    cursor = conn.cursor()
    
    try:
        cursor.execute("select * from prescribe")
        row = cursor.fetchall()

        rows5 = row
        
        cursor.execute("select p_id, name from patients")
        patients = cursor.fetchall()
        
        cursor.execute("select m_id, name from drugs")
        medicines = cursor.fetchall()
     
        cursor.execute("select d_id, name from doctors")
        doctors = cursor.fetchall()
     
     
    except Exception as e:
        cursor = conn.cursor() 
        print(e)
        rows2 = ""
        patients = ""
        medicines = ""
        doctors = ""
        return render_template("prescribe.html", **locals())
    
    return render_template("prescribe.html", **locals())


@app.route("/prescribe2/", methods=['GET', 'POST'])
def prescribe2():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = "Prescribe Medicine"
    cursor = conn.cursor()
    patidd = request.form.get('patients')
    
    try:
        cursor.execute("select * from prescribe")
        row = cursor.fetchall()
        rows5 = row
        
        cursor.execute("select p_id, name from patients order by p_id = '" + patidd + "' desc")
        patients = cursor.fetchall()
        
        cursor.execute("select m_id, name from drugs")
        medicines = cursor.fetchall()
     
        cursor.execute("select d_id, name from doctors where d_id in " +
                       "(Select d_id from patientsanddoctors where p_id = '" + patidd + "')")
        doctors = cursor.fetchall()
     
     
    except Exception as e:
        cursor = conn.cursor() 
        print(e)
        rows2 = ""
        patients = ""
        medicines = ""
        doctors = ""
        return render_template("prescribe.html", **locals())
    
    
    if request.form.get('Submit') == "Submit":
        
        medid = request.form.get('medicines')
        patid = request.form.get('patients')
        docid = request.form.get('doctors')
        date = request.form.get('date')
        description = request.form.get('description')
        
        
        if len(description) != 0:
            try:
        
                cursor.execute("insert into prescribe values (" + "'" + patid + "'" + ", " + 
                                                                    "'" + docid + "'" + ", " + 
                                                                    "'" + medid + "'" + ", " +
                                                                    "'" + date + "'" + ", "
                                                                    "'" + description + "'" +")")
                
            except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = 'iferroroccured'
                return render_template("prescribe.html", **locals())
            
        else:
            try:
        
                cursor.execute("insert into prescribe values (" + "'" + patid + "'" + ", " + 
                                                                    "'" + docid + "'" + ", " + 
                                                                    "'" + medid + "'" + ", " +
                                                                    "'" + date + "'" + ", "
                                                                    "NULL" +")")
               
                
            except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = 'iferroroccured'
                return render_template("prescribe.html", **locals())
        
        conn.commit()
    
        return redirect(url_for('prescribe'))
    
    
    scroll = 'ifselected'
    return render_template("prescribe.html", **locals())

@app.route("/enterprescription/", methods=['GET', 'POST'])
def enterprescription():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cursor = conn.cursor()
    
    medid = request.form.get('medicines')
    patid = request.form.get('patients')
    docid = request.form.get('doctors')
    date = request.form.get('date')
    description = request.form.get('description')
    
    patidd = request.form.get('patients')
    cursor.execute("select * from prescribe")
    row = cursor.fetchall()
    rows5 = row
        
    cursor.execute("select p_id, name from patients")
    patients = cursor.fetchall()
        
    cursor.execute("select m_id, name from drugs")
    medicines = cursor.fetchall()
     
    cursor.execute("select d_id, name from doctors")
    doctors = cursor.fetchall()
    
    with cursor:
        
        if len(description) != 0:
            try:
        
                cursor.execute("insert into prescribe values (" + "'" + patid + "'" + ", " + 
                                                                    "'" + docid + "'" + ", " + 
                                                                    "'" + medid + "'" + ", " +
                                                                    "'" + date + "'" + ", "
                                                                    "'" + description + "'" +")")
                
            except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = 'iferroroccured'
                return render_template("prescribe.html", **locals())
            
        else:
            try:
        
                cursor.execute("insert into prescribe values (" + "'" + patid + "'" + ", " + 
                                                                    "'" + docid + "'" + ", " + 
                                                                    "'" + medid + "'" + ", " +
                                                                    "'" + date + "'" + ", "
                                                                    "NULL" +")")
               
                
            except Exception as e:
                cursor = conn.cursor()
                print(e)
                error = "An Error has occured, " + str(e)
                scroll = 'iferroroccured'
                return render_template("prescribe.html", **locals())
        
        conn.commit()
    
    return redirect(url_for('prescribe'))


@app.route("/drugs/")
def drugs():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = "Drugs Prescribed"
    cursor = conn.cursor() 
    try:
     
     cursor.execute("select m_id, name, formula, count(d_id) " +
                     "from drugs natural join prescribe " +
                     "group by m_id order by m_id")
     row3 = cursor.fetchall()
     
     rows3 = row3
     
     
    except Exception as e:
        cursor = conn.cursor() 
        print(e)
        rows3 = ""
        return render_template("drugs.html", **locals())
    
    
    return render_template("drugs.html", **locals())


@app.route("/pharmacies/")
def pharmacies():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = "Pharmacies"
    cursor = conn.cursor() 
    try:
     cursor.execute("select d_id, name from doctors")
     doctors = cursor.fetchall()
     cursor.execute("select h_id, name, location, d_id from pharmacy")
     row4 = cursor.fetchall()
     rows4 = row4
     
     
    except Exception as e:
        cursor = conn.cursor() 
        print(e)
        rows4 = ""
        return render_template("pharmacies.html", **locals())
    
    return render_template("pharmacies.html", **locals())


@app.route('/select_doctor/', methods=['GET', 'POST'])
def select_doctor():
    cc = 'Select a Doctor'
    d_id = request.form.get('docid')
    cursor = conn.cursor() 
    with cursor:
        try:
            cursor.execute("select count(*) from patientsanddoctors where d_id = " 
                           + "'" + d_id + "'") 
            total_num_of_patients = cursor.fetchall()
            
            cursor.execute("select d_id, name from doctors where d_id = " + "'" + d_id + "'") 
            doc_name = cursor.fetchall()
            
            cursor.execute("select count(*) from primary_physician where d_id = " 
                           + "'" + d_id + "'") 
            num_of_patients = cursor.fetchall()
            
            cursor.execute("select p_id, name from patients where p_id in (SELECT p_id from primary_physician where d_id = " 
                           + "'" + d_id + "'" + ")") 
            patients_name = cursor.fetchall()
            
            cursor.execute("select name from drugs where M_id in (SELECT m_id from prescribe where d_id ="
                           + "'" + d_id + "'" + ")") 
            drugs_presc = cursor.fetchall()
            
            cursor.execute("select name from pharmacy where d_id = " 
                           + "'" + d_id + "'") 
            supervisor = cursor.fetchall()
            
        except Exception as e:
            cursor = conn.cursor()
            print(e)
            numall = "None"
            doct = "None"
            num = "None"
            pat = "None"
            drugsall = "None"
            pharm = "None"
            return render_template("selectdoctor.html", **locals())
        
        if d_id != None:
            numall = total_num_of_patients[0][0]
            doct = doc_name
            num = num_of_patients[0][0]
            pat = patients_name
            drugsall = drugs_presc
            pharm = supervisor
        
        
    return render_template("selectdoctor.html", **locals())

@app.route('/select_patient/', methods=['GET', 'POST'])
def select_patient():
    cc = 'Select a Patient'
    p_name = request.form.get('patname')
    cursor = conn.cursor() 
    with cursor:
        try:
            cursor.execute("select p_id from patients where name = " + "'" + p_name + "'") 
            pat_id = cursor.fetchall()
            
            p_id = pat_id[0][0]
            
            cursor.execute("select name from doctors where d_id in (SELECT d_id from primary_physician where p_id = " 
                           + "'" + p_id + "'" + ")") 
            primary_doctors = cursor.fetchall()
            
            cursor.execute("select name from doctors where d_id in ((SELECT d_id from patientsanddoctors where p_id = " 
                           + "'" + p_id + "'" + ") except (SELECT d_id from "
                           + "primary_physician where p_id = "
                           + "'" + p_id + "'" + "))")
            other_doctors = cursor.fetchall()
            
            cursor.execute("select M_id, name, formula from drugs where M_id in (SELECT m_id from prescribe where p_id = "
                           + "'" + p_id + "'" + ")") 
            drugs_presc_taken = cursor.fetchall()
            
        except Exception as e:
            cursor = conn.cursor()
            print(e)
            patid = "None"
            primdoct = "None"
            othdoct = "None"
            drugs = "None"
            return render_template("selectpatient.html", **locals())
        
        if p_name != None:
            patid = p_id
            primdoct = primary_doctors
            othdoct = other_doctors
            drugs = drugs_presc_taken
        
    return render_template("selectpatient.html", **locals())

@app.route('/select_location/', methods=['GET', 'POST'])
def select_location():
    conn = psycopg2.connect( 
        database="dfdaplk1cts6r", user='zbukkmhqyxcmpi', 
        password='4bf4d83a2d943e285e6da4c72ba7e4a21b7abbfdebcc6bbafa6612a6ddb61388', host='ec2-44-195-169-163.compute-1.amazonaws.com', port= '5432')
    cc = 'Nearby Pharmacies'
    locname = request.form.get('loc')
    
    if locname != None:
        loc1 = locname[:len(locname)//2]
        loc2 = locname[len(locname)//2:]

    
    cursor = conn.cursor() 
    with cursor:
        try:
            cursor.execute("select distinct name " +
                           "from patients " +
                           "where " + 
                           "(lower(address) like LOWER('%" + locname + "%')) OR" + 
                           "(lower(address) like LOWER('%" + loc1 + "%')) OR" + 
                           "(lower(address) like LOWER('%" + loc2 + "%'))")
            pat_rows = cursor.fetchall()
            
            cursor.execute("select distinct name " +
                           "from pharmacy " +
                           "where " + 
                           "(lower(location) like LOWER('%" + locname + "%')) OR" + 
                           "(lower(location) like LOWER('%" + loc1 + "%')) OR" + 
                           "(lower(location) like LOWER('%" + loc2 + "%'))")
            ph_rows = cursor.fetchall()
            
        except Exception as e:
            cursor = conn.cursor()
            print(e)
            rows7 = ""
            rows8 = ""
            return render_template("nearbylocation.html", **locals())
        
        if locname != None:
            rows7 = pat_rows
            rows8 = ph_rows
        
    return render_template("nearbylocation.html", **locals())

@app.route('/my_form/', methods=['POST'])
def my_form():
    return redirect(url_for('main'))

@app.route('/doctor/', methods=['GET'])
def doctor():
    return redirect(url_for('select_doctor'))

if __name__ == "__main__":
    app.run()