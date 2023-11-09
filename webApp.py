from flask import Flask, render_template, request, redirect, url_for
import os
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission
        input_pdf = request.files['input_pdf']
        output_pdf = request.form['output_pdf']
        width = float(request.form['width'])
        height = float(request.form['height'])

        # Save the uploaded PDF
        input_pdf.save('input.pdf')

        # Generate the image from the input PDF
        image_path = generate_image('input.pdf', width, height)

        # Call the function to convert the generated image to a PDF
        image_to_pdf('input.pdf', output_pdf, image_path, width, height)

        # Delete the generated image file
        if os.path.exists(image_path):
            os.remove(image_path)

        return 'PDF conversion is complete!'

    return render_template('index.html')

def generate_image(input_pdf_path, input_width, input_height):
    pdf_document = fitz.open(input_pdf_path)
    page = pdf_document[0]
    image = page.get_pixmap()
    desired_width = input_width * 72
    desired_height = input_height * 72
    image_path = 'image.jpg'
    image.save(image_path)
    return image_path

def image_to_pdf(input_pdf_path, output_pdf_path, image_path, input_width, input_height):
    new_height = input_height + 3
    new_width = input_width + 2
    doc = SimpleDocTemplate(output_pdf_path, pagesize=(new_width*72, new_height*72))
    story = []
    image = Image(image_path, width=input_width*72, height=input_height*72)
    story.append(image)
    doc.build(story)

if __name__ == '__main__':
    app.run(debug=True)
