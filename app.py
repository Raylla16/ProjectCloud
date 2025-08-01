from flask import Flask, render_template, request, redirect
import boto3, uuid, json, os

app = Flask(__name__)
S3_BUCKET = 'projectclouds3'
DATA_FILE = 'petsinfo.json'
s3 = boto3.client('s3')

@app.route('/update', methods=['GET', 'POST'])
def update_page():
    return render_template('UpdatePage.html')

@app.route('/viewlisting', methods=['GET', 'POST'])
def view_listing():
    pets = view_pets()
    return render_template('Listings.html', pets = pets)

def view_pets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_pets(pets):
    with open(DATA_FILE, 'w') as f:
        json.dump(pets, f)

@app.route('/')
def index():
    pets = view_pets()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['POST'])
def add_pet():
    pname = request.form['pname']
    age = request.form['age']
    breed = request.form['breed']
    image = request.files['pic']

    filename = f"pets_info_{image.filename}"
    s3.upload_fileobj(image, S3_BUCKET, filename)
    image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

    pets = view_pets()
    pets.append({'Name': pname, 'Age': age, 'Breed': breed, 'Image': image_url})
    allinfo = save_pets(pets)


    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

