from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='0.3')

@app.route('/')
def main():
  return "Hello"

@app.route('/healthz')
@metrics.counter('exceptions', 'Number of exceptions')
def healthz():
  return "Healthy as a bull"
