from flask import Flask, request, render_template
from calculator import Calculator

app = Flask(__name__)
calculator = Calculator()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        expression = request.form.get("expression")
        try:
            result = expression + " = " + str(calculator.apply(expression))
            return render_template("index.html", result=result)
        except Exception as e:
            return render_template("index.html", result=str(e) + " в выражении: " + expression)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
