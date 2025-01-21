from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is how i Deploy a Containerized Flask Application to AWS EKS using Terraform! - Sam In The Cloud'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
