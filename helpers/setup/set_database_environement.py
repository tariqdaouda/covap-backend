import os
import click

@click.command()
@click.option('--url', help='arangodb url')
@click.option('--username', help='username for the db')
@click.option('--password', help='password for the db')
def set_env(url, username, password):
    """set env variables for the database to run"""
    os.environ['WEPITOPES_ARANGODB_URL'] = url
    os.environ['WEPITOPES_ARANGODB_USERNAME'] = username
    os.environ['WEPITOPES_ARANGODB_PASSWORD'] = password
    
if __name__ == '__main__':
    set_env()