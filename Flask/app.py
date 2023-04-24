from flask import Flask, render_template, request, session, redirect,url_for
from flask_mysqldb import MySQL
import os
from recommendation_system import RecommenderSystem

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ.get('MYSQL_username')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_password')
app.config['MYSQL_DB'] = 'lessjob'
mysql = MySQL(app)

###############################################################################
'''This route displays the first page of Lessjobs'''

@app.route('/first_page')
def first_page():
    return render_template('first_page.html')

###############################################################################
'''This route displays the first page of Lessjobs. 
If the username is in the database then the user homepage is displayed. 
Else an error is thrown and the website redirects to the login page'''

@app.route('/login_page', methods = ['POST','GET'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('''call login_candidates(%s,%s)''',[username,password])
        candidate = cursor.fetchone()
        cursor.execute('''call login_recruiters(%s,%s)''',[username,password])
        recruiter = cursor.fetchone()
        cursor.close()
        if candidate:
            session['loggedin'] = True
            session['id'] = candidate[0]
            session['username'] = candidate[2]
            return render_template('candidate_homepage.html', name = candidate[1])
        elif recruiter:
            session['loggedin'] = True
            session['id'] = recruiter[0]
            session['username'] = recruiter[2]
            return render_template('recruiter_homepage.html', name = recruiter[1])
        else:
            return render_template('login.html', message = "Incorrect Username or Password!!!")
    else:
       return render_template('login.html')

###############################################################################

'''This route displays the registration page'''

@app.route('/registration_first_page')
def registration_first_page():
    return render_template('registration_first_page.html')

###############################################################################

'''This route displays the candidate registration page.
Also registers the candidate after getting the 
required inputs when the submit button in the webpage is clicked. The clicking of the
submit button invokes the POST method which in turn invokes the if branch of the code.
'''

@app.route('/candidate_registration', methods = ['POST','GET'])
def candidate_registration_page():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''call register_candidate(%s,%s,%s,%s);''',(name,username,password,phone))
            mysql.connection.commit()
            cursor.close()
            return render_template('thankyou.html', name = name)
        except:
            cursor.close()
            return render_template('login.html', message = 'Something went wrong while trying to register you. Please try again.')

    else:
        return render_template('candidate_registration.html')


###############################################################################
@app.route('/recruiter_registration', methods = ["POST","GET"])
def recruiter_registration_page():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['email']
        phone = request.form['phone']
        company = request.form['company']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''call register_recruiter(%s,%s,%s,%s,%s);''',(name,username,password,phone,company))
            mysql.connection.commit()
            cursor.close()
            return render_template('thankyou.html', name = name)
        except:
            cursor.close()
            return render_template('login.html', message = 'Something went wrong while trying to register you. Please try again.')
    else:
        return render_template('recruiter_registration.html')


###############################################################################

@app.route('/job_posting', methods = ["POST","GET"])
def job_posting_page():
    if request.method == 'POST':
        jtitle = request.form["job-title"]
        company = request.form['company']
        description = request.form['description']
        salary = request.form['salary']
        jtype = request.form['job-type']        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''call find_recruiter(%s)''',[session['username']])
            recruiter = cursor.fetchone()
            cursor.execute('''call post_job(%s,%s,%s,%s,%s,%s);''',(jtitle,company,description,salary,jtype,recruiter[0]))
            mysql.connection.commit()
            cursor.close()
            return render_template('job_skill_selection.html')
        except:
            cursor.close()
            return render_template('recruiter_homepage.html',name = recruiter[1], message = "Something went wrong while adding the job!!!")
    else:
        return render_template('New_Job_Posting.html')

###############################################################################

@app.route('/candidate_skill_select', methods = ['POST','GET'])
def candidate_skill_select_page():
    username = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('''call find_candidate(%s)''',[username])
    candidate = cursor.fetchone()
    cursor.execute('''call clear_recommendations(%s)''', [session['id']])
    mysql.connection.commit()
    if request.method == 'POST':
        skills = request.form.getlist('skills[]')
        cursor.execute('''call reset_candidate_skills(%s)''',[candidate[0]])
        mysql.connection.commit()
        for skill in skills:
            cursor.execute("update candidate_skills set "+skill+"= 1 where candidate_id = %s",[candidate[0]])
            mysql.connection.commit()
        cursor.close()
        return render_template('candidate_homepage.html',name = candidate[1] ,message = "Skills have been updated. You may now click the recommendations button to get your job recommendations")
    else:
        return render_template('candidate_skill_select.html', name = candidate[1])

###############################################################################

@app.route('/job_skill_select', methods = ['POST','GET'])
def job_skill_select_page():
    username = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('''call find_recruiter(%s)''',[username])
    recruiter = cursor.fetchone()
    if request.method == 'POST':
        skills = request.form.getlist('skill')
        cursor.execute('''call find_latest_job(%s)''',[recruiter[0]])
        job = cursor.fetchone()
        for skill in skills:
            cursor.execute("update job_skills set "+skill+"= 1 where job_id = %s",[job[0]])
            mysql.connection.commit()
        cursor.close()
        return render_template('recruiter_homepage.html',name = recruiter[1] ,message = "Job has been added Successfully")
    else:
        return render_template('recruiter_homepage.html',name = recruiter[1],message = "Something went wrong when job skills were being added")

###############################################################################

@app.route('/jobs_posted_by_recruiter', methods=['POST','GET'])
def jobs_posted_by_recruiter_page():
    cursor = mysql.connection.cursor()
    cursor.execute('''call find_recruiter(%s)''',[session['username']])
    recruiter = cursor.fetchone()
    if request.method == 'POST':
        if 'Back' in request.form:
            cursor.close()
            return render_template('recruiter_homepage.html', name = recruiter[1])
        elif 'Update' in request.form:
            return render_template('jobs_posted_by_recruiter.html')

    else:
        id = session['id']
        cursor.execute('''call jobs_posted_by_recruiter(%s)''', [id])
        jobs = cursor.fetchall()
        cursor.close()
        if jobs:
            return render_template('jobs_posted_by_recruiter.html', jobs = jobs)
        else:
            return render_template('jobs_posted_by_recruiter.html', message = "You have not posted any jobs so far")

###############################################################################

@app.route('/delete/<int:id>')
def delete_job(id):
    print(id)
    cursor = mysql.connection.cursor()
    cursor.execute('''call delete_job(%s)''',[id])
    mysql.connection.commit()
    return redirect(url_for('jobs_posted_by_recruiter_page'))

###############################################################################

@app.route('/update/<int:id>', methods = ['POST','GET'])
def update_job(id):
    if request.method == 'POST':
        title = request.form['job-title']
        company = request.form['company']
        description = request.form['description']
        salary = request.form['salary']
        jtype = request.form['job-type']
        cursor = mysql.connection.cursor()
        cursor.execute('''call update_job(%s,%s,%s,%s,%s,%s)''',[id, title, company, description, salary, jtype])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('jobs_posted_by_recruiter_page'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('''call find_job(%s)''',[id])
        job = cursor.fetchone()
        cursor.close()
        return render_template('update_job_post.html', job = job)


###############################################################################

@app.route('/update_job_skills/<int:id>', methods = ['POST','GET'])
def update_job_skills(id):
    if request.method == 'POST':
        skills = request.form.getlist('skill')
        cursor = mysql.connection.cursor()
        cursor.execute('''call reset_job_skills(%s)''',[id])
        for skill in skills:
            cursor.execute("update job_skills set "+skill+"= 1 where job_id = %s",[id])
            mysql.connection.commit()
        cursor.close()
        return redirect(url_for('jobs_posted_by_recruiter_page'))
    else:
        return render_template('update_job_skills.html')


###############################################################################


def get_data_candidate_job():
    cursor = mysql.connection.cursor()
    cursor.execute('''call get_train_x_candidate()''')
    train_x = cursor.fetchall()
    cursor.execute('''call get_train_y_candidate()''')
    train_y = cursor.fetchall()
    id = session['id']
    cursor.execute('''call get_test_x_candidate(%s)''',[id])
    test_x = cursor.fetchone()
    cursor.close()
    new_trainx = [list(x) for x in train_x]
    new_trainy = [x[0] for x in train_y]
    new_testx = list(test_x)
    return (new_trainx, new_trainy, new_testx)


def get_recommendations(train_x, train_y, test_x):
    rs = RecommenderSystem(5)
    rs.fit(train_x, train_y)
    recommendations = rs.predict(test_x)
    return recommendations


@app.route('/get_job_recommendations', methods=['POST','GET'])
def get_job_recommendations_page():
    cursor = mysql.connection.cursor()
    cursor.execute('''call find_candidate(%s)''',[session['username']])
    candidate = cursor.fetchone()
    train_x, train_y, test_x = get_data_candidate_job()
    job_ids = get_recommendations(train_x, train_y, test_x)
    if request.method == 'POST':
        return render_template('candidate_homepage.html', name = candidate[1])
    else:
        if (len(job_ids) > 0):
            for job_id in job_ids:
                cursor.execute('''call populate_recommendations_candidate(%s,%s)''',[session['id'],job_id])
                mysql.connection.commit()
            cursor.execute('''call get_recommendations_candidate(%s)''',[session['id']])
            jobs = cursor.fetchall()
            cursor.close()
            if jobs:
                return render_template('recommended_job.html', jobs = jobs)
            else:
                return render_template('recommended_job.html', message = "No Jobs available currently", name = candidate[1])
        else:
            return render_template('recommended_job.html', message = "No Jobs available in the database or you have applied for all the available jobs", name = candidate[1])


###############################################################################

@app.route('/delete_recommendation/<int:id>')
def delete_recommendation(id):
    cursor = mysql.connection.cursor()
    cursor.execute('''call apply_job_candidate(%s,%s)''',[session['id'],id])
    mysql.connection.commit()
    return redirect(url_for('get_job_recommendations_page'))

###############################################################################

@app.route('/candidate_applications', methods = ['POST','GET'])
def candidate_applications():
    cursor = mysql.connection.cursor()
    cursor.execute('''call find_candidate(%s)''', [session['username']])
    candidate = cursor.fetchone()
    if request.method == 'POST':
        return render_template('candidate_homepage.html', name = candidate[1])
    else:
        cursor.execute('''call your_applications(%s)''', [session['id']])
        jobs = cursor.fetchall()
        if jobs:
            return render_template('candidate_applications.html', jobs = jobs, name = candidate[1])
        else:
            return render_template('candidate_applications.html', name = candidate[1], message = "You have not applied for any jobs so far....")

###############################################################################


def get_data_job_candidate(id):
    cursor = mysql.connection.cursor()
    cursor.execute('''call get_train_x_recruiter()''')
    train_x = cursor.fetchall()
    cursor.execute('''call get_train_y_recruiter()''')
    train_y = cursor.fetchall()
    cursor.execute('''call get_test_x_recruiter(%s)''',[id])
    test_x = cursor.fetchone()
    cursor.close()
    new_trainx = [list(x) for x in train_x]
    new_trainy = [x[0] for x in train_y]
    new_testx = list(test_x)
    return (new_trainx, new_trainy, new_testx)

@app.route('/top_applicants/<int:id>', methods = ['POST','GET'])
def top_applicants(id):
    cursor = mysql.connection.cursor()
    cursor.execute('''call find_recruiter(%s)''', [session['username']])
    recruiter = cursor.fetchone()
    if request.method == 'POST':
        return redirect(url_for('jobs_posted_by_recruiter_page'))
    else:
        train_x, train_y, test_x = get_data_job_candidate(id)
        candidate_ids = get_recommendations(train_x, train_y, test_x)
        candidates = []
        for cid in candidate_ids:
            cursor.execute('''call top_applicants(%s,%s)''', [cid,id])
            candidates.append(cursor.fetchone())
        cursor.close()
        candidates = set(candidates)
        return render_template('top_applicants.html', candidates = candidates)


###############################################################################

@app.route('/login_page/logout')
def logout():
    cursor = mysql.connection.cursor()
    cursor.execute('''call clear_recommendations(%s)''', [session['id']])
    mysql.connection.commit()
    cursor.close()
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username',None)
    return redirect(url_for('login_page'))

###############################################################################


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug = True)
