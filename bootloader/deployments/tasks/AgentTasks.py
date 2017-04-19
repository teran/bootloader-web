from deployments.tasks import app


@app.task
def download_file(deployment, source, destination):
    pass


@app.task
def delete_file(deployment, source, destination):
    pass


@app.task
def ipmi_command(deployment, command):
    pass
