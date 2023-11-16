import argparse
from .backend import authenticate as auth
import insurit.commands as commands
from .backend.db_manager import Connection


def main():
    login_command = "login"
    start_service = "connect"
    parser = argparse.ArgumentParser(
        prog='insureit',
        description="Insurance Provider Application",
        epilog="Example usage: insureit login -u <username> -p <password>"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: start service
    service_parser = subparsers.add_parser(start_service, help="Start insurit application by connecting to remote DB")
    service_parser.add_argument('--hostname', help="Host of the Insurit service")
    service_parser.add_argument('--port', help="Port number to connect with service")
    service_parser.add_argument('--username', help="Username to access the service")

    # Subcommand: login
    login_parser = subparsers.add_parser(login_command, help="Login to Insureit")
    login_parser.add_argument("-u", "--username", help="Your Insureit login username", required=True)
    login_parser.add_argument("-p", "--password", help="Your Insureit login password", required=True)

    args = parser.parse_args()

    # Check if a subcommand is provided
    if args.command is None:
        parser.print_help()
        print("Please provide a subcommand. Use 'insureit --help' for more information.")
    # if asked to connect db
    elif args.command == start_service:
        conn = Connection(hostname=args.hostname, port=args.port, username=args.username)
        conn.fetch_creds()
        conn.connect() # TODO save the state of this conn somehow
    # if asked to log in
    elif args.command == login_command:
        if auth.login(args.username, args.password):
            print("Authentication successful.\nWelcome ", args.username)
            commands.run(args.username, parser)
        else:
            print("Authentication failed. Incorrect Username/Password.")


if __name__ == "__main__":
    main()