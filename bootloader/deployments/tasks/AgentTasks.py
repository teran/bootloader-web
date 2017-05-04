from deployments.tasks import app


@app.task
def download_file(deployment, source, destination):
    pass


@app.task
def delete_file(deployment, filename):
    pass


@app.task
def echo(message):
    pass


@app.task
def expect_callback(deployment, callback_name):
    pass


@app.task
def ipmi_command(deployment, command, parameters=None):
    pass
