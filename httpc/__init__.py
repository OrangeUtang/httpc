from httpc.Request import Request
import click
import os
import sys
from httpc.CustomTypes import HeaderKeyVal


@click.group()
def cli():
    pass


@cli.command()
@click.option('-v', '--verbose', is_flag=True, help="Prints the detail of the response such as protocol, status, and headers.")
@click.option('-h', '--header', default=None, required=False, multiple=True, type=HeaderKeyVal(), help="Enable headers")
@click.option('-o', '--output', type=str, help="Outputs HTTP response into designated file.")
@click.argument('url', nargs=1)
def get(verbose, header, output, url):
    """
    executes a HTTP GET request and prints the response.
    """

    get_req = Request("GET", header, None, url)
    print(get_req.to_string())

    if verbose:
        final_resp = get_req.send_req()
    else:
        response = get_req.send_req()
        parsed_response = response.split("\r\n\r\n")
        final_resp = parsed_response[1]

    if output is not None:
        f = open(output, "w")
        f.write(final_resp)
    else:
        print(final_resp)


@cli.command()
@click.option('-v', '--verbose', is_flag=True, help="Prints the detail of the response such as protocol, status, and headers.")
@click.option('-h', '--header', default=None, required=False, multiple=True, type=HeaderKeyVal(), help="Enable headers")
@click.option('-d', '--data', required=False, multiple=False, type=str, help="Associates an inline data to the body HTTP POST request.")
@click.option('-f', '--file', required=False, multiple=False, type=str, help="Associates the content of a file to the body HTTP POST request.")
@click.option('-o', '--output', type=str, help="Outputs HTTP response into designated file.")
@click.argument('url', nargs=1)
def post(verbose, header, data, file, output, url):
    """
    executes a HTTP POST request and prints the response.
    """
    if file and data:
        print("Either [-d] or [-f] can be used but not both.")

    req_data = ""

    if data:
        req_data = data
    elif file:
        if os.path.exists(file):
            with open(file, 'r') as a_file:
                try:
                    req_data = a_file.read()
                except:
                    print("File can't be read.")
                    sys.exit()
        else:
            print("Can't find this file!")

    post_req = Request("POST", header, req_data, url)

    if verbose:
        final_resp = post_req.send_req()
    else:
        response = post_req.send_req()
        parsed_response = response.split("\r\n\r\n")
        final_resp = parsed_response[1]

    if output is not None:
        f = open(output, "w")
        f.write(final_resp)
    else:
        print("out")
        print(final_resp)


if __name__ == '__main__':
    cli()
