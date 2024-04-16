from flask import Flask, render_template, request, redirect
import string

app = Flask(__name__)
app.config['DEBUG'] = True

def check_inputs(name, pwd, check, form_info):
    # Check the submitted username, password, and retyped password.
    valid_name = check_username(name, form_info)
    valid_password = check_password(pwd, form_info)
    valid_match = valid_password and check_confirm(check, pwd, form_info)

    # Return False if any of the checks fail.
    return valid_name and valid_password and valid_match

def check_username(name, form_info):
    if ' ' in name:
      form_info['Username'][4] = 'Username cannot contain spaces.'
    elif len(name) < 3 or len(name) > 8:
        form_info['Username'][4] = 'Username must be 3-8 characters long.'
    else:
        form_info['Username'][3] = name

    if 3 <= len(name) <= 8 and ' ' not in name:
        form_info['Username'][3] = name
    return 3 <= len(name) <= 8 and ' ' not in name # Return False if incorrect length, or if spaces are present.

def check_password(pwd, form_info):
    special_char = letter = digit = False
    formats = True

    # Return False if incorrect length, or if spaces are present.
    if len(pwd) < 8 or ' ' in pwd:
            formats = False
    # Check if pwd contains a letter, number, and special symbol.
    for char in pwd:
        if char in string.ascii_letters:
            letter = True
        if char in string.digits:
            digit = True
        if char in ['%', '#', '&', '*']:
            special_char = True
    
     # Throw error message on incorrect inputs
    if len(pwd) < 8:
        form_info['Password'][4] = 'Password must be longer than 8 characters.'
    elif ' ' in pwd:
        form_info['Password'][4] = 'Password cannot contain spaces.'
    elif special_char == False:
        form_info['Password'][4] = 'Password must contain a special character (%, #, &, *)'
    elif digit == False:
        form_info['Password'][4] = 'Password must contain at least one number'
    
    # Return False if missing any of the three.
    if letter and digit and special_char and formats: 
        form_info['Password'][3] = pwd

    return letter and digit and special_char and formats

def check_confirm(check, pwd, form_info):
    if check == pwd:
        form_info['Confirm Password'][3] = pwd
    else:
        form_info['Confirm Password'][4] = "Passwords don't match"
    return check == pwd     # Return False if the retyped password doesn't match the first.

@app.route('/', methods=['GET', 'POST'])
def sign_up():
    inputs = {
        # Label: [type, name, placeholder]
        'Username': ['text', 'username', '3-8 characters, no spaces', '', ''],
        'Password': ['password', 'password','8 or more characters, no spaces', '', ''],
        'Confirm Password': ['password', 'confirm', 'Retype password', '', '']
    }
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        # If all of the input fields contain valid data, send the user to the success page.
        if check_inputs(username, password, confirm, inputs):
            return redirect('/success', code = 307)

    tab_title = "Flask Project"
    page_title = "Improve Form UX"
    return render_template('register.html', tab_title=tab_title, page_title=page_title,
        inputs=inputs)

@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        tab_title = "Flask Project"
        page_title = "Success!"
        return render_template('success.html', tab_title=tab_title, page_title=page_title)

if __name__ == '__main__':
    app.run()