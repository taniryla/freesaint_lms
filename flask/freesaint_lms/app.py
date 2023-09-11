from flask import Flask #import Flask

# create an instance of a flask application and store it in a variable
app = Flask(__name__)

#define a simple method and decorate it with a flask decorator 
@app.cli.command('command_one')
def method_to_run_when_command_one_is_invoked():
    print('Printing some text')