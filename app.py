import os
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            image = Image.open(filepath)
            format = image.format
            size = image.size
            mode = image.mode

            # Histogram plot
            plt.figure()
            if mode == "RGB":
                colors = ['r', 'g', 'b']
                for i, color in enumerate(colors):
                    hist = np.histogram(np.array(image)[:, :, i], bins=256, range=(0, 256))[0]
                    plt.plot(hist, color=color)
            else:
                hist = np.histogram(np.array(image), bins=256, range=(0, 256))[0]
                plt.plot(hist, color='gray')

            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
            plt.title("Color Histogram")

            hist_path = os.path.join(app.config["UPLOAD_FOLDER"], "hist.png")
            plt.savefig(hist_path)
            plt.close()

            return render_template("index.html", image_path=filepath, hist_path=hist_path,
                                   format=format, size=size, mode=mode)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
