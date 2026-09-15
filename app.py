from flask import Flask, render_template_string  # import flask class
from sampler import ProcessSampler
import common

app = Flask(__name__)  # create application object
sampler = ProcessSampler(top_n=11)  # module level not inside the route

PAGE = """<!doctype html>
<title>Process Monitor</title>
<meta http-equiv="refresh" content="5">
<h1>Top 10 processes by CPU</h1>
<table border="1" cellpadding="6">
    <tr><th>PID</th><th>CPU %</th><th>Memory MB</th><th>Name</th></tr>
    {% for p in processes %}
    <tr>
        <td>{{ p.pid }}</td>
        <td>{{ "%.1f"|format(p.cpu) }}</td>
        <td>{{ "%.1f"|format(p.mem_mb) }}</td>
        <td>{{ p.name }}</td>
    </tr>
    {% endfor %}
</table>
"""

@app.route("/")  # when someone visits site root...
def hello():  # ...run this function
    return "Hello from Flask"  # whatever is returned becomes the page

@app.route("/processes")
def processes():
    readings = sampler.sample()
    readings = [p for p in readings if p["name"] != common.IDLE_NAME]  # drop idle counter
    return render_template_string(PAGE, processes=readings)

if __name__ == "__main__":  # only start server if run directly
    app.run(debug=True)  # debug=True: auto reload on save, show errors in browser