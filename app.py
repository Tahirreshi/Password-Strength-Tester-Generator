from flask import Flask, render_template, request
import random
import math
import string

app = Flask(__name__)

def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)
    if charset == 0:
        return 0
    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

def classify_entropy(entropy):
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    else:
        return "Strong"

def generate_password(length, upper, lower, digits, symbols):
    characters = ''
    if upper:
        characters += string.ascii_uppercase
    if lower:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if symbols:
        characters += string.punctuation

    if not characters:
        return ''

    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    generated = None

    if request.method == 'POST':
        if 'password' in request.form:
            password = request.form['password']
            entropy = calculate_entropy(password)
            strength = classify_entropy(entropy)
            result = {
                'password': password,
                'entropy': entropy,
                'strength': strength
            }

        if 'gen_length' in request.form:
            length = int(request.form['gen_length'])
            upper = 'gen_upper' in request.form
            lower = 'gen_lower' in request.form
            digits = 'gen_digits' in request.form
            symbols = 'gen_symbols' in request.form

            generated_password = generate_password(length, upper, lower, digits, symbols)
            if generated_password:
                generated = {
                    'password': generated_password,
                    'entropy': calculate_entropy(generated_password),
                    'strength': classify_entropy(calculate_entropy(generated_password))
                }

    return render_template('index.html', result=result, generated=generated)

if __name__ == '__main__':
    app.run(debug=True)
