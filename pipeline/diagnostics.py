from datetime import datetime


class Diagnostics:
    def log(self, filename, status):
        print(f'\n\n{datetime.utcnow()}: File: {filename}, status: {status}.\n')
